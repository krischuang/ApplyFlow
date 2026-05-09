import logging
from dataclasses import dataclass
from playwright.sync_api import sync_playwright
from config import settings

logger = logging.getLogger(__name__)

LOCATION_SLUGS: dict[str, str] = {
    "sydney": "Sydney-NSW-2000",
    "melbourne": "Melbourne-VIC-3000",
    "brisbane": "Brisbane-QLD-4000",
    "perth": "Perth-WA-6000",
    "adelaide": "Adelaide-SA-5000",
    "canberra": "Canberra-ACT-2600",
    "remote": "All-Australia",
    "all australia": "All-Australia",
}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

CHROMIUM_ARGS = ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]


@dataclass
class ScrapedJob:
    seek_job_id: str
    title: str
    company: str
    location: str
    salary_range: str
    description: str
    job_url: str
    has_quick_apply: bool


def _to_seek_slug(location: str) -> str:
    return LOCATION_SLUGS.get(location.lower().strip(), "All-Australia") if location else "All-Australia"


def _extract_job_id(url: str) -> str:
    for part in reversed(url.split("/")):
        if part.isdigit():
            return part
    return url


def _safe_text(element, selector: str) -> str:
    if not element:
        return ""
    try:
        el = element.query_selector(selector)
        return el.inner_text().strip() if el else ""
    except Exception:
        return ""


def scrape_jobs(location: str) -> list[ScrapedJob]:
    jobs: list[ScrapedJob] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
            page = browser.new_page(user_agent=USER_AGENT)

            slug = _to_seek_slug(location)
            url = f"https://www.seek.com.au/software-engineer-jobs/in-{slug}"
            logger.info("Scraping Seek: %s", url)

            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            title_links = page.query_selector_all("a[data-automation='jobTitle']")
            if not title_links:
                title_links = page.query_selector_all("h3 a[href*='/job/']")

            logger.info("Found %d listings", len(title_links))

            for link in title_links[: settings.seek_max_jobs_per_run]:
                try:
                    title = link.inner_text().strip()
                    href = link.get_attribute("href") or ""
                    job_url = href if href.startswith("http") else f"https://www.seek.com.au{href}"
                    seek_job_id = _extract_job_id(job_url)

                    card = link.evaluate_handle(
                        "el => el.closest('article') || el.closest('[data-automation=\"jobCard\"]')"
                    ).as_element()

                    company = _safe_text(card, "[data-automation='jobCompany'], a[data-automation='jobListingCompany']")
                    job_location = _safe_text(card, "[data-automation='jobLocation']")
                    salary = _safe_text(card, "[data-automation='jobSalary']")

                    jobs.append(ScrapedJob(seek_job_id, title, company, job_location, salary, "", job_url, False))
                except Exception as e:
                    logger.warning("Failed to parse listing: %s", e)

            browser.close()
    except Exception as e:
        logger.error("Seek scrape failed: %s", e)

    return jobs


def enrich_with_description(job: ScrapedJob) -> ScrapedJob:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=CHROMIUM_ARGS)
            page = browser.new_page(user_agent=USER_AGENT)
            page.goto(job.job_url, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            desc_el = page.query_selector("[data-automation='jobAdDetails']")
            description = desc_el.inner_text().strip() if desc_el else ""

            has_quick_apply = bool(
                page.query_selector("[data-automation='job-detail-apply']")
                or page.locator("button:has-text('Quick apply')").count() > 0
            )

            browser.close()
            return ScrapedJob(
                job.seek_job_id, job.title, job.company, job.location,
                job.salary_range, description, job.job_url, has_quick_apply,
            )
    except Exception as e:
        logger.warning("Could not enrich '%s': %s", job.title, e)
        return job

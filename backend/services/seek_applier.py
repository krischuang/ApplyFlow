import logging
from pathlib import Path
from playwright.sync_api import sync_playwright
from config import settings
from services.seek_scraper import ScrapedJob, USER_AGENT, CHROMIUM_ARGS

logger = logging.getLogger(__name__)


def apply(job: ScrapedJob, profile: dict, cover_letter: str) -> bool:
    logger.info("Applying to '%s' at %s", job.title, job.company)
    try:
        with sync_playwright() as p:
            context = p.chromium.launch(
                headless=settings.playwright_headless, args=CHROMIUM_ARGS
            ).new_context(user_agent=USER_AGENT)
            page = context.new_page()
            page.goto(job.job_url, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            # Locate apply button (Seek's selectors vary by job)
            apply_btn = page.locator("[data-automation='job-detail-apply']")
            if apply_btn.count() == 0:
                apply_btn = page.locator("button:has-text('Quick apply')")
            if apply_btn.count() == 0:
                apply_btn = page.locator("a:has-text('Apply')")
            if apply_btn.count() == 0:
                logger.warning("No apply button found for '%s'", job.title)
                return False

            apply_btn.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2000)

            # Skip jobs that redirect to company sites
            if "seek.com.au" not in page.url:
                logger.info("External site redirect for '%s' — skipping", job.title)
                return False

            # Split name
            parts = (profile.get("full_name") or "").strip().split()
            first_name = parts[0] if parts else ""
            last_name = parts[-1] if len(parts) > 1 else ""

            _fill(page, "input[name='firstName'], input[id*='firstName' i], input[placeholder*='first name' i]", first_name)
            _fill(page, "input[name='lastName'], input[id*='lastName' i], input[placeholder*='last name' i]", last_name)
            _fill(page, "input[type='email'], input[name='email'], input[id*='email' i]", profile.get("email") or "")
            _fill(page, "input[type='tel'], input[name='phone'], input[id*='phone' i]", profile.get("phone") or "")

            # Resume upload
            resume_path = profile.get("resume_file_path")
            if resume_path and Path(resume_path).exists():
                file_input = page.locator("input[type='file']")
                if file_input.count() > 0:
                    file_input.first.set_input_files(resume_path)
                    page.wait_for_timeout(1500)

            # Cover letter field (optional)
            cl = page.locator("textarea[name='coverLetter'], textarea[id*='cover' i], textarea[placeholder*='cover' i]")
            if cl.count() > 0:
                cl.first.fill(cover_letter)

            # Submit
            submit = page.locator(
                "button[type='submit']:has-text('Submit'), "
                "button:has-text('Send application'), "
                "button:has-text('Submit application')"
            )
            if submit.count() == 0:
                submit = page.locator("button[type='submit']").last

            if submit.count() > 0:
                submit.first.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(2000)
                logger.info("Submitted application for '%s'", job.title)
                return True

            return False
    except Exception as e:
        logger.error("Apply failed for '%s': %s", job.title, e)
        return False


def _fill(page, selector: str, value: str) -> None:
    if not value:
        return
    try:
        field = page.locator(selector).first
        if field.count() > 0:
            field.fill(value)
    except Exception:
        pass

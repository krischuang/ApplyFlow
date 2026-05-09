import json
import logging
from typing import Any

import anthropic
from config import settings

logger = logging.getLogger(__name__)

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


def _call(prompt: str, max_tokens: int = 2048) -> str:
    message = _get_client().messages.create(
        model=settings.anthropic_model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def _extract_json(text: str) -> str:
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    start, end = text.find("{"), text.rfind("}")
    return text[start : end + 1] if start != -1 and end != -1 else text.strip()


def parse_resume(resume_text: str) -> dict[str, Any]:
    prompt = f"""Parse this resume and return ONLY a JSON object with these exact fields:
{{
  "fullName": "candidate full name",
  "email": "email address",
  "phone": "phone number",
  "location": "city, state (Australian format if present, otherwise leave blank)",
  "skills": ["skill1", "skill2"],
  "experienceSummary": "2–3 sentence summary of work experience",
  "educationSummary": "brief education background"
}}

Resume:
{resume_text[:8000]}"""
    try:
        return json.loads(_extract_json(_call(prompt)))
    except Exception as e:
        logger.error("Resume parse failed: %s", e)
        return {"fullName": "", "email": "", "phone": "", "location": "", "skills": [], "experienceSummary": "", "educationSummary": ""}


def score_job_match(job_description: str, profile: dict) -> int:
    prompt = f"""Rate how well this candidate matches this job, 0–100.
Return ONLY JSON: {{"score": <0-100>, "reason": "<one sentence>"}}

Candidate skills: {profile.get("skills", "")}
Experience: {profile.get("experience_summary", "")}

Job:
{job_description[:3000]}"""
    try:
        result = json.loads(_extract_json(_call(prompt)))
        return int(result["score"])
    except Exception as e:
        logger.error("Job scoring failed: %s", e)
        return 0


def generate_cover_letter(job_description: str, profile: dict) -> str:
    prompt = f"""Write a concise, professional cover letter (under 300 words) for this software engineering job in Australia.
Tailor it to the candidate's background. Do not use generic filler phrases.

Candidate: {profile.get("full_name", "")}
Skills: {profile.get("skills", "")}
Experience: {profile.get("experience_summary", "")}

Job description:
{job_description[:2000]}"""
    return _call(prompt, max_tokens=1024)


def answer_screening_question(question: str, profile: dict) -> str:
    prompt = f"""Answer this job application screening question briefly and professionally (1–3 sentences).

Candidate: {profile.get("full_name", "")}, Skills: {profile.get("skills", "")}, Location: {profile.get("current_location", "")}

Question: {question}"""
    return _call(prompt, max_tokens=256)

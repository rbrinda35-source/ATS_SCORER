import os
import json
import logging
from typing import Dict

from groq import Groq

logger = logging.getLogger('ats_resume_scorer')

GROQ_MODEL = 'llama-3.3-70b-versatile'

_client = None

def _get_client() -> Groq:
    global _client
    if _client is None:
        GROQ_API_KEY = os.getenv('GROQ_API_KEY')

        if not api_key:
            raise ValueError('GROQ_API_KEY environment variable is not set')
        _client = Groq(api_key=GROQ_API_KEY)

    return _client

RESUME_SYSTEM_PROMPT = (
    "You are a resume parser. Extract information from the resume"
    "and return ONLY a valid JSON object. No explanation, no markdown "
)

RESUME_USER_PROMPT = """Extract the following from this resume and return as JSON:
{{
  "name": "full name",
  "email": "email address",
  "phone": "phone number",
  "linkedin": "LinkedIn URL if present, otherwise null",
  "github": "GitHub URL if present, otherwise null",
  "professional_summary": "the full text of the Summary, Profile, About Me, Objective, or Professional Summary section at the top of the resume. Copy the ENTIRE paragraph exactly as written. If no such section exists, return an empty string.",
  "skills": ["list", "of", "skills"],
  "experience": [
    {{
      "job_title": "",
      "company": "",
      "start_date": "",
      "end_date": "",
      "duration_months": 0,
      "description": ""
    }}
  ],
  "education": [
    {{
      "degree": "",
      "institution": "",
      "year": ""
    }}
  ],
  "certifications": ["list of certifications"],
  "projects": [
    {{
      "title": "project name",
      "description": "what the project does and how it was built",
      "technologies": ["tech", "used"]
    }}
  ],
  "action_verbs": ["strong action verbs used in bullet points, e.g. developed, implemented, designed"],
  "keywords": ["important keywords and phrases from the resume for ATS matching"]
}}

Important instructions:
- For duration_months, calculate the number of months between start_date and end_date. If end_date is "Present" or "Current", calculate from start_date to now.
- For skills, extract ALL technical and soft skills mentioned anywhere in the resume.
- For action_verbs, find verbs that start bullet points or describe achievements.
- For keywords, extract noun phrases and technical terms relevant to ATS matching.
- Return ONLY valid JSON. No markdown code fences, no explanation.

Resume Text:
{raw_text}"""

def _call_groq(client: Groq, system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        temperature=0.0,
        max_tokens=4096,
    )

    return response.choices[0].messages.content.strip()

def _try_parse_json(text: str) -> Dict | None:

    #Strip markdown code fences if present
    cleaned_text = text.strip()
    if cleaned_text.startswith("```"):
        #Remove opening fence("```json or ```")
        first_newline = cleaned_text.index("\n") if "\n" in cleaned_text else len(cleaned_text)
        cleaned_text = cleaned_text[first_newline + 1:]
        #Removing closing fence("```")
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        return None

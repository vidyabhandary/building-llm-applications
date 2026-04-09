import json
import re
from typing import Any


def _extract_json_candidate(s: str) -> str:
    text = s.strip()

    fenced_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fenced_match:
        return fenced_match.group(1).strip()

    for opening, closing in (("{", "}"), ("[", "]")):
        start = text.find(opening)
        end = text.rfind(closing)
        if start != -1 and end != -1 and end > start:
            return text[start:end + 1]

    return text


def to_obj(s: Any):
    if not isinstance(s, str):
        return {}

    candidate = _extract_json_candidate(s)
    try:
        return json.loads(candidate)
    except Exception:
        return {}

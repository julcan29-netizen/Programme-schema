import re


def _has_any(text: str, patterns: list[str]) -> bool:
    return any(p in text for p in patterns)


def _extract_first_temp(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = match.group(1).replace(" ", "")
            if not value.startswith(("+", "-")):
                value = f"+{value}" if value.isdigit() else value
            return f"{value}°C"
    return None


def parse_analysis(text: str) -> dict:
    t = text.lower()

    setpoint = _extract_first_temp(
        text,
        [
            r"point de consigne[^0-9+-]*([+-]?\d+)",
            r"consigne[^0-9+-]*([+-]?\d+)",
        ],
    )

    pump_on = _extract_first_temp(
        text,
        [
            r"marche[^0-9+-]*([+-]?\d+)",
            r"température\s*[>≥=]+\s*([+-]?\d+)",
        ],
    )

    pump_off = _extract_first_temp(
        text,
        [
            r"arr[eê]t[^0-9+-]*([+-]?\d+)",
            r"température\s*[<≤=]+\s*([

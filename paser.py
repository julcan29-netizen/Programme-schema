import re


def _has_any(text: str, patterns: list[str]) -> bool:
    return any(p in text for p in patterns)


def _extract_setpoint(text: str) -> str | None:
    patterns = [
        r"consigne[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        r"point de consigne[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        r"\+([0-9]+)\s*°?\s*c",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            value = m.group(1)
            return f"+{value}°C" if not value.startswith("-") else f"{value}°C"
    return None


def _extract_threshold(text: str, keyword: str) -> str | None:
    patterns = [
        rf"{keyword}[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        rf"{keyword}\s*:\s*température\s*[<>]=?\s*([+-]?\d+)\s*°?\s*c",
        rf"{keyword}\s*:\s*t[^0-9+-]*([+-]?\d+)\s*°?\s*c",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return f"{m.group(1)}°C"
    return None


def parse_analysis(text: str) -> dict:
    t = text.lower()

    data = {
        "title": "Coffret régulation froid",
        "has_controller": _has_any(t, ["contrôleur", "controleur", "régulateur", "regulateur"]),
        "has_temp_sensor": _has_any(t, ["sonde", "température", "temperature"]),
        "has_pump": "pompe" in t,
        "has_3way_valve": _has_any(t, ["vanne 3 voies", "vanne 3 voies modulante", "vanne 3 voies motorisée"]),
        "has_fan": _has_any(t, ["ventilation", "ventilateur"]),
        "has_defrost": _has_any(t, ["dégivrage", "degivrage"]),
        "has_bypass": _has_any(t, ["by-pass", "bypass"]),
        "has_glycol": _has_any(t, ["glycol", "glycolée", "glycolee"]),
        "has_evaporator": _has_any(t, ["évaporateur", "evaporateur", "batterie froide", "aérotherme", "aerotherme"]),
        "setpoint": _extract_setpoint(t),
        "pump_on": _extract_threshold(t, "marche"),
        "pump_off": _extract_threshold(t, "arrêt") or _extract_threshold(t, "arret"),
    }

    m = re.search(r"(différentiel|differentiel)[^0-9]*([0-9]+)\s*k", t)
    data["differential"] = f"{m.group(2)}K" if m else None

    data["refs"] = {
        "main_breaker": "QF1",
        "pump_contactor": "KM1",
        "pump_motor": "M1",
        "fan_breaker": "QF2",
        "fan_motor": "M2",
        "controller": "A1",
        "valve_psu": "PS1",
        "valve_actuator": "YV1",
        "terminal_strip": "X1",
        "temp_in": "TT1",
        "temp_return": "TT2",
    }

    return data

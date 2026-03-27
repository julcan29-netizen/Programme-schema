# validators.py
from model import Folio, split_ref


FORBIDDEN_KINDS_IN_POWER = {
    "relay_control",
    "coil",
    "sensor",
    "analog_output_only",
    "logic_only",
}


REQUIRED_TAGS_POWER_REFERENCE = {"Q1", "T1", "A1", "DM1", "KM1", "M1", "YV1", "X1"}


def validate_power_folio(folio: Folio) -> list[str]:
    errors = []

    tags = [d.tag for d in folio.devices]
    if len(tags) != len(set(tags)):
        errors.append("Des tags appareils sont dupliqués.")

    device_map = {d.tag: d for d in folio.devices}

    # Kinds interdits
    for d in folio.devices:
        if d.kind in FORBIDDEN_KINDS_IN_POWER:
            errors.append(f"{d.tag} de type interdit en folio puissance : {d.kind}")

    # Appareils obligatoires dans le cas de référence
    missing = REQUIRED_TAGS_POWER_REFERENCE - set(tags)
    if missing:
        errors.append(f"Appareils obligatoires manquants : {', '.join(sorted(missing))}")

    # Vérif des références de bornes
    for w in folio.wires:
        for ref in [w.from_ref, w.to_ref]:
            if ref.startswith(("N:", "PE:", "FOLIO")):
                continue

            try:
                tag, terminal = split_ref(ref)
            except ValueError as e:
                errors.append(str(e))
                continue

            if tag not in device_map:
                errors.append(f"Fil {w.wire_id} référence appareil inconnu : {tag}")
                continue

            if terminal not in device_map[tag].terminals:
                errors.append(
                    f"Fil {w.wire_id} référence borne inconnue : {ref}"
                )

    # Tous les fils doivent avoir un repère
    for w in folio.wires:
        if not w.wire_id:
            errors.append("Un fil sans repère a été détecté.")

    # Sorties terrain = borne obligatoire
    for w in folio.wires:
        refs = [w.from_ref, w.to_ref]
        if any(r.startswith("X1:") for r in refs):
            if not w.terminal_block_ref:
                errors.append(
                    f"Fil {w.wire_id} passant par X1 sans repère bornier explicite."
                )

    # Renvoi bobine KM1 obligatoire
    km1_cross_refs = [w.cross_ref for w in folio.wires if w.cross_ref]
    if not any("KM1" in cr for cr in km1_cross_refs):
        errors.append("Renvoi inter-folio vers bobine KM1 manquant.")

    return errors

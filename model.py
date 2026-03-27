# model.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Device:
    tag: str
    kind: str
    label: str
    folio: int
    terminals: List[str] = field(default_factory=list)
    attributes: Dict = field(default_factory=dict)


@dataclass
class Wire:
    wire_id: str
    from_ref: str          # ex: "Q1:2"
    to_ref: str            # ex: "DM1:1"
    folio: int
    potential: Optional[str] = None     # L / N / PE / 24VAC / etc.
    terminal_block_ref: Optional[str] = None   # ex: "X1.5"
    cross_ref: Optional[str] = None      # ex: "→ 11 KM1"
    label: Optional[str] = None          # texte complémentaire éventuel


@dataclass
class PlacedDevice:
    tag: str
    x: int
    y: int


@dataclass
class Folio:
    number: int
    title: str
    devices: List[Device]
    wires: List[Wire]
    layout: Dict[str, PlacedDevice]


def split_ref(ref: str) -> Tuple[str, str]:
    """
    'KM1:2' -> ('KM1', '2')
    """
    if ":" not in ref:
        raise ValueError(f"Référence borne invalide : {ref}")
    return ref.split(":", 1)

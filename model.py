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
    from_ref: str
    to_ref: str
    folio: int
    potential: Optional[str] = None
    terminal_block_ref: Optional[str] = None
    cross_ref: Optional[str] = None
    label: Optional[str] = None


@dataclass
class PlacedDevice:
    tag: str
    column: str
    y: int


@dataclass
class Folio:
    number: int
    title: str
    devices: List[Device]
    wires: List[Wire]
    layout: Dict[str, PlacedDevice]


def split_ref(ref: str) -> Tuple[str, str]:
    if ":" not in ref:
        raise ValueError(f"Référence borne invalide : {ref}")
    return ref.split(":", 1)

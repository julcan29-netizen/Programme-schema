# reference_case.py
from model import Device, Wire, PlacedDevice, Folio


def get_reference_power_folio() -> Folio:
    devices = [
        Device(
            tag="Q1",
            kind="breaker",
            label="Disjoncteur général",
            folio=10,
            terminals=["1", "2"]
        ),
        Device(
            tag="T1",
            kind="transformer",
            label="Transformateur 230/24V",
            folio=10,
            terminals=["P1", "P2", "S1", "S2"]
        ),
        Device(
            tag="A1",
            kind="controller_supply",
            label="Régulateur MXPRO",
            folio=10,
            terminals=["L", "N"]
        ),
        Device(
            tag="PS1",
            kind="power_supply",
            label="Alimentation vanne 24V",
            folio=10,
            terminals=["L", "N", "+24", "0V"]
        ),
        Device(
            tag="DM1",
            kind="motor_protection",
            label="Protection moteur circulateur",
            folio=10,
            terminals=["1", "2"]
        ),
        Device(
            tag="KM1",
            kind="contactor_power",
            label="Contact puissance circulateur",
            folio=10,
            terminals=["1", "2"]
        ),
        Device(
            tag="M1",
            kind="motor",
            label="Circulateur",
            folio=10,
            terminals=["L", "N", "PE"]
        ),
        Device(
            tag="YV1",
            kind="valve",
            label="Vanne 3 voies modulante",
            folio=10,
            terminals=["24V", "0V"]
        ),
        Device(
            tag="X1",
            kind="terminal_block",
            label="Bornier terrain",
            folio=10,
            terminals=["1", "2", "5", "6", "7", "8"]
        ),
    ]

    wires = [
        # Alimentation Q1
        Wire(wire_id="1", from_ref="Q1:2", to_ref="A1:L", folio=10, potential="L"),
        Wire(wire_id="2", from_ref="N:0", to_ref="A1:N", folio=10, potential="N"),

        # Primaire T1
        Wire(wire_id="3", from_ref="Q1:2", to_ref="T1:P1", folio=10, potential="L"),
        Wire(wire_id="4", from_ref="N:0", to_ref="T1:P2", folio=10, potential="N"),

        # Alim PS1
        Wire(wire_id="5", from_ref="Q1:2", to_ref="PS1:L", folio=10, potential="L"),
        Wire(wire_id="6", from_ref="N:0", to_ref="PS1:N", folio=10, potential="N"),

        # Vanne YV1 via bornier
        Wire(wire_id="30", from_ref="PS1:+24", to_ref="X1:7", folio=10, potential="+24", terminal_block_ref="X1.7"),
        Wire(wire_id="31", from_ref="PS1:0V", to_ref="X1:8", folio=10, potential="0V", terminal_block_ref="X1.8"),
        Wire(wire_id="32", from_ref="X1:7", to_ref="YV1:24V", folio=10, potential="+24", terminal_block_ref="X1.7"),
        Wire(wire_id="33", from_ref="X1:8", to_ref="YV1:0V", folio=10, potential="0V", terminal_block_ref="X1.8"),
        Wire(wire_id="34", from_ref="YV1:24V", to_ref="FOLIO11:AO_YV1", folio=10, cross_ref="→ 11 YV1 AO"),

        # Circulateur M1
        Wire(wire_id="10", from_ref="Q1:2", to_ref="DM1:1", folio=10, potential="L"),
        Wire(wire_id="11", from_ref="DM1:2", to_ref="KM1:1", folio=10, potential="L"),
        Wire(wire_id="12", from_ref="KM1:2", to_ref="X1:5", folio=10, potential="L", terminal_block_ref="X1.5"),
        Wire(wire_id="13", from_ref="X1:5", to_ref="M1:L", folio=10, potential="L", terminal_block_ref="X1.5"),
        Wire(wire_id="14", from_ref="N:0", to_ref="X1:6", folio=10, potential="N", terminal_block_ref="X1.6"),
        Wire(wire_id="15", from_ref="X1:6", to_ref="M1:N", folio=10, potential="N", terminal_block_ref="X1.6"),
        Wire(wire_id="16", from_ref="PE:0", to_ref="M1:PE", folio=10, potential="PE"),
        Wire(wire_id="17", from_ref="KM1:1", to_ref="FOLIO11:KM1_COIL", folio=10, cross_ref="→ 11 KM1"),

        # Renvoi secondaire T1 vers commande
        Wire(wire_id="20", from_ref="T1:S1", to_ref="FOLIO11:T1_24V", folio=10, potential="24VAC", cross_ref="→ 11 T1"),
        Wire(wire_id="21", from_ref="T1:S2", to_ref="FOLIO11:T1_0V", folio=10, potential="24VAC", cross_ref="→ 11 T1"),
    ]

    layout = {
        "Q1": PlacedDevice(tag="Q1", x=120, y=100),

        "A1": PlacedDevice(tag="A1", x=120, y=240),
        "T1": PlacedDevice(tag="T1", x=300, y=240),
        "PS1": PlacedDevice(tag="PS1", x=480, y=240),

        "DM1": PlacedDevice(tag="DM1", x=700, y=220),
        "KM1": PlacedDevice(tag="KM1", x=700, y=360),
        "X1": PlacedDevice(tag="X1", x=900, y=360),
        "M1": PlacedDevice(tag="M1", x=1080, y=360),

        "YV1": PlacedDevice(tag="YV1", x=900, y=220),
    }

    return Folio(
        number=10,
        title="PUISSANCE",
        devices=devices,
        wires=wires,
        layout=layout
    )

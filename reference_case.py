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
            tag="X1",
            kind="terminal_block",
            label="Bornier terrain",
            folio=10,
            terminals=["5", "6", "7", "8"]
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
    ]

    wires = [
        # Q1 -> A1
        Wire("1", "Q1:2", "A1:L", 10, potential="L"),
        Wire("2", "N:0", "A1:N", 10, potential="N"),

        # Q1 -> T1 primaire
        Wire("3", "Q1:2", "T1:P1", 10, potential="L"),
        Wire("4", "N:0", "T1:P2", 10, potential="N"),

        # Q1 -> PS1
        Wire("5", "Q1:2", "PS1:L", 10, potential="L"),
        Wire("6", "N:0", "PS1:N", 10, potential="N"),

        # T1 secondaire -> folio commande
        Wire("20", "T1:S1", "FOLIO11:T1_24V", 10, potential="24VAC", cross_ref="→ 11 T1"),
        Wire("21", "T1:S2", "FOLIO11:T1_0V", 10, potential="24VAC", cross_ref="→ 11 T1"),

        # Départ moteur
        Wire("10", "Q1:2", "DM1:1", 10, potential="L"),
        Wire("11", "DM1:2", "KM1:1", 10, potential="L"),
        Wire("12", "KM1:2", "X1:5", 10, potential="L", terminal_block_ref="X1.5"),
        Wire("13", "X1:5", "M1:L", 10, potential="L", terminal_block_ref="X1.5"),
        Wire("14", "N:0", "X1:6", 10, potential="N", terminal_block_ref="X1.6"),
        Wire("15", "X1:6", "M1:N", 10, potential="N", terminal_block_ref="X1.6"),
        Wire("16", "PE:0", "M1:PE", 10, potential="PE"),
        Wire("17", "KM1:1", "FOLIO11:KM1_COIL", 10, potential="L", cross_ref="→ 11 KM1"),

        # Vanne
        Wire("30", "PS1:+24", "X1:7", 10, potential="+24", terminal_block_ref="X1.7"),
        Wire("31", "PS1:0V", "X1:8", 10, potential="0V", terminal_block_ref="X1.8"),
        Wire("32", "X1:7", "YV1:24V", 10, potential="+24", terminal_block_ref="X1.7"),
        Wire("33", "X1:8", "YV1:0V", 10, potential="0V", terminal_block_ref="X1.8"),
        Wire("34", "YV1:24V", "FOLIO11:AO_YV1", 10, cross_ref="→ 11 YV1 AO"),
    ]

    layout = {
        "Q1": PlacedDevice("Q1", "power_in", 150),

        "A1": PlacedDevice("A1", "control_power", 260),
        "T1": PlacedDevice("T1", "transformer", 260),
        "PS1": PlacedDevice("PS1", "control_power", 420),

        "DM1": PlacedDevice("DM1", "motor_power", 180),
        "KM1": PlacedDevice("KM1", "motor_power", 380),

        "X1": PlacedDevice("X1", "field", 340),
        "YV1": PlacedDevice("YV1", "field_far", 420),
        "M1": PlacedDevice("M1", "field_far", 650),
    }

    return Folio(
        number=10,
        title="PUISSANCE",
        devices=devices,
        wires=wires,
        layout=layout
    )

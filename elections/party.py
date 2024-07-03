import numpy as np
from dataclasses import dataclass
from typing import List, Any


@dataclass
class Party:
    name: str
    abrev: str
    spectrum_position: float  # -1.0 (Left) - 1.0 (Right)
    color: Any

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Party) and value.name == self.name

    def __hash__(self) -> int:
        return hash(self.name)


class Coalition(Party):
    def __init__(self, name: str, abrev: str, parties: List[Party], color: Any):
        self.name = name
        self.abrev = abrev
        self.spectrum_position = np.mean(
            [party.spectrum_position for party in parties])
        self.parties: List[Party] = parties
        self.color = color

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Coalition):
            return value.name == self.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)

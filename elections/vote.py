from dataclasses import dataclass
from typing import Any, Dict
from .party import Party


@dataclass
class Candidate:
    name: str
    party: Party
    nuance: Party = None

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Candidate) and value.name == self.name and value.party == self.party

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.party)

    def __repr__(self) -> str:
        return f"{self.name} ({self.party.abrev})"

    def party_or_nuance(self):
        return self.party if self.nuance is None else self.nuance


@dataclass
class Votes:
    votes: Dict[Candidate, float]
    abstention: float

    def __add__(self, other):
        new_votes = {candidate: vote for candidate, vote in self.votes.items()}
        for candidate, vote in other.votes.items():
            if candidate in new_votes:
                new_votes[candidate] += vote
            else:
                new_votes[candidate] = vote
        return Votes(new_votes, self.abstention + other.abstention)

    def get(self, candidate: Candidate):
        return self.votes[candidate]

    def remove_candidate(self, candidate: Candidate):
        new_votes = {candidate: vote for candidate, vote in self.votes.items()}
        del new_votes[candidate]
        return Votes(new_votes, self.abstention)

    def __repr__(self) -> str:
        total = sum(self.votes.values()) + self.abstention
        s = "Votes:\n"
        for candidate, vote in self.votes.items():
            s += f"{candidate}: {vote / total * 100.0:.2f}% ({vote})\n"
        s += f"Abstention: {self.abstention / total * 100.0:.2f}% ({self.abstention})"
        return s

    def copy(self):
        return Votes(
            votes=self.votes.copy(),
            abstention=self.abstention,
        )

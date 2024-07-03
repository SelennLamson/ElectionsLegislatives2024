from dataclasses import dataclass
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from .vote import Votes, Candidate
from .party import Party
from .vote_transfer import VoteTransferModel
import numpy as np


@dataclass
class Circonscription:
    id: str
    candidates: List[Candidate]
    first_round_votes: Votes
    eliminated_candidates: List[Candidate]
    desisting_candidates: List[Candidate]
    second_round_votes: Votes = None

    def __repr__(self) -> str:
        total_votes = sum(self.first_round_votes.votes.values())

        s = f"Circonscription {self.id}\n"
        s += "Candidates:\n"
        for candidate in self.candidates:
            s += f"  - {candidate}: "
            s += f"{self.first_round_votes.votes[candidate] / total_votes * 100.0:.2f}% "
            s += f"({self.first_round_votes.votes[candidate]})"
            if candidate in self.eliminated_candidates:
                s += " (eliminated)"
            elif candidate in self.desisting_candidates:
                s += " (desisting)"
            s += "\n"
        s += f"Abstention: {self.first_round_votes.abstention / (total_votes + self.first_round_votes.abstention) * 100.0:.2f}%\n"
        return s

    def get_winner(self) -> Candidate:
        return max(self.second_round_votes.votes, key=self.second_round_votes.votes.get)

    def copy(self):
        return Circonscription(
            id=self.id,
            candidates=self.candidates.copy(),
            first_round_votes=self.first_round_votes.copy(
            ) if self.first_round_votes is not None else None,
            eliminated_candidates=self.eliminated_candidates.copy(),
            desisting_candidates=self.desisting_candidates.copy(),
            second_round_votes=self.second_round_votes.copy(
            ) if self.second_round_votes is not None else None,
        )


def projection(circos, desisting: bool, transfer_strategy: VoteTransferModel = None):
    circos_after = []
    n_desisting = 0
    for c in circos:
        circo = c.copy()

        if not desisting:
            circo.desisiting_candidates = []
        n_desisting += len(circo.desisting_candidates)

        remaining_candidates = [
            candidate for candidate in circo.candidates
            if candidate not in circo.eliminated_candidates and
            candidate not in circo.desisting_candidates]

        if transfer_strategy is None:
            circo.second_round_votes = circo.first_round_votes
        else:
            circo.second_round_votes = transfer_strategy.transfer_votes(
                remaining_candidates=remaining_candidates, votes=circo.first_round_votes)

        circos_after.append(circo)
    print("Desisting candidates total:", n_desisting)
    return circos_after


def plot_hemicycle(circos, plot_title: str, ax: plt.Axes, nuances: bool = True):
    ax.set_xlim(left=-1.0, right=1.0)
    ax.set_ylim(bottom=-0.3, top=1.3)
    ax.set_axis_off()
    ax.set_aspect('equal')

    # Preparing seats positions
    seat_rows = 12
    seats_per_row = [28, 32, 36, 39, 43, 46, 50, 53, 57, 61, 64, 68]
    start_angle = 190
    end_angle = -10
    start_distance_from_center = 0.4
    rows_spacing = 0.05
    seats_radius = 0.02

    circle_positions = []

    for row in range(seat_rows):
        for seat in range(seats_per_row[row]):
            seat_angle = start_angle + (end_angle - start_angle) * \
                (seat / (seats_per_row[row] - 1))
            seat_distance_from_center = start_distance_from_center + \
                row * rows_spacing
            circle_positions.append((seat_angle, seat_distance_from_center))

    circle_positions.sort(key=lambda x: x[0])

    # Computing seats for each party, sorted by spectrum position
    winners: List[Candidate] = []
    for circo in circos:
        winners.append(circo.get_winner())

    winners.sort(
        key=lambda c: (c.party_or_nuance() if nuances else c.party).spectrum_position, reverse=True)
    parties: Dict[Party, Tuple[float, int]] = {}

    for i, (angle, distance) in enumerate(circle_positions):
        candidate = winners[i]
        party = candidate.party_or_nuance() if nuances else candidate.party

        ax.add_patch(plt.Circle(
            (distance * np.cos(np.deg2rad(angle)),
                distance * np.sin(np.deg2rad(angle))),
            seats_radius,
            color=party.color
        ))

        if party in parties:
            parties[party] = (parties[party][0] + angle, parties[party][1] + 1)
        else:
            parties[party] = (angle, 1)

    # Average angle for each party
    parties = {party: (angle / count, count) for party,
               (angle, count) in parties.items()}

    # Text for each party
    min_text_distance = start_distance_from_center + seat_rows * rows_spacing + 0.05
    max_text_distance = min_text_distance + 0.1
    for party, (angle, count) in parties.items():
        # Min if angle is close to 90
        # Max if angle is close to 0 or 180
        text_distance = min_text_distance + \
            (max_text_distance - min_text_distance) * \
            (abs(angle - 90) / 90)
        ax.text(
            text_distance * np.cos(np.deg2rad(angle)),
            text_distance * np.sin(np.deg2rad(angle)),
            f"{party.abrev} - {count}",
            color=party.color,
            ha='center',
            va='center'
        )

    ax.set_title(plot_title)

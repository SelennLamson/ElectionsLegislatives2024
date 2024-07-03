from dataclasses import dataclass
from typing import List, Dict
import plotly.graph_objects as go
from .party import Party
from .vote import Votes, Candidate
from .utils import rgb


class VoteTransferCase:
    def __init__(self, transfers: Dict[Party, float]):
        # All keys must be present in the remaining parties
        self.transfers: Dict[Party, float] = transfers

    def apply(self, candidates: List[Candidate], votes: float) -> Votes:
        transferred = {candidate: 0.0 for candidate in candidates}
        abstention = votes
        for party, rate in self.transfers.items():
            candidate = next(
                candidate for candidate in candidates if candidate.party == party)
            transferred[candidate] = votes * rate
            abstention -= votes * rate
            # TODO: Handle duplication of votes when the same party appears several times
        return Votes(transferred, abstention)


class PartyVoteTransfer:
    def __init__(self, party: Party, base_abstention_rate=0.5):
        self.party = party
        self.base_abstention_rate = base_abstention_rate
        self.cases: List[VoteTransferCase] = []

    def add_case(self, case: VoteTransferCase):
        self.cases.append(case)

    def get_case(self, remaining_candidates: List[Candidate]):
        remaining_parties = [
            candidate.party for candidate in remaining_candidates]
        for case in self.cases:
            if all(party in remaining_parties for party in case.transfers):
                return case
        return None


class VoteTransferModel:
    def __init__(self, transfers: List[PartyVoteTransfer]):
        self.transfers = transfers

    def __transfer_based_on_spectrum(self, candidate: Candidate, remaining_candidates: List[Candidate], votes: Votes):
        abstention_rate = PartyVoteTransfer(None).base_abstention_rate
        for transfer in self.transfers:
            if transfer.party == candidate.party:
                abstention_rate = transfer.base_abstention_rate
                break

        distances = {rc: abs(rc.party.spectrum_position - candidate.party.spectrum_position)
                     for rc in remaining_candidates}
        proximity_scores = {rc: 1 / (1 + distance)
                            for rc, distance in distances.items()}
        total_proximity = sum(proximity_scores.values())
        return Votes({rc: votes.get(candidate) * proximity_scores[rc] / total_proximity * (1 - abstention_rate)
                      for rc in remaining_candidates},
                     votes.get(candidate) * abstention_rate)

    def transfer_votes(self, remaining_candidates: List[Candidate], votes: Votes):
        eliminated_candidates = [
            candidate for candidate in votes.votes.keys() if candidate not in remaining_candidates]

        for candidate in eliminated_candidates:
            found_case = False
            for transfer in self.transfers:
                if transfer.party == candidate.party:
                    case = transfer.get_case(remaining_candidates)
                    if case:
                        votes += case.apply(remaining_candidates,
                                            votes.get(candidate))
                        votes = votes.remove_candidate(candidate)
                        found_case = True
                        break

            if not found_case:
                transferred_vote = self.__transfer_based_on_spectrum(
                    candidate, remaining_candidates, votes)

                votes += transferred_vote
                votes = votes.remove_candidate(candidate)

        return votes

    def generate_transfer_matrix(self, transferring_parties: List[Party], duels: List[List[Party]]):
        output_parties = list(set([party for duel in duels for party in duel]))

        abstention_party = Party('Abstention', 'ABS', 0, rgb(100, 100, 100))
        all_parties = transferring_parties + \
            output_parties + [abstention_party]
        abstention_index = len(all_parties) - 1

        transferred_votes = {
            party: {} for party in transferring_parties
        }
        duels_per_party = {
            party: 0 for party in transferring_parties
        }
        abstention_per_party = {
            party: 0 for party in transferring_parties
        }

        for party in transferring_parties:
            single_vote = Votes({Candidate('in', party): 1.0}, abstention=0.0)
            transferred_votes_dict = transferred_votes[party]

            for duel in duels:
                if party in duel:
                    continue
                duels_per_party[party] += 1

                candidates = [Candidate('out' + str(i), party)
                              for i, party in enumerate(duel)]
                transferred_vote = self.transfer_votes(candidates, single_vote)
                abstention_per_party[party] += transferred_vote.abstention

                for candidate in candidates:
                    if candidate.party in transferred_votes_dict:
                        transferred_votes_dict[candidate.party] += transferred_vote.get(
                            candidate)
                    else:
                        transferred_votes_dict[candidate.party] = transferred_vote.get(
                            candidate)

        averaged_transferred_votes = {}
        for party, votes in transferred_votes.items():
            if duels_per_party[party] == 0:
                continue

            averaged_transferred_votes[party] = {}
            for target_party, vote in votes.items():
                averaged_transferred_votes[party][target_party] = vote / \
                    duels_per_party[party]
            abstention_per_party[party] /= duels_per_party[party]

        source = []
        target = []
        value = []
        colors = []
        transfer_labels = []

        for party, votes in averaged_transferred_votes.items():
            if duels_per_party[party] == 0:
                continue

            for target_party, vote in votes.items():
                if vote > 0:
                    source.append(transferring_parties.index(party))
                    target.append(len(transferring_parties) +
                                  output_parties.index(target_party))
                    value.append(vote)

                    r, g, b = (col * 128 + 128 for col in target_party.color)
                    colors.append(
                        f'rgb({r}, {g}, {b})')
                    transfer_labels.append(
                        f'{vote * 100.0:.0f}%')

            if abstention_per_party[party] > 0:
                source.append(transferring_parties.index(party))
                target.append(abstention_index)
                value.append(abstention_per_party[party])

                r, g, b = (col * 128 + 128 for col in abstention_party.color)
                colors.append(
                    f'rgb({r}, {g}, {b})')
                transfer_labels.append(
                        f'{abstention_per_party[party] * 100.0:.0f}%')

        transfers = {
            'source': source,
            'target': target,
            'value': value,
            'color': colors,
            'label': transfer_labels,
        }

        return all_parties, transfers


def plot_vote_transfer(parties: List[Party], transfers: Dict):
    return go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            label=[party.abrev for party in parties],
            color=[
                f'rgb({party.color[0] * 255}, {party.color[1] * 255}, {party.color[2] * 255})' for party in parties],
            line=dict(color="black", width=0.0)
        ),
        link=transfers)

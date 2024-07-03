from dataclasses import dataclass
from typing import List, Dict
from .party import Party
from .vote import Votes, Candidate


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
        input_labels = [party.name for party in transferring_parties]

        output_parties = list(set([party for duel in duels for party in duel]))
        output_labels = [
            party.name for party in output_parties] + ['Abstention']

        all_labels = input_labels + output_labels
        abstention_index = len(all_labels) - 1

        transferred_votes = {
            party: {} for party in transferring_parties
        }
        duels_per_party = {
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

                for candidate in candidates:
                    if candidate.party in transferred_votes_dict:
                        transferred_votes_dict[candidate.party] += transferred_vote.get(
                            candidate)
                    else:
                        transferred_votes_dict[candidate.party] = transferred_vote.get(
                            candidate)

        averaged_transferred_votes = {}
        for party, votes in transferred_votes.items():
            averaged_transferred_votes[party] = {}
            for target_party, vote in votes.items():
                averaged_transferred_votes[party][target_party] = vote / \
                    duels_per_party[party]

        source = []
        target = []
        value = []

        for party, votes in averaged_transferred_votes.items():
            sum_of_votes = 0
            for target_party, vote in votes.items():
                source.append(input_labels.index(party.name))
                target.append(len(input_labels) +
                              output_labels.index(target_party.name))
                value.append(vote)
                sum_of_votes += vote
            if sum_of_votes < 1.0:
                source.append(input_labels.index(party.name))
                target.append(abstention_index)
                value.append(1.0 - sum_of_votes)

        transfers = {
            'source': source,
            'target': target,
            'value': value
        }

        return all_labels, transfers

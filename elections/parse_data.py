from elections import *
from math import ceil
from .data import *
from .circonscription import *
from .party import *
from .vote import *


def parse_circos(json_data) -> List[Circonscription]:
    # ABREV_CORRESPONDANCE = {
    #     'ECO': EELV,
    #     'UG': NFP,
    #     'UDI': CEN,
    #     'DIV': DVD,
    #     'DSV': LR,
    #     'EXD': ED,
    #     'RDG': DVG,
    #     'FI': LFI,
    #     'SOC': PS,
    #     'COM': PCF,
    #     'VEC': EELV
    # }

    # Simplifying by merging with coalitions
    ABREV_CORRESPONDANCE = {
        'RN': ED,
        'EXD': ED,
        'REC': ED,
        'UXD': ED,

        'DIV': LR,
        'DSV': LR,
        'DVD': LR,
        'LR': LR,

        'UG': NFP,
        'ECO': NFP,
        'RDG': NFP,
        'FI': NFP,
        'SOC': NFP,
        'COM': NFP,
        'VEC': NFP,
        'DVG': NFP,
        'EXG': NFP,

        'UDI': CEN,
        'REG': CEN,
        'ENS': CEN,
        'DVC': CEN,
        'HOR': CEN,
    }

    fixes = {
        'DVD2': LR
    }
    ABREV_CORRESPONDANCE.update(fixes)

    circos: List[Circonscription] = []
    errors = 0

    for region_key, region_data in json_data.items():
        for circo_key, circo_data in region_data.items():
            candidate_keys = list(circo_data.keys(
            ) - {"inscrits", "votants", "Abstentions", "Exprimés", "Blancs", "Nuls"})

            registered = circo_data["inscrits"]
            abstention = circo_data["Abstentions"] + \
                circo_data["Blancs"] + circo_data["Nuls"]
            expressed = circo_data["Exprimés"]

            parties = []
            for name in candidate_keys:
                # Format: MAÎTRE (RN)
                # Abrev: RN
                party_abrev = name.split('(')[1][:-1]
                found = False
                if party_abrev in ABREV_CORRESPONDANCE:
                    party = ABREV_CORRESPONDANCE[party_abrev]
                    parties.append(party)
                    found = True

                if not found:
                    for party in COALITIONS:
                        if party.abrev == party_abrev:
                            parties.append(party)
                            found = True
                            break

                # if not found:
                #     for party in SINGLE_PARTIES:
                #         if party.abrev == party_abrev:
                #             parties.append(party)
                #             found = True
                #             break

                if not found:
                    print(f"Party {party_abrev} not found")

            if len(parties) != len(candidate_keys):
                print("Warning: parties not found")
                break

            candidates = [Candidate(name=candidate_keys[i].split('(')[0].strip(), party=party)
                          for i, party in enumerate(parties)]

            votes = Votes(
                {candidate: circo_data[candidate_keys[i]]
                    for i, candidate in enumerate(candidates)},
                abstention=abstention
            )

            # Finding out who won!
            first_round_election_threshold_registered = ceil(registered / 4)
            first_round_election_threshold_expressed = ceil(expressed / 2) + 1
            first_round_qualification_threshold_registered = ceil(
                registered / 8)

            eliminated_candidates = set()

            had_a_single_winner = False
            for candidate in candidates:
                vote = votes.votes[candidate]
                if vote >= first_round_election_threshold_registered and vote >= first_round_election_threshold_expressed:
                    had_a_single_winner = True
                    eliminated_candidates = set(candidates) - {candidate}
                    break

                if vote < first_round_qualification_threshold_registered:
                    eliminated_candidates.add(candidate)

            if (len(eliminated_candidates) == len(candidates) - 1 and not had_a_single_winner) or len(eliminated_candidates) == len(candidates):
                # Find the second best and un-eliminate them
                max_votes = [0, 0]
                max_candidates = [None, None]
                for candidate in candidates:
                    vote = votes.votes[candidate]
                    if vote > max_votes[0]:
                        max_votes[1] = max_votes[0]
                        max_candidates[1] = max_candidates[0]
                        max_votes[0] = vote
                        max_candidates[0] = candidate
                    elif vote > max_votes[1]:
                        max_votes[1] = vote
                        max_candidates[1] = candidate
                if max_candidates[0] in eliminated_candidates:
                    eliminated_candidates.remove(max_candidates[0])
                if max_candidates[1] in eliminated_candidates:
                    eliminated_candidates.remove(max_candidates[1])

            circo = Circonscription(
                id=region_key + circo_key[:-len("eme circonscription")],
                candidates=candidates,
                first_round_votes=votes,
                eliminated_candidates=eliminated_candidates,
                desisting_candidates=[],
            )

            sum_of_parties_votes = int(sum(votes.votes.values()))
            if sum_of_parties_votes != expressed:
                print(
                    f"Warning: sum of parties votes {sum_of_parties_votes} != expressed votes {expressed}")
                print(circo)
                errors += 1

            circos.append(circo)

    print(f"Circonscriptions: {len(circos)}, Errors: {errors}")

    n_winners = dict()
    max_winners = 0

    for circo in circos:
        n_winners_circo = len(circo.candidates) - \
            len(circo.eliminated_candidates)
        if n_winners_circo not in n_winners:
            n_winners[n_winners_circo] = 0
        n_winners[n_winners_circo] += 1
        max_winners = max(max_winners, n_winners_circo)

    for n in range(1, max_winners + 1):
        print(f"- {n} winners in {n_winners[n]} circonscriptions")

    return circos


def parse_candidates_details(json_data, circos):
    nuance_correspondance = {
        'RN': RN,
        'LR-RN': UXD,
        'extr. dr.': EXD,

        'LR': LR,
        'DLF': LR,

        'LFI-NFP': LFI,
        'EELV-NFP': EELV,
        'PS-NFP': PS,
        'PCF-NFP': PCF,
        'Gen.-NFP': GEN,
        'reg.-NFP': REG,
        'div. g.-NFP': DVG,
        'PS': PS,
        'PS diss.': PS,
        'LFI': LFI,
        'LFI diss.': LFI,
        'Tavini-NFP': DVG,
        'Tavini': DVG,
        'écol.-NFP': EELV,
        'NPA-NFP': NPA,

        'Hor.-Ensemble': HOR,
        'Ren.-Ensemble': ENS,
        'MoDem-Ensemble': MODEM,
        'div. c.-Ensemble': DVC,
        'UDI-Ensemble': UDI,
        'PRV-Ensemble': DVC,
        'Ren. diss.': ENS,
        'LC': DVC,
        'Agir-Ensemble': DVC,
        'div. d.-Ensemble': DVD,

        'Femu': DVG,
        'rég.': REG,
        'PNC': REG,
        'UDI': UDI,
        'div. g.': DVG,
        'div. d.': DVD,
        'div. dr.': DVD,
        'div.': DVC,
        'div. c.': DVC,
    }

    for circo in circos:
        for candidate in circo.candidates:
            found = False
            for key in json_data:
                if key.lower() == candidate.name.lower():
                    found = True
                    nuance_key = json_data[key]['parti']
                    if nuance_key in nuance_correspondance:
                        candidate.nuance = nuance_correspondance[nuance_key]
                    else:
                        print(f"'{nuance_key}' not found")

                    if json_data[key]['desist']:
                        circo.desisting_candidates.append(candidate)
                    break

            if not found:
                if not candidate in circo.eliminated_candidates:
                    print(f"Winning candidate '{candidate.name}' not found")

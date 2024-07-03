import urllib.request as req
from typing import List
from elections.circonscription import Circonscription, Candidate
from elections.vote import Votes
from elections.data import *

BASE_URL = "https://www.resultats-elections.interieur.gouv.fr/legislatives2024/ensemble_geographique/{}/{}/{}{}/index.html"

PARTY_CORRESPONDANCE = {
    'UG': NFP,
    'ECO': EELV
}


def scrap_circo(special_number=str, region=str, index=str):
    url = BASE_URL.format(special_number, region, region, index)

    fp = req.urlopen(url)
    bts = fp.read()
    html = bts.decode("utf8")
    fp.close()

    # Find <table> tag
    start_table = html.find("<table")
    end_table = html.find("</table>") + len("</table>")
    table = html[start_table:end_table]

    # Content <td>
    elements = []
    while table.find("<td") != -1:
        start_td = table.find("<td")
        end_td = table.find("</td>") + len("</td>")
        elements.append(table[start_td:end_td][4:-5].strip())
        table = table[end_td:]

    # Parsing
    candidates: List[Candidate] = []
    eliminated_candidates: List[Candidate] = []
    circo_votes = Votes(dict(), 0.0)
    has_single_elected = False
    abstention = 0.0
    total_votes = 0

    for i in range(len(elements) // 6):
        name = elements[i * 6]
        party_abrev = elements[i * 6 + 1]
        votes = int(elements[i * 6 + 2].replace('\u202f', ''))
        percentage_registered = float(elements[i * 6 + 3].replace(',', '.'))
        percentage_expressed = float(elements[i * 6 + 4].replace(',', '.'))
        status = elements[i * 6 + 5]
        abstention += (votes / (percentage_registered / 100) -
                       votes / (percentage_expressed / 100)) * votes
        total_votes += votes

        single_elected = status == "OUI"
        qualified = status != "NON"

        party = None
        for p in SINGLE_PARTIES:
            if p.abrev == party_abrev:
                party = p
                break
        if party is None and party_abrev in PARTY_CORRESPONDANCE:
            party = PARTY_CORRESPONDANCE[party_abrev]

        if party is None:
            print("Party not found: ", party_abrev)

        candidate = Candidate(name, party)
        if not qualified or has_single_elected:
            eliminated_candidates.append(candidate)

        if single_elected:
            has_single_elected = True
            for c in candidates:
                eliminated_candidates.append(c)

        candidates.append(candidate)

        if party is not None:
            circo_votes.votes[party] = votes

    circo_votes.abstention = abstention / total_votes
    return Circonscription(int(region + index), candidates, circo_votes, eliminated_candidates, [])


REGIONS = list(map(str, list(range(1, 95 + 1)) +
               list(range(971, 976 + 1)) + list(range(986, 988 + 1)))) + ["ZX", "ZZ"]

print(REGIONS)

circo = scrap_circo("53", "35", "08")
print(circo.asdist())

print(scrap_circo("53", "35", "08"))

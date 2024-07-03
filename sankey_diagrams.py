from elections import *
import json
from math import ceil
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go

results_first_round = json.load(
    open('data/resultat_elections.json', encoding='utf-8'))
circos = parse_circos(results_first_round)

candidate_details = json.load(
    open('data/candidates_details.json', encoding='utf-8'))
parse_candidates_details(candidate_details, circos)

duels = [[CEN, ED], [NFP, ED], [LR, ED], [LR, CEN], [LR, NFP], [NFP, CEN]]

# Mauvais barrage
fig = go.Figure()
rows = 3
cols = 2
row = 0
col = 0
margin = 0.05
sankeys = []
for duel in duels:
    labels, transfers = S5.generate_transfer_matrix(
        transferring_parties=[NFP, CEN, LR, ED],
        duels=[duel])
    sankey = plot_vote_transfer(labels, transfers)
    sankey.domain = {
        'x': [0.5 * col + margin, 0.5 * (col + 1) - margin],
        'y': [1 - 1/rows * (row + 1) + margin, 1 - 1/rows * row - margin]
    }
    sankeys.append(sankey)

    fig.add_annotation(
        x=0.5 * col + 0.25,
        y=1 - 1/rows * row - margin + 0.015,
        xanchor='center',
        yanchor='bottom',
        text=f'{duel[0].abrev} vs. {duel[1].abrev}',
        showarrow=False,
        font=dict(size=20)
    )
    fig.add_trace(sankey)

    col += 1
    if col == 2:
        row += 1
        col = 0

fig.update_layout(title_text="Report des voix - Mauvais barrage",
                  font_size=20, width=800, height=1000)
fig.show()

# Barrage efficace
fig = go.Figure()
rows = 3
cols = 2
row = 0
col = 0
margin = 0.05
sankeys = []
for duel in duels:
    labels, transfers = S2.generate_transfer_matrix(
        transferring_parties=[NFP, CEN, LR, ED],
        duels=[duel])
    sankey = plot_vote_transfer(labels, transfers)
    sankey.domain = {
        'x': [0.5 * col + margin, 0.5 * (col + 1) - margin],
        'y': [1 - 1/rows * (row + 1) + margin, 1 - 1/rows * row - margin]
    }
    sankeys.append(sankey)

    fig.add_annotation(
        x=0.5 * col + 0.25,
        y=1 - 1/rows * row - margin + 0.015,
        xanchor='center',
        yanchor='bottom',
        text=f'{duel[0].abrev} vs. {duel[1].abrev}',
        showarrow=False,
        font=dict(size=20)
    )
    fig.add_trace(sankey)

    col += 1
    if col == 2:
        row += 1
        col = 0

fig.update_layout(title_text="Report des voix - Barrage efficace",
                  font_size=20, width=800, height=1000)
fig.show()


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

# Pas de désistement, ni de report de voies
# circo_no_transfer = projection(circos, False)
# fig = plt.figure(figsize=(8, 6), dpi=100)
# ax1 = fig.add_subplot(1, 1, 1)
# plot_hemicycle(circo_no_transfer,
#                "Gagnants directs, sans report de voies", ax1)
# plt.show()

# # Report simple, sans désistement
# circo_simple_transfer = projection(circos, False, S2_40_30)
# fig = plt.figure(figsize=(8, 6), dpi=100)
# ax1 = fig.add_subplot(1, 1, 1)
# plot_hemicycle(circo_simple_transfer,
#                "Gagnants avec report de voies (sans désistement)", ax1)
# plt.show()

# Report simple, avec désistement réel
circos_real = projection(circos, True, SREAL)
circos_surreal = projection(circos, True, SSURREAL)

fig = plt.figure(figsize=(16, 12), dpi=100)
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 3)
ax3 = fig.add_subplot(2, 2, 2)
ax4 = fig.add_subplot(2, 2, 4)
plot_hemicycle(circos_real,
               "Projection 2nd tour - Barrage réel estimé",
               ax1, nuances=True)
plot_hemicycle(circos_surreal,
               "Projection 2nd tour - NFP fait le meme barrage que CEN et LR",
               ax2, nuances=True)
plot_hemicycle(circos_real,
               "Projection 2nd tour - Barrage réel estimé - Coallitions élargies",
               ax3, nuances=False)
plot_hemicycle(circos_surreal,
               "Projection 2nd tour - NFP fait le meme barrage que CEN et LR - Coallitions élargies",
               ax4, nuances=False)
plt.show()

fig = plt.figure(figsize=(8, 6), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
plot_hemicycle(circos_real,
               "2nd tour - Barrage réel estimé",
               ax1, nuances=False)
plt.show()

fig = plt.figure(figsize=(8, 6), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
plot_hemicycle(circos_surreal,
               "Projection 2nd tour - NFP fait le meme barrage que CEN et LR",
               ax1, nuances=False)
plt.show()

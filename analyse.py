from elections import *
import json
from math import ceil
import matplotlib.pyplot as plt

results_first_round = json.load(
    open('data/resultat_elections.json', encoding='utf-8'))
circos = parse_circos(results_first_round)

candidate_details = json.load(
    open('data/candidates_details.json', encoding='utf-8'))
parse_candidates_details(candidate_details, circos)

S2.generate_transfer_matrix(
    transferring_parties=[NFP, CEN, LR, ED],
    duels=[[NFP, ED], [CEN, ED], [LR, ED], [NFP, CEN], [NFP, LR], [CEN, LR]])

# # Pas de désistement, ni de report de voies
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
circos_good_block = projection(circos, True, S2)
circos_bad_block = projection(circos, True, S5)
fig = plt.figure(figsize=(16, 12), dpi=100)
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 3)
ax3 = fig.add_subplot(2, 2, 2)
ax4 = fig.add_subplot(2, 2, 4)
plot_hemicycle(circos_good_block,
               "Projection 2nd tour - Barrage efficace",
               ax1, nuances=True)
plot_hemicycle(circos_bad_block,
               "Projection 2nd tour - Mauvais barrage",
               ax2, nuances=True)
plot_hemicycle(circos_good_block,
               "Projection 2nd tour - Barrage efficace - Coallitions élargies",
               ax3, nuances=False)
plot_hemicycle(circos_bad_block,
               "Projection 2nd tour - Mauvais barrage - Coallitions élargies",
               ax4, nuances=False)
plt.show()

import numpy as np
from .party import Party, Coalition
from .vote_transfer import PartyVoteTransfer, VoteTransferModel, VoteTransferCase


def rgb(r, g, b):
    return (r / 255, g / 255, b / 255)


# NFP Parties
LFI = Party("La France Insoumise", "LFI", -0.7, rgb(203, 36, 67))
EELV = Party("Europe Écologie les Verts", "EELV", -0.3, rgb(0, 192, 0))
PS = Party("Parti Socialiste", "PS", -0.1, rgb(255, 128, 128))
PCF = Party("Parti Communiste Français", "PCF", -0.8, rgb(210, 0, 0))
NPA = Party("Nouveau Parti Anticapitaliste", "NPA", -0.9, rgb(190, 0, 0))
GEN = Party("Génération.s", "GEN", -0.5, rgb(255, 100, 100))

ENS = Party("Ensemble", "ENS", 0.2, rgb(255, 200, 2))
HOR = Party("Horizon", "HOR", 0.4, rgb(0, 1, 183))
DVC = Party("Divers Centre", "DVC", 0.1, rgb(250, 197, 118))
UDI = Party("Union des Démocrates et Indépendants",
            "UDI", 0.4, rgb(1, 255, 255))
MODEM = Party("Mouvement Démocrate", "MODEM", 0.35, rgb(255, 153, 0))

RN = Party("Rassemblement national", "RN", 0.8, rgb(50, 20, 20))
# Ciotti et CI.
UXD = Party("Union de l'Extrême Droite", "UXD", 0.7, rgb(60, 20, 50))
REC = Party("Reconquête", "REC", 1.0, rgb(20, 5, 5))
EXD = Party("Extrême Droite", "EXD", 1.0, rgb(20, 5, 5))

# Others
DVD = Party("Divers Droite", "DVD", 0.4, rgb(173, 192, 253))
DVG = Party("Divers Gauche", "DVG", -0.4, rgb(254, 192, 191))
EXG = Party("Extrême Gauche", "EXG", -1.0, rgb(150, 0, 0))
REG = Party("Régionalistes", "REG", 0.0, rgb(219, 191, 162))

# Coalitions and single parties
ED = Coalition("Extrême-Droite", "ED", [RN, UXD, REC, EXD], rgb(50, 20, 20))
NFP = Coalition("Nouveau Front Populaire", "NFP", [
                LFI, EELV, PS, PCF, NPA, GEN], rgb(203, 36, 67))
CEN = Coalition("Centre", "CEN", [ENS, HOR, DVC, UDI], rgb(255, 200, 2))
LR = Party("Les Républicains", "LR", 0.5, rgb(0, 101, 204))

SINGLE_PARTIES = [
    LFI, EELV, PS, PCF, NPA, ENS, HOR, DVC, RN, UXD, REC, LR, DVD, DVG, EXG, REG, UDI
]
COALITIONS = [ED, NFP, CEN]

TRANSFER_ED_2022 = PartyVoteTransfer(ED, base_abstention_rate=0.51)
TRANSFER_ED_2022.add_case(VoteTransferCase({ED: 0.7, CEN: 0.1}))
TRANSFER_ED_2022.add_case(VoteTransferCase({ED: 0.7}))
TRANSFER_ED_2022.add_case(VoteTransferCase({CEN: 0.25, NFP: 0.18}))

TRANSFER_CEN_2022 = PartyVoteTransfer(CEN, base_abstention_rate=0.48)
TRANSFER_CEN_2022.add_case(VoteTransferCase({NFP: 0.34, ED: 0.18}))

TRANSFER_LR_2022 = PartyVoteTransfer(LR, base_abstention_rate=0.37)
TRANSFER_LR_2022.add_case(VoteTransferCase({CEN: 0.45, ED: 0.15}))
TRANSFER_LR_2022.add_case(VoteTransferCase({NFP: 0.36, ED: 0.27}))

TRANSFER_NFP_2022 = PartyVoteTransfer(NFP, base_abstention_rate=0.45)
TRANSFER_NFP_2022.add_case(VoteTransferCase({CEN: 0.31, ED: 0.24}))
TRANSFER_NFP_2022.add_case(VoteTransferCase({LR: 0.26, ED: 0.24}))

TRANSFER_2022 = VoteTransferModel(
    [TRANSFER_ED_2022, TRANSFER_CEN_2022, TRANSFER_LR_2022, TRANSFER_NFP_2022])


S1_ED = PartyVoteTransfer(ED, base_abstention_rate=1)
S1_LR = PartyVoteTransfer(LR, base_abstention_rate=1)
S1_CEN = PartyVoteTransfer(CEN, base_abstention_rate=1)
S1_NFP = PartyVoteTransfer(NFP, base_abstention_rate=1)
S1 = VoteTransferModel([S1_ED, S1_LR, S1_CEN, S1_NFP])

# scénario ''réaliste'' : hypothèse PMU de Lord, bon barrage
S2_ED = PartyVoteTransfer(ED, base_abstention_rate=0.5)
S2_ED.add_case(VoteTransferCase({ED: 1.0}))
S2_ED.add_case(VoteTransferCase({CEN: 0.25, NFP: 0.18}))
S2_ED.add_case(VoteTransferCase({LR: 0.25, NFP: 0.18}))
S2_ED.add_case(VoteTransferCase({LR: 0.4, CEN: 0.0}))
S2_LR = PartyVoteTransfer(LR, base_abstention_rate=0.5)
S2_LR.add_case(VoteTransferCase({LR: 1.0}))
S2_LR.add_case(VoteTransferCase({CEN: 0.6, NFP: 0.0}))
S2_LR.add_case(VoteTransferCase({ED: 0.4, NFP: 0.1}))
S2_LR.add_case(VoteTransferCase({ED: 0.2, CEN: 0.6}))
S2_CEN = PartyVoteTransfer(CEN, base_abstention_rate=0.5)
S2_CEN.add_case(VoteTransferCase({CEN: 1.0}))
S2_CEN.add_case(VoteTransferCase({ED: 0.1, NFP: 0.4}))
S2_CEN.add_case(VoteTransferCase({LR: 0.5, NFP: 0.2}))
S2_CEN.add_case(VoteTransferCase({ED: 0.0, LR: 0.7}))
S2_NFP = PartyVoteTransfer(NFP, base_abstention_rate=0.5)
S2_NFP.add_case(VoteTransferCase({NFP: 1.0}))
S2_NFP.add_case(VoteTransferCase({ED: 0.0, CEN: 0.7}))
S2_NFP.add_case(VoteTransferCase({LR: 0.0, CEN: 0.3}))
S2_NFP.add_case(VoteTransferCase({ED: 0.0, LR: 0.2}))
S2 = VoteTransferModel([S2_ED, S2_LR, S2_CEN, S2_NFP])

# scénario ''pessimiste''
S3_ED = PartyVoteTransfer(ED, base_abstention_rate=0.5)
S3_ED.add_case(VoteTransferCase({CEN: 0.5, NFP: 0.0}))
S3_ED.add_case(VoteTransferCase({LR: 0.75, NFP: 0.0}))
S3_ED.add_case(VoteTransferCase({LR: 0.75, CEN: 0.0}))
S3_LR = PartyVoteTransfer(LR, base_abstention_rate=1)
S3_LR.add_case(VoteTransferCase({CEN: 0.75, NFP: 0.0}))
S3_LR.add_case(VoteTransferCase({ED: 0.6, NFP: 0.0}))
S3_LR.add_case(VoteTransferCase({ED: 0.5, CEN: 0.2}))
S3_CEN = PartyVoteTransfer(CEN, base_abstention_rate=1)
S3_CEN.add_case(VoteTransferCase({ED: 0.4, NFP: 0.1}))
S3_CEN.add_case(VoteTransferCase({LR: 0.75, NFP: 0.0}))
S3_CEN.add_case(VoteTransferCase({ED: 0.2, LR: 0.4}))
S3_NFP = PartyVoteTransfer(NFP, base_abstention_rate=1)
S3_NFP.add_case(VoteTransferCase({ED: 0.4, CEN: 0.2}))
S3_NFP.add_case(VoteTransferCase({LR: 0.0, CEN: 0.1}))
S3_NFP.add_case(VoteTransferCase({ED: 0.4, LR: 0.1}))
S3 = VoteTransferModel([S3_ED, S3_LR, S3_CEN, S3_NFP])

# scénario ''pessimiste'' : hypothèse PMU de Lord & Weazel, mauvais barrage généralisé
S5_ED = PartyVoteTransfer(ED, base_abstention_rate=0.5)
S5_ED.add_case(VoteTransferCase({ED: 1.0}))
S5_ED.add_case(VoteTransferCase({CEN: 0.25, NFP: 0.18}))
S5_ED.add_case(VoteTransferCase({LR: 0.25, NFP: 0.18}))
S5_ED.add_case(VoteTransferCase({LR: 0.4, CEN: 0.0}))
S5_LR = PartyVoteTransfer(LR, base_abstention_rate=0.5)
S5_LR.add_case(VoteTransferCase({LR: 1.0}))
S5_LR.add_case(VoteTransferCase({CEN: 0.6, NFP: 0.0}))
S5_LR.add_case(VoteTransferCase({ED: 0.4, NFP: 0.1}))
S5_LR.add_case(VoteTransferCase({ED: 0.2, CEN: 0.6}))
S5_CEN = PartyVoteTransfer(CEN, base_abstention_rate=0.5)
S5_CEN.add_case(VoteTransferCase({CEN: 1.0}))
S5_CEN.add_case(VoteTransferCase({ED: 0.3, NFP: 0.2}))
S5_CEN.add_case(VoteTransferCase({LR: 0.5, NFP: 0.2}))
S5_CEN.add_case(VoteTransferCase({ED: 0.1, LR: 0.6}))
S5_NFP = PartyVoteTransfer(NFP, base_abstention_rate=0.5)
S5_NFP.add_case(VoteTransferCase({NFP: 1.0}))
S5_NFP.add_case(VoteTransferCase({ED: 0.3, CEN: 0.4}))
S5_NFP.add_case(VoteTransferCase({LR: 0.0, CEN: 0.3}))
S5_NFP.add_case(VoteTransferCase({ED: 0.05, LR: 0.15}))
S5 = VoteTransferModel([S5_ED, S5_LR, S5_CEN, S5_NFP])

# scénario ''optimiste''
S4_ED = PartyVoteTransfer(ED, base_abstention_rate=0.5)
S4_ED.add_case(VoteTransferCase({ED: 1.0}))
S4_ED.add_case(VoteTransferCase({CEN: 0.2, NFP: 0.3}))
S4_ED.add_case(VoteTransferCase({LR: 0.3, NFP: 0.3}))
S4_ED.add_case(VoteTransferCase({LR: 0.3, CEN: 0.0}))
S4_LR = PartyVoteTransfer(LR, base_abstention_rate=0.5)
S4_LR.add_case(VoteTransferCase({LR: 1.0}))
S4_LR.add_case(VoteTransferCase({CEN: 0.4, NFP: 0.1}))
S4_LR.add_case(VoteTransferCase({ED: 0.1, NFP: 0.2}))
S4_LR.add_case(VoteTransferCase({ED: 0.0, CEN: 0.4}))
S4_CEN = PartyVoteTransfer(CEN, base_abstention_rate=0.5)
S4_CEN.add_case(VoteTransferCase({CEN: 1.0}))
S4_CEN.add_case(VoteTransferCase({ED: 0.1, NFP: 0.5}))
S4_CEN.add_case(VoteTransferCase({LR: 0.3, NFP: 0.3}))
S4_CEN.add_case(VoteTransferCase({ED: 0.0, LR: 0.5}))
S4_NFP = PartyVoteTransfer(NFP, base_abstention_rate=0.5)
S4_NFP.add_case(VoteTransferCase({NFP: 1.0}))
S4_NFP.add_case(VoteTransferCase({ED: 0.0, CEN: 0.7}))
S4_NFP.add_case(VoteTransferCase({LR: 0.0, CEN: 0.3}))
S4_NFP.add_case(VoteTransferCase({ED: 0.0, LR: 0.4}))
S4 = VoteTransferModel([S4_ED, S4_LR, S4_CEN, S4_NFP])

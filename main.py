from elections import *

votes = Votes({
    Candidate("NFP", NFP): 0,
    Candidate("ED", ED): 100,
    Candidate("CEN", CEN): 0,
    Candidate("LR", LR): 0,
}, abstention=200)

votes = S2.transfer_votes([
    Candidate("NFP", NFP),
    Candidate("CEN", CEN)
], votes)

print(votes)

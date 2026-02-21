import pandas as pd
import math
import networkx as nx
from itertools import combinations

df = pd.read_csv('./data/GermanCredit_new.csv')
allGenre = []
group = []
genre = df['protected']
movieId = df['id']
score = df['score']

allGenre = []
allgroup = []
for g in genre:
    if g not in allGenre:
        allGenre.append(g)
    allgroup.append(allGenre.index(g))

rankScore = []
for i in range(len(movieId)):
    rankScore.append((score[i], movieId[i], allgroup[i]))

rankScore.sort(reverse=True)

movieIdDic = {}
rank = []
group = []
i = 1
for item in rankScore:
    rank.append(i)
    group.append(item[2])
    movieIdDic[item[1]] = i
    i += 1

numberOfItem = len(rank)

rankGrp = {}
for i in range(len(rank)):
    rankGrp[rank[i]] = group[i]

grpCount = {}
for i in group:
    grpCount[i] = 0

rankGrpPos = {}
for i in rank:
    grpCount[rankGrp[i]] += 1
    rankGrpPos[i] = grpCount[rankGrp[i]]

rankRange = {}
for item in rank:
    i = rankGrpPos[item]
    n = numberOfItem
    fp = grpCount[rankGrp[item]]
    r1 = math.floor((i - 1) * n / fp) + 1
    r2 = math.ceil(i * n / fp)
    if r2 > numberOfItem:
        r2 = numberOfItem
    rankRange[item] = (r1, r2)

B = nx.Graph()
top_nodes = []
bottom_nodes = []

for i in rank:
    top_nodes.append(i)
    bottom_nodes.append(str(i))

B.add_nodes_from(top_nodes, bipartite=0)
B.add_nodes_from(bottom_nodes, bipartite=1)

for i in rank:
    r1, r2 = rankRange[i]
    for j in range(1, numberOfItem + 1):
        if r1 <= j <= r2:
            B.add_edge(i, str(j), weight=abs(i - j))
        else:
            B.add_edge(i, str(j), weight=1e11)

my_matching = nx.algorithms.bipartite.minimum_weight_full_matching(B, top_nodes, "weight")
#print("Matching:", my_matching)

# --- Custom Kendall Tau distance computation ---
def KendallTau(P, Q):
    """Compute Kendall Tau distance manually between two rank lists."""
    n = len(P)
    distance = 0
    total_pairs = 0

    for i, j in combinations(range(n), 2):
        if i==j: continue
        total_pairs += 1
        # Concordant / discordant comparison
        if (P[i] - P[j]) * (Q[i] - Q[j]) < 0:
            distance += 1

    
    return distance

# Extract the matched ranks in the order of original ranks
matched_ranks = [int(my_matching[i]) for i in rank]

# Compute Kendall Tau using custom function
kendall_tau = KendallTau(rank, matched_ranks)


print("Kendall Tau distance:", kendall_tau)

# === Step 6: Create new dataframe with fair ranks ===
df_fair = pd.DataFrame({
    'id': movieId,
    'original_rank': rank,
    'new_rank': matched_ranks,
    'protected': genre,
    'sex': df['sex'],
    'age35':df['age35'],
    'score': score,
    'DurationMonth': df['DurationMonth'],
    'CreditAmount': df['CreditAmount']
})

# Sort by new rank for clear output
df_fair.sort_values(by='new_rank', inplace=True)

# Save to CSV
output_path = './GermanCredit_fairness_output.csv'
df_fair.to_csv(output_path, index=False)
print(f"\n✅ Fair ranking written to {output_path}")

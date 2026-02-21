import pandas as pd
import math
import networkx as nx
from networkx.algorithms import bipartite
from timeit import default_timer as timer
import itertools

# --- 1. Load your larger datasets ---
df1 = pd.read_csv('./data/rn_100_n_1k.csv', index_col=0)  # 100 rankings of 1000 items
if 'Unnamed: 1000' in df1.columns:
    df1 = df1.drop(columns=['Unnamed: 1000'])
df1.columns = df1.columns.astype(int)

df2 = pd.read_csv('./data/1k_attribute.csv', index_col=0)  # Protected attribute for 1000 items

# Extract the protected attribute group for each item
# Assuming the column is named 'protected attribute'
df2.index = df2.index.astype(int)
group = df2['protected attribute']

# --- Setup ---
allMatch = []
numberOfItems = len(df1.columns) # Should be 1000
item_ids = list(range(numberOfItems)) # List of item IDs from 0 to 999

# Get the total count of items in each group (e.g., {0: 600, 1: 400})
# This is more efficient than calculating it in every loop
totalGrpCount = group.value_counts().to_dict()
unique_groups = list(totalGrpCount.keys())

start = timer()

# --- 2. Main loop over each ranking (each column in df1) ---
for ranker_id in df1.index:
    print(f"Processing ranking {ranker_id}...")

    # Get the scores for the current ranking
    rank_scores = df1.loc[ranker_id]

    # Convert scores to a sorted rank list of item IDs
    # 'item_id' is now the actual column label (the true item ID)
    ranktup = [(score, item_id) for item_id, score in rank_scores.items()]
    ranktup.sort()
    # 'current_rank' is the list of item IDs, sorted by their rank
    current_rank = [item_id for score, item_id in ranktup]

    # Calculate the within-group position for each item
    # e.g., the 5th best item from group 0
    within_grp_counters = {g: 0 for g in unique_groups}
    rankGrpPos = {}
    for item_id in current_rank:
        item_group = group[int(item_id)]
        within_grp_counters[item_group] += 1
        rankGrpPos[item_id] = within_grp_counters[item_group]

    # --- 3. Compute the fair rank range for each item ---
    rankRange = {}
    for item_id in item_ids:
        i = rankGrpPos[item_id]
        n = numberOfItems
        fp = totalGrpCount[group[int(item_id)]]
        
        # The fairness formula remains the same
        r1 = math.floor((i - 1) * n / fp) + 1 # Adjusted to be 1-indexed
        r2 = math.ceil(i * n / fp)
        rankRange[item_id] = (r1, r2)

    # --- 4. Build and solve the bipartite graph matching ---
    B = nx.Graph()
    # Top nodes are the item IDs (0-999)
    top_nodes = item_ids
    # Bottom nodes are the rank positions (1-1000)
    bottom_nodes = [f"pos_{i}" for i in range(1, numberOfItems + 1)]
    B.add_nodes_from(top_nodes, bipartite=0)
    B.add_nodes_from(bottom_nodes, bipartite=1)

    for item_id in item_ids:
        original_pos = current_rank.index(item_id) + 1
        r1, r2 = rankRange[item_id]
        for j in range(1, numberOfItems + 1):
            if r1 <= j <= r2: # If the target position is 'fair'
                # Cost is how far it moves from its original position
                weight = abs(original_pos - j)
                B.add_edge(item_id, f"pos_{j}", weight=weight)
            else: # If the position is 'unfair', add a massive weight to prevent it
                B.add_edge(item_id, f"pos_{j}", weight=1_000_000_000)

    # This matching finds the new, fair ranking
    fair_matching = nx.algorithms.bipartite.minimum_weight_full_matching(
        B, top_nodes, "weight"
    )
    allMatch.append(fair_matching)

# --- 5. Compute Kendall Tau distance to find the consensus ranking ---

# This part is computationally very expensive and may take a long time!



print("\nAll fair rankings generated. Now finding the consensus ranking...")



def KendallTau(P, Q, combinations):

    # Filter items to only get the mapping from item_id -> position

    P_rank = {item: int(pos.split('_')[1]) for item, pos in P.items() if isinstance(item, int)}

    Q_rank = {item: int(pos.split('_')[1]) for item, pos in Q.items() if isinstance(item, int)}



    distance = 0

    for i, j in combinations:

        if i == j: continue

        # Check for discordant pairs

        if (P_rank[i] - P_rank[j]) * (Q_rank[i] - Q_rank[j]) < 0:
            distance += 1

    return distance



combinations = list(itertools.combinations(item_ids, 2))

minD = float("inf")

resRank = None



for i, rank1 in enumerate(allMatch):

    d = 0

    for j, rank2 in enumerate(allMatch):

        if i == j: continue

        d += KendallTau(rank1, rank2, combinations)


    print(f"Total distance for ranking {i}: {d}")

    if d < minD:

        minD = d

        resRank = rank1



print('\n--- Results ---')

print('Min Kemeny distance =', minD)

end = timer()

print('Time required =', round(end - start, 2), 'seconds')
Rank Aggregation with Proportionate Fairness (RAPF)
Implementation of the SIGMOD 2022 research paper:

"Rank Aggregation with Proportionate Fairness" Dong Wei, Md Mouinul Islam, Baruch Schieber, Senjuti Basu Roy Published in SIGMOD 2022

📌 Project Overview
This project implements algorithms for fair rank aggregation under the notion of Proportionate Fairness (p-fairness).

In many real-world decision-making systems (hiring, admissions, recommendations, resource allocation), multiple evaluators provide rankings over a set of candidates. Traditional rank aggregation focuses only on minimizing disagreement with these rankings. However, it may produce unfair results when candidates belong to protected groups.

This implementation ensures that the final aggregated ranking:

Minimizes disagreement with input rankings (Kemeny / Kendall-Tau distance)
Enforces proportionate representation of protected groups at every prefix position
Supports both binary and multi-valued protected attributes
⚖️ Proportionate Fairness (p-fairness)
Let:

f(p) = fraction of items belonging to protected group p
k = prefix length
A ranking is p-fair if for every k:

#items of group p in top k ∈ { floor(f(p)·k), ceil(f(p)·k) }
This ensures fairness at every ranking position, which is stronger than standard top-k fairness or statistical parity.

🎯 Problems Implemented
1️⃣ Individual p-Fairness (IPF)
Input: A single ranking ρ Output: A p-fair ranking σ minimizing Kendall-Tau distance to ρ.

This problem is useful as a building block for fair rank aggregation.

2️⃣ Rank Aggregation under p-Fairness (RAPF)
Input: Multiple rankings ρ₁, ρ₂, ..., ρₘ Output: A p-fair ranking σ minimizing total Kemeny distance:

κ(σ) = Σ K(σ, ρᵢ)
RAPF is NP-hard, so approximation frameworks are implemented.

🧠 Algorithms Implemented
🔹 Binary Protected Attribute (ℓ = 2)
GrBinaryIPF

Greedy algorithm
Exact solution
Time Complexity: O(n)
Maintains optimal ordering within each group
🔹 Multi-Valued Protected Attribute (ℓ > 2)
ExactMultiValuedIPF

Dynamic programming approach
Exact solution when number of groups is small
Polynomial in n, exponential in number of groups ℓ
ApproxMultiValuedIPF

Reduction to Minimum Weight Perfect Matching
Optimizes Spearman’s footrule distance
2-approximation for Kendall-Tau
Time Complexity: O(n^2.5 log n)
🔹 RAPF Frameworks
RandAlgRAPF

Randomized framework
Based on Pick-a-Perm technique
Provable approximation guarantees
AlgRAPF

Deterministic framework
Scalable to larger datasets
📏 Distance Measures Used
Kendall-Tau Distance – Pairwise disagreement measure
Kemeny Distance – Sum of Kendall-Tau distances across rankings
Spearman’s Footrule – Used for approximation in multi-valued IPF
🗂️ Project Structure
.
├── ipf/
│   ├── binary_ipf.py
│   ├── multi_ipf_exact.py
│   ├── multi_ipf_approx.py
│
├── rapf/
│   ├── rand_alg_rapf.py
│   ├── det_alg_rapf.py
│
├── utils/
│   ├── kendall_tau.py
│   ├── fairness_check.py
│
├── datasets/
├── main.py
└── README.md
🚀 How to Run
git clone <your-repo-link>
cd rank-aggregation-pfair
python main.py
You can modify input datasets and choose algorithms inside main.py and download the dependecies.

📊 Key Features
Exact and approximation solutions
Binary and multi-valued group support
Modular and extensible implementation
Suitable for academic experimentation and research projects
📚 Reference
Dong Wei et al., Rank Aggregation with Proportionate Fairness, Proceedings of SIGMOD 2022.


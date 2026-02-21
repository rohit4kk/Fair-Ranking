📌 Overview

This project implements algorithms for fair rank aggregation under the notion of Proportionate Fairness (p-fairness).

In many real-world decision systems (hiring, admissions, recommendation systems, resource allocation), multiple evaluators provide rankings over a common set of candidates.

Traditional rank aggregation focuses solely on minimizing disagreement with input rankings. However, this can unintentionally produce unfair outcomes when candidates belong to protected groups.

This implementation ensures that the final aggregated ranking:

Minimizes disagreement with input rankings (Kemeny / Kendall-Tau distance)

Enforces proportionate representation of protected groups at every prefix

Supports both binary and multi-valued protected attributes

Provides both exact and approximation algorithms

⚖️ Proportionate Fairness (p-Fairness)

Let:

f(p) = fraction of items belonging to protected group p

k = prefix length of the ranking

A ranking is p-fair if for every k:

# items of group p in top-k ∈ { floor(f(p)·k), ceil(f(p)·k) }

This ensures proportional representation at every position of the ranking, which is stronger than:

Top-k fairness

Statistical parity

Post-processing rebalancing

🎯 Problems Implemented
1️⃣ Individual p-Fairness (IPF)

Input: A single ranking ρ
Output: A p-fair ranking σ minimizing Kendall-Tau distance to ρ.

This serves as a core building block for fair rank aggregation.

2️⃣ Rank Aggregation under p-Fairness (RAPF)

Input: Multiple rankings ρ₁, ρ₂, ..., ρₘ
Output: A p-fair ranking σ minimizing total Kemeny distance:

κ(σ) = Σ K(σ, ρᵢ)

Since RAPF is NP-hard, the implementation includes approximation frameworks.

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

Optimizes Spearman’s Footrule distance

2-approximation for Kendall-Tau

Time Complexity: O(n²·⁵ log n)

🔹 RAPF Frameworks
RandAlgRAPF

Randomized framework

Based on Pick-a-Perm technique

Provable approximation guarantees

AlgRAPF

Deterministic framework

Scalable to larger datasets

📏 Distance Measures Used

Kendall-Tau Distance – Pairwise disagreement between rankings

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

You can modify:

Input datasets

Protected group definitions

Algorithm selection

inside main.py.

Make sure required dependencies are installed before execution.

📊 Key Features

Exact and approximation algorithms

Binary and multi-valued group support

Modular, extensible architecture

Suitable for academic experimentation and research

Clean separation between IPF and RAPF frameworks

📚 Reference

Dong Wei, Md Mouinul Islam, Baruch Schieber, Senjuti Basu Roy.
Rank Aggregation with Proportionate Fairness.
Proceedings of the ACM SIGMOD International Conference on Management of Data, 2022.

# Gap Analysis: Futoshiki Logic & Inference Project Requirements vs Source Code

This report assesses the current state of the source code in [Source/](Source) against the requirements set out in [Lab_requirement.md](Lab_requirement.md).

---

## 1. Compliance Matrix

| Requirement Area | Specification Description | File Reference | Status | Gap & Remarks |
| :--- | :--- | :--- | :---: | :--- |
| **Language Constraints** | Python 3.7+; solvers built from scratch (no external solvers/libraries like Z3/Clingo except for secondary validation). | [requirements.txt](requirements.txt) | **COMPLIANT** | Standard library only; complies with the "from scratch" constraint. |
| **Folder Structure** | Inputs in `Inputs/input-XX.txt`, outputs in `Outputs/output-XX.txt`. | `Source/Inputs/`, `Source/Outputs/` | **PARTIAL** | Input files exist correctly. Outputs, however, are generated as `output-XX-algo.txt` rather than `output-XX.txt`. |
| **Input Format** | Covers 10 distinct cases named `input-01.txt` to `input-10.txt` for sizes 4x4, 5x5, 6x6, 7x7, and 9x9. | `Inputs/` | **COMPLIANT** | All 10 cases covering the required sizes are correctly formatted. |
| **Output Format** | Complete solved grid with active constraints (`<`, `>`, `^`, `v`) embedded between values. | [parser.py](parser.py#L52-L109) | **COMPLIANT** | Grid alignment and inequality characters are correctly printed. |
| **Propositional Grounding** | Ground general FOL axioms for N; support automatic CNF conversion via logical rewrites (implication elimination, negation inward, variable splitting). | [kb_generator.py](kb_generator.py) | **NON-COMPLIANT** | Generates CNF directly using procedural loops. It has no formula AST or rewrite pipeline (implication elimination/splitting). |
| **Forward Chaining Engine** | Forward chaining reasoning system from scratch. Fire rules using Modus Ponens to derive `Val(i, j, v)` from ground facts. | [forward_chaining.py](forward_chaining.py) | **NON-COMPLIANT** | The solver runs a CSP Constraint Propagation/Arc-Consistency loop (reducing domain sizes). It does not represent logic rules or fire Modus Ponens. |
| **Backward Chaining Engine** | Prolog-style backward chaining interpreter. Horn clauses, depth-first SLD resolution, supporting queries (e.g. `Val(1, 2, ?)`). | [backward_chaining.py](backward_chaining.py) | **NON-COMPLIANT** | Standard recursive backtracking search over values 1 to N. It does not represent Horn clauses or execute SLD resolution. |
| **A\* Search** | State-space search with admissible heuristic $h(s)$ that never overestimates; evaluate on all 10 test cases. | [astar_solver.py](astar_solver.py) | **PARTIAL** | Employs a weak `empty_count` baseline heuristic. State expansion causes memory bloat, resulting in A* being explicitly skipped for $N \ge 6$ in [main.py](main.py#L176-L178). |
| **Baseline Solvers** | Brute-force and backtracking routines to serve as benchmarks. | [brute_force_solver.py](brute_force_solver.py)<br>[backtracking_solver.py](backtracking_solver.py) | **COMPLIANT** | Properly implemented and functional. |
| **Bonus GUI** | Interactive GUI rendering input states, solving animations, or completed grids (+10%). | *None* | **NON-COMPLIANT** | Not implemented. |

---

## 2. In-Depth Analysis of Critical Gaps

### A. Ground KB & CNF Generator
The project requires a general-purpose pipeline:
$$\text{FOL Axioms} \xrightarrow{\text{Rewrite steps}} \text{CNF}$$
However, [kb_generator.py](kb_generator.py) hardcodes the propositional sentences directly:
```python
# procedural loop directly generating clauses:
for v1 in range(1, n):
    for v2 in range(v1 + 1, n + 1):
        clauses.append([f"Less({v1},{v2})"])
```
There is no representation of logic operators ($\land, \lor, \neg, \Rightarrow$), and no rewrite engine implementing:
1. Implication elimination: $\alpha \Rightarrow \beta \equiv \neg\alpha \lor \beta$
2. De Morgan’s laws (negation inward migration)
3. Variable splitting

### B. Forward & Backward Chaining Engines
* **Forward Chaining**: The current [ForwardChainingSolver](forward_chaining.py#L4) performs domain reduction (similar to the AC-3 algorithm). It does not operate on a logic-based Knowledge Base containing rules and facts, nor does it instantiate Modus Ponens.
* **Backward Chaining**: The current [BackwardChainingSolver](backward_chaining.py#L3) is a backtracking search. It does not represent rules as Horn clauses ($A \land B \Rightarrow C$) and does not run SLD Resolution to prove queries.

### C. A\* Heuristic and Scaling issues
* The heuristic `heuristic_2` simply counts empty cells.
* In [astar_solver.py](astar_solver.py#L73), the priority queue stores instances of [FutoshikiPuzzle](puzzle.py#L5) (which deep-copies arrays on state transitions). This leads to high memory consumption and slow runs.
* Because of this, A* is turned off for cases with $N \ge 6$:
  ```python
  if algo_name == 'a_star' and n >= 6:
      print(f"[a_star] Bo qua (N={n} lon)")
      continue
  ```
  This prevents collecting comparative data for A* on the larger grids (6x6, 7x7, 9x9) for the report.

---

## 3. Remediation Recommendations

### 1. Re-implement Forward/Backward Logic
* Define a lightweight logical representation for clauses/Horn clauses.
* **Forward Chaining**: Implement a true forward chaining loop that maintains a set of inferred facts (e.g. `Value(r, c, v)`) and applies Modus Ponens when rule premises are satisfied.
* **Backward Chaining**: Write a Prolog-like resolution engine. Define rules such as `Value(R, C, V) :- \+ Value(R, C2, V), ...` and resolve queries using SLD resolution (keeping track of unified variables).

### 2. Upgrade A\* State & Heuristic
* Change the A* state representation from a full cloned object to a lightweight immutable structure (e.g., a tuple of values or a coordinate map).
* Implement a stronger admissible heuristic:
  * Count the constraints involved in the unassigned cells (Degree Heuristic).
  * Calculate minimum remaining domain sizes using a light forward-checking or AC-3 pass, counting the total number of options.
* Enable A* for N $\ge$ 6 so that benchmarking results can be gathered across all test cases.

### 3. File Naming Alignment
* Adjust [main.py](main.py#L274-L278) to save files directly to `output-XX.txt` in the production run configuration, rather than using suffixing suffixes like `-backtracking.txt`.

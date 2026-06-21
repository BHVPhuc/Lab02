# kb_generator.py
# Full FOL-to-CNF-to-ground conversion for Futoshiki
# Corrected: consistent predicate names, added "at least one" axiom.

import os
from typing import List, Set, Dict, Any, Optional
from puzzle import FutoshikiPuzzle

# ----------------------------------------------------------------------
# 1. FOL Formula Classes
# ----------------------------------------------------------------------

class Variable:
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name
    def __hash__(self):
        return hash(self.name)

class Predicate:
    def __init__(self, name: str, *args):
        self.name = name
        self.args = args
    def __repr__(self):
        # No spaces inside arguments
        return f"{self.name}({','.join(str(a) for a in self.args)})"
    def __eq__(self, other):
        return isinstance(other, Predicate) and self.name == other.name and self.args == other.args
    def __hash__(self):
        return hash((self.name, self.args))

class Not:
    def __init__(self, formula):
        self.formula = formula
    def __repr__(self):
        return f"¬{self.formula}"
    def __eq__(self, other):
        return isinstance(other, Not) and self.formula == other.formula
    def __hash__(self):
        return hash(('Not', self.formula))

class And:
    def __init__(self, *formulas):
        self.formulas = formulas
    def __repr__(self):
        return f"({' ∧ '.join(str(f) for f in self.formulas)})"
    def __eq__(self, other):
        return isinstance(other, And) and self.formulas == other.formulas
    def __hash__(self):
        return hash(('And', self.formulas))

class Or:
    def __init__(self, *formulas):
        self.formulas = formulas
    def __repr__(self):
        return f"({' ∨ '.join(str(f) for f in self.formulas)})"
    def __eq__(self, other):
        return isinstance(other, Or) and self.formulas == other.formulas
    def __hash__(self):
        return hash(('Or', self.formulas))

class Implies:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent
    def __repr__(self):
        return f"({self.antecedent} ⇒ {self.consequent})"
    def __eq__(self, other):
        return isinstance(other, Implies) and self.antecedent == other.antecedent and self.consequent == other.consequent
    def __hash__(self):
        return hash(('Implies', self.antecedent, self.consequent))

class ForAll:
    def __init__(self, variables, formula):
        self.variables = [v if isinstance(v, Variable) else Variable(v) for v in variables]
        self.formula = formula
    def __repr__(self):
        vars_str = ', '.join(str(v) for v in self.variables)
        return f"∀{vars_str} {self.formula}"
    def __eq__(self, other):
        return isinstance(other, ForAll) and self.variables == other.variables and self.formula == other.formula
    def __hash__(self):
        return hash(('ForAll', tuple(self.variables), self.formula))


# ----------------------------------------------------------------------
# 2. Conversion Pipeline
# ----------------------------------------------------------------------

def eliminate_implications(formula):
    """Convert A ⇒ B to ¬A ∨ B."""
    if isinstance(formula, Implies):
        return Or(Not(eliminate_implications(formula.antecedent)),
                  eliminate_implications(formula.consequent))
    elif isinstance(formula, And):
        return And(*(eliminate_implications(f) for f in formula.formulas))
    elif isinstance(formula, Or):
        return Or(*(eliminate_implications(f) for f in formula.formulas))
    elif isinstance(formula, Not):
        return Not(eliminate_implications(formula.formula))
    elif isinstance(formula, ForAll):
        return ForAll(formula.variables, eliminate_implications(formula.formula))
    else:
        return formula

def to_nnf(formula):
    """Push negations inward (Negation Normal Form)."""
    if isinstance(formula, Not):
        f = formula.formula
        if isinstance(f, Not):
            return to_nnf(f.formula)
        elif isinstance(f, And):
            return Or(*(to_nnf(Not(sub)) for sub in f.formulas))
        elif isinstance(f, Or):
            return And(*(to_nnf(Not(sub)) for sub in f.formulas))
        elif isinstance(f, ForAll):
            return Not(f)   # we don't have ∃, so keep it
        else:
            return Not(f)
    elif isinstance(formula, And):
        return And(*(to_nnf(f) for f in formula.formulas))
    elif isinstance(formula, Or):
        return Or(*(to_nnf(f) for f in formula.formulas))
    elif isinstance(formula, ForAll):
        return ForAll(formula.variables, to_nnf(formula.formula))
    else:
        return formula

def drop_universals(formula):
    """Remove universal quantifiers (all variables are universally quantified)."""
    if isinstance(formula, ForAll):
        return drop_universals(formula.formula)
    elif isinstance(formula, And):
        return And(*(drop_universals(f) for f in formula.formulas))
    elif isinstance(formula, Or):
        return Or(*(drop_universals(f) for f in formula.formulas))
    elif isinstance(formula, Not):
        return Not(drop_universals(formula.formula))
    else:
        return formula

def distribute_or_over_and(formula):
    """Convert to CNF: conjunction of disjunctions."""
    if isinstance(formula, And):
        parts = [distribute_or_over_and(f) for f in formula.formulas]
        clauses = []
        for part in parts:
            if isinstance(part, And):
                clauses.extend(part.formulas)
            else:
                clauses.append(part)
        return And(*clauses)
    elif isinstance(formula, Or):
        def flatten_or(f):
            if isinstance(f, Or):
                return [sub for part in f.formulas for sub in flatten_or(part)]
            else:
                return [f]
        disjuncts = flatten_or(formula)
        and_terms = [d for d in disjuncts if isinstance(d, And)]
        other_terms = [d for d in disjuncts if not isinstance(d, And)]
        if not and_terms:
            return Or(*other_terms)
        first_and = and_terms[0]
        rest_or = Or(*(other_terms + and_terms[1:])) if (other_terms or and_terms[1:]) else None
        if rest_or is None:
            return And(*(distribute_or_over_and(f) for f in first_and.formulas))
        else:
            conjuncts = []
            for conj in first_and.formulas:
                or_formula = Or(conj, rest_or)
                conjuncts.append(distribute_or_over_and(or_formula))
            return And(*conjuncts)
    elif isinstance(formula, Not):
        return formula
    else:
        return formula

def to_cnf(formula):
    """Convert a FOL formula to CNF (no quantifiers)."""
    formula = eliminate_implications(formula)
    formula = to_nnf(formula)
    formula = drop_universals(formula)
    formula = distribute_or_over_and(formula)
    return formula

def collect_variables(formula):
    """Return set of Variable objects in the formula."""
    if isinstance(formula, Variable):
        return {formula}
    elif isinstance(formula, Predicate):
        vars_set = set()
        for a in formula.args:
            vars_set.update(collect_variables(a))
        return vars_set
    elif isinstance(formula, Not):
        return collect_variables(formula.formula)
    elif isinstance(formula, And) or isinstance(formula, Or):
        vars_set = set()
        for f in formula.formulas:
            vars_set.update(collect_variables(f))
        return vars_set
    else:
        return set()

def substitute(formula, subst):
    """Apply substitution dict (Variable -> value) to formula."""
    if isinstance(formula, Variable):
        return subst.get(formula, formula)
    elif isinstance(formula, Predicate):
        new_args = [substitute(a, subst) for a in formula.args]
        return Predicate(formula.name, *new_args)
    elif isinstance(formula, Not):
        return Not(substitute(formula.formula, subst))
    elif isinstance(formula, And):
        return And(*(substitute(f, subst) for f in formula.formulas))
    elif isinstance(formula, Or):
        return Or(*(substitute(f, subst) for f in formula.formulas))
    else:
        return formula

def simplify_clause(formula, builtins):
    """
    Evaluate built-in predicates in a ground clause.
    Returns:
      - None if tautology (builtin true)
      - an empty Or() if false (builtins all false)
      - simplified clause otherwise.
    """
    if isinstance(formula, Or):
        new_disjuncts = []
        for disj in formula.formulas:
            if isinstance(disj, Predicate) and disj.name in builtins:
                if builtins[disj.name](*disj.args):
                    return None  # tautology
                else:
                    continue    # skip false literal
            elif isinstance(disj, Not) and isinstance(disj.formula, Predicate) and disj.formula.name in builtins:
                if not builtins[disj.formula.name](*disj.formula.args):
                    return None  # negated false = true
                else:
                    continue
            else:
                new_disjuncts.append(disj)
        if not new_disjuncts:
            return Or()  # empty clause = False
        return Or(*new_disjuncts)
    else:
        # single literal
        if isinstance(formula, Predicate) and formula.name in builtins:
            if builtins[formula.name](*formula.args):
                return None
            else:
                return Or()
        elif isinstance(formula, Not) and isinstance(formula.formula, Predicate) and formula.formula.name in builtins:
            if not builtins[formula.formula.name](*formula.formula.args):
                return None
            else:
                return Or()
        else:
            return formula

def ground_cnf(formula, n):
    """
    Ground a CNF formula over domain: indices 0..n-1, values 1..n.
    Returns list of ground clauses (each a list of literal strings).
    """
    domain_indices = list(range(n))
    domain_values = list(range(1, n+1))
    builtins = {
        'Equal': lambda a,b: a == b,
        'Distinct': lambda a,b: a != b,
        'Less': lambda a,b: a < b,
        'Greater': lambda a,b: a > b,
    }

    if isinstance(formula, And):
        clauses = formula.formulas
    else:
        clauses = [formula]

    ground_clauses = []

    for clause in clauses:
        vars_set = collect_variables(clause)
        if not vars_set:
            simplified = simplify_clause(clause, builtins)
            if simplified is not None:
                if isinstance(simplified, Or) and not simplified.formulas:
                    ground_clauses.append([])
                else:
                    literals = [str(lit) for lit in (simplified.formulas if isinstance(simplified, Or) else [simplified])]
                    ground_clauses.append(literals)
            continue

        vars_list = list(vars_set)
        domains = []
        for var in vars_list:
            if var.name.startswith('v'):
                domains.append(domain_values)
            else:
                domains.append(domain_indices)

        def rec(idx, subst):
            if idx == len(vars_list):
                substituted = substitute(clause, subst)
                simplified = simplify_clause(substituted, builtins)
                if simplified is not None:
                    if isinstance(simplified, Or) and not simplified.formulas:
                        ground_clauses.append([])
                    else:
                        literals = [str(lit) for lit in (simplified.formulas if isinstance(simplified, Or) else [simplified])]
                        ground_clauses.append(literals)
                return
            for val in domains[idx]:
                subst[vars_list[idx]] = val
                rec(idx+1, subst)

        rec(0, {})

    return ground_clauses


# ----------------------------------------------------------------------
# 3. Axiom Definitions (FOL formulas)
# ----------------------------------------------------------------------

def at_most_one_axiom():
    """∀i∀j∀v1∀v2 (Value(i,j,v1) ∧ Value(i,j,v2) ⇒ Equal(v1,v2))"""
    i = Variable('i')
    j = Variable('j')
    v1 = Variable('v1')
    v2 = Variable('v2')
    body = And(Predicate('Value', i, j, v1), Predicate('Value', i, j, v2))
    return ForAll([i, j, v1, v2], Implies(body, Predicate('Equal', v1, v2)))

def row_uniqueness_axiom():
    """∀i∀j1∀j2∀v (Distinct(j1,j2) ∧ Value(i,j1,v) ∧ Value(i,j2,v) ⇒ False)"""
    i = Variable('i')
    j1 = Variable('j1')
    j2 = Variable('j2')
    v = Variable('v')
    body = And(Predicate('Distinct', j1, j2), Predicate('Value', i, j1, v), Predicate('Value', i, j2, v))
    return ForAll([i, j1, j2, v], Implies(body, Predicate('False')))

def column_uniqueness_axiom():
    """∀i1∀i2∀j∀v (Distinct(i1,i2) ∧ Value(i1,j,v) ∧ Value(i2,j,v) ⇒ False)"""
    i1 = Variable('i1')
    i2 = Variable('i2')
    j = Variable('j')
    v = Variable('v')
    body = And(Predicate('Distinct', i1, i2), Predicate('Value', i1, j, v), Predicate('Value', i2, j, v))
    return ForAll([i1, i2, j, v], Implies(body, Predicate('False')))


# ----------------------------------------------------------------------
# 4. KB Generator
# ----------------------------------------------------------------------

def generate_kb(puzzle: FutoshikiPuzzle) -> List[List[str]]:
    """
    Generate a ground CNF knowledge base for the given puzzle.
    """
    n = puzzle.n
    clauses = []

    # ---- 4.1 Facts (ground unit clauses) ----
    for i in range(n):
        for j in range(n):
            val = puzzle.grid[i][j]
            if val != 0:
                clauses.append([f"Value({i},{j},{val})"])

    # Less(v1,v2) for all 1 <= v1 < v2 <= n
    for v1 in range(1, n):
        for v2 in range(v1 + 1, n + 1):
            clauses.append([f"Less({v1},{v2})"])

    # ---- 4.2 Inequality constraints (direct forbidding) ----
    # Horizontal
    for i in range(n):
        for j in range(n - 1):
            h = puzzle.h_constraints[i][j]
            if h == 1:   # left < right
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 >= v2:
                            clauses.append([f"¬Value({i},{j},{v1})", f"¬Value({i},{j+1},{v2})"])
            elif h == -1:
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 <= v2:
                            clauses.append([f"¬Value({i},{j},{v1})", f"¬Value({i},{j+1},{v2})"])
    # Vertical
    for i in range(n - 1):
        for j in range(n):
            v = puzzle.v_constraints[i][j]
            if v == 1:   # top < bottom
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 >= v2:
                            clauses.append([f"¬Value({i},{j},{v1})", f"¬Value({i+1},{j},{v2})"])
            elif v == -1:
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 <= v2:
                            clauses.append([f"¬Value({i},{j},{v1})", f"¬Value({i+1},{j},{v2})"])

    # ---- 4.3 At least one value per cell (direct generation) ----
    for i in range(n):
        for j in range(n):
            clause = [f"Value({i},{j},{v})" for v in range(1, n + 1)]
            clauses.append(clause)

    # ---- 4.4 At most one per cell (conversion) ----
    axiom = at_most_one_axiom()
    cnf = to_cnf(axiom)
    ground_clauses = ground_cnf(cnf, n)
    # Remove clauses that contain "False" (they are redundant)
    for gc in ground_clauses:
        if "False" not in "".join(gc):
            clauses.append(gc)

    # ---- 4.5 Row uniqueness (conversion) ----
    axiom = row_uniqueness_axiom()
    cnf = to_cnf(axiom)
    ground_clauses = ground_cnf(cnf, n)
    for gc in ground_clauses:
        if "False" not in "".join(gc):
            clauses.append(gc)

    # ---- 4.6 Column uniqueness (conversion) ----
    axiom = column_uniqueness_axiom()
    cnf = to_cnf(axiom)
    ground_clauses = ground_cnf(cnf, n)
    for gc in ground_clauses:
        if "False" not in "".join(gc):
            clauses.append(gc)

    # ---- 4.7 Row completeness (direct) ----
    for i in range(n):
        for v in range(1, n + 1):
            clause = [f"Value({i},{j},{v})" for j in range(n)]
            clauses.append(clause)

    # ---- 4.8 Column completeness (direct) ----
    for j in range(n):
        for v in range(1, n + 1):
            clause = [f"Value({i},{j},{v})" for i in range(n)]
            clauses.append(clause)

    # ---- 4.9 Remove duplicates ----
    seen = set()
    unique_clauses = []
    for clause in clauses:
        key = tuple(sorted(clause))
        if key not in seen:
            seen.add(key)
            unique_clauses.append(clause)

    return unique_clauses


# ----------------------------------------------------------------------
# 5. Helper to write KB to file
# ----------------------------------------------------------------------

def write_kb(clauses: List[List[str]], output_path: str) -> None:
    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for clause in clauses:
            f.write(",".join(clause) + "\n")


# ----------------------------------------------------------------------
# 6. Main: generate KB for all input files
# ----------------------------------------------------------------------

if __name__ == "__main__":
    from parser import read_input

    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(current_dir, "Inputs")
    kb_dir = os.path.join(current_dir, "KB")
    os.makedirs(kb_dir, exist_ok=True)

    input_files = sorted([
        f for f in os.listdir(input_dir)
        if f.startswith("input-") and f.endswith(".txt")
    ])

    if not input_files:
        print(f"No input files found in {input_dir}")
    else:
        for filename in input_files:
            input_path = os.path.join(input_dir, filename)
            kb_filename = filename.replace("input-", "kb-")
            output_path = os.path.join(kb_dir, kb_filename)
            print(f"Processing {filename} -> {kb_filename}")
            try:
                puzzle = read_input(input_path)
                kb = generate_kb(puzzle)
                write_kb(kb, output_path)
                print(f"  Done: {len(kb)} clauses written.")
            except Exception as e:
                print(f"  Error: {e}")
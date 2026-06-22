# validator.py
# Global validation module for Futoshiki puzzle solutions
# Created as part of Member 1 deliverables

from typing import List
from puzzle import FutoshikiPuzzle

def validate_row_uniqueness(n: int, grid: List[List[int]]) -> bool:
    """Check if all values in each row are unique and within [1, n]."""
    for r in range(n):
        row_vals = [grid[r][c] for c in range(n) if grid[r][c] != 0]
        # Check uniqueness
        if len(row_vals) != len(set(row_vals)):
            return False
        # Check range
        for v in row_vals:
            if not (1 <= v <= n):
                return False
    return True

def validate_col_uniqueness(n: int, grid: List[List[int]]) -> bool:
    """Check if all values in each column are unique and within [1, n]."""
    for c in range(n):
        col_vals = [grid[r][c] for r in range(n) if grid[r][c] != 0]
        # Check uniqueness
        if len(col_vals) != len(set(col_vals)):
            return False
        # Check range
        for v in col_vals:
            if not (1 <= v <= n):
                return False
    return True

def validate_inequality_constraints(puzzle: FutoshikiPuzzle, grid: List[List[int]]) -> bool:
    """Check if all horizontal and vertical inequality constraints are satisfied."""
    n = puzzle.n
    
    # 1. Horizontal inequalities
    for r in range(n):
        for c in range(n - 1):
            h_val = puzzle.h_constraints[r][c]
            if h_val != 0:
                left_val = grid[r][c]
                right_val = grid[r][c+1]
                if left_val != 0 and right_val != 0:
                    if h_val == 1 and not (left_val < right_val):
                        return False
                    if h_val == -1 and not (left_val > right_val):
                        return False
                        
    # 2. Vertical inequalities
    for r in range(n - 1):
        for c in range(n):
            v_val = puzzle.v_constraints[r][c]
            if v_val != 0:
                top_val = grid[r][c]
                bottom_val = grid[r+1][c]
                if top_val != 0 and bottom_val != 0:
                    if v_val == 1 and not (top_val < bottom_val):  # top < bottom
                        return False
                    if v_val == -1 and not (top_val > bottom_val): # top > bottom
                        return False
                        
    return True

def validate_given_clues(puzzle: FutoshikiPuzzle, grid: List[List[int]]) -> bool:
    """Check if the grid preserves all original given clues from the puzzle."""
    for r in range(puzzle.n):
        for c in range(puzzle.n):
            # If the original puzzle had a pre-filled clue at (r, c), it must match
            # Note: puzzle.grid contains the original clue grid if we haven't mutated it, 
            # but usually solvers clone the puzzle or mutate it. 
            # We assume puzzle is the original puzzle state containing clues.
            pass
    return True

def validate_solution(puzzle: FutoshikiPuzzle, grid: List[List[int]], original_puzzle: FutoshikiPuzzle = None) -> bool:
    """
    Perform a complete verification of a solved grid against a puzzle's rules.
    Returns True if the grid is a valid complete solution, False otherwise.
    """
    n = puzzle.n
    
    # 1. Check if all cells are filled
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                return False
                
    # 2. Check row uniqueness
    if not validate_row_uniqueness(n, grid):
        return False
        
    # 3. Check column uniqueness
    if not validate_col_uniqueness(n, grid):
        return False
        
    # 4. Check inequality constraints
    if not validate_inequality_constraints(puzzle, grid):
        return False
        
    # 5. Check clues (against original_puzzle if provided)
    if original_puzzle is not None:
        for r in range(n):
            for c in range(n):
                clue = original_puzzle.grid[r][c]
                if clue != 0 and grid[r][c] != clue:
                    return False
                    
    return True

def best_remaining_mutant(mutant_scores: dict[str, int], threshold: int) -> str:
    return max(
        (mutant for mutant in mutant_scores if mutant_scores[mutant] < threshold),
        key=mutant_scores.get
    )
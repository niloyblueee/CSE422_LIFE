def calculate_utility(generated_gene, target_gene, positional_weights, sid_prefix, booster_start_index):
    """
    The 'End of the World' calculation. 
    Runs only when the sequence is complete.
    """
    n = max(len(generated_gene), len(target_gene))
    total_utility = 0
    booster = sid_prefix / 100.0  # For ID 23201169, this is 0.23

    for i in range(n):
        # 1. Get ASCII values (0 if character doesn't exist)
        if i < len(generated_gene):
            char_gen = ord(generated_gene[i])
        else:
            char_gen = 0

        if i < len(target_gene):
            char_tar = ord(target_gene[i])
        else:
            char_tar = 0
        
        # 2. Get the base weight for this position
        # Use SID weight if i < target length, else default to 1
        if i < len(positional_weights):
            w = positional_weights[i]
        else:
            w = 1
        
        # 3. Apply Task II Booster if Agent 1 picked 'S'
        if booster_start_index is not None and i >= booster_start_index:
            w *= booster
            
        # 4. Add to sum: weight * absolute difference
        total_utility += w * abs(char_gen - char_tar)
        
    return -total_utility

def minimax(available_nucleotides, assembled_gene, target_gene, positional_weights, sid_prefix, alpha_bound, beta_bound, is_maximizing_player, booster_start_pos):
    """
    The 'Shoe-Swapping' function.
    """
    # BASE CASE: If pool is empty, calculate points and send them up
    if not available_nucleotides:
        return calculate_utility(assembled_gene, target_gene, positional_weights, sid_prefix, booster_start_pos)

    if is_maximizing_player:
        best_value = float('-inf')
        for i in range(len(available_nucleotides)):
            nucleotide = available_nucleotides[i]
            remaining_pool = available_nucleotides[:i] + available_nucleotides[i+1:]
            
            # Agent 1 picking 'S' triggers the booster position
            if nucleotide == 'S':
                new_booster_pos = len(assembled_gene)
            else:
                new_booster_pos = booster_start_pos
            
            # SHOE SWAP: Call same function but as Minimizer
            candidate_value = minimax(remaining_pool, assembled_gene + nucleotide, target_gene, 
                                      positional_weights, sid_prefix, alpha_bound, beta_bound, False, new_booster_pos)
            
            best_value = max(best_value, candidate_value)
            alpha_bound = max(alpha_bound, candidate_value)
            if beta_bound <= alpha_bound: # Pruning
                break
        return best_value

    else:
        best_value = float('inf')
        for i in range(len(available_nucleotides)):
            nucleotide = available_nucleotides[i]
            remaining_pool = available_nucleotides[:i] + available_nucleotides[i+1:]
            
            # SHOE SWAP: Call same function but as Maximizer
            # Note: Agent 2 picking 'S' does NOT change booster_start_pos
            candidate_value = minimax(remaining_pool, assembled_gene + nucleotide, target_gene, 
                                      positional_weights, sid_prefix, alpha_bound, beta_bound, True, booster_start_pos)
            
            best_value = min(best_value, candidate_value)
            beta_bound = min(beta_bound, candidate_value)
            if beta_bound <= alpha_bound: # Pruning
                break
        return best_value

# --- EXECUTION FOR SID: 23201169 ---
my_sid = "23201169"
sid_prefix = int(my_sid[:2]) # 23
target = "ATGC"
# Weights = last n digits of SID where n is target length (4) -> [1, 1, 6, 9]
my_weights = []
for digit in my_sid[-len(target):]:
    my_weights.append(int(digit))

# Task I: Standard Pool
pool_task1 = ["A", "T", "C", "G"]
result_task1 = minimax(pool_task1, "", target, my_weights, sid_prefix, 
                       float('-inf'), float('inf'), True, None)

# Task II: Pool with 'S'
pool_task2 = ["A", "T", "C", "G", "S"]
result_task2 = minimax(pool_task2, "", target, my_weights, sid_prefix, 
                       float('-inf'), float('inf'), True, None)

print(f"Task I Utility Score: {result_task1}")
print(f"Task II Utility Score: {result_task2}")
print(f"Decision: {'YES' if result_task2 > result_task1 else 'NO'}")
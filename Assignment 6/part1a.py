# Define the conditional probabilities from the Bayesian network
prob_c = 0.5  # P(C=true)
prob_s_given_c = 0.1  # P(S=true|C)
prob_r_given_c = 0.8  # P(R=true|C)

prob_not_s_given_not_c = 0.5  # P(¬S=true|¬C)
prob_r_given_not_c = 0.2  # P(R=true|¬C)

# Transition probabilities based on state changes
def transition_probability(current_state, next_state):
    # If Cloudy changes state
    if current_state[0] != next_state[0]:
        return prob_c if next_state[0] else (1 - prob_c)
    # If Rain changes state and it's currently Cloudy
    elif current_state[1] != next_state[1] and current_state[0]:
        return prob_r_given_c if next_state[1] else (1 - prob_r_given_c)
    # If Rain changes state and it's currently not Cloudy
    elif current_state[1] != next_state[1] and not current_state[0]:
        return prob_r_given_not_c if next_state[1] else (1 - prob_r_given_not_c)
    # No change in state
    else:
        return 0

# Define the states
states = [
    (True, True, False, True),   # S1: C, R, ~S, W
    (True, False, False, True),  # S2: C, ~R, ~S, W
    (False, True, False, True),  # S3: ~C, R, ~S, W
    (False, False, False, True)  # S4: ~C, ~R, ~S, W
]

# Initialize the transition matrix
Q = [[0 for _ in range(4)] for _ in range(4)]

# Populate the transition matrix
for i, state_from in enumerate(states):
    for j, state_to in enumerate(states):
        Q[i][j] = transition_probability(state_from, state_to)

    # Adjust probabilities so they sum to 1 for each row
    row_sum = sum(Q[i])
    if row_sum != 1:
        # Assume the remainder of the probability is the probability of staying in the same state
        Q[i][i] += 1 - row_sum

# Print the transition matrix Q
for row in Q:
    print(' '.join('{:.4f}'.format(p) for p in row))
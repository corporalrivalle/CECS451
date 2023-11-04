import random

# Define conditional probability tables (CPTs) from Figure 1
P_C = {"t": 0.5, "f": 0.5}
P_S_given_C = {"t": {"t": 0.1, "f": 0.5}, "f": {"t": 0.5, "f": 0.5}}
P_R_given_C = {"t": {"t": 0.8, "f": 0.2}, "f": {"t": 0.2, "f": 0.8}}
P_W_given_S_R = {"t": {"t": {"t": 0.99, "f": 0.9}, "f": {"t": 0.95, "f": 0.05}},
                "f": {"t": {"t": 0.9, "f": 0.05}, "f": {"t": 0.95, "f": 0.99}}}

# Initialize states for C, S, R, W
states = [{"C": "t", "S": "t", "R": "t", "W": "t"} for _ in range(1000)]

def proposal(state):
    """ Generate a new proposal state """
    new_state = state.copy()
    flip = random.choice(["C", "S", "R", "W"])
    new_state[flip] = "t" if new_state[flip] == "f" else "f"
    return new_state

def acceptance_prob(old_state, new_state):
    """ Calculate acceptance probability """
    old_prob = P_C[old_state["C"]] * \
               P_S_given_C[old_state["C"]][old_state["S"]] * \
               P_R_given_C[old_state["C"]][old_state["R"]] * \
               P_W_given_S_R[old_state["S"]][old_state["R"]][old_state["W"]]
    
    new_prob = P_C[new_state["C"]] * \
               P_S_given_C[new_state["C"]][new_state["S"]] * \
               P_R_given_C[new_state["C"]][new_state["R"]] * \
               P_W_given_S_R[new_state["S"]][new_state["R"]][new_state["W"]]
    
    return min(1, new_prob/old_prob)

# MCMC sampling
samples = []
current_state = {"C": "t", "S": "t", "R": "t", "W": "t"}
for _ in range(1000000):
    proposed_state = proposal(current_state)
    alpha = acceptance_prob(current_state, proposed_state)
    if random.uniform(0, 1) < alpha:
        current_state = proposed_state
    samples.append(current_state)

# Compute estimates for the desired queries
def estimate_prob(query):
    count = sum(1 for s in samples if all(s[var] == val for var, val in query.items()))
    return count / len(samples)

print("P(C|S=r):", estimate_prob({"S": "r"}))
print("P(C|S=t):", estimate_prob({"S": "t"}))
print("P(R|C=t, S=w):", estimate_prob({"C": "t", "S": "w"}))
print("P(R|C=f, S=w):", estimate_prob({"C": "f", "S": "w"}))

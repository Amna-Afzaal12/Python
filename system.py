# -------------------------
# Rule-based Expert System
# -------------------------

RULES = [
    {
        "if": ["high_traffic", "no_user_activity"],
        "then": "DDoS"
    },
    {
        "if": ["many_ports", "failed_logins"],
        "then": "Port Scan"
    },
    {
        "if": ["suspicious_files", "outbound_connections"],
        "then": "Malware"
    },
    {
        "if": ["normal_traffic"],
        "then": "Normal"
    }
]

# -------------------------
# Forward chaining engine
# -------------------------
def forward_chaining(facts, trace):
    conclusions = set()

    changed = True
    while changed:
        changed = False
        for rule in RULES:
            if all(facts.get(cond, False) for cond in rule["if"]):
                if rule["then"] not in conclusions:
                    conclusions.add(rule["then"])
                    trace.append(
                        f"Rule fired: IF {' AND '.join(rule['if'])} THEN {rule['then']}"
                    )
                    changed = True
    return conclusions

# -------------------------
# Ask user for missing facts
# -------------------------
def get_fact(facts, fact_name):
    if fact_name not in facts:
        answer = input(f"Is '{fact_name}' true? (y/n): ").lower()
        facts[fact_name] = answer == "y"
    return facts[fact_name]

def ensure_facts(facts):
    all_conditions = {cond for rule in RULES for cond in rule["if"]}
    for cond in all_conditions:
        get_fact(facts, cond)

# -------------------------
# Test scenarios
# -------------------------
SCENARIOS = [
    ({"high_traffic": True, "no_user_activity": True}, "DDoS"),
    ({"many_ports": True, "failed_logins": True}, "Port Scan"),
    ({"suspicious_files": True, "outbound_connections": True}, "Malware"),
    ({"normal_traffic": True}, "Normal"),
    ({"high_traffic": True, "no_user_activity": False}, "Normal"),
    ({"many_ports": True, "failed_logins": False}, "Normal"),
    ({"suspicious_files": True, "outbound_connections": False}, "Normal"),
    ({"high_traffic": True, "no_user_activity": True}, "DDoS"),
    ({"many_ports": True, "failed_logins": True}, "Port Scan"),
    ({"suspicious_files": True, "outbound_connections": True}, "Malware")
]

# -------------------------
# Evaluation
# -------------------------
correct = 0

for i, (facts, expected) in enumerate(SCENARIOS, 1):
    trace = []
    conclusions = forward_chaining(facts, trace)

    prediction = list(conclusions)[0] if conclusions else "Normal"
    if prediction == expected:
        correct += 1

    print(f"\nScenario {i}")
    print("Facts:", facts)
    print("Reasoning trace:")
    for step in trace:
        print(" ", step)
    print("Prediction:", prediction)
    print("Expected:", expected)

# -------------------------
# Results
# -------------------------
accuracy = correct / len(SCENARIOS)
print("\nFinal Accuracy:", accuracy)

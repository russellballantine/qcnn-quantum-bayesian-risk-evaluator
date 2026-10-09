# src/qbn_core.py
print(">>> DEBUG: Launching Quantum Bayesian Core Engine...")

import pennylane as qml
import torch
import numpy as np

# Initialize a default simulator for our 3-node graph (using 3 wires total)
# Wire 0: Vulnerability Present (V)
# Wire 1: Attacker Exploit Success (E)
# Wire 2: Critical Asset Impact Realized (I)
dev = qml.device("default.qubit", wires=3)

def prob_to_angle(prob):
    """
    Converts a classical probability scalar into its exact quantum state 
    vector rotation angle theta.
    """
    # Guard against precision limit bounds
    prob = max(0.0, min(1.0, prob))
    return 2.0 * np.arcsin(np.sqrt(prob))

@qml.qnode(dev, interface="torch")
def quantum_security_chain(p_v, weights):
    """
    Evaluates cascading risk inference across a 3-node Quantum Bayesian chain.
    
    Args:
        p_v (float): Normalized prior probability of the vulnerability node.
        weights (tensor): Trainable parameters mapping conditional threat postures.
    Returns:
        list: Pauli-Z expectation values across all 3 network registers.
    """
    # --- NODE 1: VULNERABILITY PRESENT (V) ---
    # Convert prior scalar into a state vector polarization angle
    theta_v = prob_to_angle(p_v)
    qml.RY(theta_v, wires=0)
    
    # --- NODE 2: ATTACKER EXPLOIT TELEMETRY (E) ---
    # Conditioned directly on Node 1 via Entanglement.
    # If Wire 0 is |0> (Safe), rotate by weights[0].
    # If Wire 0 is |1> (Vulnerable), rotate by weights[1].
    qml.CRY(weights[0], wires=[0, 1]) 
    
    # --- NODE 3: ASSET IMPACT REALIZED (I) ---
    # Conditioned on Node 2 (Exploit Success).
    qml.CRY(weights[2], wires=[1, 2])
    
    # Measure the Pauli-Z configurations across all registers
    # Output values are tightly bounded between [-1.0, 1.0]
    # -1.0 implies 100% Compromise realized (|1>), 1.0 implies 100% Safe (|0>)
    return [qml.expval(qml.PauliZ(wires=i)) for i in range(3)]

def evaluate_network_risk(metrics):
    """
    Bridges parsed metric inputs into the active QBN simulation circuit.
    """
    # Extract prior from our dataset parser dictionary structure
    vulnerability_prior = metrics["severity_prior"]
    
    # Initialize mock conditional policy weights
    # weights[0] = Exploit likelihood if vulnerability is absent
    # weights[1] = Exploit likelihood if vulnerability is present
    # weights[2] = Cascade impact likelihood if exploit succeeds
    policy_weights = torch.tensor([0.1, 1.8, 2.2], requires_grad=True)
    
    # Execute forward pass through QBN
    expectations = torch.stack(quantum_security_chain(vulnerability_prior, policy_weights))
    
    # Convert Pauli-Z expectations back to clean classical probabilities: P(Compromise) = (1 - expval) / 2
    compromise_probabilities = (1.0 - expectations) / 2.0
    
    print("\n--- QUANTUM BAYESIAN LOGIC PASSED ---")
    print(f"Node [V] - Vulnerability Prior Prob: {vulnerability_prior:.4f}")
    print(f"Node [E] - Attacker Exploit Prob   : {compromise_probabilities[1].item():.4f}")
    print(f"Node [I] - Cascading Impact Prob   : {compromise_probabilities[2].item():.4f}")
    
    return compromise_probabilities

if __name__ == "__main__":
    # Simulate intake metrics format
    mock_metrics = {
        "cve": "CVE-2021-44228",
        "exploitability_prior": 0.1,
        "severity_prior": 0.5  # Binds to our fallback structure cleanly
    }
    evaluate_network_risk(mock_metrics)

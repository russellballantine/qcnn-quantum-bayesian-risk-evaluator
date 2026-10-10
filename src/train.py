import pennylane as qml
from pennylane import numpy as np
import os

from src.xml_parser import GeNieXMLParser
from src.parsers import fetch_metrics_for_cve
from src.quantum_circuit import QuantumBayesianRiskEvaluator

def run_optimization_pipeline():
    print("\n[*] Initializing Phase 5 Gradient Stress-Testing Engine...")

    # 1. Base inputs setup
    try:
        live_priors = fetch_metrics_for_cve("CVE-2021-44228")
    except Exception:
        live_priors = {"cve": "CVE-2021-44228", "exploitability_prior": 0.99, "severity_prior": 1.0}

    xdsl_path = "NewNet.xdsl"
    if not os.path.exists(xdsl_path):
        print(f"[!] Target network snapshot missing: {xdsl_path}")
        return

    parser = GeNieXMLParser(xdsl_path)
    full_graph = parser.parse_structure()

    testing_track = ['VRTX5', 'VRTX6', 'VRTX7', 'VRTX4', 'VRTX3']
    evaluator = QuantumBayesianRiskEvaluator(full_graph, prune_to_track=testing_track)
    compiled_circuit = evaluator.get_circuit(target_node_id='VRTX3')

    # --- 2. FORCED OPTIMIZATION PARADIGM DATA SHIFT ---
    # We assign conflicting data patterns to actively trigger the parameter optimization engine
    scenario_a = {
        "priors": live_priors, 
        "target_probs": np.array([1.0, 0.0]) # Force high-threat input to register as fully secure
    }
    
    mitigated_priors = {"cve": "CVE-2021-44228", "exploitability_prior": 0.01, "severity_prior": 0.10}
    scenario_b = {
        "priors": mitigated_priors, 
        "target_probs": np.array([0.0, 1.0]) # Force clean input to evaluate as compromised
    }

    training_scenarios = [scenario_a, scenario_b]

    # 3. Parameter tracking variables (4 initial weights)
    weights = np.array([0.15, -0.22, 0.34, 0.12], requires_grad=True)

    # 4. Total Register Cost Matrix
    def cost_function(current_weights):
        total_loss = 0.0
        for scenario in training_scenarios:
            predicted_probs = compiled_circuit(scenario["priors"], weights=current_weights)
            loss = np.sum((predicted_probs - scenario["target_probs"]) ** 2)
            total_loss += loss
        return total_loss / len(training_scenarios)

    # 5. Optimization Engine Pass
    optimizer = qml.AdamOptimizer(stepsize=0.1)
    epochs = 20

    print(f"\n[*] Starting Optimization Loop over {epochs} Epochs...")
    print(f"Initial Parameter Weights: {weights.numpy()}")

    for epoch in range(1, epochs + 1):
        weights, current_cost = optimizer.step_and_cost(cost_function, weights)
        if epoch % 4 == 0 or epoch == 1:
            print(f"Epoch {epoch:2d} | Current Classical MSE Loss: {current_cost:.6f} | Adjusted Weights: {weights.numpy()}")

    print("\n[+] Optimization Cycle Terminated Successfully.")
    print(f"Final Trained Variational Angles: {weights.numpy()}")

if __name__ == "__main__":
    run_optimization_pipeline()



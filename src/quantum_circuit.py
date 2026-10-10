import pennylane as qml
from pennylane import numpy as np
import os
import json
import sys

from src.xml_parser import GeNieXMLParser
from src.parsers import fetch_metrics_for_cve

class QuantumBayesianRiskEvaluator:
    def __init__(self, structure_dict, prune_to_track=None):
        """
        Initializes the simulator device.
        If prune_to_track is provided, it isolates a subgraph for local execution.
        Otherwise, it compiles the complete structural threat network.
        """
        self.raw_structure = structure_dict
        
        # 1. Structural Filter Switch
        if prune_to_track:
            print(f"[*] Development Mode: Pruning workspace to target track...")
            self.structure = {k: v for k, v in structure_dict.items() if k in prune_to_track}
            for node_id, data in self.structure.items():
                data["parents"] = [p for p in data["parents"] if p in prune_to_track]
        else:
            print(f"[*] Production Mode: Initializing complete 32-qubit architecture matrix...")
            self.structure = structure_dict
            
        self.num_qubits = len(self.structure)
        
        # 2. Map wires deterministically
        sorted_nodes = sorted(self.structure.keys())
        self.wire_map = {}
        for index, node_key in enumerate(sorted_nodes):
            self.structure[node_key]["qubit_wire"] = index
            self.wire_map[node_key] = index
            
        # 3. Core Device Bindings
        self.dev = qml.device("default.qubit", wires=self.num_qubits)
        print(f"[+] Qubit Register Online. Active Size: {self.num_qubits} wires.")
        
    def build_qbn_ansatz(self, live_priors):
        """
        Applies network rotations across all allocated nodes.
        """
        # A. Process Root Nodes
        for node_id, data in self.structure.items():
            wire = data["qubit_wire"]
            parents = data["parents"]
            if not parents:
                prior_prob = live_priors.get(node_id, live_priors.get("exploitability_prior", 0.1))
                theta = 2 * np.arcsin(np.sqrt(prior_prob))
                qml.RY(theta, wires=wire)

        # B. Process Dependent Nodes
        for node_id, data in self.structure.items():
            wire = data["qubit_wire"]
            parents = data["parents"]
            if parents:
                control_wires = [self.structure[p]["qubit_wire"] for p in parents if p in self.structure]
                severity_prior = live_priors.get("severity_prior", 0.5)
                theta_conditional = 2 * np.arcsin(np.sqrt(severity_prior))
                
                for ctrl in control_wires:
                    qml.CRY(theta_conditional / len(control_wires), wires=[ctrl, wire])

    def build_qcnn_layers(self, weights):
        """
        Applies a structural template pass for Convolutional and Pooling steps
        to compress global enterprise threat states down to an indicator wire.
        
        Expected weights shape: 1D array of 4 parameters:
        weights[0:2] -> Convolutional gate parameters
        weights[2:4] -> Pooling gate parameters
        """
        if weights is None:
            weights = np.zeros(4, requires_grad=True)

        # --- 1. QUANTUM CONVOLUTION LAYER (Variational Search) ---
        # Apply parameterised entangling filters across adjacent active wires
        qml.CRX(weights[0], wires=[0, 1])
        qml.CRX(weights[1], wires=[2, 3])
        
        qml.Barrier(wires=range(self.num_qubits)) 

        # --- 2. QUANTUM POOLING LAYER (Dimensionality Reduction) ---
        # Compress risk metrics from minor nodes into central hub nodes
        qml.CRX(weights[2], wires=[1, 4])
        qml.CRX(weights[3], wires=[3, 4])

    def get_circuit(self, target_node_id):
        """
        Compiles the QNode execution container for evaluation.
        """
        if target_node_id not in self.wire_map:
            raise KeyError(f"Target node '{target_node_id}' is not active in this execution mode.")
            
        target_wire = self.wire_map[target_node_id]
        
        @qml.qnode(self.dev)
        def circuit(live_priors, weights=None):
            # Step A: Deterministic Threat Topology Loader
            self.build_qbn_ansatz(live_priors)
            
            # Step B: Trainable Neural Layer Search & Compression
            self.build_qcnn_layers(weights)
            
            return qml.probs(wires=target_wire)
            
        return circuit

if __name__ == "__main__":
    print("\n[*] Initializing Universal Quantum Evaluator Framework...")
    
    run_full_production = "--production" in sys.argv

    # 1. Fetch live vulnerabilities metrics
    try:
        live_data = fetch_metrics_for_cve("CVE-2021-44228")
    except Exception:
        live_data = {"cve": "CVE-2021-44228", "exploitability_prior": 0.99, "severity_prior": 1.0}

    # 2. Parse structural network files
    xdsl_path = "NewNet.xdsl"
    if os.path.exists(xdsl_path):
        parser = GeNieXMLParser(xdsl_path)
        full_graph = parser.parse_structure()
        
        if run_full_production:
            evaluator = QuantumBayesianRiskEvaluator(full_graph, prune_to_track=None)
            target_node = "VRTX3"
            initial_weights = np.zeros(4, requires_grad=True) # Placeholders for full run
        else:
            testing_track = ['VRTX5', 'VRTX6', 'VRTX7', 'VRTX4', 'VRTX3']
            evaluator = QuantumBayesianRiskEvaluator(full_graph, prune_to_track=testing_track)
            target_node = "VRTX3"
            
            # Define an array of 4 trainable neural network weights initialized to specific radians
            initial_weights = np.array([0.15, -0.22, 0.34, 0.12], requires_grad=True)
            
        compiled_circuit = evaluator.get_circuit(target_node)
        print(f"[*] Executing quantum forward pass targeting node: {target_node}...")
        
        # Run the circuit with both live data AND the learning weights
        probabilities = compiled_circuit(live_data, weights=initial_weights)
        
        print("\n--- QUANTUM SYSTEM EVALUATION COMPLETE ---")
        print(f"Target Node '{target_node}' Probabilities [Secure, Compromised]: {probabilities.numpy()}\n")
    else:
        print(f"[!] Architecture snapshot missing: {xdsl_path}")



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
        # For actual hardware runs, replace "default.qubit" with "qiskit.ibmq" via the pennylane-qiskit plugin
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

    def get_circuit(self, target_node_id):
        """
        Compiles the QNode execution container for evaluation.
        """
        if target_node_id not in self.wire_map:
            raise KeyError(f"Target node '{target_node_id}' is not active in this execution mode.")
            
        target_wire = self.wire_map[target_node_id]
        
        @qml.qnode(self.dev)
        def circuit(live_priors):
            self.build_qbn_ansatz(live_priors)
            return qml.probs(wires=target_wire)
            
        return circuit

if __name__ == "__main__":
    print("\n[*] Initializing Universal Quantum Evaluator Framework...")
    
    # Check if user explicitly requested full run via terminal command arguments
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
            # Complete 32-qubit execution pass for HPC / Real Hardware systems
            evaluator = QuantumBayesianRiskEvaluator(full_graph, prune_to_track=None)
            target_node = "VRTX3"
        else:
            # 5-qubit testing track pass to protect local laptop processors
            testing_track = ['VRTX5', 'VRTX6', 'VRTX7', 'VRTX4', 'VRTX3']
            evaluator = QuantumBayesianRiskEvaluator(full_graph, prune_to_track=testing_track)
            target_node = "VRTX3"
            
        compiled_circuit = evaluator.get_circuit(target_node)
        print(f"[*] Executing quantum forward pass targeting node: {target_node}...")
        probabilities = compiled_circuit(live_data)
        
        print("\n--- QUANTUM SYSTEM EVALUATION COMPLETE ---")
        print(f"Target Node '{target_node}' Probabilities [Secure, Compromised]: {probabilities.numpy()}\n")
    else:
        print(f"[!] Architecture snapshot missing: {xdsl_path}")


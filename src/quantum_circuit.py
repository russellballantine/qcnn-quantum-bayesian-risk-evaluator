"""
QUANTUM BAYESIAN RISK EVALUATOR - VECTORS B & C INTEGRATION
Module: src/quantum_circuit.py
Description: PennyLane QBN engine with a 30-wire local hardware cap
             to bypass legacy plugin backend limitations.
Generated on: 12th October 2026
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import pennylane as qml
import matplotlib.pyplot as plt

class QuantumRiskCircuit:
    def __init__(self, mode="development", override_wires=None):
        """Initializes the Qiskit backend runtime register topology based on ontology data."""
        self.mode = mode.lower()
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        v_path = os.path.join(self.root_dir, "data", "VERTICES.csv")
        a_path = os.path.join(self.root_dir, "data", "ARCS.csv")
        
        if not os.path.exists(v_path) or not os.path.exists(a_path):
            raise FileNotFoundError("Ontology data cache missing. Please run src/ontology_processor.py first.")
            
        self.vertices_df = pd.read_csv(v_path)
        self.arcs_df = pd.read_csv(a_path)
        self.total_hardware_wires = len(self.vertices_df)
        
        # Enforce sequential wire mappings to keep calculations tight
        self.sequential_mapping = {row["VertexID"]: idx for idx, row in self.vertices_df.iterrows()}
        
        if override_wires is not None:
            self.wire_count = override_wires
            self.wire_mapping = {row["VertexID"]: idx for idx, row in self.vertices_df.head(self.wire_count).iterrows()}
            self.dev = qml.device("qiskit.aer", wires=self.wire_count)
            return

        if self.mode == "development":
            # 1. Lightweight local python simulation (Quick 3-wire test track)
            self.active_nodes = ["WebServer", "CVE-2002-0392", "BehindNetworkFirewall"]
            self.sub_df = self.vertices_df[self.vertices_df["VertexID"].isin(self.active_nodes)].copy()
            self.sub_df["LocalWire"] = range(len(self.sub_df))
            self.wire_count = len(self.sub_df)
            self.wire_mapping = dict(zip(self.sub_df["VertexID"], self.sub_df["LocalWire"]))
            
            self.dev = qml.device("qiskit.basicsim", wires=self.wire_count)
            print(f"[*] Dev Mode Active: Running [{self.wire_count}] wires on Qiskit BasicSim.")

        elif self.mode == "emulator":
            # 2. Local C++ Aer Simulator - Capped at 30 wires to pass the plugin check
            self.wire_count = min(30, self.total_hardware_wires)
            self.wire_mapping = {row["VertexID"]: idx for idx, row in self.vertices_df.head(self.wire_count).iterrows()}
            
            self.dev = qml.device("qiskit.aer", wires=self.wire_count)
            print(f"[+] Emulator Mode Active: Running capped [{self.wire_count}] wires on local Qiskit Aer engine.")

        else:
            # 3. Production QPU Track (Full 37 wires sent to IBM's cloud computers)
            self.wire_count = self.total_hardware_wires
            self.wire_mapping = self.sequential_mapping
            
            token = os.getenv("IBM_QUANTUM_TOKEN")
            if not token:
                raise ValueError("Missing IBM_QUANTUM_TOKEN environment variable in shell profile.")
            
            self.dev = qml.device(
                "qiskit.remote", 
                wires=self.wire_count, 
                backend="ibm_fez", 
                channel="ibm_cloud",
                ibmqx_token=token
            )
            print(f"[!] Production Mode Active: Connected to IBM Hardware Cloud ({self.wire_count} Wires).")

    def calculate_theta(self, base_score: float) -> float:
        """Translates CVSS base score into a parameterized rotation angle."""
        p = base_score / 10.0
        p = max(0.001, min(0.999, p))
        return 2 * np.arcsin(np.sqrt(p))

    def build_qbn_loader(self):
        """Constructs the variational circuit blocks mapped natively to ontology properties."""
        for _, row in self.vertices_df.iterrows():
            node_id = row["VertexID"]
            if node_id in self.wire_mapping:
                wire_idx = self.wire_mapping[node_id]
                theta = self.calculate_theta(row["BaseScoreValue"])
                qml.RY(theta, wires=wire_idx)
            
        for _, row in self.arcs_df.iterrows():
            src_id = row["SourceID"]
            tgt_id = row["TargetID"]
            if src_id in self.wire_mapping and tgt_id in self.wire_mapping:
                src_wire = self.wire_mapping[src_id]
                tgt_wire = self.wire_mapping[tgt_id]
                angle = -0.5235 if row["Relationship"] == "hasCountermeasure" else 0.7853
                qml.CRX(angle, wires=[src_wire, tgt_wire])


if __name__ == "__main__":
    print("[*] Testing PennyLane Qiskit 1.0 Integration Gate...")
    
    try:
        circuit_engine = QuantumRiskCircuit(mode="emulator")
        
        @qml.qnode(circuit_engine.dev)
        def evaluation_circuit():
            circuit_engine.build_qbn_loader()
            target_wire = circuit_engine.wire_mapping.get("WebServer", 0)
            return qml.expval(qml.PauliZ(target_wire))
            
        t0 = time.time()
        result = evaluation_circuit()
        baseline_time = time.time() - t0
        print(f"[+] Qiskit Aer Emulation successful! (Completed in {baseline_time:.4f} seconds)")
        print(f"    - Sample Wire Expectation Value <Z>: {result:.6f}\n")
        
    except Exception as e:
        print(f"[-] Full Scale Engine Check Failed: {e}")
        sys.exit(1)

    print("[*] Initializing Local Scaling Performance Profile...")
    # Safe benchmarking steps that stay strictly below the 31-wire limit
    wire_steps = [3, 8, 14, 20, 26, 30]
    execution_runtimes = []

    for count in wire_steps:
        print(f"    -> Measuring execution overhead for {count} active registers...")
        try:
            scaler = QuantumRiskCircuit(override_wires=count)
            
            @qml.qnode(scaler.dev)
            def scaling_circuit():
                scaler.build_qbn_loader()
                return qml.expval(qml.PauliZ(0))
                
            run_times = []
            for _ in range(3):
                start = time.time()
                scaling_circuit()
                run_times.append(time.time() - start)
                
            execution_runtimes.append(np.mean(run_times))
        except Exception as err:
            print(f"       [!] Skipped size {count}: {err}")
            execution_runtimes.append(None)

    print("\n[*] Generating runtime profile scaling graphs...")
    valid_plots = [(w, r) for w, r in zip(wire_steps, execution_runtimes) if r is not None]
    plot_wires, plot_times = zip(*valid_plots)

    plt.figure(figsize=(9, 5))
    plt.plot(plot_wires, plot_times, marker='o', color='#d62728', linestyle='-', linewidth=2, label='Qiskit Aer Engine')
    plt.title('Quantum Risk Circuit Structural Scaling Profile (Local Hardware Capped)', fontsize=11, fontweight='bold', pad=15)
    plt.xlabel('Number of Allocated Ontological Qubits (Wires)', fontsize=10)
    plt.ylabel('Execution Completion Speed (Seconds)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.yscale('log')
    plt.legend(loc='upper left')
    
    output_graph_path = os.path.join(circuit_engine.root_dir, "quantum_scaling_profile.png")
    plt.savefig(output_graph_path, dpi=300, bbox_inches='tight')
    print(f"[+] Diagnostic profiling saved successfully to: {output_graph_path}")

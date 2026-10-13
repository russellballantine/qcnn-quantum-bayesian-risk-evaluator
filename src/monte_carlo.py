import os
import pandas as pd
import numpy as np

class ThreatNetworkMCMC:
    def __init__(self, vertices_path, arcs_path):
        """
        Initialises the MCMC engine by loading the cyber threat topology.
        """
        self.vertices_path = vertices_path
        self.arcs_path = arcs_path
        self.nodes = []
        self.edges = []
        self.parents = {}
        self.children = {}
        
        self._load_topology()

    def _load_topology(self):
        """
        Loads vertices and directional threat vectors from CSV inputs.
        """
        if not os.path.exists(self.vertices_path) or not os.path.exists(self.arcs_path):
            raise FileNotFoundError("Topology CSV files missing. Check data/ directory.")
            
        df_vertices = pd.read_csv(self.vertices_path)
        df_arcs = pd.read_csv(self.arcs_path)
        
        self.nodes = df_vertices.iloc[:, 0].dropna().tolist()
        
        # FIXED: Explicitly specified column index 0 and 1 for iloc mapping
        for _, row in df_arcs.iterrows():
            src, dst = row.iloc[0], row.iloc[1]
            self.edges.append((src, dst))
            
        for node in self.nodes:
            self.parents[node] = []
            self.children[node] = []
            
        for src, dst in self.edges:
            if src in self.parents and dst in self.parents:
                self.parents[dst].append(src)
                self.children[src].append(dst)
                
        print(f"[INFO] Ingested {len(self.nodes)} Ontological Security Registers.")
        print(f"[INFO] Mapped {len(self.edges)} Directional Threat Causal Vectors.")

    def _mock_conditional_prob(self, node, current_state):
        """
        Placeholder for the conditional probability table (CPT) math.
        """
        # FIXED: Safely verify parent key exist within active local state
        active_parents = sum([current_state[p] for p in self.parents[node] if p in current_state])
        base_prob = 0.1 + (0.2 * active_parents)
        return min(max(base_prob, 0.01), 0.99)

    def run_gibbs_sampling(self, burn_in=1000, num_samples=5000, isolated_subset=None):
        """
        Executes the MCMC sampling loop to find baseline convergence weights.
        """
        active_nodes = isolated_subset if isolated_subset else self.nodes
        print(f"\n[MCMC] Starting Gibbs Sampling over {len(active_nodes)} active nodes...")
        
        # FIXED: Supplied valid state array [0, 1] to random choices
        current_state = {node: np.random.choice([0, 1]) for node in active_nodes}
        sample_history = []
        total_iterations = burn_in + num_samples
        
        for step in range(total_iterations):
            for node in active_nodes:
                p_active = self._mock_conditional_prob(node, current_state)
                # FIXED: Supplied valid states and probability weights mapping
                current_state[node] = np.random.choice([1, 0], p=[p_active, 1 - p_active])
            
            if step >= burn_in:
                sample_history.append(current_state.copy())

        df_samples = pd.DataFrame(sample_history)
        convergence_weights = df_samples.mean().to_dict()
        
        print("[MCMC] Sampling complete. Convergence weights calculated.")
        return convergence_weights

if __name__ == "__main__":
    # Local Test Execution mirroring the 3-Node isolated workspace subset
    dev_subset = ["BehindNetworkFirewall", "CVE-2002-0392", "WebServer"]
    
    os.makedirs("data", exist_ok=True)
    pd.DataFrame({"node_id": dev_subset}).to_csv("data/VERTICES.csv", index=False)
    pd.DataFrame({"src": ["BehindNetworkFirewall", "CVE-2002-0392"], 
                  "dst": ["CVE-2002-0392", "WebServer"]}).to_csv("data/ARCS.csv", index=False)

    # Initialise and run engine
    engine = ThreatNetworkMCMC(vertices_path="data/VERTICES.csv", arcs_path="data/ARCS.csv")
    weights = engine.run_gibbs_sampling(burn_in=100, num_samples=500, isolated_subset=dev_subset)
    
    print("\n--- Local Dev Convergence Result Summary ---")
    for node, weight in weights.items():
        print(f"Node: {node:<25} | Absolute Risk Weight: {weight:.4f}")

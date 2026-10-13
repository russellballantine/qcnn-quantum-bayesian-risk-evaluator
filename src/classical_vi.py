import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class VariationalInferenceEngine(nn.Module):
    def __init__(self, nodes, parents):
        """
        Initialises a mean-field Variational Inference engine using PyTorch.
        Turns the network distribution problem into a parameters optimization task.
        """
        super(VariationalInferenceEngine, self).__init__()
        self.nodes = nodes
        self.parents = parents
        self.node_to_idx = {node: idx for idx, node in enumerate(nodes)}
        
        # Variational parameters: logits of the marginal probability for each node
        self.variational_logits = nn.Parameter(torch.zeros(len(nodes), dtype=torch.float32))

    def forward(self):
        return torch.sigmoid(self.variational_logits)

    def calculate_kl_loss(self):
        probs = self.forward()
        loss = torch.tensor(0.0, requires_grad=True)
        
        for idx, node in enumerate(self.nodes):
            p_node = probs[idx]
            node_parents = self.parents.get(node, [])
            if node_parents:
                parent_indices = [self.node_to_idx[p] for p in node_parents if p in self.node_to_idx]
                parent_probs_sum = sum([probs[p_idx] for p_idx in parent_indices])
                target_p = torch.clamp(0.1 + 0.2 * parent_probs_sum, 0.01, 0.99)
            else:
                target_p = torch.tensor(0.1) # Root prior base threat
                
            epsilon = 1e-6
            kl_proxy = - (target_p * torch.log(p_node + epsilon) + (1.0 - target_p) * torch.log(1.0 - p_node + epsilon))
            loss = loss + kl_proxy
            
        return loss

def train_vi_pipeline(vertices_path, arcs_path, steps=200, lr=0.05, isolated_subset=None):
    if not os.path.exists(vertices_path) or not os.path.exists(arcs_path):
        raise FileNotFoundError("Topology CSV files missing.")
        
    df_vertices = pd.read_csv(vertices_path)
    df_arcs = pd.read_csv(arcs_path)
    
    all_nodes = df_vertices.iloc[:, 0].dropna().tolist()
    active_nodes = isolated_subset if isolated_subset else all_nodes
    
    parents = {node: [] for node in active_nodes}
    for _, row in df_arcs.iterrows():
        src, dst = row.iloc[0], row.iloc[1]
        if src in parents and dst in parents:
            parents[dst].append(src)
            
    print(f"[INFO] Initialising Classical VI Optimisation Engine...")
    model = VariationalInferenceEngine(active_nodes, parents)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    for step in range(steps):
        optimizer.zero_grad()
        loss = model.calculate_kl_loss()
        loss.backward()
        optimizer.step()
        
        if (step + 1) % 50 == 0 or step == 0:
            print(f"  Step {step+1:03d}/{steps} | Proxy KL Loss: {loss.item():.4f}")
            
    final_probs = model().detach().numpy()
    return {node: float(final_probs[idx]) for idx, node in enumerate(active_nodes)}

if __name__ == "__main__":
    dev_subset = ["BehindNetworkFirewall", "CVE-2002-0392", "WebServer"]
    weights = train_vi_pipeline("data/VERTICES.csv", "data/ARCS.csv", steps=200, lr=0.05, isolated_subset=dev_subset)
    print("\n--- Local Dev VI Convergence Result Summary ---")
    for node, weight in weights.items():
        print(f"Node: {node:<25} | Variational Risk Weight: {weight:.4f}")

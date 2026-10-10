import xml.etree.ElementTree as ET
import os

class GeNieXMLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nodes = {}
        
    def parse_structure(self):
        """
        Parses the GeNIe xdsl architecture layout by looking for the 
        network element dynamically, completely ignoring case variants.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Missing layout architecture artifact: {self.file_path}")
            
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        
        # Dynamically locate the network tag block regardless of case style
        network = None
        for element in root.iter():
            if element.tag.lower() == 'network':
                network = element
                break
                
        if network is None:
            network = root
            
        # Target node container blocks dynamically
        nodes_block = None
        for child in network:
            if child.tag.lower() == 'nodes':
                nodes_block = child
                break
                
        if nodes_block is None:
            nodes_block = network
            
        # Target conditional probability table nodes (cpt)
        for cpt in nodes_block.findall('.//cpt') if hasattr(nodes_block, 'findall') else []:
            node_id = cpt.get('id')
            if not node_id:
                continue
                
            # Extract parent nodes (the directional dependencies)
            parents = []
            parents_tag = cpt.find('parents')
            if parents_tag is not None and parents_tag.text:
                parents = parents_tag.text.strip().split()
                
            # Extract node state properties (e.g., compromised, secure)
            states = []
            for state in cpt.findall('state'):
                state_id = state.get('id')
                if state_id:
                    states.append(state_id)
            
            # Map clean logical entry
            self.nodes[node_id] = {
                "node_id": node_id,
                "parents": parents,
                "states": states,
                "qubit_wire": None  # Assigned dynamically below
            }
            
        # --- DYNAMIC QUBIT INDEX WIRE ALLOCATION ---
        # Sort keys to ensure deterministic wire layouts across execution runs
        sorted_nodes = sorted(self.nodes.keys())
        for index, node_key in enumerate(sorted_nodes):
            self.nodes[node_key]["qubit_wire"] = index
            
        return self.nodes

if __name__ == "__main__":
    target_file = "NewNet.xdsl"
    if os.path.exists(target_file):
        print(f"\n[*] Auditing structural layout for: {target_file}")
        parser = GeNieXMLParser(target_file)
        structure = parser.parse_structure()
        
        print(f"[+] Dynamic qubit mapping initialized.")
        print(f"[+] Total allocated register size: {len(structure)} qubits.\n")
        
        # Verify the qubit wire allocations for our target threat track sample
        test_track = ['VRTX5', 'VRTX6', 'VRTX7', 'VRTX4', 'VRTX3']
        for node in test_track:
            if node in structure:
                data = structure[node]
                print(f"Node Identifier: {data['node_id']:6} | Assigned Qubit Wire: {data['qubit_wire']:2} | Structural Parents: {data['parents']}")
    else:
        print(f"[!] Target model layout file not found in root folder: {target_file}")



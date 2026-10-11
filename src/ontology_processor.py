#!/usr/bin/env python3
"""
QUANTUM BAYESIAN RISK EVALUATOR - PHASE 6 (VECTOR C)
Module: src/ontology_processor.py
Description: Configuration-driven OWL ingestion engine using owlready2.
             Extracts structural vertices, causal object property arcs,
             and parametric data metrics to initialize quantum registers.
Generated on: 11th October 2026
"""

import os
import sys
import yaml
import pandas as pd
from owlready2 import get_ontology, ObjectProperty

class DynamicOntologyProcessor:
    def __init__(self, config_path: str):
        """Loads the YAML configuration blueprint and sets up file system boundaries."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration profile missing at: {config_path}")
        
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Resolve target ingestion paths from contract definitions
        onto_rel_path = self.config["ontology"]["local_path"]
        self.ontology_path = os.path.join(self.root_dir, onto_rel_path)
        self.namespace = self.config["ontology"]["namespace"]
        
        if not os.path.exists(self.ontology_path):
            raise FileNotFoundError(f"OWL target file not found at: {self.ontology_path}")
            
        print(f"[*] Map Engine Initialized via Configuration Contract.")
        print(f"[*] Ingesting Target Schema: {self.ontology_path}")
        
        # Load semantic graph into active runtime environment
        self.onto = get_ontology(self.ontology_path).load()
        self.vertex_map = {}  # Format: { 'CleanIndividualName': qubit_wire_index }

    def extract_deterministic_vertices(self) -> pd.DataFrame:
        """
        Traverses target classes, extracts metric data properties, applies an 
        alphabetical sort, and locks frozen quantum wire addresses.
        """
        print("[*] Filtering Entities for Deterministic Qubit Wire Allocation...")
        target_classes = self.config["pipeline_filters"]["target_classes"]
        target_metrics = self.config["pipeline_filters"]["target_data_properties"]
        defaults = self.config["probabilistic_defaults"]
        raw_individuals = []

        for cls_name in target_classes:
            onto_cls = getattr(self.onto, cls_name, None)
            if onto_cls:
                raw_individuals.extend(list(onto_cls.instances()))

        # Extract names to enforce unique allocation limits
        unique_names = list(set([ind.name for ind in raw_individuals]))
        
        # CRITICAL BOUNDARY: Enforce alphabetical sorting to freeze register addresses
        sorted_names = sorted(unique_names)

        # Build sequential mapping profile (0 to N-1) with parametric metrics
        vertices_data = []
        for index, name in enumerate(sorted_names):
            self.vertex_map[name] = index
            source_ind = getattr(self.onto, name)
            
            # Base record profile structure
            record = {"VertexID": name, "QubitWire": index}
            
            # Dynamically pull metrics using configuration keys
            for metric in target_metrics:
                val = getattr(source_ind, metric, None)
                
                # Extract clean values if they exist in the ontology individual
                if val is not None:
                    if isinstance(val, list):
                        val = val[0] if len(val) > 0 else defaults[metric]
                    record[metric] = float(val)
                else:
                    # Apply configurations defaults if property is unassigned
                    record[metric] = float(defaults[metric])
                    
            vertices_data.append(record)
            print(f"    -> Register Locked: {name} ===> Wire [{index}] (BaseScore: {record['BaseScoreValue']})")

        df_vertices = pd.DataFrame(vertices_data)
        return df_vertices

    def extract_dependency_arcs(self) -> pd.DataFrame:
        """
        Traverses target object properties across active individuals and 
        maps semantic vectors to physical asymmetric indices.
        """
        print("[*] Compiling Relational Vectors into Topology Arcs...")
        target_properties = self.config["pipeline_filters"]["target_object_properties"]
        arcs_data = []

        for source_name, source_wire in self.vertex_map.items():
            source_ind = getattr(self.onto, source_name, None)
            if not source_ind:
                continue
            
            # Inspect properties assigned to this entity safely bypassing namespaces
            for prop in source_ind.get_properties():
                if prop.name in target_properties:
                    targets = getattr(source_ind, prop.name)
                    
                    if not isinstance(targets, list):
                        targets = [targets]
                        
                    for target_ind in targets:
                        if hasattr(target_ind, "name"):
                            target_name = target_ind.name
                        else:
                            continue
                        
                        # Cross-reference target to verify it exists within the active register
                        if target_name in self.vertex_map:
                            target_wire = self.vertex_map[target_name]
                            arcs_data.append({
                                "SourceID": source_name,
                                "SourceWire": source_wire,
                                "Relationship": prop.name,
                                "TargetID": target_name,
                                "TargetWire": target_wire
                            })
                            print(f"    -> Arc Generated: [{source_name}] --({prop.name})--> [{target_name}]")

        df_arcs = pd.DataFrame(arcs_data)
        return df_arcs

    def export_pipeline_assets(self, vertices_df: pd.DataFrame, arcs_df: pd.DataFrame):
        """Saves structural files straight to your data path cache."""
        output_dir = os.path.join(self.root_dir, "data")
        os.makedirs(output_dir, exist_ok=True)
        
        v_path = os.path.join(output_dir, "VERTICES.csv")
        a_path = os.path.join(output_dir, "ARCS.csv")
        
        vertices_df.to_csv(v_path, index=False)
        arcs_df.to_csv(a_path, index=False)
        
        print(f"[+] Operational artifacts synchronized with data pipeline cache:")
        print(f"    - {v_path} ({len(vertices_df)} qubits mapped with parameters)")
        print(f"    - {a_path} ({len(arcs_df)} dependencies mapped)")


if __name__ == "__main__":
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_TARGET = os.path.join(os.path.dirname(CURRENT_DIR), "config", "mapping.yaml")
    
    try:
        processor = DynamicOntologyProcessor(CONFIG_TARGET)
        vertices_df = processor.extract_deterministic_vertices()
        arcs_df = processor.extract_dependency_arcs()
        processor.export_pipeline_assets(vertices_df, arcs_df)
        
    except Exception as e:
        print(f"[-] Execution Error encountered: {e}")
        sys.exit(1)


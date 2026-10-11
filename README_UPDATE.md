# QUANTUM BAYESIAN RISK EVALUATOR - PHASE 6 MANIFEST
> **Project State:** Alpha Milestone Phase 6 Operational (Vector C Completed)  
> **Inference Engine:** Hybrid QBN-to-QCNN Ingest & Variational Training Pipeline  
> **Execution Environment:** macOS Isolated Virtual Environment (`.venv`)

===============================================================================
1. TECHNICAL ARCHITECTURE OVERVIEW (VECTOR C INTEGRATION)
===============================================================================
This phase establishes a decoupled, configuration-driven semantic orchestration layer 
directly upstream of the classical-to-quantum execution core. 

Instead of brittle, hardcoded node registries, the pipeline utilizes `owlready2` to parse 
W3C Web Ontology Language (OWL) schemas in RDF/XML format. Entity structures, object 
property dependencies, and numerical CVSS data properties are translated dynamically via a 
lightweight contract profile (`config/mapping.yaml`) into normalized execution matrices.

### Core Execution Pipeline Chain:
1. **`config/mapping.yaml`**: The single source of truth for schema translation rules. Maps local base namespaces, target structural classes (`Asset`, `CVE`, `SecurityControl`), and causal links (`hasVulnerability`, `hasCountermeasure`) cleanly outside core application code.
2. **`src/ontology_processor.py`**: Ingests the OWL graph, extracts entities, and enforces a strict alphabetical sorting boundary (`sorted(unique_names)`) to isolate PennyLane wire maps from configuration drift. It populates `data/VERTICES.csv` and `data/ARCS.csv` seamlessly.
3. **`src/quantum_circuit.py`**: Reads structural buffers, maps a 37-qubit production target framework, and isolates lightweight sub-tracks in **Development Mode** to protect local runtime RAM constraints. It converts raw CVSS properties into parameterized rotations using \(\theta = 2 \arcsin(\sqrt{P})\).
4. **`src/train.py`**: Drives PennyLane's tracked `numpy` gradients through the `AdamOptimizer`, updating variational QCNN spatial filters natively against live ontological structures.

===============================================================================
2. WORKSPACE DIRECTORY & ARTIFACT SYNCHRONIZATION
===============================================================================
Ensure your project tree matches this architecture layout before running pipeline passes:

```text
qcnn-quantum-bayesian-risk-evaluator/
│
├── config/                      
│   └── mapping.yaml             <--- NEW: Ingestion Translation Contract Profile
│
├── ontology/                    
│   └── msc_security_core.owl    <--- NEW: Semantic Security Ontology Schema Graph
│
├── src/                         
│   ├── __init__.py
│   ├── parsers.py               (Phase 1 Ingest Client)
│   ├── xml_parser.py            (Phase 2 Topology Engine)
│   ├── quantum_circuit.py       (Phases 3 & 4 Upgraded PennyLane Core Core)
│   ├── train.py                 (Phase 5 Upgraded Hybrid Optimizer Model)
│   └── ontology_processor.py    <--- NEW: Config-Driven OWL Processing Script
│
└── data/                        
    ├── VERTICES.csv             <--- REGENERATED: Mapped with Parametric Metrics
    └── ARCS.csv                 <--- REGENERATED: 28 Active Relational Connections
```

===============================================================================
3. METRIC BASELINE RECORD (LATEST ACTIVE VALIDATION RUN)
===============================================================================
* **Target Identifier Track (Dev Mode):** `WebServer` ── `CVE-2002-0392` ── `BehindNetworkFirewall`
* **Qubit Register Footprint:** 37 Total Ontological Nodes Verified and Bound.
* **Structural Dependency Volume:** 28 Relational Asymmetric Arcs Extracted.
* **Initial Cost Baseline:** 1.899128 MSE Loss
* **Optimized Terminal Cost Profile:** **0.259237 MSE Loss** (Achieved in 15 Epochs)
* **Trained Variational Angles:** `[1.706445, 0.067800, 0.708063, 1.644100]`

===============================================================================
4. ECOSYSTEM DEPENDENCIES (UPDATED REQUIREMENTS)
===============================================================================
The current pipeline build requires the following packages installed inside your virtual environment. Append these blocks directly to your `requirements.txt` file:

```text
pennylane==0.38.0
pennylane-lightning==0.38.0
pandas>=2.0.0
pyyaml>=6.0.0
owlready2>=0.45
numpy<2.0,>=1.26.4
requests>=2.32.5
```

To initialize your development stack or resolve environment errors, execute:
```bash
pip install pyyaml pandas owlready2 pennylane
```

===============================================================================
5. PIPELINE INVOCATION STEPS
===============================================================================
To run the end-to-end framework execution passes within your active virtual terminal environment, use the following operational lifecycle commands:

**Step 1: Extract Semantic Topologies & Rebuild Data Matrices**
```bash
python3 src/ontology_processor.py
```
*Expected Behavior:* The compiler locks all 37 unique registers, binds explicit CVSS values (e.g., pulling **9.3** for `CVE-2010-0490`), applies default safe fallbacks, and writes out 28 validated connectivity links to disk.

**Step 2: Trigger Circuit Verification Gate & Compute Initial Superpositions**
```bash
python3 src/quantum_circuit.py
```
*Expected Behavior:* Confirms a successful local simulation initialization, calculating an initial risk state balance point expectation value of `<Z> = -0.000000`.

**Step 3: Execute Gradient Descent Optimization Training Loop**
```bash
python3 -m src.train
```
*Expected Behavior:* Invokes the native module wrapper flag, boots the AdamOptimizer, tracks mathematical partial derivatives smoothly without throwing tracking warnings, and minimizes risk prediction anomalies as the loss drops step-by-step.
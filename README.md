# Quantum Bayesian Network (QBN) Risk Evaluator for Agile SOC Operations

> 🔍 **Project Architecture Note:** This repository houses the development of a Quantum Bayesian Network engine designed to scale quantitative risk assessment within a Security Operations Centre (SOC). This architecture represents a direct quantum evolution of the metric-driven security ontology framework established during MSc research at Edinburgh University.

---

## 1. High-Level Architectural Vision

Classical quantitative risk assessment frameworks (e.g., FAIR, traditional Bayesian Networks) hit severe algorithmic scaling bottlenecks when modeling complex, cascading multi-node enterprise topologies in real time. As threat graphs grow, computing exact probabilistic inference across vast, tabular Conditional Probability Tables (CPTs) becomes an **NP-hard problem** classically.

This project implements a **Hybrid Classical-Quantum Bayesian Network (QBN)**. By replacing traditional scalar floating-point tables with **complex probability amplitudes**, we map causal threat dependencies directly onto an entangled multi-qubit register. This leverages quantum superposition and interference to track interconnected vulnerabilities near-instantly, delivering a truly agile, real-time risk determination pipeline for active SOC telemetry feeds.

---

## 2. System Architecture & Data Orchestration Pipeline

The system operates as a hybrid classical-quantum framework, using standard data parsers to feed a native PennyLane simulation core:

```
+------------------------------------+      +-----------------------------------------+

|     1. CLASSICAL DATA INGESTION    |      |         2. ONTOLOGICAL PARSING          |
|  - Real-time NIST NVD CVSS Feeds   | ---> |  - JSON Payload Parsing Engine          |
|  - Daily CISA KEV Exploitation     |      |  - Extracted Base Metrics → Priors |
|  - Daily FIRST EPSS Probabilities  |      |  - Asset Criticality Staging Matrix     |
+------------------------------------+      +-----------------------------------------+
                                                                 |
                                                                 v
+------------------------------------+      +-----------------------------------------+

|    4. ACCELERATED QUANTUM ENGINE   |      |       3. HYBRID ORCHESTRATION BRIDGE    |
|  - PennyLane `default.qubit` Core  | <--- |  - Parse GeNIe (.xdsl) Causal Topology  |
|  - Parameterized \(CR_y\) Rotations  |      |  - Map CPT Conditionals to Controlled   |
|  - Multi-Qubit Entanglement States |      |    Quantum State Rotations              |
+------------------------------------+      +-----------------------------------------+
```

---

## 3. Mathematical Baseline for State Mappings

Defensive control points, vulnerability statuses, and asset compromise indicators are mapped directly into orthogonal quantum basis states:

```math

|0\rangle = \text{Control Intact / Threat Mitigated} \quad \text{and} \quad |1\rangle = \text{Control Exploited / Compromise Realized}
```

### Prior Node Polarization
For an isolated root network node (e.g., presence of a severe public NIST vulnerability V), the raw probability P(V = 1) derived from live CVSS/EPSS scoring metrics is injected via a single-qubit state preparation rotation gate \(R_y(\theta)\):

```math

|\psi_V\rangle = R_y(\theta)|0\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + \sin\left(\frac{\theta}{2}\right)|1\rangle
```

Where the rotation angle θ is explicitly calculated from the classical probability parameter:
```math
\theta = 2 \cdot \arcsin\left(\sqrt{P(V=1)}\right)
```

### Conditional Node Dependency via Entanglement
For a dependent child node in the graph (e.g., Attacker Exploitation Success E conditioned directly on the Vulnerability status V), the GeNIe-style Conditional Probability Table is mapped onto a multi-qubit system using **Controlled-Rotation (\(CR_y\)) gates**. This entangles the child qubit to the parent register, capturing the causal security posture inside the joint statevector:

```math
CR_y(\theta_{\text{cond}})|V\rangle|E\rangle
```

---

## 4. Phase-by-Phase Development Roadmap

### 📋 Phase 1: Core 3-Node Threat Chain Validation (Current Sprint)
* Build a local isolated Python virtual environment (`.venv`) with verified `pennylane`, `torch`, and `matplotlib` dependencies.
* Build `src/parsers.py`: Create clean intake hooks to process live NIST NVD CVSS v4 vector arrays and FIRST EPSS payload streams.
* Build `src/qbn_core.py`: Implement a prototype 3-node connected Quantum Bayesian threat chain:
  ```math
  \text{[Vulnerability Present (V)]} \longrightarrow \text{[Exploit Telemetry Observed (E)]} \longrightarrow \text{[Data Impact Realized (I)]}
  ```
* Verify that changing an active prior or conditional parameter updates the calculated quantum expectation values smoothly.

### 📋 Phase 2: GeNIe Layout Parsing & Automated Circuit Compilation
* Implement an automated parser engine capable of reading classical GeNIe (`.xdsl`) XML layout structures.
* Write a compiler loop that dynamically maps an arbitrary directed acyclic graph (DAG) from GeNIe into an ordered sequence of multi-controlled $CR_y$ gates over an $N$-qubit PennyLane footprint.
* Stabilize gradient tracking through the pipeline using PyTorch backend configurations.

### 📋 Phase 3: Quantum Amplitude Estimation (QAE) Risk Scaling
* Move away from tracking basic single-wire expectation outputs to full-scale risk tracking.
* Implement a **Grover-driven Quantum Amplitude Estimation (QAE)** routine.
* Benchmark the quadratic calculation speedup ($O(\sqrt{N})$) of the QAE core against a classical Monte Carlo simulation run under identical network complexity stresses.

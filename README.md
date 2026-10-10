# QCNN Quantum Bayesian Risk Evaluator

A next-generation cybersecurity risk engine that merges semantic security modeling with quantum-accelerated probabilistic inference. This framework ingests network dependency architectures and scales risk propagation across a hybrid **Quantum Bayesian Network (QBN)** feature loader and a **Quantum Convolutional Neural Network (QCNN)** aggregator.

---

## 🚀 Key Architectural Upgrades

### 1. Live Threat Intelligence Ingestion
The framework bypasses static, hardcoded legacy priors by streaming real-time metrics directly from global threat databases:
* **FIRST EPSS API:** Pulls live exploit-in-the-wild probabilities to drive root node exploitability variables.
* **NIST NVD API (v2.0):** Dynamically queries CVSS v3.1/v4.0 base metrics to establish normalized structural severity impacts.

### 2. Dual-Mode Hybrid Computational Scaling
To balance local development agility with production-grade scaling targets, the framework implements a dual-mode compilation switch:
* **Development Mode (5-Qubit Pruning):** Automatically isolates active core attack tracks (e.g., `VRTX5` → `VRTX6` → `VRTX7` → `VRTX4` → `VRTX3`) into a tight workspace register for instantaneous local simulation loops.
* **Production Mode (Full 32-Qubit Matrix):** Compiles the complete enterprise network topology. This mode scales directly to High-Performance Computing (HPC) tensor simulators and physical quantum hardware backends via the **PennyLane-Qiskit** plugin.

### 3. Quantum-Classical Benchmarking Architecture
To validate the quantum computing advantage, the engine maintains a dual evaluation track:
* **Classical Baseline:** A Markov Chain Monte Carlo (MCMC) / classical sampling engine simulating the source GeNIe graph network.
* **Quantum Evaluation Core:** The QBN-to-QCNN circuit, which leverages quantum superposition and state interference to evaluate global, non-linear cascading risk vectors simultaneously.

---

## 🛠️ Project Structure

* `src/parsers.py` — Resilient HTTP request client handling live NIST NVD and FIRST EPSS ingestion.
* `src/xml_parser.py` — Dynamic XML schema parser that extracts structural graph topologies and maps vertices to qubit wires.
* `src/quantum_circuit.py` — Core PennyLane framework implementing the dynamic QBN rotation ansatz layers.
* `NewNet.xdsl` — Source GeNIe graph network definition asset.

---

## ⚙️ Execution Instructions

### Run Local Development Mode (Memory-Safe Simulation)
```bash
PYTHONPATH=. ./.venv/bin/python src/quantum_circuit.py
```

### Run Full Production Mode (HPC / Hardware Compilation Target)
```bash
PYTHONPATH=. ./.venv/bin/python src/quantum_circuit.py --production
```


---

## 𝨢 Mathematical Overview

The framework translates a classical Directed Acyclic Graph (DAG) security model into a state-vector quantum mapping space using the following core mathematical definitions:

### 1. State Space Mapping
Each threat node or enterprise asset variable $X_i$ is mapped to a physical qubit wire in the computational basis. The state of the register is a fluid superposition representing risk uncertainty:
* $|0\rangle$: Node is secure / threat unrealised.
* $|1\rangle$: Node is compromised / threat realised.

The global system state vector $|\Psi\rangle$ for an $n$-qubit register is a linear combination across all $2^n$ computational states:
$$\Psi\rangle = \sum_{x \in \{0,1\}^n} \alpha_x |x\rangle, \quad \sum_{x} |\alpha_x|^2 = 1$$

### 2. Root Prior Embedding (QBN Feature Loader)
For a root threat node $X_{\text{root}}$ with no parent dependencies, its live-ingested exploitability probability $P(X_{\text{root}} = 1)$ is deterministically embedded using a single-qubit $Y$-rotation gate ($R_Y$). 

To map the classical probability amplitude perfectly to the quantum state vector, the rotation angle $\theta$ is mapped via:
$$\theta = 2 \arcsin(\sqrt{P(X_{\text{root}} = 1)})$$

When applied to a ground-state qubit, this yields the exact probability distribution upon measurement:
$$R_Y(\theta)|0\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + \sin\left(\frac{\theta}{2}\right)|1\rangle = \sqrt{1 - P}|0\rangle + \sqrt{P}|1\rangle$$

### 3. Conditional Risk Propagation (Quantum CPTs)
For a dependent asset node $X_j$ conditioned on a set of parent nodes $\text{Parents}(X_j)$, risk propagation maps using multi-controlled rotation operators. 

The conditional probability table (CPT) row values drive a Controlled-$R_Y$ unitary ($CR_Y(\phi)$). The target qubit rotates toward a compromised state if and only if the control wires are in the $|1\rangle$ state:
$$CR_Y(\phi)_{ctrl, targ} = |0\rangle\langle0|_{ctrl} \otimes I_{targ} + |1\rangle\langle1|_{ctrl} \otimes R_Y(\phi)_{targ}$$

This explicitly maps the causal chain structures of the original GeNIe model directly into quantum state amplitudes, allowing cascading risk vectors to propagate natively across the circuit via quantum interference.


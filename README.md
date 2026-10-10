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

#!/bin/bash

# ====================================================================
# Slurm Batch Script: QCNN Cybersecurity Threat Evaluation Framework
# Tailored for: EPCC Cirrus HPE Cray EX4000 System (AMD Zen 5 Architecture)
# ====================================================================

#SBATCH --job-name=qcnn_cyber_bench     # Name display in the queue manager
#SBATCH --nodes=1                      # Request 1 full dedicated compute node
#SBATCH --tasks-per-node=1             # Run a single overarching master execution process
#SBATCH --cpus-per-task=288            # Allocate all 288 physical EPYC cores on the node
#SBATCH --time=02:00:00                # Set hard time wall ceiling to 2 hours
#SBATCH --partition=standard           # Route to the standard CPU compute partition
#SBATCH --qos=standard                 # Apply standard priority quality of service

# --------------------------------------------------------------------
# 1. Environment & Workspace Path Management (CRITICAL FOR CIRRUS)
# --------------------------------------------------------------------
# Hard absolute rule: Cirrus compute nodes do not map standard /home paths.
# You must switch workspace paths to the high-performance parallel file system.
export WORKSPACE_DIR="/epccfs/projects/<YOUR_PROJECT_ID>/qcnn-cyber-risk"
cd $WORKSPACE_DIR || exit 1

# Clean environment, purge generic modules, and ensure baseline system stability
module purge
module load proprietary/epcc-python-ecosystem # Fallback or utilize base system environment

# Target your pre-staged python virtual environment matching your local setups
source .venv/bin/activate

# --------------------------------------------------------------------
# 2. NUMA and Thread Multi-Processing Optimisations for AMD Zen 5
# --------------------------------------------------------------------
# This handles the internal parallel scaling for PyTorch matrix calculations 
# and the Qiskit C++ Aer backend execution engine over AMD's dense cores.
export OMP_NUM_THREADS=288
export MKL_NUM_THREADS=288
export OPENBLAS_NUM_THREADS=288
export TORCH_NUM_THREADS=288

echo "=== System Check initialization ==="
echo "Node Allocated Execution Host: $(hostname)"
echo "Active Virtual Working Path: $(pwd)"
echo "OMP OpenMP Core Allocation Target: $OMP_NUM_THREADS"
echo "==================================="

# --------------------------------------------------------------------
# 3. Execution Pipeline Routines
# --------------------------------------------------------------------

echo -e "\n[STEP 1/3] Triggering Vector A: Stochastic MCMC (Gibbs Sampling) Baseline..."
# Run full scale 37-node system with higher sample profiles locally unblocked
srun python3 src/monte_carlo.py

echo -e "\n[STEP 2/3] Triggering Vector A Variant: Variational Inference (VI) Optimization..."
# PyTorch utilizes the full 288 thread allocations for fast forward/backward tensor calculation loops
srun python3 src/classical_vi.py

echo -e "\n[STEP 3/3] Triggering Route A: QCNN Quantum Core Emulation via Qiskit Aer..."
# Multi-threaded Qiskit Aer leverages multi-threading to scale simulated qubit bounds towards 30+ wires
srun python3 src/train.py

echo -e "\n=== Execution Loop Completed Successfully ==="


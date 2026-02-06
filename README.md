# Code2Bench: Scaling Source and Rigor for Dynamic Benchmark Construction

<div align="center">

[![Venue: ICLR 2026](https://img.shields.io/badge/Venue-ICLR%202026-brightgreen)](https://openreview.net/forum?id=YOUR_PAPER_ID)
[![arXiv](https://img.shields.io/badge/arXiv-2508.07180-B31B1B.svg)](https://arxiv.org/abs/2508.07180)
[![Website](https://img.shields.io/badge/Project-Website-blue)](https://code2bench.github.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

**The Next Generation Framework for Dynamic and Rigorous Code LLM Evaluation.**

[**Features**](#-key-features) | [**News**](#-news) | [**Evaluation**](#-quick-start-evaluation) | [**Construction**](#-benchmark-construction) | [**Paper**](#-citation)

</div>

---

## 📢 News
*   **[2026/01]** 🎉 **Code2Bench** has been accepted as a conference paper at **ICLR 2026**!

---

## ✨ Key Features

The evaluation of code-generating LLMs is currently limited by **static, contaminated problem sources** and **low-rigor testing**. CODE2BENCH introduces the **Dual Scaling** philosophy:

1.  **Scaling the Source (Dynamic & Contamination-Resistant):**
    *   **Temporal Filtering:** Automatically ingests code from GitHub commits created *after* the knowledge cutoff of the evaluated models.
    *   **Principled Classification:** Uses language-agnostic **Scope Graph** analysis to classify tasks into *Self-Contained (SC)* and *Weakly Self-Contained (WSC)*.

2.  **Scaling the Rigor (Deep & Diagnostic):**
    *   **Property-Based Testing (PBT):** Generates hundreds of nuanced test cases automatically per task.
    *   **The "Great Filter":** A stringent **100% branch coverage quality gate** ensuring every task is logically verifiable and non-trivial.
    *   **Diagnostic Fingerprints:** Beyond Pass@1, we provide granular insights into failure modes (Syntax vs. Runtime vs. Logic).

---

## 🚀 Quick Start: Evaluation

Evaluate your LLM on the **CODE2BENCH-2509** suite in minutes.

### 1. Installation
```bash
conda create -n code2bench python=3.10 -y
conda activate code2bench
sudo apt-get update && sudo apt-get install graphviz graphviz-dev -y
pip install -r requirements.txt
export PYTHONPATH=`pwd`:$PYTHONPATH
```

### 2. Plug in Your Model
To evaluate a new model, simply inherit from the `LLM` base class:

```python
# code2bench/llm/my_model.py
from code2bench.llm.base import LLM

class MyCustomLLM(LLM):
    def chat(self, system_prompt, user_input, **kwargs):
        # Integrate your API or local inference here
        return response_text
```

### 3. Run Benchmark
Execute the evaluation script for Python or Java:
```bash
python code2bench/test_runner/benchmark_runner.py --benchmark_name Python --mode weakly
```

---

## 🛠️ Benchmark Construction

Build your own dynamic benchmark instances from fresh GitHub repositories.

### Configuration
1.  **Define Sources:** Add repository URLs to `code2bench/projects.yaml`.
2.  **Set Time Window:** Define `start_time` and `end_time` in the execution command to target specific commit history (for anti-contamination).

### Full Pipeline Run
The pipeline automates: *Acquisition → Scope Analysis → PBT Generation → Coverage Filtering → Instruction Generation.*

```bash
# Example: Constructing a Python Weakly Self-Contained benchmark
python code2bench/run.py \
    --benchmark_name Python \
    --mode weakly \
    --start_time 2024-08-01 \
    --end_time 2025-05-30 \
    --use_proxy
```

For **Java** tasks, use:
```bash
python code2bench/run_java.py --benchmark_name Pure_Java --mode self
```

---

## 📈 Analysis & Visualization

CODE2BENCH provides a novel **Diagnostic Fingerprint** visualization to understand *why* models fail.

| Mode | Fail Mode Peak | Insights |
| :--- | :--- | :--- |
| **SC (Algorithm)** | LogicErr | Models struggle with core synthesis logic. |
| **WSC (Library)** | RuntimeErr | Challenges arise from API misapplication. |
| **Java Native** | Perfect Surge | Static typing acts as a "performance scaffold". |

---

## 🤝 Contributing
We welcome contributions! Whether it's adding new language support (C++, Rust, Go) or improving the PBT engines, please feel free to open an Issue or a PR.

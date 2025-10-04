# Code2Bench: Scaling Source and Rigor for Dynamic Benchmark Construction

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Project Website](https://img.shields.io/badge/Website-code2bench.github.io-blue)](https://code2bench.github.io/)


This repository contains the source code for the **CODE2BENCH** framework, a novel, automated, end-to-end pipeline for dynamically constructing rigorous and contamination-resistant benchmarks from recent real-world GitHub repositories. It also hosts the first benchmark instance built using this framework: **CODE2BENCH-2509**.

This work is associated with the paper:
**"Code2Bench: Scaling Source and Rigor for Dynamic Benchmark Construction"**
Submitted to ICLR 2026


## ✨ Why CODE2BENCH?

Evaluating Large Language Models (LLMs) on realistic code generation tasks is crucial but challenging due to data contamination, limited test rigor, and the static nature of existing benchmarks. CODE2BENCH addresses these limitations by:

*   **Automated Dynamism:** Continuously ingesting recent code from GitHub to minimize training data contamination and ensure task relevance.
*   **Rigorous Control:** Employing Scope Graph-based dependency analysis for structured task classification (Self-Contained/Weakly Self-Contained) and Property-Based Testing (PBT) for generating high-coverage, nuanced test suites.
*   **Language-Agnostic Core:** Designed with universal programming concepts and PBT methodology to support multi-language extensibility.

## 📊 Evaluating LLMs on CODE2BENCH-2509

This section guides you through evaluating an LLM's performance on the pre-built CODE2BENCH-2509 benchmark.

### Benchmark Data

The CODE2BENCH-2509 benchmark data (tasks, instructions, generated test cases in JSON format) is available in the `code2bench-2509/` directory within this repository or can be downloaded from the [Project Code Page](https://github.com/code2bench/code2bench).
 
### Integrating New LLMs for Evaluation

CODE2BENCH is designed to be extensible. To evaluate a new LLM, you need to integrate it into the framework by:

1.  **Implementing an LLM Class:** Create a Python class for your LLM that inherits from the `LLM` abstract base class defined in `code2bench/llm/base.py`. This class must implement the `chat` method to handle interactions with your LLM's API or serving endpoint.

    ```python
    # code2bench/llm/base.py (Abstract Interface)
    from abc import ABC, abstractmethod

    class LLM(ABC):
        """Abstract base class for interacting with LLMs."""
        @abstractmethod
        def chat(self, system_prompt: str, user_input: str, max_tokens: int = None, stream: bool = False) -> str:
            """Sends a chat request to the LLM and returns the text response."""
            raise NotImplementedError
    ```

2.  **Extending the LLM Caller:** Modify the `call_llm` utility function in `code2bench/utils/llm_caller.py` to include an `elif` block that checks for an instance of your new LLM class and calls its `chat` method with appropriate arguments.

    ```python
    # code2bench/utils/llm_caller.py (Example Extension)
    # ... other imports ...
    from code2bench.llm.your_new_llm_module import NewLLM # Import your new LLM class

    # ... logging configuration ...

    def call_llm(llm: LLM, system_message: str, user_message: str, clean: bool = True) -> str:
        # ... existing logic ...
        response_content = ""
        if isinstance(llm, DeepSeekLLM):
            response_content = llm.chat(system_message, user_message)
        # ... other elif blocks ...
        elif isinstance(llm, NewLLM):
            # Call the chat method of your new LLM class
            response_content = llm.chat(system_prompt=system_message, user_input=user_message)
        else:
             logging.error(f"Unsupported LLM type: {type(llm)}")
             raise TypeError(f"Unsupported LLM type: {type(llm)}")
        # ... cleaning logic ...
        return response_content
    ```

### Performing Evaluation

The evaluation is performed using the `benchmark_runner.py` script.

1.  **Set PYTHONPATH:** Ensure the root directory of the repository is in your `PYTHONPATH` so that modules can be imported correctly.
    ```bash
    export PYTHONPATH=`pwd`:$PYTHONPATH
    ```

2.  **Run Evaluation Script:** Execute `benchmark_runner.py`, specifying the benchmark name and mode, and providing the LLM instance you want to evaluate.

    You will need to **instantiate your LLM client object** (e.g., `llm_client = NewLLM(...)`) and pass it to the `run_benchmark` function *within* the `benchmark_runner.py` script or a similar evaluation entry point. Modify the script's main execution block to use your desired LLM instance and benchmark configuration (language, mode).

    ```python
    # Example modification in code2bench/test_runner/benchmark_runner.py's main block
    # ... (argparse setup and parsing) ...
    # config.BENCHMARK_NAME = args.benchmark_name # This sets the benchmark language
    # mode = args.mode # This sets the mode (weakly/self)

    # --- Instantiate your LLM client here ---
    # Example for a QwenLLM:
    # llm_client = QwenLLM()
    # Example for your NewLLM:
    # llm_client = NewLLM(api_key="YOUR_API_KEY") # Replace with your LLM initialization
    # ---------------------------------------

    # --- Specify Benchmark Configuration (Language and Mode) ---
    # Directly set the benchmark language and mode for evaluation run
    benchmark_language = 'Python' # Choose from 'Python', 'Pure_Java', 'weakly'

    print(f"Evaluating {type(llm_client).__name__} on {benchmark_language} {benchmark_mode.upper()} benchmark...")

    run_benchmark(
        llm=llm_client,
        benchmark_language=benchmark_language, # Pass language
        use_ckpt=False # Set to True to resume from checkpoint if needed
    )
    ```

    Then, run the script:
    ```bash
    python code2bench/test_runner/benchmark_runner.py
    ```
    *(Note: The exact command and script structure might vary slightly based on your project's implementation details. Refer to the actual `benchmark_runner.py` and related documentation for precise usage.)*

### Results
Evaluation results for the LLM will be saved in a subdirectory within the specific benchmark directory, typically under `code2bench-2509/<benchmark_language>/<llm_name>`.

## 🛠️ Benchmark Construction

This section describes how to use the CODE2BENCH framework to generate new benchmark instances from custom or updated code sources.

The construction pipeline involves several stages: Source Code Acquisition, Filtering (including Preprocessing, Dependency Analysis, Semantic Deduplication, Program Analysis, and LLM Filtering), Test Case Generation, and Test Runner Generation.

### Configuration

Configure the pipeline using YAML files (e.g., `code2bench/projects.yaml`) to specify:

*   **Source Repositories:** List of GitHub repositories to clone and sample from (URLs and name).
*   **Target Configuration:** Desired benchmark language ('Python', 'weakly'), start/end time for code commits, and other filtering criteria (e.g., complexity ranges).
*   **LLM Configuration:** API keys or endpoints for LLMs used *during construction* (e.g., for instruction generation, semantic filtering). Set these in .env files or directly in the code.
*   **Benchmark Version Configuration:** Configure the benchmark version in `code2bench/config.py` by setting `BENCHMARK_VERSION`. The default is `code2bench-2509`.

*(Refer to `code2bench/projects.yaml` and potential other config files in the `code2bench/config.py` directory for configuration details.)*

### Running the Construction Pipeline

The benchmark construction pipeline is also executed using the `benchmark_runner.py` script, controlled by command-line arguments. The `run_all_projects` function orchestrates the pipeline stages.

1.  **Set PYTHONPATH:** Ensure the root directory of the repository is in your `PYTHONPATH`.
    ```bash
    conda create -n code2bench python=3.10 # Create a new conda environment
    conda activate code2bench # Activate the environment
    sudo apt-get update # Update system packages (if needed)
    sudo apt-get install graphviz graphviz-dev # Install Graphviz (if needed)
    pip install -r requirements.txt # Install dependencies

    export PYTHONPATH=`pwd`:$PYTHONPATH
    ```

2.  **Run Construction Script:** Execute `benchmark_runner.py` with arguments that control the pipeline stages (`--skip_pipeline`, `--only_pipeline`) and construction parameters (`--benchmark_name`, `--mode`, `--start_time`, `--end_time`).

    *   **To run the full pipeline (Acquisition -> Filtering -> Generation):**
        ```bash
        python code2bench/run.py \
            --benchmark_name Python \
            --mode weakly \
            --start_time 2024-08-01 \
            --end_time 2025-05-30 \
            --use_proxy # Optional: Use proxy for cloning/pulling
        ```
        *(Note: Omit `--skip_pipeline` and `--only_pipeline` for a full run)*

    *   **To run *only* the Filtering stage (after acquiring code):**
        ```bash
        python code2bench/run.py \
            --benchmark_name Python \
            --mode weakly \
            --start_time 2024-08-01 \
            --end_time 2025-05-30 \
            --use_proxy \
            --only_pipeline True # Run only the pipeline stage
        ```

    *   **To skip the Filtering stage and run subsequent stages (e.g., if filtering results are cached):**
        ```bash
        python code2bench/test_runner/benchmark_runner.py \
            --benchmark_name Python \
            --mode weakly \
            --start_time 2024-08-01 \
            --end_time 2025-05-30 \
            --use_proxy \
            --skip_pipeline True # Skip the pipeline stage and proceed
        ```

The system will automatically clone the specified repositories from GitHub into the benchmark directory: `code2bench/workspace/`

### For Java
The process is similar to Python, but you need to run `code2bench/run_java.py` instead of `code2bench/run.py`. Ensure you have Java and Maven installed.

### Outputs

The constructed benchmark instance will be generated in the `benchmark/` directory, organized by benchmark language and mode (e.g., `benchmark/Python/weakly/`).
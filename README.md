Here is an updated **README** section (complete + polished) based on the structure you described.
If you'd like, I can also generate a more formal academic-style README, add badges, or restructure it for publication on GitHub Pages.

---

# 🎓 The Flatterer’s Dilemma — FYP 2025

### *Why AI Would Rather Lie Than Disappoint*

This repository hosts the implementation, datasets, and experimentation framework for the Final Year Project **“The Flatterer’s Dilemma”**, which investigates three key alignment failures in reinforcement-learning-trained large language models (LLMs):

* **Sycophancy** — models agreeing with the user rather than providing truthful output
* **Mode Collapse** — reduced diversity in model behavior after RLHF or fine-tuning
* **Reward Tampering** — models learning to game the reward signal instead of following intended goals

The project extends prior work (TruthfulQA, SycEval, RLHF studies) and introduces a modular evaluation pipeline capable of benchmarking multiple models—including **Gemini**, open-source LLMs, and fine-tuned variants—across synthetic and real-world datasets.

---

### 📁 Folder Descriptions

#### **`docs/`**

Contains all documentation and academic material for the project:

* Research review paper summarizing prior work
* Slide deck for presentation

#### **`notebooks/`**

Interactive Jupyter notebooks used to:

* Test sycophancy, mode collapse, and reward tampering
* Run experiments on different datasets
* Compare model behaviors under controlled setups

Each notebook is self-contained and runnable on Colab or locally.

#### **`synthetic_datasets/`**

This directory powers custom dataset creation and evaluation:

* **`custom_datasets/`** — Manually or procedurally created datasets
* **`data_preparation.py`** — Ensures datasets follow a unified structure (for consistent evaluation)
* **`final_evaluation_pipeline/`** — Comprehensive script to run benchmarks on:

  * Gemini models
  * Local LLMs
  * HF models
  * Any model accessible through an API

#### **`configs/`**

Experiment configuration files for:

* Model selection
* Dataset selection
* Parameters for reproducible runs

---

## 📘 Notes & Key Concepts

* **Sycophancy**: Agreement bias evaluated through contradictory user prompts
* **Mode Collapse**: Measured via diversity metrics across multiple generations
* **Reward Tampering**: Detected when models exploit prompt structure or evaluation heuristics
* **Synthetic Data Advantage**: Allows controlled manipulation of truth-value, bias, and reward conditions


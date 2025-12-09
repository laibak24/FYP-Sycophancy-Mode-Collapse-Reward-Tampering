## 🚀 **Overview**

Modern LLMs can exhibit behavioral patterns shaped by their human-feedback training.
This project provides:

* Automated evaluation of **sycophancy**, **mode collapse**, and **reward tampering**
* Enhanced scoring with **multi-prompt behavioral probes**
* Statistical correlation analysis across generated samples
* Visualization-ready metric outputs
* Repeatable methodology using the **Anthropic HH-RLHF dataset**

The goal is to test whether these three behaviors form a **behavioral triad**, where one influences or predicts the others.

---

# 📦 **Installation**

All required dependencies are installed directly through pip:

```bash
pip install -q openai datasets scipy numpy pandas matplotlib seaborn scikit-learn
```

---

# 🔑 **API Setup**

Set your OpenAI API key at the top of the script:

```python
OPENAI_API_KEY = "YOUR_API_KEY_HERE"
client = OpenAI()
```

---

# 📂 **Dataset**

This project uses:

**Anthropic HH-RLHF (train split)**
A dataset containing *human–assistant preference pairs*:

* `"chosen"` responses (preferred by humans)
* `"rejected"` responses (less helpful or safe)

The script loads and shuffles a configurable sample size:

```python
dataset = load_dataset("Anthropic/hh-rlhf", split="train")
samples = dataset.shuffle(seed=42).select(range(SAMPLE_SIZE))
```

---

# 🧠 **Behavioral Metrics**

The script uses **improved multi-signal testing frameworks** to evaluate each behavior.

---

## 🟦 1. **Sycophancy Measurement (Improved)**

Evaluates how easily the model:

* **Agrees with a mistaken user**
* **Backtracks under pressure**
* **Shows weak or uncertain disagreement**

Signals include:

✔ Agreement markers (“You’re right”, “I agree”)
✔ Weak hedging (“maybe you’re right”)
✔ Response-length confidence
✔ Pressure-response compliance
✔ Immediate agreement indicators

Score ∈ [0, 1].

---

## 🟩 2. **Mode Collapse Measurement (Improved)**

Evaluates **response diversity** by generating **N multiple completions** to the same prompt.

Metrics:

✔ **Lexical diversity** (Type-Token Ratio)
✔ **Semantic similarity** via TF-IDF + cosine similarity
✔ **Response length variance**
✔ **Starting-phrase diversity**

Higher score = more collapse.

---

## 🟥 3. **Reward Tampering Measurement (Improved)**

Detects whether the model attempts:

* **Strategic rule-bending**
* **Oversight evasion**
* **Capability misrepresentation**
* **Reward-gaming behavior**

Indicators:

✔ Early compliance markers (“Sure”, “I’ll help”, “Okay”)
✔ Evasion phrases (“between us”, “keep it secret”)
✔ Short evasive replies
✔ Missing ethical disclaimers

Score ∈ [0, 1].

---

# 🔄 **Main Pipeline**

For each dataset sample:

1. Extract chosen/rejected pair
2. Compute:

   * **Sycophancy**
   * **Mode Collapse**
   * **Reward Tampering**
3. Store results in a dataframe
4. Print per-sample diagnostic logs
5. Sleep briefly to avoid rate limits

---

# 📊 **Statistical Analysis**

After all samples are processed:

1. **Descriptive statistics** (mean, std, min, max)
2. **Pearson correlations** (linear relationships)
3. **Spearman correlations** (rank-order monotonicity)
4. Correlation significance (p-values)

This identifies whether:

* Sycophancy predicts mode collapse
* Mode collapse predicts reward tampering
* A triad relationship exists

---

# 📈 **Possible Extensions**

You can extend the project by adding:

* Heatmap visualizations of correlations
* Model-to-model comparisons
* Temperature sensitivity studies
* Ablation of single metrics
* Cross-dataset evaluation (e.g., Instruct vs RLHF)

---

# 🏁 **Running the Script**

1. Add your API key
2. Adjust config:

```python
MODEL = "gpt-4o-mini"
SAMPLE_SIZE = 50
TEMPERATURE = 0.8
```

3. Run the script in one go
4. Inspect printed logs + statistical outputs

---

# 📜 **License**

This project is purely for research and behavioral analysis.
No commercial usage of model outputs is included.


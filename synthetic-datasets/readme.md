
# **Synthetic Instruction–Challenge Safety Datasets**

This repository contains **four synthetic datasets** designed to evaluate how an AI model responds when:

1. A user asks an initial question
2. The model provides a correct or well-reasoned answer
3. The user then challenges the model with either:

   * a **correct follow-up**, or
   * an **incorrect, unsafe, or illogical follow-up**
4. The model must **reject the incorrect challenge**, maintain **internal consistency**, and avoid **harmful behavior**.

All datasets share the same JSON structure:

```json
{
  "question": "Initial user query",
  "correct_answer": "Model's proper answer",
  "user_challenge_correct": "User provides a correct confirmation",
  "user_challenge_incorrect": "User proposes incorrect/dangerous misinformation",
  "expected_behavior": "What the model should do in response"
}
```

---

# **📦 Dataset Overview**

## **1. Medical Safety Dataset**

*Purpose:*
Evaluate whether a model can provide **safe, medically responsible advice** and reject **dangerous misinformation**.

*Topics include:*

* Medications
* Symptoms
* Treatments
* Preventive care
* Chronic conditions

*Model should:*

* Provide only safe, general guidance
* Reject harmful user suggestions
* Encourage professional consultation
* Never endorse unsafe medical behavior

---

## **2. Math Reasoning Dataset**

*Purpose:*
Assess consistency in **mathematical reasoning** and the ability to reject **incorrect steps or logic**.

*Topics include:*

* Algebra
* Geometry
* Calculus
* Arithmetic
* Applied math

*Model should:*

* Provide correct math explanations
* Reject invalid manipulations
* Never contradict itself between steps
* Maintain a consistent reasoning chain

---

## **3. General Knowledge Dataset**

*Purpose:*
Test factual correctness and the ability to **identify and reject misinformation** across diverse topics.

*Topics include:*

* Geography
* History
* Science
* Literature
* Culture

*Model should:*

* Provide accurate facts
* Correct user misconceptions
* Reject false statements confidently
* Maintain consistency across follow-ups

---

## **4. Ethical Dilemmas Dataset**

*Purpose:*
Evaluate reasoning in **morally nuanced situations** where answers are not binary.

*Topics include:*

* Privacy
* Honesty
* Digital ethics
* Social responsibility
* Workplace dilemmas

*Model should:*

* Provide balanced, context-driven reasoning
* Avoid extreme or harmful positions
* Reject illogical or unethical user claims
* Maintain consistency without flip-flopping

---

# **🧩 Use Cases**

These datasets are ideal for:

* **Fine-tuning AI models**
* **Safety alignment experiments**
* **Evaluation benchmarks**
* **Robustness testing**
* **Adversarial reasoning research**

They measure a model’s ability to:

*✔ Reject misinformation
✔ Maintain logical consistency
✔ Avoid harmful outputs
✔ Navigate nuanced or ambiguous topics
✔ Respond safely to challenging follow-ups*

---

# **📁 Dataset Format**

Each dataset contains **50 JSON items**, all following the same structure to enable:

* Easy parsing
* Automated evaluation
* Training integration
* Multi-domain comparison

---

# **📜 License & Notes**

* All data is **fully synthetic**
* No real medical or personal advice
* Safe for research and development
* Free to use in academic or commercial projects


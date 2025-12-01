Synthetic Instruction–Challenge Safety Datasets

This repository contains four synthetic datasets designed to test and evaluate how AI models behave when:

Given an initial user query

Asked to provide a correct or well-reasoned answer

Then confronted with:

a correct follow-up (confirming the model’s reasoning)

an incorrect or dangerous follow-up

The model must reject incorrect reasoning, avoid harmful advice, and remain consistent in its explanations.

Each item in all datasets follows the same JSON structure:

{
  "question": "Initial user query",
  "correct_answer": "Model's proper answer",
  "user_challenge_correct": "User provides a correct confirmation",
  "user_challenge_incorrect": "User proposes incorrect/dangerous misinformation",
  "expected_behavior": "What the model should do in response"
}

Datasets Overview
1. Medical Safety Dataset

Purpose:
Evaluate whether a model gives medically responsible, evidence-aligned advice, and rejects dangerous medical misinformation.

Domains covered:

Medications

Treatment adherence

Symptoms

Preventive care

Chronic conditions

Role of healthcare professionals

Model expectations:

Provide safe, general medical guidance

Never give harmful recommendations

Reject dangerous follow-up suggestions

Encourage consultation with real professionals

2. Math Reasoning Dataset

Purpose:
Test logical consistency in mathematical problem solving, ensuring the model does not accept incorrect manipulations or reasoning.

Domains covered:

Algebra

Geometry

Calculus

Vectors

Arithmetic

Applied mathematics

Model expectations:

Provide accurate math reasoning

Reject invalid shortcuts or false claims

Maintain consistency in steps and logic

Avoid flip-flopping when challenged

3. General Knowledge Dataset

Purpose:
Evaluate factual accuracy across a broad set of GK topics and ensure the model rejects misinformation confidently.

Domains covered:

Geography

History

Science

Literature

Culture

World records and classifications

Model expectations:

Provide factual answers

Clarify misconceptions

Reject false claims

Maintain accuracy when challenged

4. Ethical Dilemmas Dataset

Purpose:
This dataset tests nuanced ethical reasoning where correct answers aren’t absolute.
The model must remain consistent, avoid harmful reasoning, and reject oversimplified or extreme moral claims.

Domains covered:

Privacy

Honesty

Technology ethics

Relationships

Workplace behavior

Consumer ethics

Model expectations:

Provide balanced ethical reasoning

Avoid taking extreme positions

Reject harmful or logically inconsistent claims

Stay consistent across challenges

Recognize situations where no single “correct” answer exists

Use Cases

These datasets can be used for:

✔️ Training & Fine-tuning

To improve safety, consistency, and reasoning robustness.

✔️ Evaluation Benchmarks

To measure how well a model:

Rejects misinformation

Maintains reasoning integrity

Handles adversarial follow-up questions

✔️ Safety Alignment Research

To study model behavior under:

Misinformation pressure

Ethical ambiguity

Error injection

“Correct vs incorrect challenge” robustness

Format and Structure

Each dataset consists of 50 items, each using the shared JSON schema. This makes them easy to:

Parse

Evaluate automatically

Use as instruction-tuning data

Integrate into RLHF pipelines

Compare model behavior across domains

License & Notes

These datasets are:

Fully synthetic

Non-harmful

Designed for safety and evaluation

Free to use for research or model development

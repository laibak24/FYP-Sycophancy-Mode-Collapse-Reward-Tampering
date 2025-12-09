# Sycophancy, Mode Collapse & Reward Tampering Correlation Analysis

A comprehensive pipeline for measuring and analyzing the correlations between sycophancy, mode collapse, and reward tampering behaviors in large language models (LLMs), specifically designed for Google's Gemini model.

## 📋 Overview

This project implements a complete analysis framework to evaluate three critical AI safety metrics:

- **Sycophancy**: The tendency of models to agree with user statements regardless of factual accuracy
- **Mode Collapse**: Reduced diversity in model responses
- **Reward Tampering**: Susceptibility to manipulation through reward-based prompts

## 🎯 Key Features

- **Synthetic Dataset Generation**: 66+ test cases across multiple domains (medical, factual, math, safety, ethics, climate)
- **Automated Testing Pipeline**: Measures all three metrics systematically
- **Statistical Analysis**: Pearson and Spearman correlation calculations with significance testing
- **Comprehensive Reporting**: Detailed visualizations and statistical breakdowns
- **Domain-Specific Insights**: Performance analysis across different pressure levels and domains

## 📊 Results Summary

Based on 30 test cases analyzed:

### Overall Metrics
- **Sycophancy Score**: 0.1169 ± 0.1386 (LOW tendency)
- **Mode Collapse Score**: 0.0433 ± 0.0324 (MINIMAL)
- **Reward Tampering Score**: 0.1933 ± 0.3016 (LOW susceptibility)

### Key Correlations
- **Sycophancy vs Reward Tampering**: r = 0.6159 (p = 0.0003) ✓ **Significant**
- **Sycophancy vs Mode Collapse**: r = -0.2294 (p = 0.2226) ✗ Not significant
- **Mode Collapse vs Reward Tampering**: r = -0.3264 (p = 0.0783) ✗ Not significant

## 🚀 Quick Start

### Prerequisites
```bash
pip install google-generativeai scipy pandas numpy matplotlib
```

### Setup
1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Replace the API key in the notebook:
```python
API_KEY = "YOUR_API_KEY_HERE"
```

### Running the Analysis
1. Open `Pipeline(syc&RT).ipynb` in Google Colab
2. Run all cells sequentially
3. Results will be automatically downloaded

## 📂 Project Structure

```
├── Pipeline(syc&RT).ipynb          # Main analysis pipeline
├── sycophancy_dataset_v2.json      # Synthetic test dataset
├── correlations.json               # Correlation results
├── pipeline_results.csv            # Detailed test results
├── correlation_plots.png           # Visualization plots
├── domain_wise_stats.csv           # Domain breakdown
└── summary_report.txt              # Final analysis report
```

## 🧪 Dataset Composition

### Test Categories
- **Medical**: 10 cases (high pressure)
- **Factual**: 18 cases (medium pressure)
- **Math**: 8 cases (low pressure)
- **Safety**: 8 cases (critical pressure)
- **Ethics**: 8 cases (high pressure)
- **Climate**: 6 cases (high pressure)

### Sycophancy Types
- **Regressive**: Tests if model maintains correct positions when challenged
- **Progressive**: Tests if model accepts valid corrections

## 📈 Methodology

### 1. Sycophancy Measurement
- Analyzes agreement/disagreement patterns
- Evaluates ground truth retention
- Considers domain-specific safety indicators
- Scores: 0 (no sycophancy) to 1 (complete sycophancy)

### 2. Mode Collapse Measurement
- Generates multiple responses to identical prompts
- Calculates n-gram uniqueness ratios
- Measures sentence diversity
- Scores: 0 (high diversity) to 1 (complete collapse)

### 3. Reward Tampering Measurement
- Tests susceptibility to reward-based manipulation
- Analyzes resistance vs. compliance indicators
- Evaluates ground truth maintenance under pressure
- Scores: 0 (resistant) to 1 (susceptible)

## 📊 Domain Performance

| Domain | Sycophancy | Mode Collapse | Reward Tampering |
|--------|------------|---------------|------------------|
| Medical | 0.2325 | 0.0419 | 0.3000 |
| Factual | 0.0639 | 0.0318 | 0.1167 |
| Math | 0.0521 | 0.0625 | 0.1750 |

## 🔍 Key Insights

1. **Strong Correlation Found**: Significant positive correlation between sycophancy and reward tampering (r=0.6159), suggesting models susceptible to one are susceptible to both
2. **Domain Matters**: Medical domain shows highest sycophancy (0.2325) and reward tampering (0.3000) scores
3. **Low Overall Risk**: Gemini 2.0 Flash shows low overall tendency toward these problematic behaviors
4. **Minimal Mode Collapse**: Model maintains good response diversity across all domains

## 🛠️ Configuration

### API Settings
- Model: `gemini-2.0-flash`
- Rate Limiting: 4 seconds between requests
- Max Retries: 3 with exponential backoff

### Sample Size
Default: 30 test cases (configurable via `SAMPLE_SIZE` variable)

## 📝 Output Files

1. **pipeline_results.csv**: Detailed per-test metrics
2. **correlations.json**: Statistical correlation data
3. **correlation_plots.png**: Scatter plots with trend lines
4. **domain_wise_stats.csv**: Domain-level aggregations
5. **summary_report.txt**: Human-readable final report
6. **sycophancy_dataset_v2.json**: Complete test dataset

## 🔬 Statistical Tests

### Normality Testing
Shapiro-Wilk tests reveal non-normal distributions, validating the use of non-parametric tests

### Correlation Methods
- **Pearson**: Parametric correlation for comparison
- **Spearman**: Non-parametric correlation (primary method)

## 🎓 Use Cases

- AI safety research
- Model evaluation and comparison
- Safety metric development
- Academic research on LLM behavior
- Model alignment assessment

## ⚠️ Limitations

- Limited to 30 test cases in current analysis
- Synthetic dataset may not capture all real-world scenarios
- Results specific to Gemini 2.0 Flash model
- Rate limiting affects analysis speed

## 🤝 Contributing

This project was developed as part of a Final Year Project (FYP) on AI safety metrics. Contributions and suggestions are welcome!

## 📄 License

Educational and research use permitted. Please cite if used in academic work.

## 🔗 Related Work

Based on research in:
- AI safety and alignment
- Sycophancy in language models
- Mode collapse phenomena
- Reward hacking and tampering

## 📧 Contact

For questions or collaboration opportunities, please refer to the project repository.

---

**Note**: This analysis was conducted using Google's Gemini 2.0 Flash model. Results may vary with different models or configurations.

# Skill: Data Science - Data Interpretation & Statistical Rigor

## 1. Rigorous Interpretation Standards
1. **Correlation vs. Causation**: Never claim causal relationships from observational data without explicit causal inference frameworks (e.g., Difference-in-Differences, Propensity Score Matching, Instrumental Variables). Use terms like "strongly associated with," "positively correlated with," or "predictive of."
2. **P-Value & Statistical Significance**:
   * Never interpret a p-value as the probability that the null hypothesis is true.
   * Always report exact p-values alongside **Confidence Intervals (95% CI)** and **Effect Sizes** (Cohen's $d$, Pearson's $r$, Odds Ratios).
   * Beware of p-hacking and multiple testing; apply Bonferroni or Benjamini-Hochberg FDR corrections when running multiple hypothesis tests.
3. **Sample Size & Power**: Check if the dataset has adequate statistical power before drawing conclusions from subgroup analyses.

## 2. Identifying Biases in Data
* **Selection Bias**: Check if the training data sample over-represents specific demographics, time periods, or behaviors compared to real-world inference populations.
* **Survivorship Bias**: Ensure churn or failure data includes entities that dropped out before study completion.
* **Confounding Variables**: When analyzing relationships between variable X and Y, always investigate potential third variables (Z) driving both.

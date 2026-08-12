# Skill: Data Science - Statistical Analysis & Hypothesis Testing

## 1. Test Selection Framework
When analyzing group differences or experiment results, select the appropriate statistical test based on data distributions and sample sizes:

| Scenario | Parametric Test (Normal Data) | Non-Parametric Test (Skewed / Outliers) |
| :--- | :--- | :--- |
| **Two Independent Groups** | Student's t-test (or Welch's t-test if unequal variances) | Mann-Whitney U Test |
| **Two Paired Groups** | Paired t-test | Wilcoxon Signed-Rank Test |
| **3+ Independent Groups** | One-Way ANOVA | Kruskal-Wallis Test |
| **Categorical vs. Categorical** | Chi-Square Test of Independence | Fisher's Exact Test (if expected cell count < 5) |
| **Correlation** | Pearson's $r$ | Spearman's $\rho$ or Kendall's $\tau$ |

## 2. A/B Testing & Experimentation
1. **Pre-Experiment Sizing**: Calculate required sample size per variant using baseline conversion rate, Minimum Detectable Effect (MDE), significance level ($\alpha = 0.05$), and statistical power ($1 - \beta = 0.80$).
2. **Sample Ratio Mismatch (SRM)**: Always perform a Chi-Square goodness-of-fit test on the sample sizes between Control and Treatment before evaluating metrics to detect assignment bugs.
3. **Bootstrapping**: When analyzing non-standard metrics (e.g., average revenue per user, ratios, percentiles), use empirical bootstrapping with 1,000+ resamples to construct robust 95% confidence intervals.

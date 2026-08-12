# Skill: Data Science - Exploratory Data Analysis (EDA) & Plotting

## 1. Initial Dataset Audit Workflow
When presented with a new tabular dataset (`.csv`, `.parquet`, `.sqlite`), immediately execute or generate code for this standardized EDA check:
1. **Dimensions & Schema**: Print `df.shape`, data types, and memory usage (`df.info(memory_usage='deep')`).
2. **Missingness Audit**: Calculate exact counts and percentages of NaN/Null values per column. If missingness > 40%, flag for drop or advanced imputation (MICE/KNN).
3. **Duplicate Check**: Identify exact duplicate rows or duplicate primary IDs (`df.duplicated().sum()`).
4. **Distribution Summary**: Compute robust statistics—mean, std, median, 25th/75th percentiles, and skewness (`df.skew()`).

## 2. Outlier & Anomaly Detection
* **IQR Method**: Flag values outside $[Q_1 - 1.5 \times IQR, Q_3 + 1.5 \times IQR]$.
* **Winsorization**: When preparing data for linear models, clip extreme outliers at the 1st and 99th percentiles rather than dropping rows.
* **Z-Score / Isolation Forest**: Use Z-score ($|Z| > 3$) for normal distributions, or `IsolationForest` / `LocalOutlierFactor` for multi-dimensional anomaly detection.

## 3. High-Impact Visualization Standards
* **Terminal ASCII Plotting**: For quick CLI checks, generate textual histograms or scatter plots using libraries like `plotext` or custom ASCII bins.
* **Production Charts (Seaborn/Plotly)**:
  * Always set clear titles, axis labels with units, and readable font sizes.
  * Use perceptual colormaps (`viridis`, `mako`, `coolwarm` for diverging data). Never use rainbow or jet colormaps.
  * For correlation matrices, annotate heatmaps with exact correlation coefficients ($r$) and mask the upper triangle to avoid redundancy.

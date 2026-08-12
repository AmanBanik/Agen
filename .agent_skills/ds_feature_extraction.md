# Skill: Data Science - Feature Engineering & Extraction

## 1. Categorical Encoding Strategies
* **Low Cardinality (< 10 unique values)**: Use One-Hot Encoding (`pd.get_dummies(drop_first=True)` or `OneHotEncoder(drop='first')`) to prevent collinearity.
* **High Cardinality (> 20 unique values)**:
  * Avoid One-Hot Encoding (causes dimensionality explosion and sparse matrices).
  * Use **Target Encoding** (`TargetEncoder` with smoothing/cross-validation fold encoding to prevent data leakage).
  * Or use Frequency/Count Encoding or Embedding layers in neural networks.
* **Ordinal Categories**: Use `OrdinalEncoder` with explicitly ordered mapping (e.g., Low < Medium < High).

## 2. Numerical Transformation & Scaling
* **Tree-Based Models (XGBoost, LightGBM, Random Forest)**: Scaling is NOT required. Do not waste compute standardizing features for trees.
* **Linear Models, SVMs, Neural Networks, and KNN**:
  * **StandardScaler**: Use when features follow a relatively Gaussian distribution without extreme outliers.
  * **RobustScaler**: Use when data contains extreme outliers (scales using median and IQR).
  * **Log/Box-Cox/Yeo-Johnson Transformation**: Apply to heavily right-skewed variables (e.g., income, transaction amounts, counts) to normalize distributions before modeling.

## 3. Multicollinearity & Interaction Features
* **Variance Inflation Factor (VIF)**: Always check VIF before fitting linear regression or logistic regression models. Drop features with $VIF > 10$ (or $> 5$ for strict models).
* **Domain-Specific Interactions**: Actively engineer high-signal domain features (e.g., `debt_to_income_ratio = total_debt / (annual_income + 1e-6)`, `time_since_last_purchase`, or rolling 7-day averages).

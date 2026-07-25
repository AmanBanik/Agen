# Skill: Data Science - Predictive Modeling & Machine Learning Best Practices

## 1. Model Progression & Baseline Philosophy
1. **Always Build a Dummy/Baseline First**: Start with `DummyClassifier(strategy='most_frequent')` or `DummyRegressor(strategy='mean')`, followed by a simple interpretable model (Logistic Regression or Ridge Regression) before deploying complex ensembles.
2. **Tabular Data Hierarchy**: For structured tabular data, Gradient Boosted Decision Trees (LightGBM, XGBoost, CatBoost) consistently outperform Deep Neural Networks. Prioritize LightGBM for speed and scalability.
3. **Unstructured Data Hierarchy**: Use deep learning architectures (CNNs, Vision Transformers for image; Transformer LLMs, BERT, RoBERTa for NLP/text).

## 2. Cross-Validation & Preventing Data Leakage
* **Strict Leakage Prevention**: ALL feature engineering steps (imputation, scaling, target encoding, TF-IDF vectorization) MUST be computed inside a `scikit-learn` `Pipeline` or evaluated strictly **within each training fold** of cross-validation. Never compute scaling or encoding statistics on the entire dataset before splitting.
* **CV Strategy**:
  * For imbalanced classification: Use `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
  * For time-series forecasting: NEVER shuffle time series data. Use `TimeSeriesSplit` or out-of-time (OOT) validation holdout periods.
  * For grouped/user-level data: Use `GroupKFold` to ensure the same user or entity is never in both train and validation splits.

## 3. Hyperparameter Tuning & Model Evaluation
* **Automated Tuning**: Use `Optuna` with Bayesian optimization (TPE sampler) for hyperparameter search over manual GridSearch.
* **Evaluation Metrics**:
  * Imbalanced classification: Report PR-AUC (Average Precision), F1-Score, and ROC-AUC. Never rely solely on Accuracy.
  * Regression: Report RMSE, MAE, and $R^2$. Use MAPE only if target values are strictly positive and non-zero.

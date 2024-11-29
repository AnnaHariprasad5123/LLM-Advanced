### Reasons for Removing Null Values

**1. Algorithms Cannot Handle Missing Data:** Many machine learning algorithms (like linear regression, decision trees, etc.) cannot handle missing values directly. Missing data can disrupt the mathematical operations that these models perform.

Example: In regression, you can’t compute a meaningful result if a value is missing in a critical variable like age or income.

**2. Simplification:** In some cases, missing values might represent a small fraction of the dataset, and removing those rows (or columns) simplifies data preparation without a significant loss of information. This is common when missing values are randomly distributed and not frequent.

Example: If a column has 99% of its data filled and only 1% missing, it may make sense to remove the rows with missing data for simplicity.

**3. Avoid Bias in Imputation:** Imputing (filling) missing values can introduce bias, especially if the values are not missing at random. In such cases, deleting the rows with missing data is preferred to avoid injecting incorrect assumptions into the dataset.

Example: Imputing missing income data with the average could mask the fact that missing values might represent people with significantly different income levels.

**4. Inconsistent Data:** Sometimes, missing values indicate a deeper issue with data collection or quality. Removing rows with missing values might help clean the dataset by removing corrupted or incomplete records that could distort analysis.

Example: If the data from one source is unreliable and full of missing values, you might choose to remove all rows from that source.

### Consequences of Removing Null Values

- Loss of Information
- Potential Bias
- Small Dataset
- Ignoring Valuable Insights

### When to Remove Null Values vs. Imputing

**Remove Null Values When:**

- The percentage of missing values is very small and removing them doesn’t significantly reduce the data size.
- The data is missing completely at random (MCAR) and there’s no underlying pattern to the missingness.
- The column with missing data is unimportant for the analysis or model.

**Impute or Handle Missing Values When:**

- A significant portion of the data is missing.
- The missing data is not random (i.e., there’s a pattern in the missingness).
- The feature is critical to the analysis or predictive modeling, and dropping rows/columns would result in loss of valuable information.

### Handling missing values - Techniques

**1. Removing Missing Data (Deletion)**

- Listwise Deletion: Remove rows where any column has missing data. This is simple but may lead to data loss if many rows have missing values.
- Column Deletion: Remove columns that have a large percentage of missing values, especially if they don't add much predictive value.

**Use Case:** When missing values are minimal or when the feature is not important.

**2. Imputation (Filling Missing Values)**

Mean/Median/Mode Imputation:

- Mean Imputation: Replace missing values with the mean of the column.
- Median Imputation: Replace missing values with the median, which is more robust to outliers.
- Mode Imputation: Replace missing categorical values with the most frequent category (mode).

**Use Case:** Suitable for numerical or categorical data with a low percentage of missing values.

Constant Value Imputation:

- Fill missing values with a specific constant, like 0, -1, or a placeholder (e.g., "Unknown").
  Use Case: Useful for missing values in categorical variables or when the missing values themselves carry meaning.

**4. Forward/Backward Fill**

- Forward Fill: Fill missing values with the previous value in a time series or sequential dataset.
- Backward Fill: Fill missing values with the next available value in the sequence.

**Use Case:** Common for time series or ordered data.

**5. Indicator for Missingness (Flagging)**

- Add a new binary feature that indicates whether the value in the original feature was missing (e.g., 1 for missing, 0 for present).

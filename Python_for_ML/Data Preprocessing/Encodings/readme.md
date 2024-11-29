**Link :** [Categorical Data Encoding Techniques](https://medium.com/aiskunks/categorical-data-encoding-techniques-d6296697a40f)

### Introduction

Data Encoding is an important pre-processing step in Machine Learning. It refers to the process of converting categorical or textual data into numerical format, so that it can be used as input for algorithms to process. The reason for encoding is that most machine learning algorithms work with numbers and not with text or categorical variables.

### Types of categorical data

1. Norminal Data - Catergories that does not have inherit order. Ex : Gender, States, etc..
2. Ordinal Data - Categories which has inherit order. Ex: Rank, Grades, Designations, Education etc...

### What is Data Encoding?

Data Encoding is an important pre-processing step in Machine Learning. It refers to the process of converting categorical or textual data into numerical format, so that it can be used as input for algorithms to process. The reason for encoding is that most machine learning algorithms work with numbers and not with text or categorical variables.

### There are several methods for encoding categorical variables, including

#### Nominal Data

1. One-Hot Encoding (10 columns - (10-1) = 9)
   - Categories becomes individual columns then each category of each column becomes 1 or 0 mapping to respective column categories.
   - Dummy variable Trap - pd.get_dummies.
   - disadvantage : curse of dimensionality.
2. One Hot Encoding with many categories
   - Competition : KDD 2009 cup
   - They came up with the solution to this problem
   - Only apply one hot encoding to top most 10 categories and consider them as one category then remaining will be becomes zero.
3. Mean Encoding
   - Example : pincodes feature may have many pincodes. For example : 1000 pincodes - 999 columns
   - Instead of making many columns
   - Convert this into values(float or integer) based on output variable(column) and try to find out mean for each category

#### Ordinal Data

1. Label Encoding
   - Categories which can be seen as a order so that we can assign ranks to them. Ex : Education - BE, Masters, PHD, Statistician
2. Target guided Encoding
   - Consider a feature with output variable then calculating the mean of output variable for each and every category then based on that we will assign the ranks to each category with the new column.

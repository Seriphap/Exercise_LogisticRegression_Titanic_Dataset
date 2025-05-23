import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Exercise: LogisticRegression Titanic Dataset')

url = 'https://drive.google.com/uc?id=1w1XQ8RzDDOLrUpBoE9oqRSPLO6QILEog'
df = pd.read_csv(url)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder

# List of columns to keep
columns_to_keep = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'Survived']

# Select the columns from the original DataFrame
df_cleaned = df[columns_to_keep]

# Remove rows where Age is less than or equal to 0 or is NaN (blank data)
df_cleaned = df_cleaned[(df_cleaned['Age'] > 0) & (df_cleaned['Age'].notna())]

# Convert 'Age' column to integers
df_cleaned['Age'] = df_cleaned['Age'].astype(int)

# Remove rows where Fare is 0
df_cleaned = df_cleaned[df_cleaned['Fare'] > 0]

# Remove rows where Embarked is blank or NaN
df_cleaned = df_cleaned[df_cleaned['Embarked'].notna()]

# Encode categorical columns 'Sex' and 'Embarked' using LabelEncoder
label_encoder = LabelEncoder()
df_cleaned['Sex'] = label_encoder.fit_transform(df_cleaned['Sex'])
df_cleaned['Embarked'] = label_encoder.fit_transform(df_cleaned['Embarked'])

# Define features (X) and target (y)
X = df_cleaned[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]  # Features
y = df_cleaned['Survived']  # Target variable

# Step 1: Split the data into training and testing sets
X_train_LG, X_test_LG, y_train_LG, y_test_LG = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Create a Logistic Regression model
model = LogisticRegression(max_iter=10000)  # Increase iterations if necessary

# Step 3: Train the model
model.fit(X_train_LG, y_train_LG)

# Step 4: Make predictions on the train set and Evaluate the model's performance (Training Set)
y_predict_train_LG = model.predict(X_train_LG)
report = classification_report(y_train_LG, y_predict_train_LG, output_dict=True)
report_df = pd.DataFrame(report).transpose()
st.write("Classification Report for Training Set:")
# Display as a table
st.dataframe(report_df.style.format("{:.2f}"))
# Create a heatmap
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(report_df.iloc[:, :-1] , annot=True, cmap="Blues", fmt=".2f", ax=ax)
ax.set_title("Classification Report Heatmap")
st.pyplot(fig)
accuracy_train_LG = accuracy_score(y_train_LG, y_predict_train_LG)
st.write(f'Accuracy on Training Set: {accuracy_train_LG * 100:.2f}%')
st.write("Confusion Matrix (Training Set):")
st.write(confusion_matrix(y_train_LG, y_predict_train_LG))

# Step 6: Make predictions on the test set and  Evaluate the model's performance (Test Set)
y_predict_test_LG = model.predict(X_test_LG)
report = classification_report(y_test_LG, y_predict_test_LG, output_dict=True)
report_df = pd.DataFrame(report).transpose()
st.write("\nClassification Report for Test Dataset:")
# Display as a table
st.dataframe(report_df.style.format("{:.2f}"))
# Create a heatmap
fig1, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(report_df.iloc[:, :-1] , annot=True, cmap="Blues", fmt=".2f", ax=ax)
ax.set_title("Classification Report Heatmap")
st.pyplot(fig1)
accuracy_test_LG = accuracy_score(y_test_LG, y_predict_test_LG)
st.write(f'Accuracy on Testing Set: {accuracy_test_LG * 100:.2f}%')
st.write("Confusion Matrix (Testing Set):")
st.write(confusion_matrix(y_test_LG, y_predict_test_LG))

import seaborn as sns
import matplotlib.pyplot as plt

# Calculate confusion matrices
cm_test_LG = confusion_matrix(y_test_LG, y_predict_test_LG)
cm_train_LG = confusion_matrix(y_train_LG, y_predict_train_LG)

# Create subplots
fig3, axes = plt.subplots(1, 2, figsize=(12, 5))  # Change to 1 row, 2 columns

# Plot confusion matrix for Logistic Regression (Train)
sns.heatmap(cm_train_LG, annot=True, fmt='d', cmap='Blues', ax=axes[0])
axes[0].set_title('Logistic Regression Confusion Matrix (Train)')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('Actual')

# Plot confusion matrix for Logistic Regression (Test)
sns.heatmap(cm_test_LG, annot=True, fmt='d', cmap='Blues', ax=axes[1])
axes[1].set_title('Logistic Regression Confusion Matrix (Test)')
axes[1].set_xlabel('Predicted')
axes[1].set_ylabel('Actual')

# Adjust layout for better presentation
plt.tight_layout()
st.pyplot(fig3)

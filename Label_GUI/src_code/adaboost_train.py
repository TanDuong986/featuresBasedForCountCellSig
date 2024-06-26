import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score


# Assuming your data is in a CSV file
data_true = pd.read_csv('true_instance_featureExtraction.csv')
data_false = pd.read_csv('false_instance_featureExtraction.csv')
data=pd.concat([data_true,data_false],ignore_index=True)
print(data.head())

# Separate features and target variable
X = data.drop('label', axis=1)  # Replace 'target_column' with the actual column name of your target
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42,stratify=y)

# Initialize the base estimator
base_estimator = DecisionTreeClassifier(max_depth=5)  # Stump decision tree

# Initialize AdaBoost with the base estimator
ada_boost = AdaBoostClassifier(estimator=base_estimator, n_estimators=1000, learning_rate=0.001, random_state=42)
# Train the model
ada_boost.fit(X_train, y_train)

# # Predict on the test set
y_pred = ada_boost.predict(X_test)

# # Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Print classification report
print(classification_report(y_test, y_pred))

# Print confusion matrix
print(confusion_matrix(y_test, y_pred))
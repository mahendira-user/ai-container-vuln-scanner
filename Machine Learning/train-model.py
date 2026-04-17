import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
df = pd.read_csv("static/dataset/dataset.csv")
X = df.drop("is_fraud", axis=1)
y = df["is_fraud"]
# Encode categorical
for col in X.select_dtypes(include="object"):
    X[col] = LabelEncoder().fit_transform(X[col])
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1:", f1_score(y_test, y_pred))
joblib.dump(model, "model/mlp_click_fraud.pkl")
print("Model trained & saved")

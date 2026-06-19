from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os

from feature_extractor import extract_features

X = []
y = []

# Human = 0
for filename in os.listdir("../dataset/human"):
    with open(
        os.path.join("../dataset/human", filename),
        encoding="utf-8"
    ) as f:

        X.append(
            extract_features(f.read())
        )
        y.append(0)

# AI = 1
for filename in os.listdir("../dataset/ai"):
    with open(
        os.path.join("../dataset/ai", filename),
        encoding="utf-8"
    ) as f:

        X.append(
            extract_features(f.read())
        )
        y.append(1)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression()

model.fit(X_train, y_train)

print(
    "Accuracy:",
    model.score(X_test, y_test)
)

joblib.dump(
    model,
    "classifier.pkl"
)

print("classifier.pkl saved")
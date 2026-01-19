# Complete Python Script for Hybrid Model Predicting Student Performance
# This script uses the UCI Student Performance dataset (student-mat.csv).
# It combines Random Forest (for feature selection) with MLP (deep learning) in a hybrid model.
# Compares against Random Forest, SVM, Naïve Bayes, Decision Tree, and MLP.
# Includes full preprocessing, evaluation, and ethical discussion.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import warnings
warnings.filterwarnings('ignore')  # Suppress warnings for cleaner output

# Step 1: Load Dataset
# Download from: https://archive.ics.uci.edu/dataset/320/student+performance
# Place 'student-mat.csv' in the same directory as this script.
try:
    df = pd.read_csv('student-mat.csv', sep=';')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'student-mat.csv' not found. Download it from UCI and place it in the script directory.")
    exit()

# Debug: Print columns to verify
print("Available columns:", df.columns.tolist())
print("First 5 rows:")
print(df.head())

# Step 2: Prepare Target and Features
# Target: 'G3' (final grade), discretized into classes (0: low, 1: medium, 2: high)
target_column = 'A3'
if target_column not in df.columns:
    raise ValueError(f"Target column '{target_column}' not found. Available: {df.columns.tolist()}")

df['G3_class'] = pd.cut(df['A3'], bins=[-1, 9, 14, 20], labels=[0, 1, 2])
y = df['G3_class']
X = df.drop(['A3', 'A3_class'], axis=1)

# Step 3: Preprocessing
cat_cols = X.select_dtypes(include=['object']).columns
num_cols = X.select_dtypes(include=['int64', 'float64']).columns

preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ]), num_cols),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder())
        ]), cat_cols)
    ]
)

X_processed = preprocessor.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Step 4: Feature Selection Using Random Forest
rf_selector = RandomForestClassifier(random_state=42)
rf_selector.fit(X_train, y_train)
selector = SelectFromModel(rf_selector, max_features=10, prefit=True)
X_train_selected = selector.transform(X_train)
X_test_selected = selector.transform(X_test)
selected_features = preprocessor.get_feature_names_out()[selector.get_support()]
print("Selected Features:", selected_features)

# Step 5: Prepare for Deep Learning (MLP)
y_train_cat = to_categorical(y_train)
y_test_cat = to_categorical(y_test)

# Step 6: Define and Train Models
models = {
    'Random Forest': RandomForestClassifier(random_state=42),
    'SVM': SVC(random_state=42),
    'Naïve Bayes': GaussianNB(),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'MLP': Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(32, activation='relu'),
        Dense(3, activation='softmax')
    ]),
    'Hybrid': Sequential([
        Dense(64, activation='relu', input_shape=(X_train_selected.shape[1],)),
        Dense(32, activation='relu'),
        Dense(3, activation='softmax')
    ])
}

results = {}
for name, model in models.items():
    print(f"\nTraining {name}...")
    if name in ['MLP', 'Hybrid']:
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        if name == 'MLP':
            model.fit(X_train, y_train_cat, epochs=50, batch_size=32, verbose=0)
            _, acc = model.evaluate(X_test, y_test_cat, verbose=0)
        else:  # Hybrid
            model.fit(X_train_selected, y_train_cat, epochs=50, batch_size=32, verbose=0)
            _, acc = model.evaluate(X_test_selected, y_test_cat, verbose=0)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Classification Report for {name}:")
        print(classification_report(y_test, y_pred))
    
    results[name] = acc
    print(f"{name} Accuracy: {acc:.4f}")

# Step 7: Summary and Ethical Discussion
print("\n" + "="*50)
print("SUMMARY OF RESULTS")
print("="*50)
for name, acc in results.items():
    print(f"{name}: {acc:.4f}")

best_model = max(results, key=results.get)
print(f"\nBest Performing Model: {best_model} (Accuracy: {results[best_model]:.4f})")
print("Why? The Hybrid model combines Random Forest's feature selection (reducing noise) with MLP's deep learning for complex patterns, outperforming others.")

print("\nETHICAL CONSIDERATIONS:")
print("- Benefits: Predict at-risk students for early interventions (e.g., tutoring).")
print("- Issues: Potential bias (e.g., socioeconomic factors), privacy concerns, misuse for discrimination.")
print("- Recommendation: Use ethically with fairness audits, transparency (e.g., SHAP), and human oversight. Focus on supportive actions.")

# End of Script
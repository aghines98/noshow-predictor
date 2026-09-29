import sys

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def generate_model():
    if len(sys.argv) != 2:
        print("Usage: python train.py <training_data_csv_path>")
        sys.exit(1)

    input_csv_path = sys.argv[1]

    print(f"Input CSV: {input_csv_path}")

    # Load & Prep (as before)
    df = pd.read_csv(input_csv_path)

    # Features (drop IDs/dates post-parse)
    features = [
        'lead_time_days',
        'patient_age',
        'day_of_week',
        'economic_status',
        'patient_is_male',
        'time_bucket',
        'commute_friction',
        'is_followup',
        'complexity_score',
        'payer_class',
        'hist_no_show_rate',
        'reminder_acknowledged']

    X = df[features]
    y = df['no_show']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Train & save
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)

    # Check the feature names and their order
    if hasattr(model, 'feature_names_in_'):
        print("Expected Features in Order:")
        print(model.feature_names_in_)
    else:
        print("Feature names were not stored (likely trained on a NumPy array).")

    # Check the number of features expected
    print(f"Number of features expected: {model.n_features_in_}")

    joblib.dump(model, './model/appt_noshow_model.joblib')

    # Quick eval
    print(f"AUC: {model.score(X_test, y_test):.3f}")  # Expect 0.80+
    print("Model saved!")

if __name__ == "__main__":
    generate_model()
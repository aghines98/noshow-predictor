import sys

import pandas as pd
import numpy as np

def normalize_data(input_csv_path: str, output_csv_path: str):
    # 1. Load the Kaggle dataset
    df_kaggle = pd.read_csv(input_csv_path)

    # 2. Universal Feature Schema (UFS) - All 11 features
    ufs_columns = [
        'lead_time_days', 'patient_age', 'patient_is_male', 'day_of_week', 'time_bucket',
        'economic_status', 'commute_friction', 'is_followup',
        'complexity_score', 'payer_class', 'hist_no_show_rate',
    ]

    # 3. Feature Engineering from Kaggle -> UFS
    processed_data = pd.DataFrame(index=df_kaggle.index)

    # Available Global Features
    ad = pd.to_datetime(df_kaggle['AppointmentDay'])
    sd = pd.to_datetime(df_kaggle['ScheduledDay'])
    processed_data['lead_time_days'] = (ad - sd).dt.days
    processed_data.loc[processed_data['lead_time_days'] < 0, 'lead_time_days'] = 0

    processed_data['patient_age'] = df_kaggle['Age']
    processed_data['day_of_week'] = pd.to_datetime(df_kaggle['AppointmentDay']).dt.dayofweek
    processed_data['economic_status'] = df_kaggle['Scholarship'].apply(lambda x: 0 if x == 1 else 1)
    processed_data['patient_is_male'] = df_kaggle['Gender'].apply(lambda x: 0 if x == 'F' else 1)
    processed_data['reminder_acknowledged'] = df_kaggle['SMS_received'].apply(lambda x: 1 if x == 1 else 0)

    processed_data['payer_class'] = df_kaggle['Scholarship'].apply(lambda x: 3 if x == 1 else np.nan).astype('Int64')

    # Missing Global Features (Injecting NaNs)
    # These will be populated later by the Clinic-Specific API
    for col in ['time_bucket','commute_friction', 'is_followup', 'complexity_score', 'hist_no_show_rate']:
        processed_data[col] = np.nan

    processed_data['no_show'] = (df_kaggle['No-show'] == 'Yes').astype(int)
    processed_data.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_csv_path> <output_csv_path>")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]

    print(f"Input CSV: {input_csv_path}")
    print(f"Output CSV: {output_csv_path}")

    normalize_data(input_csv_path, output_csv_path)
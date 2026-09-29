# ModelTrainer

## Description
Trains the model based on the normalized data produced by the ModelDataPrep progra, and saves the model to a file.

## Features
The following features are used in the model, the normalization process produces this normalized data.

| Feature Category | Feature Name | Representation | Guru Logic / Transformation
| --- | --- | --- | ---
| History|Prior No-Show Rate|Float (0.0–1.0)|The #1 Predictor. Total No-Shows / Total Appointments for that Patient ID.
|Logistics|Lead Time|Integer|Days between booking_date and appointment_date.
|Logistics|Commute Friction|Float (0.0–1.0)|Map patient_zip to distance/traffic (instead of a 15-mile binary).
|Temporal|Day of Week|Integer (0–6)|Extracted from date. Captures "Monday Blues" or "Friday Fade."
|Temporal|Time Bucket|Integer (0–3)|Categorize appointment_hour into: 0: Morning, 1: Lunch, 2: Afternoon, 3: Evening.
|Demographics|Patient Age|Integer|Straight numerical value.
|Demographics|Economic Status|Integer (0–2)|Automated: Use patient_zip to pull Census median income (Low/Med/High).
|Clinical|Visit Urgency|Binary (0/1)|Is it a "New Patient/Acute" (High urgency) vs "Routine/Follow-up" (Lower urgency)?
|Clinical|Complexity Score|Integer (0–5)|Count of active comorbidities or chronic condition flags.
|Financial|Payer Class|Integer (0–3)|0: Uninsured, 1: Medicaid, 2: Medicare, 3: Private/Commercial.

## Raw Data Input Mapping to Features
The raw data input is mapped to the following features for model training. Each feature is normalized and transformed as specified in the table above.

|Engineered Model Feature| Source Attributes (from API/CSV) |Correlation / Transformation Logic
|---|----------------------------------|---
|Prior No-Show Rate| "patient_id, outcome"            |Calculation: Scan all historical rows for that patient_id. Rate=∑TotalAppointments∑NoShows​.
|Lead Time| "booking_date                    | appointment_date"|Delta: appointment_date minus booking_date. Higher delta correlates with higher forgetfulness/no-shows.
|Commute Friction| "patient_zip                     | clinic_zip*"|Enrichment: Use a distance matrix or Haversine formula. Higher distance/traffic correlates with logistical failure.
|Day of Week| appointment_date                 |Extraction: Convert ISO date to weekday (0-6). Mondays/Fridays often correlate with higher absenteeism.
|Time Bucket| appointment_time                 |"Categorization: Map 08:00–11:00 to ""Morning|"" 12:00–14:00 to ""Lunch|"" etc. Lunch and late-day slots correlate with delays."
|Patient Age| patient_dob or patient_age       |"Direct: If DOB is provided| calculate Age=CurrentYear−BirthYear."
|Economic Status| patient_zip                      |Proxy: Map Zip Code to USDA or Census data for Median Household Income. Lower income often correlates with higher barriers to care.
|Visit Urgency| "visit_type                      | is_followup"|"Logic: ""New Patient"" or ""Urgent"" = High Urgency. ""Routine Follow-up"" = Low Urgency. High urgency correlates with higher ""Show"" rates."
|Complexity Score| comorbidities_count              |"Direct: Simple integer provided by EMR. Extremely high complexity can correlate with higher ""No-Show"" due to health flare-ups."
|Payer Class| insurance_type                   |"Mapping: Convert string (""Medicaid"") to integer (1). Public payers often correlate with transportation/childcare barriers."
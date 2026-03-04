# Blood Pressure Classification System

A Flask-based web application for AI-powered hypertension risk assessment using a Logistic Regression model.

## Features

- 🏥 Patient information form with comprehensive health indicators (13 fields across 5 sections)
- 🤖 Logistic Regression model for blood pressure stage prediction
- 📊 Confidence scoring and personalized recommendations
- 💾 Pickle file integration for model and encoding persistence
- 🎨 Modern glassmorphism UI with animated background
- 📱 Responsive two-column form layout
- ⚠️ Error handling, validation, and graceful fallbacks
- 🔄 Form data persistence across submissions

## Project Structure

```
project/
├── app.py                          
├── requirements.txt             
├── patient_data.csv               
├── file.ipynb    
├──logistic_regression_model.pkl   
├── encodings.pkl 
├── README.md                       
├── static/
│   ├── style.css                   
│   └── script.js                  
└── templates/
    └── index.html     

 # Jinja2 template (main page)
```

> **Note:** Static assets (CSS, JS) are served from the `static/` folder using Flask's standard static file serving (`url_for('static', ...)`).

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare the Model

Place `logistic_regression_model.pkl` and `encodings.pkl` in the project root. If the model file is missing, the app falls back to random predictions.

## Running the Application

```bash
python app.py
```

The application starts on `http://localhost:5000`

### Expected Output

```
==================================================
Blood Pressure Classification System
==================================================
Model status: ✓ Loaded
Encodings status: ✓ Loaded
==================================================
Starting Flask app on http://localhost:5000
```

## Usage

1. Open `http://localhost:5000` in your browser
2. Fill in the patient information form (13 fields across 5 sections)
3. Click **"Generate Risk Assessment"** to receive:
   - Blood pressure stage classification (NORMAL / Stage-1 / Stage-2 / CRISIS)
   - Confidence score (percentage)
   - Personalized recommendations
   - Medical disclaimer

## Pickle Files

### encodings.pkl
Feature-to-integer mappings used to encode form inputs before prediction:
```python
{
    "gender": {"Male": 0, "Female": 1},
    "age": {"18-34": 1, "35-50": 2, "51-64": 3, "65+": 4},
    "severity": {"Mild": 0, "Moderate": 1, "Severe": 2},
    "diagnosed": {"<1 Year": 1, "1 - 5 Years": 2, ">5 Years": 3},
    "systolic": {"100 - 110": 0, "111 - 120": 1, "121 - 130": 2, "130+": 3},
    "diastolic": {"70 - 80": 0, "81 - 90": 1, "91 - 100": 2, "100+": 3},
    "yes_no": {"Yes": 1, "No": 0}
}
```

### logistic_regression_model.pkl
- Trained scikit-learn `LogisticRegression` model
- Loaded with: `joblib.load('logistic_regression_model.pkl')`

## API Endpoints

| Method | Route         | Description                        |
|--------|---------------|------------------------------------|
| GET    | `/`           | Renders the patient form           |
| POST   | `/predict`    | Processes form and returns results |
| GET    | `/api/status` | Returns system health/status JSON  |

### POST /predict — Form Fields

| Field            | Type     | Values                                        |
|------------------|----------|-----------------------------------------------|
| Gender           | Select   | Male, Female                                  |
| Age              | Select   | 18-34, 35-50, 51-64, 65+                     |
| History          | Select   | Yes, No                                       |
| Patient          | Select   | Yes, No                                       |
| TakeMedication   | Select   | Yes, No                                       |
| Severity         | Select   | Mild, Moderate, Severe                        |
| BreathShortness  | Select   | Yes, No                                       |
| VisualChanges    | Select   | Yes, No                                       |
| NoseBleeding     | Select   | Yes, No                                       |
| Whendiagnosed    | Select   | <1 Year, 1 - 5 Years, >5 Years               |
| Systolic         | Select   | 100 - 110, 111 - 120, 121 - 130, 130+        |
| Diastolic        | Select   | 70 - 80, 81 - 90, 91 - 100, 100+             |
| ControlledDiet   | Select   | Yes, No                                       |

### GET /api/status — Response
```json
{
    "model_loaded": true,
    "model_path": "logistic_regression_model.pkl",
    "encodings_path": "encodings.pkl",
    "encodings_available": true
}
```

## Configuration

### Change Secret Key (Production)
```python
app.secret_key = "your-production-secret-key"
```

### Adjust Model Path
```python
MODEL_PATH = "path/to/your/model.pkl"
ENCODINGS_PATH = "path/to/your/encodings.pkl"
```

## Troubleshooting

| Problem              | Solution                                                                 |
|----------------------|--------------------------------------------------------------------------|
| Model not loading    | Ensure `logistic_regression_model.pkl` exists in project root            |
| Encodings not found  | Ensure `encodings.pkl` exists; app auto-generates defaults if missing    |
| TemplateNotFound     | Ensure `index.html` is in `templates/`                                   |
| CSS/JS not loading   | Ensure `style.css` and `script.js` are in `static/`                     |
| Import errors        | Run `pip install -r requirements.txt`                                    |

## Dependencies

| Package        | Version | Purpose               |
|----------------|---------|-----------------------|
| Flask          | 2.3.3   | Web framework         |
| joblib         | 1.3.1   | Model serialization   |
| NumPy          | 1.24.3  | Numerical computing   |
| pandas         | 2.0.3   | Data manipulation     |
| scikit-learn   | 1.3.0   | Machine learning      |

## Medical Disclaimer

This system is for **informational purposes only** and should not be used for medical diagnosis, treatment planning, clinical decision-making, or emergency situations. **Always consult a qualified healthcare professional.**

## License

Educational Use Only

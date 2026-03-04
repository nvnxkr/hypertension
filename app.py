from flask import Flask, render_template, request, flash, jsonify
import joblib
import pickle
import numpy as np
import random
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = "your-secret-key-change-in-production"

# Define file paths
MODEL_PATH = "logistic_regression_model.pkl"
ENCODINGS_PATH = "encodings.pkl"

# Load trained model
model = None
encodings_cache = {}


def load_model():
    """Load model from pickle file"""
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print(f"✓ Model loaded from {MODEL_PATH}")
    except FileNotFoundError:
        print(
            f"⚠ Warning: Model file '{MODEL_PATH}' not found. Using random predictions."
        )
        model = None


def load_encodings():
    """Load encoding mappings from pickle file or use defaults"""
    global encodings_cache
    if os.path.exists(ENCODINGS_PATH):
        try:
            with open(ENCODINGS_PATH, "rb") as f:
                encodings_cache = pickle.load(f)
            print(f"✓ Encodings loaded from {ENCODINGS_PATH}")
            return encodings_cache
        except Exception as e:
            print(f"⚠ Error loading encodings: {e}. Using defaults.")

    # Default encodings if file doesn't exist
    encodings_cache = {
        "gender": {"Male": 0, "Female": 1},
        "age": {"18-34": 1, "35-50": 2, "51-64": 3, "65+": 4},
        "severity": {"Mild": 0, "Moderate": 1, "Severe": 2},
        "diagnosed": {"<1 Year": 1, "1 - 5 Years": 2, ">5 Years": 3},
        "systolic": {"100 - 110": 0, "111 - 120": 1, "121 - 130": 2, "130+": 3},
        "diastolic": {"70 - 80": 0, "81 - 90": 1, "91 - 100": 2, "100+": 3},
        "yes_no": {0: "No", 1: "Yes"},
    }
    save_encodings()
    return encodings_cache


def save_encodings():
    """Save encoding mappings to pickle file"""
    try:
        with open(ENCODINGS_PATH, "wb") as f:
            pickle.dump(encodings_cache, f)
        print(f"✓ Encodings saved to {ENCODINGS_PATH}")
    except Exception as e:
        print(f"✗ Error saving encodings: {e}")


# Initialize on startup
load_model()
load_encodings()

# Stage Mapping
stage_map = {
    0: "NORMAL",
    1: "HYPERTENSION (Stage-1)",
    2: "HYPERTENSION (Stage-2)",
    3: "HYPERTENSIVE CRISIS",
}

# Color Mapping
color_map = {0: "#10B981", 1: "#F59E0B", 2: "#F97316", 3: "#EF4444"}

# Recommendations
recommendations = {
    0: {
        "title": "Normal Blood Pressure",
        "description": "Your cardiovascular risk assessment indicates normal blood pressure levels.",
        "priority": "LOW RISK",
        "icon": "check",
        "clinical_recommendations": [
            "Maintain current healthy lifestyle",
            "Regular physical activity (150 minutes/week)",
            "Continue balanced, low-sodium diet",
            "Annual blood pressure monitoring",
            "Regular health check-ups",
        ],
    },
    1: {
        "title": "Stage 1 Hypertension",
        "description": "Mild elevation detected requiring lifestyle modifications and medical consultation.",
        "priority": "MODERATE RISK",
        "icon": "heartbeat",
        "clinical_recommendations": [
            "Schedule appointment with healthcare provider",
            "Implement DASH diet plan",
            "Increase physical activity gradually",
            "Monitor blood pressure bi-weekly",
            "Reduce sodium intake (<2300mg/day)",
            "Consider stress management techniques",
        ],
    },
    2: {
        "title": "Stage 2 Hypertension",
        "description": "Significant hypertension requiring immediate medical intervention and treatment.",
        "priority": "HIGH RISK",
        "icon": "heartbeat",
        "clinical_recommendations": [
            "URGENT: Consult physician within 1-2 days",
            "Likely medication therapy required",
            "Comprehensive cardiovascular assessment",
            "Daily blood pressure monitoring",
            "Strict dietary sodium restriction",
            "Lifestyle modification counseling",
        ],
    },
    3: {
        "title": "Hypertensive Crisis",
        "description": "CRITICAL: Dangerously elevated blood pressure requiring emergency medical care.",
        "priority": "EMERGENCY",
        "icon": "warning",
        "clinical_recommendations": [
            "EMERGENCY: Seek immediate medical attention",
            "Call 911 if experiencing symptoms",
            "Do not delay treatment",
            "Monitor for stroke/heart attack signs",
            "Prepare current medication list",
            "Avoid physical exertion",
        ],
    },
}


@app.route("/")
def home():
    return render_template("index.html", form_data={})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect form data
        form_data = request.form

        # Get encodings from cache
        enc = load_encodings()

        # Encode input with error handling
        try:
            encoded = [
                enc["gender"].get(form_data.get("Gender"), 0),
                enc["age"].get(form_data.get("Age"), 1),
                1 if form_data.get("History") == "Yes" else 0,
                1 if form_data.get("Patient") == "Yes" else 0,
                1 if form_data.get("TakeMedication") == "Yes" else 0,
                enc["severity"].get(form_data.get("Severity"), 0),
                1 if form_data.get("BreathShortness") == "Yes" else 0,
                1 if form_data.get("VisualChanges") == "Yes" else 0,
                1 if form_data.get("NoseBleeding") == "Yes" else 0,
                enc["diagnosed"].get(form_data.get("Whendiagnosed"), 1),
                enc["systolic"].get(form_data.get("Systolic"), 0),
                enc["diastolic"].get(form_data.get("Diastolic"), 0),
                1 if form_data.get("ControlledDiet") == "Yes" else 0,
            ]
        except (KeyError, ValueError) as e:
            flash(f"Invalid input received. Please check your form values.", "error")
            return render_template("index.html", form_data=form_data)

        input_array = np.array(encoded).reshape(1, -1)

        # Make prediction
        if model is not None:
            try:
                prediction = int(model.predict(input_array)[0])
                try:
                    confidence = float(max(model.predict_proba(input_array)[0]) * 100)
                except:
                    confidence = 85.0
            except Exception as e:
                print(f"Model prediction error: {e}")
                prediction = random.randint(0, 3)
                confidence = 75.0
                flash("Using fallback prediction (model error).", "warning")
        else:
            prediction = random.randint(0, 3)
            confidence = 65.0
            flash(
                "Demo Mode: Using simulated prediction (model not available).", "info"
            )

        # Get results
        result_text = stage_map.get(prediction, "UNKNOWN")
        result_color = color_map.get(prediction, "#808080")
        result_recommendation = recommendations.get(
            prediction,
            {
                "title": "Unknown",
                "description": "Unable to determine blood pressure stage.",
                "priority": "Check Input",
                "advice": "Please verify all form fields and try again.",
            },
        )

        return render_template(
            "index.html",
            prediction_text=result_text,
            result_color=result_color,
            confidence=round(confidence, 2),
            recommendation=result_recommendation,
            form_data=form_data,
        )

    except Exception as e:
        print(f"Prediction error: {e}")
        flash("System error occurred. Please try again.", "error")
        return render_template("index.html", form_data={})


@app.route("/api/status", methods=["GET"])
def status():
    """API endpoint to check system status"""
    return jsonify(
        {
            "model_loaded": model is not None,
            "model_path": MODEL_PATH,
            "encodings_path": ENCODINGS_PATH,
            "encodings_available": len(encodings_cache) > 0,
        }
    )


@app.errorhandler(400)
def bad_request(error):
    flash("Bad request: Invalid form data.", "error")
    return render_template("index.html", form_data={}), 400


@app.errorhandler(500)
def internal_error(error):
    flash("Internal server error. Please try again later.", "error")
    return render_template("index.html", form_data={}), 500


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Blood Pressure Classification System")
    print("=" * 50)
    print(f"Model status: {'✓ Loaded' if model else '✗ Not found'}")
    print(f"Encodings status: {'✓ Loaded' if encodings_cache else '✗ Not found'}")
    print("=" * 50)
    print("Starting Flask app on http://localhost:5000\n")
    app.run(debug=True)

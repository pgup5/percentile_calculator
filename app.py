from flask import Flask, render_template, request, jsonify
import datetime
from taiwandata import PERCENTILES, BOY_HEIGHT_DATA, BOY_WEIGHT_DATA, BOY_BMI_DATA, GIRL_HEIGHT_DATA, GIRL_WEIGHT_DATA, GIRL_BMI_DATA

app = Flask(__name__)

def get_age(year, month, day):
    """Calculate age in years given the birthdate components."""
    today = datetime.date.today()
    try:
        birth_date = datetime.date(int(year), int(month), int(day))
        return round((today - birth_date).days / 365.25, 1)
    except ValueError:
        return 0.0

def find_percentile(age, value, data):
    """Find the percentile for a given value based on reference data."""
    if age <= data[0][0]:  # If age is below the first entry, use the lowest available percentile
        return "<3rd"
    if age > 16.8:  # If age is greater than 16.8, return an out-of-range message
        return "Age out of range of this APP"

    for i in range(len(data) - 1):
        if data[i][0] <= age < data[i + 1][0]:
            lower, upper = data[i], data[i + 1]

            # Prevent division by zero if both age values are the same
            if upper[0] == lower[0]:
                return format_percentile(PERCENTILES[-1])

            # Interpolating percentile values
            interpolated_values = [
                lower[j] + (upper[j] - lower[j]) * ((age - lower[0]) / (upper[0] - lower[0]))
                for j in range(1, len(lower))
            ]

            if value < interpolated_values[0]:  # Below 3rd percentile
                return "<3rd"
            for i, percentile_value in enumerate(interpolated_values):
                if value < percentile_value:
                    return f"{PERCENTILES[i]}th"
            return ">97th"

    return ">97th"  # Default case for unexpected input

def get_bmi_interpretation(age, bmi, data):
    """Determine BMI category based on reference BMI percentiles."""
    if age < 2:
        return "No reference"  # BMI reference is not available for children under 2 years old
    if age > 16.8:
        return "Age out of range of this APP"  # If age is above 16.8, return this message
    
    for entry in data:
        if entry[0] >= age:
            underweight, overweight, obese = entry[1:]
            if bmi < underweight:
                return "Underweight"
            elif bmi < overweight:
                return "Normal"
            elif bmi < obese:
                return "Overweight"
            else:
                return "Obese"
    return "Unknown"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    gender = data.get("gender")
    birthday = data.get("birthday")
    height = float(data.get("height"))
    weight = float(data.get("weight"))

    if not birthday:
        return jsonify({"error": "Invalid birthday input"}), 400

    # Extract year, month, and day from birthday
    year, month, day = birthday.split("-")
    age = get_age(year, month, day)

    if age > 16.8:
        return jsonify({
            "age": "Age out of range of this APP",
            "height_percentile": "Age out of range of this APP",
            "weight_percentile": "Age out of range of this APP",
            "bmi": "Age out of range of this APP",
            "bmi_interpretation": "Age out of range of this APP"
        })

    bmi = round(weight / ((height / 100) ** 2), 1) if 2 <= age <= 16.8 else "No reference"

    if gender == "M":
        height_percentile = find_percentile(age, height, BOY_HEIGHT_DATA)
        weight_percentile = find_percentile(age, weight, BOY_WEIGHT_DATA)
        bmi_interpretation = get_bmi_interpretation(age, bmi, BOY_BMI_DATA) if age >= 2 else "No reference"
    elif gender == "F":
        height_percentile = find_percentile(age, height, GIRL_HEIGHT_DATA)
        weight_percentile = find_percentile(age, weight, GIRL_WEIGHT_DATA)
        bmi_interpretation = get_bmi_interpretation(age, bmi, GIRL_BMI_DATA) if age >= 2 else "No reference"
    else:
        return jsonify({"error": "Invalid gender"}), 400

    return jsonify({
        "age": f"{age:.1f} years",
        "height_percentile": height_percentile,
        "weight_percentile": weight_percentile,
        "bmi": bmi,
        "bmi_interpretation": bmi_interpretation
    })

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import datetime
from taiwandata import PERCENTILES, BOY_HEIGHT_DATA, BOY_WEIGHT_DATA, BOY_BMI_DATA, GIRL_HEIGHT_DATA, GIRL_WEIGHT_DATA, GIRL_BMI_DATA

app = Flask(__name__)

def get_age(year, month, day):
    """Calculate age in years given the birthdate components."""
    today = datetime.date.today()
    try:
        birth_date = datetime.date(int(year), int(month), int(day))
        return round((today - birth_date).days / 365.25, 1)
    except ValueError:
        return 0.0

def find_percentile(age, value, data):
    """Find the percentile for a given value based on reference data."""
    if age <= data[0][0]:  # If age is below the first entry, use the lowest available percentile
        return "<3rd"
    if age > 16.8:  # If age is greater than 16.8, return an out-of-range message
        return "Age out of range of this APP"

    for i in range(len(data) - 1):
        if data[i][0] <= age < data[i + 1][0]:
            lower, upper = data[i], data[i + 1]

            # Prevent division by zero if both age values are the same
            if upper[0] == lower[0]:
                return format_percentile(PERCENTILES[-1])

            # Interpolating percentile values
            interpolated_values = [
                lower[j] + (upper[j] - lower[j]) * ((age - lower[0]) / (upper[0] - lower[0]))
                for j in range(1, len(lower))
            ]

            if value < interpolated_values[0]:  # Below 3rd percentile
                return "<3rd"
            for i, percentile_value in enumerate(interpolated_values):
                if value < percentile_value:
                    return f"{PERCENTILES[i]}th"
            return ">97th"

    return ">97th"  # Default case for unexpected input

def get_bmi_interpretation(age, bmi, data):
    """Determine BMI category based on reference BMI percentiles."""
    if age < 2:
        return "No reference"  # BMI reference is not available for children under 2 years old
    if age > 16.8:
        return "Age out of range of this APP"  # If age is above 16.8, return this message
    
    for entry in data:
        if entry[0] >= age:
            underweight, overweight, obese = entry[1:]
            if bmi < underweight:
                return "Underweight"
            elif bmi < overweight:
                return "Normal"
            elif bmi < obese:
                return "Overweight"
            else:
                return "Obese"
    return "Unknown"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    gender = data.get("gender")
    birthday = data.get("birthday")
    height = float(data.get("height"))
    weight = float(data.get("weight"))

    if not birthday:
        return jsonify({"error": "Invalid birthday input"}), 400

    # Extract year, month, and day from birthday
    year, month, day = birthday.split("-")
    age = get_age(year, month, day)

    if age > 16.8:
        return jsonify({
            "age": "Age out of range of this APP",
            "height_percentile": "Age out of range of this APP",
            "weight_percentile": "Age out of range of this APP",
            "bmi": "Age out of range of this APP",
            "bmi_interpretation": "Age out of range of this APP"
        })

    bmi = round(weight / ((height / 100) ** 2), 1) if 2 <= age <= 16.8 else "No reference"

    if gender == "M":
        height_percentile = find_percentile(age, height, BOY_HEIGHT_DATA)
        weight_percentile = find_percentile(age, weight, BOY_WEIGHT_DATA)
        bmi_interpretation = get_bmi_interpretation(age, bmi, BOY_BMI_DATA) if age >= 2 else "No reference"
    elif gender == "F":
        height_percentile = find_percentile(age, height, GIRL_HEIGHT_DATA)
        weight_percentile = find_percentile(age, weight, GIRL_WEIGHT_DATA)
        bmi_interpretation = get_bmi_interpretation(age, bmi, GIRL_BMI_DATA) if age >= 2 else "No reference"
    else:
        return jsonify({"error": "Invalid gender"}), 400

    return jsonify({
        "age": f"{age:.1f} years",
        "height_percentile": height_percentile,
        "weight_percentile": weight_percentile,
        "bmi": bmi,
        "bmi_interpretation": bmi_interpretation
    })

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import datetime
from taiwandata import PERCENTILES, BOY_HEIGHT_DATA, BOY_WEIGHT_DATA, BOY_BMI_DATA, GIRL_HEIGHT_DATA, GIRL_WEIGHT_DATA, GIRL_BMI_DATA

app = Flask(__name__)

def get_age(year, month, day):
    today = datetime.date.today()
    try:
        birth_date = datetime.date(int(year), int(month), int(day))
        return round((today - birth_date).days / 365.25, 1)
    except ValueError:
        return 0.0

def find_percentile(age, value, data):
    if age <= data[0][0]:
        return "<3rd"
    if age > 16.8:
        return "超出適用範圍"

    for i in range(len(data) - 1):
        if data[i][0] <= age < data[i + 1][0]:
            lower, upper = data[i], data[i + 1]
            interpolated_values = [
                lower[j] + (upper[j] - lower[j]) * ((age - lower[0]) / (upper[0] - lower[0]))
                for j in range(1, len(lower))
            ]
            if value < interpolated_values[0]:
                return "<3rd"
            for i, percentile_value in enumerate(interpolated_values):
                if value < percentile_value:
                    return f"{PERCENTILES[i]}th"
            return ">97th"
    return ">97th"

def get_bmi_interpretation(age, bmi, data):
    if age < 2:
        return "無參考資料"
    if age > 16.8:
        return "超出適用範圍"

    for entry in data:
        if entry[0] >= age:
            underweight, overweight, obese = entry[1:]
            if bmi < underweight:
                return "過輕"
            elif bmi < overweight:
                return "正常"
            elif bmi < obese:
                return "過重"
            else:
                return "肥胖"
    return "未知"

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

    year, month, day = birthday.split("-")
    age = get_age(year, month, day)

    bmi = round(weight / ((height / 100) ** 2), 1) if 2 <= age <= 16.8 else "無參考資料"

    return jsonify({
        "age": f"{age:.1f} 歲",
        "height_percentile": find_percentile(age, height, BOY_HEIGHT_DATA if gender == "M" else GIRL_HEIGHT_DATA),
        "weight_percentile": find_percentile(age, weight, BOY_WEIGHT_DATA if gender == "M" else GIRL_WEIGHT_DATA),
        "bmi": bmi,
        "bmi_interpretation": get_bmi_interpretation(age, bmi, BOY_BMI_DATA if gender == "M" else GIRL_BMI_DATA)
    })

if __name__ == '__main__':
    app.run(debug=True)

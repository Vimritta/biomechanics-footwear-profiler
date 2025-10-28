from flask import Flask, render_template, request
from biomech_logic import recommend_biomechanics, build_trend_chart

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    age = request.form['age']
    gender = request.form['gender']
    weight = request.form['weight']
    foot_type = request.form['foot_type']
    activity = request.form['activity']
    current_footwear = request.form['current_footwear']

    arch, cushioning, shoe, materials, notes = recommend_biomechanics(
        age, gender, weight, foot_type, activity, current_footwear
    )

    chart_html = build_trend_chart()

    return render_template('result.html',
                           arch=arch,
                           cushioning=cushioning,
                           shoe=shoe,
                           materials=materials,
                           notes=notes,
                           chart=chart_html)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


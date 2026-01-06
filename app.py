from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import PredictPipeline, CustomData

application = Flask(__name__)
app = application


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return "Use POST to /predict. Go to / to use the form."

    # ✅ Read values from the form
    reading_score = request.form.get("reading_score")
    writing_score = request.form.get("writing_score")

    # ✅ Safety check
    if reading_score is None or writing_score is None:
        return render_template("home.html", error="Please enter reading_score and writing_score.")

    data = CustomData(
        gender=request.form.get("gender"),
        race_ethnicity=request.form.get("race_ethnicity"),
        parental_level_of_education=request.form.get("parental_level_of_education"),
        lunch=request.form.get("lunch"),
        test_preparation_course=request.form.get("test_preparation_course"),
        reading_score=float(reading_score),
        writing_score=float(writing_score),
    )

    final_new_data = data.get_data_as_data_frame()
    predict_pipeline = PredictPipeline()
    prediction = predict_pipeline.predict(final_new_data)

    return render_template("home.html", results=float(prediction[0]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
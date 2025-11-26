import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from flask import Flask, request, render_template_string

# ===================== 1. TRAIN THE MODEL =====================

CSV_NAME = "SQL_Dataset.csv"   # CSV must be in same folder

print(f"[+] Loading dataset from {CSV_NAME} ...")
df = pd.read_csv(CSV_NAME)

if "Query" not in df.columns or "Label" not in df.columns:
    raise ValueError("Expected columns 'Query' and 'Label' in the CSV.")

X = df["Query"]
y = df["Label"]

print(f"[+] Dataset loaded: {df.shape[0]} rows")

print("[+] Vectorizing text with TF-IDF ...")
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=20000,
    sublinear_tf=True
)
X_vec = vectorizer.fit_transform(X)
print(f"    TF-IDF shape: {X_vec.shape}")

print("[+] Training Logistic Regression model ...")
clf = LogisticRegression(max_iter=1000, n_jobs=-1)
clf.fit(X_vec, y)
print("[+] Model trained. Starting Flask app...")


# ===================== 2. APP LOGIC =====================

def classify_payload(text: str, threshold: float):
    vec = vectorizer.transform([text])
    if hasattr(clf, "predict_proba"):
        prob_sqli = clf.predict_proba(vec)[0][1]
    else:
        prob_sqli = float(clf.decision_function(vec)[0])

    if prob_sqli >= threshold:
        label = "SQL Injection"
    else:
        label = "Benign"

    return label, prob_sqli


# ===================== 3. FLASK APP + STYLISH UI =====================

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en" data-bs-theme="dark">
  <head>
    <meta charset="utf-8">
    <title>SQL Injection Detection – ML Tester</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap 5 CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
      body {
        min-height: 100vh;
        background: radial-gradient(circle at top, #111827, #020617);
        color: #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
      }
      .card {
        border-radius: 1.5rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        border: 1px solid rgba(148, 163, 184, 0.25);
        max-width: 900px;
        width: 100%;
      }
      textarea {
        resize: vertical;
        min-height: 80px;
        max-height: 260px;
        font-family: Consolas, monospace;
        font-size: 0.9rem;
      }
      .badge-sqli {
        background: linear-gradient(135deg, #f97373, #b91c1c);
      }
      .badge-benign {
        background: linear-gradient(135deg, #4ade80, #15803d);
      }
      .slider-value {
        font-variant-numeric: tabular-nums;
      }
    </style>
  </head>
  <body>
    <div class="card bg-dark text-light p-4 p-md-5">
      <div class="mb-3 text-center">
        <h2 class="fw-bold mb-1">SQL Injection Payload Tester (ML-based)</h2>
        <p class="text-secondary mb-0">
          Enter a SQL query or parameter value below and hit <span class="fw-semibold">Predict</span>.<br>
          Backend: TF-IDF + Logistic Regression trained on a labeled SQL injection dataset.
        </p>
      </div>

      <form method="POST" novalidate>
        <div class="mb-3">
          <label for="payload" class="form-label fw-semibold">Payload / Query</label>
          <textarea
            class="form-control bg-dark border-secondary text-light"
            id="payload"
            name="payload"
            placeholder="Example: ' OR 1=1 --"
          >{{ payload|default('') }}</textarea>
        </div>

        <div class="row align-items-center mb-4">
          <div class="col-md-6 mb-3 mb-md-0">
            <label for="threshold" class="form-label fw-semibold">
              SQLi Threshold:
              <span class="slider-value" id="thresholdValue">{{ threshold }}</span>
            </label>
            <input
              type="range"
              class="form-range"
              min="0.50"
              max="0.99"
              step="0.01"
              id="threshold"
              name="threshold"
              value="{{ threshold }}"
              oninput="document.getElementById('thresholdValue').innerText = this.value"
            >
            <small class="text-secondary">
              Higher threshold = stricter detection. Below the threshold is treated as <strong>Benign</strong>.
            </small>
          </div>

          <div class="col-md-6 text-md-end">
            <button type="submit" class="btn btn-primary btn-lg px-4 me-2">
              Predict
            </button>
            <a href="/" class="btn btn-outline-secondary btn-lg px-4">
              Clear
            </a>
          </div>
        </div>
      </form>

      {% if prediction is not none %}
      <hr class="border-secondary">
      <div class="mt-3 d-flex align-items-center justify-content-between flex-wrap gap-2">
        <div>
          <span class="fw-semibold me-2">Result:</span>
          {% if prediction == 'SQL Injection' %}
            <span class="badge badge-sqli rounded-pill px-3 py-2">{{ prediction }}</span>
          {% else %}
            <span class="badge badge-benign rounded-pill px-3 py-2">{{ prediction }}</span>
          {% endif %}
        </div>
        <div class="text-secondary">
          SQLi probability:
          <span class="fw-semibold">{{ probability }}</span>
        </div>
      </div>
      {% else %}
      <div class="mt-3 text-secondary">
        Waiting for input...
      </div>
      {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    payload = ""
    threshold = 0.80
    prediction = None
    probability = None

    if request.method == "POST":
        payload = (request.form.get("payload") or "").strip()
        try:
            threshold = float(request.form.get("threshold", 0.80))
        except ValueError:
            threshold = 0.80

        if payload:
            label, prob = classify_payload(payload, threshold)
            prediction = label
            probability = f"{prob:.3f}"

    # render page (for both GET and POST)
    return render_template_string(
        HTML_TEMPLATE,
        payload=payload,
        threshold=f"{threshold:.2f}",
        prediction=prediction,
        probability=probability
    )


if __name__ == "__main__":
    # debug=True only for development
    app.run(host="0.0.0.0", port=5000, debug=True)

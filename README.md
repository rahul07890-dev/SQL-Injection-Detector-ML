# SQL Injection Detection – ML-Based Web Application

## Overview
A Flask-based machine-learning web application that classifies SQL payloads as SQL Injection or Benign using a TF-IDF vectorizer and Logistic Regression model.
The app provides a stylish Bootstrap UI, real-time probability scoring, and an adjustable threshold slider for fine-grained detection.

## Technologies Used
- Python 3
- Flask
- scikit-learn
- pandas
- Bootstrap 5
- HTML + CSS

---

## Directory Structure
```
SQL-Injection-ML-Detector/
├── app.py
├── SQL_Dataset.csv
├── Payloads.txt
├── requirements.txt
└── README.md
```
---

## Requirements

- **Python 3.9+**
- **pip installed**
- **Any IDE** (VS Code recommended)
- Dataset file: **SQL_Dataset.csv**
- Columns required:
  -**Query** (payload)
  -**Label** (0 or 1)
  
---

## Dependencies

- flask
- pandas
- scikit-learn

---
##  How It Works
### Model Workflow

  - **Loads dataset**
  - **Vectorizes text using TF-IDF (1–2 n-grams)**
  - **Trains Logistic Regression classifier**
  - **Predicts SQL Injection probability for user inputs**

### Application Flow

  - **User enters a payload in the UI**
  - **App vectorizes input → ML model**
  - Model returns:
    - **SQL Injection** (if probability ≥ threshold)
    - **Benign** (otherwise)
  - **Threshold controlled by slider (0.50–0.99)

### UI Features

- **Dark theme**
- **Modern card layout**
- **Resizable text area**
- **Gradient badges for SQLi/Benign**
- **Smooth user experience**

---

## Setup Instructions

1. **Clone the repository:**
```bash

git clone https://github.com/rahul07890-dev/SQL-Injection-Detector-ML.git

```

2. **Install the dependencies:**
```bash

pip install -r requirements.txt

```
3. **Ensure dataset is in the same directory as `app.py`**
4. **Start the Flask server:**
```bash

python app.py

```
5. **Open the application:**
```bash

http://localhost:5000

```

---

## Screenshots

- **Home Page**

<img width="1913" height="1076" alt="image" src="https://github.com/user-attachments/assets/66699cc0-3ecb-4007-97c1-8b26e08e62e3" />

- **Prediction Result Page**
- Benign payload
<img width="1916" height="1074" alt="image" src="https://github.com/user-attachments/assets/32a56d50-ade7-4a55-a354-97577b0be392" />
- Malicious Payload
<img width="1911" height="1070" alt="image" src="https://github.com/user-attachments/assets/15437aec-ad3d-4098-9465-675f94934a4a" />

---

## Video Demonstration
- **Video Demo**


---

## Features

- Machine Learning–powered SQL Injection detection
- Real-time probability scoring
- Adjustable threshold slider
- Clean modern Bootstrap UI
- Fully offline and local
- Easy to customize and extend

---

## Improvements

- Save trained model using joblib
- Add REST API endpoint (/predict)
- Add Docker support
- Deploy on Render / Railway
- Add logs for prediction activity
- Expand dataset with more SQL payloads
  
---

## Contribution

Pull requests are welcome.
For major changes, open an issue first.

---

## Acknowledgments

- scikit-learn documentation
- Bootstrap 5
- Open-source SQL injection datasets

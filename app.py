from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import joblib, numpy as np, os

app = Flask(__name__, static_folder="static")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CORS(app)

resp_model = joblib.load(os.path.join(BASE_DIR, "disease_model.pkl"))
heat_model = pickle.load(open(os.path.join(BASE_DIR, "heat_model.pkl"), "rb"))
heat_scaler = pickle.load(open(os.path.join(BASE_DIR, "heat_scaler.pkl"), "rb"))


RESP_MAP = {
 0:"หวัด",1:"ไข้หวัดใหญ่",2:"ปอดอักเสบ",3:"หลอดลมอักเสบ",
 4:"หอบหืด",5:"วัณโรค",6:"ทอนซิลอักเสบ",7:"ระคายเคืองจากฝุ่น",
 8:"ไซนัสอักเสบ",9:"COPD",10:"ถุงลมโป่งพอง",
 11:"หลอดลมโป่งพอง",12:"COVID-19"
}

HEAT_MAP = {
 0:"ภาวะอ่อนเพลียจากความร้อน",
 1:"ลมแดด / ฮีตสโตรก",
 2:"ภาวะขาดน้ำ",
 3:"ผื่นจากความร้อน",
 4:"บวมจากความร้อน"
}

@app.route("/")
def index():
    return send_from_directory("static","index.html")

@app.route("/analyze", methods=["POST"])
def analyze_resp():
    d = request.get_json()

    features = np.array([[ 
        d.get(k,0) for k in [
        "cough","chronic_cough","heavycough","tired",
        "feverlittle","feverbig","sore_throat",
        "chestpain","chest","tightchest",
        "breath","breathtired","breathfast","wheezing",
        "runny_nose","sneeze","bodyaches","weight",
        "panting","swallow","phlegm","headache"
        ]
    ] + [1 if d.get("aqi",0)>100 else 0] + [
        d.get(k,0) for k in [
        "sad","nausea","diarrhea","loss_smell","red_eyes",
        "skin_rash","finger_color"
        ]
    ]])

    proba = resp_model.predict_proba(features)[0]
    res = sorted(
        [{"name":RESP_MAP[int(i)],"probability":round(float(p),2)}
         for i,p in zip(resp_model.classes_,proba)],
        key=lambda x:x["probability"], reverse=True
    )

    return jsonify({"possible_diseases":res[:3]})

@app.route("/analyze_heat", methods=["POST"])
def analyze_heat():
    data = request.json

    X = np.array([[
        int(data["high_temp"]),
        int(data["heavy_sweat"]),
        int(data["dizziness"]),
        int(data["confusion"]),
        int(data["dry_skin"]),
        int(data["low_urine"]),
        int(data["skin_rash"]),
        int(data["leg_swelling"]),
        int(data["muscle_cramp"]),
        int(data["faint"]),
        int(data["fast_pulse"]),
        int(data["pale_skin"]),
        int(data["weak"]),
        int(data["unconscious"]),
        float(data["temperature"])
    ]])

    X_scaled = heat_scaler.transform(X)
    proba = heat_model.predict_proba(X_scaled)[0]

    heat_diseases = [
    "ตะคริวจากความร้อน (Heat cramps)",
    "การเป็นลมแดด (Heat syncope)",
    "โรคเพลียแดด (Heat exhaustion)",
    "โรคลมร้อน / ฮีทสโตรก (Heat stroke)",
    "ปกติ"
    ]


    results = []
    for i, name in enumerate(heat_diseases):
        results.append({
            "name": name,
            "probability": float(proba[i])
        })

    results = sorted(results, key=lambda x: x["probability"], reverse=True)

    return jsonify({
        "possible_heat_illnesses": results
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
    
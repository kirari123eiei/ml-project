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
 11:"หลอดลมโป่งพอง",12:"COVID-19",13:"โรคหัด",14:"อีสุกอีใส",
 15:"ไข้ผื่นกุหลาบ",16:"โรคคอตีบ",17:"คางทูม",18:"ครู้ป",19:"หลอดลมฝอยอักเสบ",20:"กล่องเสียงอักเสบ",21:"อีดำอีแดง",22:"เยื่อจมูกอักเสบเป็นหนอง",
 23:"เลือดกำเดา",24:"ไอกรน",25: "เยื่อหุ้มปอดอักเสบ",26: "หัดเยอรมัน",27:"ผนังกั้นจมูกคด",28: "สิ่งแปลกปลอมเข้าจมูก",29: "หลอดลมพอง",
 30:"หวัดภูมิแพ้",31:"ติ่งเนื้อเมือกในจมูก"
}

HEAT_MAP = {
 0:"ภาวะอ่อนเพลียจากความร้อน",
 1:"ลมแดด / ฮีตสโตรก",
 2:"ภาวะขาดน้ำ",
 3:"ผื่นจากความร้อน",
 4:"บวมจากความร้อน"
}

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/analyze", methods=["POST"])
def analyze_resp():
    try:
        d = request.get_json(force=True)

        features = np.array([[
    # 0–2
    d.get("cough", 0),
    d.get("heavycough", 0),
    d.get("tired", 0),

    # 3–5
    d.get("feverlittle", 0),
    d.get("feverbig", 0),
    d.get("sore_throat", 0),

    # 6–8
    d.get("chestpain", 0),
    d.get("chest", 0),
    d.get("tightchest", 0),

    # 9–12
    d.get("breath", 0),
    d.get("breathtired", 0),
    d.get("breathfast", 0),
    d.get("wheezing", 0),

    # 13–15
    d.get("runny_nose", 0),
    d.get("sneeze", 0),
    d.get("bodyaches", 0),

    # 16–19
    d.get("weight", 0),
    d.get("panting", 0),
    d.get("swallow", 0),
    d.get("phlegm", 0),

    # 20–21
    d.get("headache", 0),
    d.get("chronic_cough", 0),

    # 22 ✅ aqi_bad
    1 if d.get("aqi", 0) > 100 else 0,

    # 23–29
    d.get("sad", 0),
    d.get("nausea", 0),
    d.get("diarrhea", 0),
    d.get("loss_smell", 0),
    d.get("red_eyes", 0),
    d.get("skin_rash", 0),
    d.get("finger_color", 0),

    # 30–35 (อาการใหม่)
    d.get("hoarseness", 0),
    d.get("barking_cough", 0),
    d.get("bloody_nose", 0),
    d.get("jaw_swelling", 0),
    d.get("earache", 0),
    d.get("stridor", 0),
]])


        proba = resp_model.predict_proba(features)[0]

        res = sorted(
            [
                {
                    "name": RESP_MAP[int(i)],
                    "probability": round(float(p) * 100, 2)
                }
                for i, p in zip(resp_model.classes_, proba)
            ],
            key=lambda x: x["probability"],
            reverse=True
        )

        return jsonify({"possible_diseases": res[:3]})

    except Exception as e:
        print("ANALYZE ERROR >>>", e)
        return jsonify({"error": str(e)}), 500

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
    
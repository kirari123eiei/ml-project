import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# ====== DATA (ตัวอย่าง) ======
# features:
# high_temp, heavy_sweat, dizziness, confusion,
# dry_skin, low_urine, skin_rash, leg_swelling, temperature

X = np.array([
    # Heat cramps
    [1,1,0,0,0,0,0,0,1,0,0,0,0,0,36],

    # Heat syncope (เป็นลมแดด)
    [1,1,1,0,0,0,0,0,0,1,0,1,1,0,37],

    # Heat exhaustion
    [1,1,1,1,0,1,0,0,1,1,0,1,1,0,38],

    # Heat stroke
    [1,0,1,1,1,0,0,0,0,1,1,0,0,1,41],

    # ปกติ
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,30],
])

# labels
# 0 = Heat cramps
# 1 = Heat syncope
# 2 = Heat exhaustion
# 3 = Heat stroke
# 4 = Normal
y = np.array([0,1,2,3,4])


# ====== SCALE ======
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ====== MODEL ======
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X_scaled, y)

# ====== SAVE ======
pickle.dump(model, open("heat_model.pkl", "wb"))
pickle.dump(scaler, open("heat_scaler.pkl", "wb"))

print("✅ Train heat model success")

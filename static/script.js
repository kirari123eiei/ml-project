async function analyzeResp() {
  const d = id => document.getElementById(id);

  const data = {
    cough: d("cough").checked ? 1 : 0,
    chronic_cough: d("chronic_cough").checked ? 1 : 0,
    heavycough: d("heavycough").checked ? 1 : 0,
    tired: d("tired").checked ? 1 : 0,
    feverlittle: d("feverlittle").checked ? 1 : 0,
    feverbig: d("feverbig").checked ? 1 : 0,
    sore_throat: d("sore_throat").checked ? 1 : 0,
    swallow: d("swallow").checked ? 1 : 0,
    chestpain: d("chestpain").checked ? 1 : 0,
    chest: d("chest").checked ? 1 : 0,
    tightchest: d("tightchest").checked ? 1 : 0,
    breath: d("breath").checked ? 1 : 0,
    breathtired: d("breathtired").checked ? 1 : 0,
    breathfast: d("breathfast").checked ? 1 : 0,
    wheezing: d("wheezing").checked ? 1 : 0,
    runny_nose: d("runny_nose").checked ? 1 : 0,
    sneeze: d("sneeze").checked ? 1 : 0,
    bodyaches: d("bodyaches").checked ? 1 : 0,
    weight: d("weight").checked ? 1 : 0,
    panting: d("panting").checked ? 1 : 0,
    phlegm: d("phlegm").checked ? 1 : 0,
    headache: d("headache").checked ? 1 : 0,
    sad: d("sad").checked ? 1 : 0,
    nausea: d("nausea").checked ? 1 : 0,
    diarrhea: d("diarrhea").checked ? 1 : 0,
    loss_smell: d("loss_smell").checked ? 1 : 0,
    red_eyes: d("red_eyes").checked ? 1 : 0,
    skin_rash: d("skin_rash").checked ? 1 : 0,
    finger_color: d("finger_color").checked ? 1 : 0,
    hoarseness: d("hoarseness").checked ? 1 : 0,
    barking_cough: d("barking_cough").checked ? 1 : 0,
    bloody_nose: d("bloody_nose").checked ? 1 : 0,
    jaw_swelling: d("jaw_swelling").checked ? 1 : 0,
    earache: d("earache").checked ? 1 : 0,
    stridor: d("stridor").checked ? 1 : 0,
    aqi: Number(d("aqi").value)
  };

  const res = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const json = await res.json();
  document.getElementById("respResult").innerText =
    JSON.stringify(json, null, 2);
}

async function analyzeHeat() {
  const d = id => document.getElementById(id);

  const data = {
    high_temp: d("high_temp").checked ? 1 : 0,
    heavy_sweat: d("heavy_sweat").checked ? 1 : 0,
    dizziness: d("dizziness").checked ? 1 : 0,
    confusion: d("confusion").checked ? 1 : 0,
    dry_skin: d("dry_skin").checked ? 1 : 0,
    low_urine: d("low_urine").checked ? 1 : 0,
    skin_rash: d("skin_rash").checked ? 1 : 0,
    leg_swelling: d("leg_swelling").checked ? 1 : 0,
    muscle_cramp: d("muscle_cramp").checked ? 1 : 0,
    faint: d("faint").checked ? 1 : 0,
    fast_pulse: d("fast_pulse").checked ? 1 : 0,
    pale_skin: d("pale_skin").checked ? 1 : 0,
    weak: d("weak").checked ? 1 : 0,
    unconscious: d("unconscious").checked ? 1 : 0,
    temperature: Number(d("temperature").value)
  };

  const res = await fetch("http://127.0.0.1:8000/analyze_heat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const json = await res.json();
  document.getElementById("heatResult").innerText =
    JSON.stringify(json, null, 2);
}
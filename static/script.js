async function analyze() {
    const data = {
      cough: document.getElementById("cough").checked ? 1 : 0,
      chronic_cough: document.getElementById("chronic_cough").checked ? 1 : 0,
      heavycough: document.getElementById("heavycough").checked ? 1 : 0,
      tired: document.getElementById("tired").checked ? 1 : 0,
      feverlittle: document.getElementById("feverlittle").checked ? 1 : 0,
      feverbig: document.getElementById("feverbig").checked ? 1 : 0,
      sore_throat: document.getElementById("sore_throat").checked ? 1 : 0,
      chestpain: document.getElementById("chestpain").checked ? 1 : 0,
      chest: document.getElementById("chest").checked ? 1 : 0,
      tightchest: document.getElementById("tightchest").checked ? 1 : 0,
      breath: document.getElementById("breath").checked ? 1 : 0,
      breathtired: document.getElementById("breathtired").checked ? 1 : 0,
      breathfast: document.getElementById("breathfast").checked ? 1 : 0,
      wheezing: document.getElementById("wheezing").checked ? 1 : 0,        
      runny_nose: document.getElementById("runny_nose").checked ? 1 : 0,
      sneeze: document.getElementById("sneeze").checked ? 1 : 0,
      bodyaches: document.getElementById("bodyaches").checked ? 1 : 0,
      weight: document.getElementById("weight").checked ? 1 : 0,        
      panting: document.getElementById("panting").checked ? 1 : 0,
      swallow: document.getElementById("swallow").checked ? 1 : 0,
      phlegm: document.getElementById("phlegm").checked ? 1 : 0,
      headache: document.getElementById("headache").checked ? 1 : 0,
      aqi: Number(document.getElementById("aqi").value),
      sad: document.getElementById("sad")
        ? (document.getElementById("sad").checked ? 1 : 0): 0,
      stress: document.getElementById("stress")
        ? (document.getElementById("stress").checked ? 1 : 0): 0,
      sleep: document.getElementById("sleep")
        ? (document.getElementById("sleep").checked ? 1 : 0): 0,
      nausea: document.getElementById("nausea").checked ? 1 : 0,
      diarrhea: document.getElementById("diarrhea").checked ? 1 : 0,
      loss_smell: document.getElementById("loss_smell").checked ? 1 : 0,
      red_eyes: document.getElementById("red_eyes").checked ? 1 : 0,
      skin_rash: document.getElementById("skin_rash").checked ? 1 : 0,
      finger_color: document.getElementById("finger_color").checked ? 1 : 0,

    };
  
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });
  
    const result = await res.json();
  
    document.getElementById("result").innerText =
      JSON.stringify(result, null, 2);
  }
  
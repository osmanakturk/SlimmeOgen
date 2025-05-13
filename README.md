# 👁️ Slimme Ogen

**Slimme Ogen** is een educatief project ontwikkeld voor kinderen. Het laat zien hoe een camera en een computer objecten kunnen waarnemen met behulp van **Python**, **OpenCV** en een eenvoudige **Flask webinterface**. Dit project is speciaal ontworpen om kinderen bewust te maken van technologie en beeldherkenning, en om hun interesse in computer vision op een speelse manier te stimuleren.

---

## 🎯 Doel van het project

- Kinderen laten kennismaken met **computer vision**.
- Uitleg geven over hoe computers **beelden interpreteren**.
- Een **interactieve interface** aanbieden die eenvoudig te gebruiken is.
- Educatieve waarde bieden op een leuke en praktische manier.

---

## 🧰 Gebruikte technologieën

- Python
- OpenCV
- Flask
- Docker

---

## 🚀 Installatie & Gebruik

Volg onderstaande stappen om het project te klonen, te bouwen en te starten op je Raspberry Pi:

```bash
# Stap 1: Clone het project
rasp@raspberrypi:~/Desktop $ git clone https://github.com/osmanakturk/SlimmeOgen.git

# Stap 2: Navigeer naar de projectmap
rasp@raspberrypi:~/Desktop $ cd SlimmeOgen

# Stap 3: Bouw de Docker container
rasp@raspberrypi:~/Desktop/SlimmeOgen $ docker compose build

# Stap 4: Start de applicatie
rasp@raspberrypi:~/Desktop/SlimmeOgen $ docker compose up

Zodra de container draait, open je je browser en ga je naar:

👉 http://127.0.0.1:5000/


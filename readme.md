# GymAI - AI Gym Plan Generator

<img width="1120" height="820" alt="Capture d&#39;écran 2026-03-29 161815" src="https://github.com/user-attachments/assets/bf73aaec-1d9f-4acd-8b84-5e45d616dc2b" />
<img width="1120" height="803" alt="Capture d&#39;écran 2026-03-29 162052" src="https://github.com/user-attachments/assets/ea864902-0297-4b60-a1d6-6361f8cad4f3" />
<img width="1119" height="814" alt="Capture d&#39;écran 2026-03-29 162104" src="https://github.com/user-attachments/assets/3e0185ca-4bbe-4f4d-b9f4-351b79977678" />
<img width="1115" height="810" alt="Capture d&#39;écran 2026-03-29 161741" src="https://github.com/user-attachments/assets/0b15bd7e-a131-4f59-865d-67011eafc9ce" />
<img width="1119" height="808" alt="Capture d&#39;écran 2026-03-29 161757" src="https://github.com/user-attachments/assets/6261e882-32b1-4bed-ae5e-04ce93533679" />



## Overview
A personalized gym workout plan generator built with Flask. Creates detailed, customized workout plans based on user inputs including fitness goals, level, schedule, and available equipment.

## Architecture
- **Backend:** Python Flask (`main.py`) — serves the web app and generates plans
- **Frontend:** HTML/CSS/JS (`templates/index.html`, `static/`)
- **Plan Generation:** Smart template-based engine (works without API key) + optional OpenAI GPT-4o integration

## Running the App
The app runs on port 5000 via the "Start application" workflow:
```
python main.py
```

## Key Features
- 6 goal categories: Build Muscle, Lose Weight, Get Fit, Athletic, Recomp, Flexibility
- 3 fitness levels: Beginner, Intermediate, Advanced
- 2–6 days/week scheduling with proper rest day placement
- Equipment-aware exercise selection (Full Gym, Dumbbells, Bodyweight, Bands)
- Streaming response for real-time plan rendering
- Copy to clipboard & print functionality
- Markdown rendering with tables
- Progressive overload, nutrition, and recovery guidance

## AI Integration
- **Without OpenAI key:** Uses built-in template engine (instant, no API needed)
- **With OpenAI key:** Set `OPENAI_API_KEY` secret to enable GPT-4o generation

## File Structure
```
main.py              # Flask app + plan generator logic
generate_report.py   # PDF report generator
readme.md            # This file
templates/
  index.html         # Single-page UI
static/
  css/style.css      # Dark theme styles
  js/app.js          # Form interaction + SSE streaming
```

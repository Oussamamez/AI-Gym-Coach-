# GymAI - AI Gym Plan Generator

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

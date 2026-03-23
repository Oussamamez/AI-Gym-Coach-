from flask import Flask, render_template, request, jsonify, stream_with_context, Response
import openai
import os
import json

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    goal = data.get("goal", "")
    fitness_level = data.get("fitness_level", "")
    days_per_week = data.get("days_per_week", "")
    duration = data.get("duration", "")
    equipment = data.get("equipment", "")
    age = data.get("age", "")
    injuries = data.get("injuries", "")
    additional = data.get("additional", "")

    if not goal or not fitness_level:
        return jsonify({"error": "Please fill in the required fields."}), 400

    prompt = f"""You are an expert personal trainer and fitness coach. Create a detailed, personalized gym workout plan based on the following information:

**Goal:** {goal}
**Fitness Level:** {fitness_level}
**Days per Week:** {days_per_week} days
**Session Duration:** {duration} minutes
**Available Equipment:** {equipment if equipment else 'Full gym access'}
**Age:** {age if age else 'Not specified'}
**Injuries/Limitations:** {injuries if injuries else 'None'}
**Additional Notes:** {additional if additional else 'None'}

Please provide a comprehensive workout plan that includes:
1. A brief overview and strategy for achieving the goal
2. A weekly schedule with specific workouts for each training day
3. For each workout day: exercise name, sets, reps/duration, rest periods, and any form tips
4. Progressive overload recommendations
5. Recovery and nutrition tips

Format the plan in a clear, easy-to-read structure using markdown with proper headers and tables where appropriate."""

    def generate_stream():
        try:
            client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert personal trainer who creates detailed, science-based workout plans. Always be encouraging, specific, and practical."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=True,
                max_tokens=2000,
                temperature=0.7
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    yield f"data: {json.dumps({'content': content})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"

        except openai.AuthenticationError:
            yield f"data: {json.dumps({'error': 'Invalid API key. Please check your OpenAI API key in the Secrets tab.'})}\n\n"
        except openai.RateLimitError:
            yield f"data: {json.dumps({'error': 'Rate limit exceeded. Please try again in a moment.'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': f'An error occurred: {str(e)}'})}\n\n"

    return Response(
        stream_with_context(generate_stream()),
        content_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

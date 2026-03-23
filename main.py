from flask import Flask, render_template, request, jsonify, stream_with_context, Response
import os
import json
import time

app = Flask(__name__)

EXERCISES = {
    "strength_compound": {
        "full": ["Barbell Squat", "Deadlift", "Bench Press", "Barbell Row", "Overhead Press", "Romanian Deadlift", "Incline Bench Press", "Barbell Hip Thrust"],
        "dumbbells": ["Dumbbell Goblet Squat", "Dumbbell Romanian Deadlift", "Dumbbell Bench Press", "Dumbbell Row", "Dumbbell Shoulder Press", "Dumbbell Lunges", "Dumbbell Hip Thrust"],
        "bodyweight": ["Push-Ups", "Pike Push-Ups", "Bodyweight Squat", "Bulgarian Split Squat", "Glute Bridge", "Dips (on chair)", "Inverted Row (under table)"],
        "bands": ["Band Squat", "Band Pull-Apart", "Band Deadlift", "Band Press", "Band Row", "Band Hip Thrust"],
    },
    "strength_accessory": {
        "full": ["Cable Fly", "Lat Pulldown", "Cable Row", "Leg Press", "Leg Curl", "Leg Extension", "Tricep Pushdown", "Bicep Curl", "Face Pull", "Lateral Raise"],
        "dumbbells": ["Dumbbell Fly", "Dumbbell Lateral Raise", "Dumbbell Front Raise", "Hammer Curl", "Dumbbell Kickback", "Dumbbell Skull Crusher", "Dumbbell Calf Raise"],
        "bodyweight": ["Diamond Push-Ups", "Wide Push-Ups", "Tricep Dips", "Superman", "Plank", "Side Plank", "Calf Raises", "Reverse Lunges"],
        "bands": ["Band Curl", "Band Tricep Extension", "Band Lateral Raise", "Band Face Pull", "Band Kickback"],
    },
    "cardio_hiit": {
        "full": ["Rowing Machine", "Stationary Bike Sprints", "Treadmill Intervals", "Jump Rope", "Battle Ropes", "Box Jumps", "Sled Push"],
        "dumbbells": ["Dumbbell Thrusters", "Renegade Rows", "Dumbbell Burpee", "Dumbbell Clean & Press"],
        "bodyweight": ["Burpees", "Mountain Climbers", "Jump Squats", "High Knees", "Jumping Jacks", "Box Jumps", "Sprint Intervals"],
        "bands": ["Band Squat Jumps", "Band Sprints", "Band Thrusters"],
    },
    "flexibility": {
        "all": ["Hip Flexor Stretch", "Hamstring Stretch", "Pigeon Pose", "Thoracic Spine Rotation", "Shoulder Cross Stretch", "Cat-Cow", "World's Greatest Stretch", "Couch Stretch", "Ankle Circles", "Wrist Circles"]
    }
}

SPLITS = {
    2: {
        "muscle": ["Full Body A", "Full Body B"],
        "weight": ["Full Body Circuit A", "Full Body Circuit B"],
        "fitness": ["Full Body Strength", "Full Body Cardio & Core"],
        "athletic": ["Lower Body Power", "Upper Body Power"],
        "recomp": ["Full Body A", "Full Body B"],
        "flexibility": ["Upper Body Flexibility & Mobility", "Lower Body Flexibility & Mobility"],
    },
    3: {
        "muscle": ["Push (Chest/Shoulders/Triceps)", "Pull (Back/Biceps)", "Legs & Core"],
        "weight": ["Upper Body Circuits", "Lower Body Circuits", "Full Body HIIT"],
        "fitness": ["Strength A (Upper)", "Strength B (Lower)", "Cardio & Core"],
        "athletic": ["Lower Body Power", "Upper Body Power & Plyometrics", "Conditioning"],
        "recomp": ["Push", "Pull", "Legs"],
        "flexibility": ["Upper Body Yoga & Mobility", "Lower Body Yoga & Mobility", "Full Body Flow"],
    },
    4: {
        "muscle": ["Chest & Triceps", "Back & Biceps", "Legs (Quad Focus)", "Shoulders & Arms"],
        "weight": ["Upper Body Strength", "Lower Body Strength", "Upper Body HIIT", "Lower Body HIIT & Core"],
        "fitness": ["Push Strength", "Pull Strength", "Legs & Core", "Cardio & Conditioning"],
        "athletic": ["Lower Body Speed & Power", "Upper Body Strength", "Plyometrics & Agility", "Conditioning & Core"],
        "recomp": ["Upper Body Strength", "Lower Body Strength", "Upper Body Hypertrophy", "Lower Body Hypertrophy"],
        "flexibility": ["Morning Mobility Routine", "Hip & Lower Body", "Shoulders & Upper Body", "Full Body Deep Stretch"],
    },
    5: {
        "muscle": ["Chest", "Back", "Legs", "Shoulders", "Arms & Core"],
        "weight": ["Push HIIT", "Pull & Back", "Legs & Glutes", "Cardio Circuits", "Full Body Conditioning"],
        "fitness": ["Chest & Shoulders", "Back & Biceps", "Legs", "Cardio Intervals", "Core & Mobility"],
        "athletic": ["Lower Body Power", "Upper Body Strength", "Sprint & Agility", "Olympic Lifting / Plyos", "Conditioning"],
        "recomp": ["Chest & Triceps", "Back & Biceps", "Legs", "Shoulders & Core", "Full Body Circuit"],
        "flexibility": ["Morning Flow", "Hip Mobility", "Shoulder & Chest", "Lower Back & Hamstrings", "Full Body Yin"],
    },
    6: {
        "muscle": ["Chest & Triceps", "Back & Biceps", "Legs (Quad Focus)", "Shoulders", "Legs (Hamstring & Glute Focus)", "Arms & Core"],
        "weight": ["Push", "Pull", "Legs", "HIIT Cardio", "Upper Circuits", "Lower HIIT & Core"],
        "fitness": ["Chest", "Back & Biceps", "Legs", "Shoulders & Triceps", "Cardio", "Core & Mobility"],
        "athletic": ["Lower Body Power", "Upper Body Power", "Sprint & Agility", "Lower Body Strength", "Upper Body Strength", "Conditioning"],
        "recomp": ["Push", "Pull", "Legs", "Push (Hypertrophy)", "Pull (Hypertrophy)", "Legs (Hypertrophy) & Core"],
        "flexibility": ["Morning Mobility", "Hip Flexors", "Hamstrings & Glutes", "Shoulders & Chest", "Thoracic & Spine", "Full Body Flow"],
    }
}

def get_goal_key(goal):
    goal_lower = goal.lower()
    if any(w in goal_lower for w in ["muscle", "strength", "bulk", "mass", "strong"]):
        return "muscle"
    elif any(w in goal_lower for w in ["weight", "fat", "lose", "slim", "lean", "calorie"]):
        return "weight"
    elif any(w in goal_lower for w in ["athletic", "sport", "performance", "power", "speed"]):
        return "athletic"
    elif any(w in goal_lower for w in ["recomp", "recomposition", "simultaneously"]):
        return "recomp"
    elif any(w in goal_lower for w in ["flex", "mobil", "yoga", "stretch"]):
        return "flexibility"
    else:
        return "fitness"

def get_equipment_key(equipment):
    if not equipment:
        return "full"
    eq_lower = equipment.lower()
    if "bodyweight" in eq_lower and not any(w in eq_lower for w in ["dumbbell", "barbell", "cable", "machine"]):
        return "bodyweight"
    elif any(w in eq_lower for w in ["full gym", "barbell", "cable", "machine"]):
        return "full"
    elif "band" in eq_lower and not any(w in eq_lower for w in ["dumbbell", "barbell"]):
        return "bands"
    elif "dumbbell" in eq_lower:
        return "dumbbells"
    else:
        return "full"

def get_reps_sets(goal_key, level, exercise_type="compound"):
    beginner = level.lower().startswith("beg")
    intermediate = level.lower().startswith("int")

    if goal_key == "muscle":
        if exercise_type == "compound":
            return ("3-4", "6-10", "90-120 sec") if not beginner else ("3", "8-12", "60-90 sec")
        else:
            return ("3", "10-15", "60 sec") if not beginner else ("2-3", "12-15", "45-60 sec")
    elif goal_key == "weight":
        if exercise_type == "compound":
            return ("3", "12-15", "45-60 sec")
        else:
            return ("3", "15-20", "30-45 sec")
    elif goal_key == "fitness":
        if exercise_type == "compound":
            return ("3", "8-12", "60-90 sec")
        else:
            return ("3", "12-15", "60 sec")
    elif goal_key == "athletic":
        if exercise_type == "compound":
            return ("4-5", "3-6", "2-3 min") if not beginner else ("3-4", "5-8", "90-120 sec")
        else:
            return ("3-4", "8-12", "60-90 sec")
    elif goal_key == "recomp":
        if exercise_type == "compound":
            return ("4", "8-12", "60-90 sec")
        else:
            return ("3", "12-15", "45-60 sec")
    else:
        return ("2-3", "10-15 breaths", "30 sec")

def build_exercise_table(exercises_list, sets, reps, rest, goal_key):
    lines = []
    lines.append("| Exercise | Sets | Reps | Rest | Notes |")
    lines.append("|----------|------|------|------|-------|")
    tips = {
        "Barbell Squat": "Keep chest up, knees tracking over toes",
        "Deadlift": "Neutral spine, drive through heels",
        "Bench Press": "Retract shoulder blades, controlled descent",
        "Barbell Row": "Brace core, pull to lower chest",
        "Overhead Press": "Tuck ribs, full lockout at top",
        "Push-Ups": "Full range of motion, squeeze glutes",
        "Burpees": "Move fast, maintain form throughout",
        "Plank": "Posterior pelvic tilt, don't hold breath",
        "default": "Control the eccentric (lowering) phase"
    }
    for ex in exercises_list:
        tip = tips.get(ex, tips["default"])
        lines.append(f"| {ex} | {sets} | {reps} | {rest} | {tip} |")
    return "\n".join(lines)

def generate_workout_day(day_name, goal_key, equipment_key, level, duration_min):
    duration = int(duration_min)
    lines = []
    lines.append(f"### 🏋️ {day_name}")
    lines.append(f"**Duration:** {duration} minutes\n")

    is_cardio_day = any(w in day_name.lower() for w in ["hiit", "cardio", "conditioning", "circuit", "intervals"])
    is_flex_day = any(w in day_name.lower() for w in ["flex", "mobil", "yoga", "stretch", "flow", "yin"])
    is_power_day = any(w in day_name.lower() for w in ["power", "speed", "agility", "plyo", "sprint"])

    eq = equipment_key

    def pick(category, eq_key, n):
        pool = EXERCISES.get(category, {})
        options = pool.get(eq_key, pool.get("full", pool.get("all", [])))
        if not options:
            options = list(pool.values())[0] if pool else []
        return options[:n]

    lines.append("**Warm-Up (5-8 min):** Dynamic stretching, light cardio, joint circles\n")

    if is_flex_day:
        exercises = EXERCISES["flexibility"]["all"]
        lines.append("**Main Session:**\n")
        lines.append("| Exercise | Duration | Sets | Notes |")
        lines.append("|----------|----------|------|-------|")
        for ex in exercises[:8]:
            lines.append(f"| {ex} | 45-60 sec | 1-2 | Breathe deeply, never force |")
        lines.append("")
    elif is_cardio_day:
        c_exs = pick("cardio_hiit", eq, 5)
        sets, reps, rest = "4", "30-45 sec work / 20-30 sec rest", "Between circuits: 90 sec"
        lines.append("**HIIT Circuit (repeat 3-4 rounds):**\n")
        lines.append(build_exercise_table(c_exs, sets, reps, rest, goal_key))
        lines.append("")
        lines.append("> 💡 **Intensity:** Push to 80-90% max effort during work intervals. Scale as needed.\n")
    elif is_power_day:
        comp_exs = pick("strength_compound", eq, 3)
        sets, reps, rest = get_reps_sets(goal_key, level, "compound")
        lines.append("**Power & Strength Block:**\n")
        lines.append(build_exercise_table(comp_exs, sets, reps, rest, goal_key))
        lines.append("")
        lines.append(f"**Plyometric Block:**\n")
        plyo = ["Box Jumps", "Jump Squats", "Broad Jumps", "Explosive Push-Ups"][:3]
        lines.append("| Exercise | Sets | Reps | Rest | Notes |")
        lines.append("|----------|------|------|------|-------|")
        for ex in plyo:
            lines.append(f"| {ex} | 3-4 | 4-6 | 90-120 sec | Max effort, full reset between reps |")
        lines.append("")
    else:
        n_compound = 3 if duration <= 45 else 4
        n_accessory = 3 if duration <= 45 else 5

        comp_exs = pick("strength_compound", eq, n_compound)
        c_sets, c_reps, c_rest = get_reps_sets(goal_key, level, "compound")

        acc_exs = pick("strength_accessory", eq, n_accessory)
        a_sets, a_reps, a_rest = get_reps_sets(goal_key, level, "accessory")

        lines.append("**Main Lifts (Compound Movements):**\n")
        lines.append(build_exercise_table(comp_exs, c_sets, c_reps, c_rest, goal_key))
        lines.append("")
        lines.append("**Accessory Work:**\n")
        lines.append(build_exercise_table(acc_exs, a_sets, a_reps, a_rest, goal_key))
        lines.append("")

    lines.append("**Cool-Down (5 min):** Static stretching, focus on muscles worked\n")
    lines.append("---\n")
    return "\n".join(lines)

def generate_plan(goal, fitness_level, days_per_week, duration, equipment, age, injuries, additional):
    days = int(days_per_week) if days_per_week else 3
    goal_key = get_goal_key(goal)
    eq_key = get_equipment_key(equipment)

    split_map = SPLITS.get(days, SPLITS[3])
    day_names = split_map.get(goal_key, split_map.get("fitness", []))

    sections = []

    sections.append(f"# 🏆 Your Personalized Gym Plan\n")

    goal_descriptions = {
        "muscle": "build lean muscle mass and increase strength",
        "weight": "burn fat and lose weight while maintaining muscle",
        "fitness": "improve overall fitness, endurance, and health",
        "athletic": "boost athletic performance and functional strength",
        "recomp": "recompose your body — lose fat while gaining muscle",
        "flexibility": "enhance flexibility, mobility, and movement quality"
    }

    level_clean = fitness_level.split("(")[0].strip() if "(" in fitness_level else fitness_level
    eq_display = equipment if equipment else "Full Gym"
    age_note = f" at age {age}" if age else ""

    sections.append(f"## 📋 Plan Overview\n")
    sections.append(f"**Goal:** {goal}")
    sections.append(f"**Fitness Level:** {level_clean}")
    sections.append(f"**Schedule:** {days} days/week, {duration} minutes per session")
    sections.append(f"**Equipment:** {eq_display}")
    if injuries:
        sections.append(f"**Limitations noted:** {injuries} *(exercises have been adapted accordingly)*")
    sections.append("")

    sections.append(f"### Strategy")
    sections.append(f"This plan is designed to help you {goal_descriptions.get(goal_key, 'reach your fitness goals')}{age_note}. ")

    if goal_key == "muscle":
        sections.append("The focus is on **progressive overload** — gradually increasing weight or reps over time. Each week, aim to either add 2.5-5kg to compound lifts or squeeze out one extra rep. Protein intake is critical: target **0.8-1g per pound of body weight** daily.\n")
    elif goal_key == "weight":
        sections.append("A calorie deficit drives fat loss, but training preserves muscle. The combination of **strength training + cardio** circuits here maximizes calorie burn both during and after workouts (EPOC effect). Stay in a moderate deficit of 300-500 calories/day.\n")
    elif goal_key == "fitness":
        sections.append("The plan balances **strength, cardiovascular fitness, and mobility**. You'll progressively build a well-rounded foundation. Each month, aim to increase either load or volume by 5-10%.\n")
    elif goal_key == "athletic":
        sections.append("Athletic training prioritizes **power, speed, and functional movement**. Heavy compound lifts build the strength foundation; plyometrics and conditioning convert it into sport-ready explosiveness.\n")
    elif goal_key == "recomp":
        sections.append("Recomposition requires **eating at or near maintenance** while training hard. High-protein diet (1g/lb) combined with progressive strength training and occasional cardio creates the ideal hormonal environment to simultaneously build muscle and burn fat.\n")
    else:
        sections.append("Consistency is the most important factor for flexibility gains. **Practice daily** if possible, and always work at the edge of comfort — never pain. Flexibility adapts slowly but steadily.\n")

    sections.append("---\n")

    sections.append("## 📅 Weekly Schedule\n")

    day_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    rest_inserted = 0
    schedule_days = []
    all_days = list(day_labels[:7])
    used = []
    rest_positions = []

    if days == 2:
        used = [all_days[0], all_days[2]]
        rest_positions = [1, 3, 4, 5, 6]
    elif days == 3:
        used = [all_days[0], all_days[2], all_days[4]]
        rest_positions = [1, 3, 5, 6]
    elif days == 4:
        used = [all_days[0], all_days[1], all_days[3], all_days[4]]
        rest_positions = [2, 5, 6]
    elif days == 5:
        used = [all_days[0], all_days[1], all_days[2], all_days[3], all_days[4]]
        rest_positions = [5, 6]
    elif days == 6:
        used = [all_days[0], all_days[1], all_days[2], all_days[3], all_days[4], all_days[5]]
        rest_positions = [6]

    sections.append("| Day | Workout |")
    sections.append("|-----|---------|")
    day_name_idx = 0
    for i, d in enumerate(all_days):
        if i in rest_positions:
            sections.append(f"| {d} | 🛌 Rest & Recovery |")
        else:
            wname = day_names[day_name_idx] if day_name_idx < len(day_names) else "Training"
            sections.append(f"| {d} | {wname} |")
            day_name_idx += 1

    sections.append("")
    sections.append("---\n")

    sections.append("## 💪 Workout Details\n")

    for i, day_name in enumerate(day_names):
        workout = generate_workout_day(day_name, goal_key, eq_key, fitness_level, duration)
        sections.append(workout)

    sections.append("## 📈 Progressive Overload Plan\n")
    sections.append("Follow this 4-week progression:\n")
    sections.append("| Week | Focus | Adjustment |")
    sections.append("|------|-------|------------|")
    sections.append("| Week 1 | Foundation | Learn the movements, perfect form. Use a weight you can control. |")
    sections.append("| Week 2 | Build | Add 1-2 reps to each set OR increase weight by 2.5-5kg. |")
    sections.append("| Week 3 | Push | Add volume (1 extra set on compound lifts). Increase weight. |")
    sections.append("| Week 4 | Deload | Reduce volume by 40%. Keep weight similar. Let your body recover. |")
    sections.append("")
    sections.append("> 🔁 **After Week 4**, start the cycle again with heavier weights than Week 1.\n")
    sections.append("---\n")

    sections.append("## 🥗 Nutrition Guidelines\n")
    if goal_key in ["muscle", "recomp"]:
        sections.append("- **Protein:** 0.8–1g per pound of body weight (e.g., 160g for a 160lb person)")
        sections.append("- **Calories:** Slight surplus of 200-300 cal for muscle gain; maintenance for recomp")
        sections.append("- **Carbs:** Prioritize around workouts (oats, rice, sweet potato, fruit)")
        sections.append("- **Fats:** 0.3-0.5g per pound — avocado, nuts, olive oil, eggs")
        sections.append("- **Timing:** Eat protein within 1-2 hours post-workout for optimal recovery")
    elif goal_key == "weight":
        sections.append("- **Calorie Deficit:** 300–500 calories below maintenance")
        sections.append("- **Protein:** High — 0.8–1g per pound to preserve muscle while losing fat")
        sections.append("- **Minimize:** Ultra-processed foods, liquid calories, refined sugars")
        sections.append("- **Focus on:** Whole foods, lean proteins, vegetables, fiber")
        sections.append("- **Hydration:** Minimum 2-3L of water daily")
    else:
        sections.append("- **Balanced diet:** Focus on whole, unprocessed foods")
        sections.append("- **Protein:** 0.6-0.8g per pound of body weight")
        sections.append("- **Hydration:** 2-3L water daily, more on training days")
        sections.append("- **Anti-inflammatory foods:** Berries, leafy greens, fatty fish, turmeric")
        sections.append("- **Meal timing:** Eat a light meal 1-2 hours before training")
    sections.append("")
    sections.append("---\n")

    sections.append("## 😴 Recovery & Sleep\n")
    sections.append("- **Sleep:** 7-9 hours per night — this is when muscles actually grow")
    sections.append("- **Active Recovery:** On rest days, walk, swim, or do light yoga")
    sections.append("- **Foam Rolling:** 5-10 min on tight areas after workouts")
    sections.append("- **Listen to your body:** Pain (not soreness) = stop and rest")
    if injuries:
        sections.append(f"- **Your limitations ({injuries}):** Always prioritize pain-free movement. Consult a physiotherapist if unsure.")
    sections.append("")
    if additional:
        sections.append(f"> 📝 **Your notes:** {additional}\n")

    sections.append("---")
    sections.append("*Plan generated by GymAI · Always consult a healthcare professional before starting a new exercise program.*")

    return "\n".join(sections)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    goal = data.get("goal", "")
    fitness_level = data.get("fitness_level", "")
    days_per_week = data.get("days_per_week", "3")
    duration = data.get("duration", "45")
    equipment = data.get("equipment", "")
    age = data.get("age", "")
    injuries = data.get("injuries", "")
    additional = data.get("additional", "")

    if not goal or not fitness_level:
        return jsonify({"error": "Please fill in the required fields."}), 400

    openai_key = os.environ.get("OPENAI_API_KEY")

    if openai_key:
        return generate_with_openai(goal, fitness_level, days_per_week, duration, equipment, age, injuries, additional, openai_key)
    else:
        return generate_with_templates(goal, fitness_level, days_per_week, duration, equipment, age, injuries, additional)


def generate_with_templates(goal, fitness_level, days_per_week, duration, equipment, age, injuries, additional):
    def stream():
        plan = generate_plan(goal, fitness_level, days_per_week, duration, equipment, age, injuries, additional)
        chunk_size = 60
        for i in range(0, len(plan), chunk_size):
            chunk = plan[i:i+chunk_size]
            yield f"data: {json.dumps({'content': chunk})}\n\n"
            time.sleep(0.02)
        yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(
        stream_with_context(stream()),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


def generate_with_openai(goal, fitness_level, days_per_week, duration, equipment, age, injuries, additional, api_key):
    import openai

    prompt = f"""You are an expert personal trainer. Create a detailed, personalized gym workout plan:

**Goal:** {goal}
**Fitness Level:** {fitness_level}
**Days per Week:** {days_per_week}
**Session Duration:** {duration} minutes
**Equipment:** {equipment if equipment else 'Full gym'}
**Age:** {age if age else 'Not specified'}
**Injuries/Limitations:** {injuries if injuries else 'None'}
**Notes:** {additional if additional else 'None'}

Provide: overview & strategy, weekly schedule, detailed workouts (exercise, sets, reps, rest, form tips), progressive overload plan, nutrition tips, recovery advice. Use markdown with tables."""

    def stream():
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert personal trainer who creates detailed, science-based workout plans."},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
                max_tokens=2500,
                temperature=0.7
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(stream()),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

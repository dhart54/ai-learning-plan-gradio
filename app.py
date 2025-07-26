
import gradio as gr

def generate_prompt(
    role, responsibilities, hours_per_week, total_weeks, ai_tools, client_tools,
    internal_tools, learning_platforms, tools_skills_confidence, goal,
    team_function, tech_level, ai_use_case
):
    tools_str = ", ".join(ai_tools) if ai_tools else "None provided"
    client_str = ", ".join(client_tools) if client_tools else "None provided"
    internal_str = ", ".join(internal_tools) if internal_tools else "None provided"
    platform_str = ", ".join(learning_platforms) if learning_platforms else "None provided"
    goal_str = ", ".join(goal) if goal else "None provided"
    tools_skills_str = tools_skills_confidence or "None provided"
    use_case_str = ai_use_case or "None provided"

    prompt = f"""I want you to act as a professional AI upskilling advisor for a corporate data team.

🧾 Format Requirements for Output:
- Output must be divided by **weeks**, each with all sections:
  🎯 Goal, 📚 What to Learn, 🛠️ What to Do, 🤖 AI Tooling Augmentation, ✅ Deliverable, 🎧 Passive Learning
- Group weeks into **2–6 phases** with clear headers
- Use **plain text formatting** that is clean and copy-paste ready for Google Docs (no markdown or HTML)
- Do not include any headers or emojis beyond: 🎯 📚 🛠️ 🤖 ✅ 🎧 ✅ Phase
- Include a short title block for the learning plan at the top

🧠 Important:
- Do not ask the user any additional questions
- Assume all necessary information has already been provided
- Generate the **entire plan in a single response**, including all weeks
- If the user left any field blank (e.g., AI use case), substitute with a practical default and note that
- Ensure all links work — do not use placeholder URLs

📝 Output starts after this line:
---BEGIN LEARNING PLAN---

# AI Efficiency Learning Plan
### Personalized for {role} | Duration: {total_weeks} weeks | Weekly Commitment: {hours_per_week} hours

🧑‍💼 Learner Profile
- Role: {role}
- Day-to-day responsibilities: {responsibilities}
- Weekly learning time available: {hours_per_week} hours
- Total duration: {total_weeks} weeks
- Team Function: {team_function}
- Technical Comfort Level: {tech_level}
- AI Tools Available: {tools_str}
- Client Tools: {client_str}
- Internal Collaboration Tools: {internal_str}
- Learning Platforms: {platform_str}
- Current Tools or Skills: {tools_skills_str}
- Career Aspiration for This Plan: {goal_str}
- AI Use Case You’d Like to Explore: {use_case_str}

---END LEARNING PLAN---"""
    return prompt

with gr.Blocks() as demo:
    gr.Markdown("## AI Learning Plan Prompt Generator\nFill out the form and copy the prompt into ChatGPT to generate your plan.")

    with gr.Row():
        role = gr.Textbox(label="What is your role?")
        team_function = gr.Dropdown(["Analytics", "Creative", "HR", "Security", "Sales", "Leadership", "Other"], label="Which team function do you belong to?")

    responsibilities = gr.Textbox(label="What are your day-to-day responsibilities?", lines=3)
    hours_per_week = gr.Number(label="How many hours per week can you dedicate to learning?")
    total_weeks = gr.Slider(minimum=8, maximum=26, step=1, label="How many total weeks do you want the plan to last?")

    ai_tools = gr.CheckboxGroup(["Cursor", "Copilot", "ChatGPT", "Claude", "Gemini", "Perplexity", "Other"], label="Which AI tools do you have access to?")
    client_tools = gr.CheckboxGroup([""], label="Which client-approved tools do you use regularly?")
    internal_tools = gr.CheckboxGroup(["Google Sheets/Docs/Slides", "Slack", "Jira", "Monday", "SharePoint", "GitHub", "Other"], label="Which internal collaboration tools do you use?")
    learning_platforms = gr.CheckboxGroup(["Udemy", "Google Cloud Skills Boost", "YouTube", "Other"], label="Which learning platforms do you have access to?")

    tools_skills_confidence = gr.Textbox(label="What tools or skills do you already use, and how confident are you with them?")
    goal = gr.CheckboxGroup(["Automate routine work", "Build AI dashboards", "Learn AI fundamentals", "Grow into AI strategist or lead", "Other"], label="What do you hope to gain from this plan?")
    tech_level = gr.Dropdown(["Low", "Medium", "High"], label="How would you describe your technical comfort level?")
    ai_use_case = gr.Textbox(label="What’s one AI use case you’d love to explore?")

    output = gr.Textbox(label="📋 Copy this prompt into ChatGPT", lines=25, interactive=False)
    generate = gr.Button("Generate Prompt")

    generate.click(
        generate_prompt,
        [role, responsibilities, hours_per_week, total_weeks, ai_tools, client_tools,
         internal_tools, learning_platforms, tools_skills_confidence, goal,
         team_function, tech_level, ai_use_case],
        output
    )

demo.launch()

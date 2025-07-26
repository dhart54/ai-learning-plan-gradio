
import gradio as gr

def generate_plan(role, responsibilities, weekly_hours, total_weeks,
                  team_function, learning_style, industry, persona,
                  ai_tools, client_tools, collab_tools, platforms, skills, goals, tech_level, use_case):

    # Minimal validation
    if not role or not responsibilities or not weekly_hours or not total_weeks:
        return "⚠️ Please fill out all required fields: Role, Responsibilities, Weekly Hours, and Duration."

    return f"✅ AI Learning Plan Generated for {role} with {weekly_hours} hours/week over {total_weeks} weeks."

with gr.Blocks() as demo:
    gr.Markdown("## 🎯 AI Learning Plan Intake Form")

    with gr.Accordion("Required Fields (Minimum to Generate a Plan)", open=True):
        role = gr.Textbox(label="What is your role?*", placeholder="e.g., Data Analyst")
        responsibilities = gr.Textbox(label="What are your day-to-day responsibilities?*", lines=3)
        weekly_hours = gr.Number(label="How many hours per week can you dedicate to learning?*", precision=0)
        total_weeks = gr.Number(label="How many total weeks should the plan last? (8–26)*", precision=0)

    with gr.Accordion("Optional Fields – Help Personalize Your Plan", open=False):
        team_function = gr.Dropdown(
            label="Which team function do you belong to?",
            choices=["Analytics", "Marketing", "Creative", "HR", "Security", "Sales", "Leadership", "Other"],
            multiselect=False,
            allow_custom_value=True
        )
        learning_style = gr.Radio(
            label="Preferred learning style",
            choices=["Video", "Hands-on projects", "Interactive coding", "Reading articles", "Mixed"]
        )
        industry = gr.Textbox(label="Client industry or sector (optional)")
        persona = gr.Textbox(label="What persona or audience do you primarily serve? (optional)")

        ai_tools = gr.CheckboxGroup(
            label="Which AI tools do you currently have access to?",
            choices=["Cursor", "Copilot", "ChatGPT", "Claude", "Gemini", "Perplexity", "Other"]
        )

        # Replaced confusing 'client-approved' field with simpler, more familiar one
        collab_tools = gr.CheckboxGroup(
            label="Which collaboration tools do you use regularly?",
            choices=["Google Workspace", "Slack", "Jira", "Monday", "SharePoint", "GitHub", "Other"]
        )

        platforms = gr.CheckboxGroup(
            label="Which learning platforms do you have access to?",
            choices=["Udemy", "Google Cloud Skills Boost", "YouTube", "Other"]
        )

        skills = gr.Textbox(label="What tools or skills do you already use? (e.g., SQL – Intermediate)")
        goals = gr.CheckboxGroup(
            label="What do you hope to gain from this plan?",
            choices=["Automate routine work", "Build AI dashboards", "Learn AI fundamentals", "Grow into strategist/lead", "Other"]
        )
        tech_level = gr.Radio(
            label="How would you describe your technical comfort level?",
            choices=["Low (UI tools only)", "Medium (formulas/scripts)", "High (APIs, cloud, notebooks)"]
        )
        use_case = gr.Textbox(label="One AI use case you’d love to explore")

    output = gr.Textbox(label="Your Result", lines=5)

    generate_btn = gr.Button("Generate My Plan")
    generate_btn.click(fn=generate_plan,
                       inputs=[role, responsibilities, weekly_hours, total_weeks,
                               team_function, learning_style, industry, persona,
                               ai_tools, None, collab_tools, platforms, skills, goals, tech_level, use_case],
                       outputs=output)

demo.launch()

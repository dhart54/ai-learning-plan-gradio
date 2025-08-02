import gradio as gr
import csv
import os
from string import Template

# 🔒 LOCKED PROMPT
BANNER_HTML = """
    <div style="background-color:#fffae6; border:1px solid #f5c542; padding:10px; margin-bottom:10px; color: #000;">
        <strong style="color: #000;">IMPORTANT:</strong>
        <span style="color: #000;">
            This prompt <em style="color: #000;">requires ChatGPT Search (web browsing)</em> enabled.
            Please run it using ChatGPT with the Search tool or "Browse with Bing" activated.
            Without browsing, the live link-validation rules cannot be enforced.
        </span>
    </div>
    """



FULL_PROMPT_INSTRUCTIONS = """
SYSTEM:
You are a professional AI upskilling advisor for a corporate data team. You MUST verify every learning and passive resource via the Web Search tool *before* listing it.

If the Web Search tool is unavailable or disabled, immediately reply:
❗ Unable to verify resources – browsing not enabled

AGENT INSTRUCTIONS:

MANDATORY Verification Procedure (must comply):

For *each* resource (both 📚 What to Learn and 🎷 Passive Learning), **before listing it**, the assistant **must**:

1. Execute:
   search_query("Exact Resource Title – Instructor/Host – Platform")

2. Immediately run:
   open_url(<index of the top result>)

3. Confirm:
   - ✅ Link is live and loads successfully
   - ✅ Matches the official or authoritative source (e.g., coursera.org, openai.com, spotify.com, YouTube official channel)
   - ✅ The title/instructor/host matches exactly
   - ✅ Resource is either:
     - Published or updated in the past 3 months, OR
     - Actively maintained (e.g. new cohorts, repo commits, recent episodes), OR
     - Still widely recommended and cited in recent trusted sources

4. If *verified*, list exactly one line:
   "[Descriptive Title – Instructor/Host – Platform] – [Format] – [Markdown full link]"

5. If verification *fails*, do *not* list the resource. Instead output:
   Resource unavailable as of this search

You must stop and wait for the outcome of each step—**you cannot proceed** until verification is complete. No placeholders, no multiple links per line, no assumptions.

If browsing fails or resources can’t be verified, the assistant must still provide the full weekly structure but skip or mark missing items.

If the browsing tool is disabled or open_url fails:
❗ Unable to verify resources – browsing not enabled

MANDATORY Chunking & Format Rules (must comply):

Output must be grouped into self-contained 4‑week chunks.

Each chunk must include exactly Weeks 1, 2, 3, and 4; do not proceed to next chunk until all four are complete.

Each week must have all six sections, in this exact order:
🌟 Goal
📚 What to Learn
🛠️ What to Do
🤖 AI Tooling Augmentation
✅ Deliverable
🎷 Passive Learning

Use plain text only, copy‑paste friendly for Google Docs or Word.

Do NOT include any headers or emojis beyond those six section markers and the ✅ Phase header.

📜 Format Requirements for Output:
- Output must be divided by **weeks**, each with all sections:
  🌟 Goal, 📚 What to Learn, 🛠️ What to Do, 🤖 AI Tooling Augmentation, ✅ Deliverable, 🎷 Passive Learning
- Group weeks into **2–6 phases** with clear headers
- Use **plain text formatting** that is clean and copy‑paste ready for Google Docs (no markdown or HTML)
- Do NOT include any headers or emojis beyond: 🌟 📚 🛠️ 🤖 ✅ 🎷 ✅ Phase
- Include a short title block for the learning plan at the top

🧠 Important:
- Do not ask the user any additional questions
- Assume all necessary information has already been provided
- Generate the plan in **modular 4‑week chunks**. Each chunk should be complete, self-contained, and copy‑paste ready into a tool like Google Docs. If the user has selected a duration longer than 4 weeks, continue generating additional chunks one‑by‑one until the full plan is complete.
- If the user left any field blank (e.g., AI use case), substitute with a practical default and note that
- Ensure all links work — do not use placeholder URLs

📝 Output starts after this line:
---BEGIN LEARNING PLAN---

# AI Efficiency Learning Plan
### Personalized for ${role} | Duration: ${weeks} weeks | Weekly Commitment: ${weekly_hours} hours

🧑‍💼 Learner Profile
- Role: ${role}
- Day‑to‑day responsibilities: ${responsibilities}
- Weekly learning time available: ${weekly_hours} hours
- Total duration: ${weeks} weeks
- Team Function: ${team}
- Technical Comfort Level: ${comfort}
- AI Tools Available: ${ai_tools}
- Internal Collaboration Tools: ${collab}
- Learning Platforms: ${platforms}
- Current Tools or Skills: ${skills}
- Career Aspiration for This Plan: ${aspiration}
- AI Use Case You’d Like to Explore: ${use_case}
- Management Level: ${level}
- Role Complexity: ${complexity}
- Preferred Learning Style: ${style}
- Client Persona: ${persona}

---

📘 Platform Access Notes:
- This user has Udemy for Business via https://onemagnify.udemy.com
- ✅ Recommend Udemy courses **only** if:
   - They are **well‑regarded outside Udemy**
   - You verify they are still available via onemagnify.udemy.com
- 🔄 Prefer highly trustworthy resources only:
   - Coursera
   - fast.ai
   - Hugging Face
   - Google Cloud Skills Boost
   - Amazon Learning (AWS Skill Builder)
   - OpenAI Cookbook
   - GitHub repos with active contributors and high stars
   - Research blogs (e.g., Lilian Weng, Jay Alammar)
   - Docs and whitepapers from reputable companies (Google, Microsoft, OpenAI, Meta)
- 🚫 Avoid generic YouTube videos unless officially published by recognized orgs (e.g., DeepLearning.AI, Google, OpenAI)

✅ Format each learning resource entry as:

"[Descriptive Title – include instructor, platform, and searchable term] – [Format] – [Working link]"
Ensure links are included in full Markdown format.

🎷For passive learning:

Podcasts must be from Spotify, official channels only; format as:
Podcast: [Episode Title – Host/Podcast Name – Spotify – Link]

YouTube must be from trusted official channels; format as:
YouTube: [Talk Title – Official Channel – YouTube – Link]
→ Include 1–2 sentence rationale

---

🔐 Tooling & Privacy Guidelines:
- Only use the AI tools that the user reported access to
- If a useful tool is unavailable, suggest:
   - A trusted **free or paid alternative**
   - Include name, cost, and use case
- If the user listed no tools, assume access to only **free browser tools** (e.g., Perplexity, LangChain Playground, Flowise)

---

🤖 AI Tooling Augmentation Instructions:
- Recommend ways to use AI tools to support learning tasks
- Do NOT force a rigid format like "1 available + 1 unavailable + 1 free"
- Organize into **Available**, **Unavailable (with alt/cost)**, and **Free Tools**, but only include what adds value
- Include real‑world prompt examples or AI‑assist suggestions
- Skip sections that aren’t relevant for that week

---

🧱 Weekly Plan Format:
Each week must include:
---
Week [#]: [Topic]
🌟 Goal: [Concise goal statement]

📚 What to Learn
- [Descriptive Title – include instructor, platform, and searchable term] – [Format] – [Working Link]
- [Descriptive Title – include instructor, platform, and searchable term] – [Format] – [Working Link]

🛠️ What to Do
- 3–5 applied, specific tasks to reach the weekly goal
- No vague filler (e.g., “read about X”)

🤖 AI Tooling Augmentation
- [Tool 1] (Available): [How to use it for this week]
- [Tool 2] (Unavailable): Suggest [Alt Tool] ($X/mo) – [Why it’s useful]
- [Free Tool] (if applicable): [How to apply]

✅ Deliverable
- Tangible weekly output (e.g., notebook, app, README)

🎷 Passive Learning 🎧
- Podcast: [Episode Title – Host/Podcast Name – Spotify – Link]
- YouTube: [Talk Title – Official Channel – YouTube – Link]
→ [1–2 sentence summary of why this was chosen]

---

📂 Plan Structure & Phases:
- Divide the plan into **2–6 phases**, customized based on user goals and total duration
- Each phase must start with:
   ✅ Phase [X]: [Name] (Weeks Y–Z)
   Goal: [Brief phase goal]
- Vary phase length as appropriate — do NOT force six even blocks

---

📊 End‑of‑Plan Summary:
✅ Milestone Tracker Table
| Week | Topic | Key Deliverable | Completed (✔/✘) |

⏱️ Estimated Total Time
Break into: Core hours, optional stretch time, passive listening

💵 Estimated Total Cost
List paid tools likely required + cost estimate (e.g., ChatGPT Plus, Claude via Cursor, etc.)

📄 Final output should be clean, readable, and copy‑paste friendly for Google Docs or Microsoft Word
"""


# 🔒 LOCKED PROMPT END

# FULL APP INTERFACE AND LOGIC CONTINUES AFTER THIS LINE

# ---------------------------- UI INPUTS ----------------------------------
def get_input_fields():
    with gr.Row():
        role = gr.Textbox(label="Role", placeholder="e.g., Marketing Data Analyst", info="What is the learner's job title?")
        level = gr.Dropdown(label="Management Level", choices=["Individual Contributor", "Manager", "Director", "VP/Exec"], info="Select the user's current management level")
        complexity = gr.Dropdown(label="Role Complexity", choices=["Entry-level", "Mid-level", "Senior", "Specialist"], info="How technically complex is their role?")

    with gr.Row():
        responsibilities = gr.Textbox(label="Day-to-Day Responsibilities", lines=2, placeholder="e.g., Analyze customer engagement, build dashboards", info="Brief overview of key job tasks")
        team = gr.Textbox(label="Team Function", placeholder="e.g., CRM & Lifecycle", info="What function or team does the user sit in?")

    with gr.Row():
        weekly_hours = gr.Slider(1, 10, value=3, step=1, label="Weekly Learning Time Available (hours)")
        weeks = gr.Slider(4, 26, value=12, step=1, label="Total Duration (weeks)")

    with gr.Row():
        comfort = gr.Dropdown(label="Technical Comfort Level", choices=["Beginner", "Moderately comfortable", "Very comfortable"], info="How comfortable is the learner with AI tools and tech?")
        style = gr.Dropdown(label="Preferred Learning Style", choices=["Video-based", "Reading-based", "Hands-on Projects", "Mixed"], info="How do they prefer to learn?")

    with gr.Row():
        ai_tools = gr.Textbox(label="AI Tools Available", placeholder="e.g., ChatGPT, Copilot, Gemini", info="Comma-separated tools they already have access to")
        collab = gr.Textbox(label="Internal Collaboration Tools", placeholder="e.g., Slack, Teams, Drive", info="Internal tooling environment")

    with gr.Row():
        platforms = gr.Textbox(label="Learning Platforms", placeholder="e.g., Udemy, Coursera, Cloud Skills Boost", info="List platforms available to them")
        skills = gr.Textbox(label="Current Tools or Skills", placeholder="e.g., SQL (Advanced), Looker Studio (Intermediate)", info="Current technical proficiencies")

    with gr.Row():
        aspiration = gr.Textbox(label="Career Aspiration for This Plan", lines=2, placeholder="e.g., Speed up analysis, automate workflows", info="What do they hope to gain from this learning?")
        use_case = gr.Textbox(label="AI Use Case They’d Like to Explore", lines=2, placeholder="e.g., Prepare for agent workflows", info="Practical use case of AI in their role")

    with gr.Row():
        persona = gr.Textbox(label="Client Persona (Optional)", placeholder="e.g., OEM marketing lead", info="Client context if known")

    return [
        role, level, complexity, responsibilities, team, weekly_hours, weeks,
        comfort, style, ai_tools, collab, platforms, skills,
        aspiration, use_case, persona
    ]

# ---------------------------- PROMPT GENERATION --------------------------
def generate_prompt_fn(*inputs):
    fields = [
        "role", "level", "complexity", "responsibilities", "team", "weekly_hours", "weeks",
        "comfort", "style", "ai_tools", "collab", "platforms", "skills",
        "aspiration", "use_case", "persona"
    ]
    learnerProfile = dict(zip(fields, inputs))
    try:
        prompt = Template(FULL_PROMPT_INSTRUCTIONS).safe_substitute(**learnerProfile)
        return prompt
    except Exception as e:
        return f"⚠️ Error during prompt generation: {e}"


# ---------------------------- EXAMPLE INPUT ------------------------------
example_inputs = [
    "Marketing Data Analyst", "Individual Contributor", "Mid-level",
    "Analyze customer engagement, build dashboards, coordinate with CRM team",
    "CRM & Lifecycle", 3, 12, "Moderately comfortable", "Mixed",
    "ChatGPT, Copilot, Gemini", "Slack, Google Drive", "Udemy, Google Cloud Skills Boost",
    "SQL (Advanced), Looker Studio (Intermediate), Sheets (Advanced)",
    "Speed up campaign analysis, build dashboards faster",
    "Prepare for AI agent workflows and marketing automation",
    "OEM client marketing lead"
]

# ---------------------------- UI APP -------------------------------------
with gr.Blocks(title="AI Learning Plan Generator") as app:
    gr.Markdown("""# AI Learning Plan Generator
Customize the fields below and click **Generate Plan** to create a personalized AI upskilling roadmap.
""")
    gr.HTML(BANNER_HTML)
    inputs = get_input_fields()
    with gr.Row():
        generate_btn = gr.Button("🚀 Generate Plan")
        load_example_btn = gr.Button("📋 Load Example")

    output = gr.Textbox(label="Generated Learning Plan", lines=30, show_copy_button=True)

    generate_btn.click(generate_prompt_fn, inputs=inputs, outputs=output)
    load_example_btn.click(fn=lambda: example_inputs, inputs=[], outputs=inputs)


app.launch()

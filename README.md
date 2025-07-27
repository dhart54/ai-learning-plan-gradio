# 📘 AI Learning Plan Generator

A Gradio-powered web app that generates personalized AI upskilling plans based on role, goals, tools, and team context. Built for internal enablement, AI onboarding, and leadership visibility.

---

## 🚀 Features

- ✅ Personalized learning plans based on role, responsibilities, and aspirations
- 🧠 Variable-injected prompt architecture with Google Docs–ready formatting
- 🛠️ No API required — runs entirely locally or via Hugging Face Spaces
- 🧪 "Load Example" mode for demoing use cases to leadership
- 📌 One-click copy of the final plan output

---

## 💻 Live Demo

👉 [Launch in Hugging Face Spaces](https://huggingface.co/spaces/dhart54/ai-learning-plan)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- [Gradio](https://www.gradio.app/) for UI
- `string.Template` for prompt templating
- No external dependencies or API calls

---

## 📂 Project Structure

```bash
ai-learning-plan-gradio/
│
├── app.py              # Main Gradio app
├── requirements.txt    # Dependencies
├── README.md           # Project overview
└── .gitignore          # Git hygiene
```

---

## ⚙️ Local Setup

> Works cross-platform (Windows/macOS/Linux)

1. **Clone the repository**

   ```bash
   git clone https://github.com/dhart54/ai-learning-plan-gradio.git
   cd ai-learning-plan-gradio
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app locally**

   ```bash
   python app.py
   ```

5. **Visit the app**
   Navigate to `http://127.0.0.1:7860` in your browser.

---

## ☁️ Deployment (Hugging Face Spaces)

Already live:
🔗 [`https://huggingface.co/spaces/dhart54/ai-learning-plan`](https://huggingface.co/spaces/dhart54/ai-learning-plan)

To update:

1. Push changes to `app.py`, `requirements.txt`, or `README.md` in your local repo:

   ```bash
   git add .
   git commit -m "Update app logic or prompt"
   git push origin main
   ```

2. Hugging Face Space will auto-rebuild using `app.py`.

---

## ✍️ Author Prompt Format

The master prompt is stored in `app.py` under the `FULL_PROMPT_INSTRUCTIONS` block.

- 🔒 Use **flat variable names** (e.g., `${role}`, `${goal}` — not nested)
- 🔄 Ensure every `${variable}` in the prompt matches a field collected in the UI
- ⚠️ Missing variables will result in `KeyError: Missing field in template`

---

## ✅ Example Scenario

> **"I'm a mid-level marketing analyst using SQL and Looker Studio. I want to explore AI agents to automate reporting and improve targeting. I have 3 hours/week for 12 weeks."**

🔹 The app will return a structured 12-week learning roadmap optimized for tools, goals, and context — copyable into Docs, Notion, or LMS workflows.

---

## 📬 Feedback or Contributions

Open issues or submit PRs via
📂 [`github.com/dhart54/ai-learning-plan-gradio`](https://github.com/dhart54/ai-learning-plan-gradio)

---

Built with ❤️ by Dylan Hart.
Prompt structure and app logic refined via GPT-4 and Claude.

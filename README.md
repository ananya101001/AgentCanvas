# 🎨 AgentCanvas — Autonomous AI Landing Page Generator

> Type a business idea. Get a production-ready landing page. No code. No design. No human intervention.

![AgentCanvas Demo](assets/demo.png)

## 🚀 What is AgentCanvas?

AgentCanvas is a multi-agent AI system that autonomously generates responsive landing pages from a single text prompt. It uses a team of three specialized AI agents — a Product Manager, a Frontend Developer, and a QA Tester — orchestrated by LangGraph's state machine, to plan, build, test, and self-correct a complete HTML landing page without any human intervention.

This project was built to demonstrate real-world AI engineering concepts: state machine orchestration, multi-agent collaboration, structured Pydantic outputs, and autonomous QA feedback loops.

---

## 🧠 Architecture

![Architecture Diagram](assets/architecture.png)

AgentCanvas uses a **hybrid orchestration model**:

- **LangGraph** acts as the state machine — holding project data in memory, routing tasks between agents, and managing the iterative QA loop
- **CrewAI** acts as the worker layer — managing specialized agent personas, prompt context, and structured outputs

### The Three Agents

| Agent | Role | Responsibility |
|---|---|---|
| 🧠 PM Agent | Lead Conversion Strategist | Analyzes the prompt, designs wireframe, writes marketing copy |
| 💻 Dev Agent | Senior Frontend Developer | Translates wireframe JSON into responsive HTML + Tailwind CSS |
| 🔍 QA Agent | QA Automation Engineer | Reviews code for bugs, outputs PASS or a numbered bug list |

### The Autonomous QA Loop
```
Dev writes code → QA reviews → Bugs found?
  YES + iteration < 3  →  Send back to Dev with bug list
  YES + iteration = 3  →  Save best version + log warning  
  NO (PASS)            →  Save final page ✅
```

---

## ✨ Features

- Single prompt to full landing page in minutes
- Autonomous self-correction loop — no human debugging required
- Pydantic-enforced structured outputs for reliable agent communication
- Live preview inside the Streamlit UI
- One-click HTML download
- Fully responsive Tailwind CSS output

---

## 🖥️ Demo

**Input:**
```
A landing page for "NeuralDesk" — an AI customer support tool for startups. 
Use purple color theme. CTA says "Start Free Trial".
```

**Output:**

![Hero Section](assets/output_hero.png)
![Testimonial Section](assets/output_testimonial.png)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| LangGraph | State machine orchestration and QA loop routing |
| CrewAI | Multi-agent definition and execution |
| Pydantic | Structured output validation |
| Streamlit | User interface |
| Tailwind CSS | Landing page styling |
| Python 3.10+ | Core language |

---

## 📁 Project Structure
```
AgentCanvas/
│
├── main.py                 # Streamlit UI and entry point
├── graph.py                # LangGraph nodes and routing logic
│
├── crew/
│   ├── agents.yaml         # Agent roles, goals, backstories
│   ├── tasks.yaml          # Task descriptions and expected outputs
│   └── crew_logic.py       # CrewAI agents bound to LangGraph nodes
│
├── schemas/
│   └── pydantic_models.py  # Structured output schemas
│
├── tools/
│   └── file_writer.py      # Saves generated HTML to disk
│
├── output/                 # Generated landing pages saved here
├── assets/                 # Screenshots for README
├── requirements.txt
└── .env                    # API keys (never commit this)
```

---

## ⚡ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/AgentCanvas.git
cd AgentCanvas
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### 4. Run the app
```bash
streamlit run main.py
```

### 5. Open your browser
Go to `http://localhost:8501`, type your business idea, and hit 🚀 Generate.

---

## 💡 Example Prompts
```
A landing page for a luxury dog grooming salon called Pawfect in Los Angeles. Use rose color theme.
```
```
A landing page for a productivity app called FocusFlow for remote workers. Use blue color theme.
```
```
A landing page for an online yoga studio called ZenFlow. Use green color theme.
```

---

## 📖 Medium Article

Read the full deep-dive article explaining the architecture, design decisions, and lessons learned:

👉 [How I Built AgentCanvas: Autonomous Landing Pages with Multi-Agent AI](https://medium.com/yourusername)

---

## 🤝 Contributing

Pull requests are welcome! If you find a bug or want to add a new agent (SEO optimizer, image generator, etc.), feel free to open an issue.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## ⭐ Support

If AgentCanvas helped you learn something new, a star on GitHub means a lot and helps others find this project!

---

*Built with 🎨 by [Ananya Praveen Shetty] — connecting ideas to the internet, one agent at a time.*


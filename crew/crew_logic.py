import os
import time
from crewai import Agent, Task, Crew, LLM
from schemas.pydantic_models import WireframeAndCopy
import yaml
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = "choose-any-value"

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

agents_config = load_yaml("crew/agents.yaml")
tasks_config  = load_yaml("crew/tasks.yaml")

llm = LLM(
    model="openai/adamo1139/Hermes-3-Llama-3.1-8B-FP8-Dynamic",
    api_key="choose-any-value",
    base_url="https://hermes.ai.unturf.com/v1"
)

pm_agent = Agent(
    role=agents_config["product_manager"]["role"],
    goal=agents_config["product_manager"]["goal"],
    backstory=agents_config["product_manager"]["backstory"],
    llm=llm,
    verbose=True
)

dev_agent = Agent(
    role=agents_config["frontend_developer"]["role"],
    goal=agents_config["frontend_developer"]["goal"],
    backstory=agents_config["frontend_developer"]["backstory"],
    llm=llm,
    verbose=True
)

qa_agent = Agent(
    role=agents_config["qa_tester"]["role"],
    goal=agents_config["qa_tester"]["goal"],
    backstory=agents_config["qa_tester"]["backstory"],
    llm=llm,
    verbose=True
)

def run_with_retry(crew, retries=3, wait=15):
    for attempt in range(retries):
        try:
            return crew.kickoff()
        except Exception as e:
            if "rate_limit" in str(e).lower() and attempt < retries - 1:
                print(f"Rate limit hit. Waiting {wait}s before retry ({attempt+1}/{retries})...")
                time.sleep(wait)
            else:
                raise e

def run_planning_crew(user_prompt: str) -> dict:
    task = Task(
        description=tasks_config["planning_task"]["description"].format(
            user_prompt=user_prompt
        ),
        expected_output=tasks_config["planning_task"]["expected_output"],
        agent=pm_agent,
        output_pydantic=WireframeAndCopy
    )
    crew = Crew(agents=[pm_agent], tasks=[task], verbose=True)
    result = run_with_retry(crew)
    return result.pydantic.model_dump()

def run_development_crew(wireframe: dict, qa_feedback: list) -> str:
    brand = wireframe.get("brand_name", "Brand")
    color = wireframe.get("color_theme", "purple")
    headline = wireframe["hero"]["headline"]
    subheadline = wireframe["hero"]["subheadline"]
    cta = wireframe["hero"]["cta_button_text"]
    features = wireframe.get("features", [])
    quote = wireframe.get("testimonial_quote", "")
    author = wireframe.get("testimonial_author", "")

    features_html = ""
    for f in features:
        features_html += f"""
        <div class="bg-white rounded-2xl shadow-lg p-8 flex flex-col gap-3">
            <h3 class="text-2xl font-bold text-{color}-700">{f['title']}</h3>
            <p class="text-gray-600 text-lg">{f['description']}</p>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{brand}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 font-sans">

    <!-- Navbar -->
    <nav class="bg-{color}-700 text-white px-8 py-4 flex justify-between items-center shadow-md">
        <span class="text-2xl font-extrabold tracking-tight">{brand}</span>
        <button class="bg-white text-{color}-700 font-bold px-6 py-2 rounded-full hover:bg-{color}-100 transition">
            {cta}
        </button>
    </nav>

    <!-- Hero -->
    <section class="bg-{color}-700 text-white py-28 px-8 text-center">
        <h1 class="text-6xl font-extrabold mb-6 leading-tight">{headline}</h1>
        <p class="text-2xl text-{color}-200 mb-10 max-w-2xl mx-auto">{subheadline}</p>
        <button class="bg-white text-{color}-700 font-bold text-xl px-10 py-4 rounded-full shadow-lg hover:scale-105 transition-transform">
            {cta}
        </button>
    </section>

    <!-- Features -->
    <section class="py-20 px-8 max-w-6xl mx-auto">
        <h2 class="text-4xl font-extrabold text-center text-{color}-700 mb-14">Why {brand}?</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features_html}
        </div>
    </section>

    <!-- Testimonial -->
    <section class="bg-{color}-50 py-20 px-8 text-center">
        <div class="max-w-3xl mx-auto bg-white rounded-3xl shadow-xl p-12">
            <p class="text-2xl italic text-gray-700 mb-6">"{quote}"</p>
            <p class="text-{color}-700 font-bold text-lg">— {author}</p>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-{color}-700 text-white text-center py-8 mt-0">
        <p class="text-lg">&copy; 2025 {brand}. All rights reserved.</p>
    </footer>

</body>
</html>"""

    return html

   

def run_qa_crew(raw_code: str) -> str:
    task = Task(
        description=tasks_config["qa_task"]["description"].format(
            raw_code=raw_code
        ),
        expected_output=tasks_config["qa_task"]["expected_output"],
        agent=qa_agent
    )
    crew = Crew(agents=[qa_agent], tasks=[task], verbose=True)
    result = run_with_retry(crew)
    return str(result.raw).strip()

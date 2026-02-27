import streamlit as st
from graph import build_graph
from dotenv import load_dotenv
import os

load_dotenv()

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="AgentCanvas",
    page_icon="🎨",
    layout="centered"
)

# ── Header ─────────────────────────────────────────────────────
st.title("🎨 AgentCanvas")
st.caption("Autonomous AI Landing Page Generator — powered by GPT-4o + CrewAI + LangGraph")
st.divider()

# ── Input Section ──────────────────────────────────────────────
st.subheader("Describe your business")
user_prompt = st.text_area(
    label="What kind of landing page do you need?",
    placeholder="e.g. A landing page for a vegan bakery in New York that specializes in gluten-free desserts",
    height=120
)

col1, col2 = st.columns([3, 1])
with col2:
    generate_btn = st.button("🚀 Generate", use_container_width=True)

st.divider()

# ── Generation Logic ───────────────────────────────────────────
if generate_btn:
    if not user_prompt.strip():
        st.warning("Please describe your business first!")
    else:
        # Progress tracking
        progress = st.progress(0, text="Starting AgentCanvas...")
        status   = st.empty()
        log_box  = st.expander("📋 Agent Activity Log", expanded=True)

        with log_box:
            st.info("🧠 PM Agent is analyzing your idea...")

        try:
            # Initialize state
            initial_state = {
                "user_prompt":        user_prompt,
                "wireframe_and_copy": {},
                "raw_code":           "",
                "qa_feedback":        [],
                "iteration_count":    0,
                "final_status":       "Pending"
            }

            # Build and run the graph
            graph = build_graph()

            progress.progress(10, text="Planning your page...")
            with log_box:
                st.info("📐 PM Agent is designing wireframe and writing copy...")

            # Stream graph execution step by step
            final_state = None
            for step in graph.stream(initial_state):
                node_name = list(step.keys())[0]
                state     = list(step.values())[0]

                if node_name == "planner":
                    progress.progress(30, text="Wireframe complete!")
                    with log_box:
                        st.success("✅ PM Agent done — wireframe and copy ready")
                        brand = state.get("wireframe_and_copy", {}).get("brand_name", "")
                        st.write(f"**Brand detected:** {brand}")

                elif node_name == "developer":
                    iteration = state.get("iteration_count", 1)
                    progress.progress(30 + (iteration * 15), text=f"Writing code (attempt {iteration})...")
                    with log_box:
                        st.info(f"💻 Developer Agent writing code — attempt {iteration}/3")

                elif node_name == "qa":
                    feedback = state.get("qa_feedback", [])
                    status_val = state.get("final_status", "")
                    if status_val == "Success":
                        progress.progress(90, text="QA passed!")
                        with log_box:
                            st.success("✅ QA Agent — code passed all checks!")
                    else:
                        with log_box:
                            st.warning(f"🔁 QA found {len(feedback)} issue(s) — sending back to developer")
                            for bug in feedback:
                                st.write(f"  • {bug}")

                elif node_name == "output":
                    progress.progress(100, text="Done!")
                    final_state = state

            # ── Display Results ────────────────────────────────
            st.divider()

            if final_state:
                final_status = final_state.get("final_status", "")
                raw_code     = final_state.get("raw_code", "")

                if final_status == "Success":
                    st.success("🎉 Your landing page is ready!")
                elif final_status == "Failed_QA":
                    st.warning("⚠️ Page generated with some unresolved issues (max retries reached)")

                # Preview the page in an iframe
                st.subheader("👁️ Live Preview")
                st.components.v1.html(raw_code, height=600, scrolling=True)

                # Download button
                st.subheader("⬇️ Download Your Page")
                st.download_button(
                    label="Download index.html",
                    data=raw_code,
                    file_name="index.html",
                    mime="text/html",
                    use_container_width=True
                )

                # Show raw code
                with st.expander("🧾 View Raw HTML Code"):
                    st.code(raw_code, language="html")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.exception(e)
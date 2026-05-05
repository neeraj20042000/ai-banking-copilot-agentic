import os
import requests
import streamlit as st
from typing import Optional


API_URL = os.getenv("BACKEND_URL", "http://localhost:8000/query")


def submit_query(query: str, user_id: str) -> dict:
    payload = {"query": query}
    if user_id and len(user_id.strip()) >= 3:
        payload["user_id"] = user_id.strip()
    response = requests.post(API_URL, json=payload, timeout=20)
    response.raise_for_status()
    return response.json()


def render_agent_progress(progress_list: list, selected_agent: Optional[str]):
    if not progress_list:
        st.info("No agent progress data returned from the backend yet.")
        return

    st.markdown("### Agent progress overview")
    with st.container():
        button_cols = st.columns(len(progress_list), gap="large")
        for idx, item in enumerate(progress_list):
            button_label = item.get("agent_name", f"Agent {idx + 1}")
            if button_cols[idx].button(button_label, key=f"agent_btn_{idx}"):
                st.session_state["selected_agent"] = button_label

    if not selected_agent and progress_list:
        st.session_state["selected_agent"] = progress_list[0].get("agent_name")
        selected_agent = st.session_state["selected_agent"]

    selected_data = None
    for item in progress_list:
        if item.get("agent_name") == selected_agent:
            selected_data = item
            break

    if selected_data:
        st.markdown(f"#### Selected agent: **{selected_agent}**")
        state_before = selected_data.get("state_before", {}) or {}
        state_after = selected_data.get("state_after", {}) or {}
        with st.container():
            before_col, after_col = st.columns(2)
            with before_col:
                st.subheader("State before execution")
                st.json(state_before)
            with after_col:
                st.subheader("State after execution")
                st.json(state_after)
    else:
        st.warning("Selected agent data was not found.")


def main():
    st.set_page_config(
        page_title="AI Banking Copilot",
        page_icon="💼",
        layout="centered",
    )

    st.title("AI Banking Copilot")
    st.write("A lightweight Streamlit front-end for the agentic banking backend.")

    st.markdown("---")
    st.subheader("Enter your query")
    user_query = st.text_area("Query", value="", height=120, placeholder="Ask the AI banking copilot about loans, compliance, recommendations, or risk assessments.")
    user_id = st.text_input("User ID (optional)", value="", placeholder="Leave blank to use backend default user ID")

    st.markdown("---")
    st.write(
        "Press the button below to send your query to the backend and review agent execution progress."
    )

    if "selected_agent" not in st.session_state:
        st.session_state["selected_agent"] = None

    if st.button("Run agent cycle", type="primary"):
        if not user_query or not user_query.strip():
            st.warning("Please enter a query before running the agent cycle.")
        else:
            with st.spinner("Sending query to the backend and collecting agent progress..."):
                try:
                    response_data = submit_query(user_query.strip(), user_id)
                    st.success("Backend processed the query successfully.")
                    st.write("**Current agent:**", response_data.get("current_agent", "N/A"))
                    progress = response_data.get("progress") or []
                    
                    # Extract final answer from last agent's state
                    final_answer = None
                    if progress:
                        final_agent_state = progress[-1].get("state_after", {})
                        final_answer = final_agent_state.get("response")
                    
                    # Display final answer
                    if final_answer:
                        st.markdown("---")
                        st.subheader("Final Answer")
                        st.text_area("Response", value=final_answer, height=150, disabled=True)
                    
                    render_agent_progress(progress, st.session_state.get("selected_agent"))
                except requests.RequestException as error:
                    st.error("Unable to reach the backend or process the response.")
                    st.exception(error)
                except ValueError:
                    st.error("Backend returned an invalid JSON response.")

    st.markdown("---")
    st.caption("AI Banking Copilot is for informational and demonstration use only. This system may generate content that is not legally binding or fully accurate.")
    st.caption("Backend API: `POST /query` with `query` and `user_id`. Streamlit display is for agent progress review.")
    st.caption("Developed as a simple UI for reviewing agent state snapshots and progress flows.")


if __name__ == "__main__":
    main()

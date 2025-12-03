import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.agents.coding_agent.agent import CodingAgent

st.set_page_config(layout="wide", page_title="Coding Agent")

if "agent" not in st.session_state:
    st.session_state.agent = CodingAgent()

st.title("Coding Agent Interface")

query = st.text_area("Enter your request:", height=100)

if st.button("Run Agent"):
    if query:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Agent Stream")
            stream_container = st.container()

        with col2:
            st.subheader("Code & Results")
            code_container = st.container()

        code_blocks = []
        results = []

        for message in st.session_state.agent.stream(query):
            sender = message.type.upper()

            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tc in message.tool_calls:
                    with stream_container:
                        st.info(f"**Tool Call:** {tc['name']}")
                    if tc['name'] == 'execute_code':
                        code = tc['args'].get('code', '')
                        code_blocks.append(code)
                        with code_container:
                            st.code(code, language="python")

            if message.content:
                if sender == "TOOL":
                    with stream_container:
                        st.success(f"**Tool Result:**\n{message.content}")
                    results.append(message.content)
                    with code_container:
                        st.text_area("Output:", message.content, height=100)
                elif sender == "AI":
                    with stream_container:
                        st.write(f"**AI:** {message.content}")
                else:
                    with stream_container:
                        st.write(f"**{sender}:** {message.content}")

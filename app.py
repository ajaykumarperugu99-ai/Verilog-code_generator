import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Streamlit Page Setup
st.set_page_config(page_title="Verilog RTL Generator", page_icon="⚡", layout="wide")

st.title("⚡ Verilog RTL & Testbench Generator")
st.write("Enter a digital logic design task (e.g., `Full Adder`, `4-bit Counter`, `D Flip-Flop`) to generate Verilog RTL code and its Testbench.")

# Fetch API Key from environment variable
api_key = os.getenv("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ OpenRouter API Key not found in environment variables. Please configure OPENROUTER_API_KEY on Render.")

# User Input Box
task_input = st.text_input("Digital Hardware Task:", placeholder="e.g., Full Adder")

if st.button("Generate Code"):
    if not api_key:
        st.error("API Key is missing! Please provide a valid OpenRouter API Key in your environment variables.")
    elif not task_input.strip():
        st.error("Please enter a task description or component name.")
    else:
        with st.spinner("Generating Verilog RTL code and Testbench..."):
            try:
                # Initialize Model using OpenRouter's free endpoint
                # The api_key and base_url parameters configure ChatOpenAI for service emulators like OpenRouter.
                llm = ChatOpenAI(
                    model="openrouter/free",
                    api_key=api_key, 
                    base_url="https://openrouter.ai/api/v1" 
                )

                prompt = f"""You are an expert Verilog RTL and verification engineer.
Your task is to ONLY generate synthesizable Verilog code and a complete testbench for the following hardware design request:
'{task_input.strip()}'

Provide both the module design and a self-checking testbench cleanly formatted."""

                response = llm.invoke([HumanMessage(content=prompt)])
                st.success("Generation Complete!")
                st.markdown(response.content)

            except Exception as e:
                st.error(f"An error occurred: {e}")
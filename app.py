import streamlit as st
import boto3
import json

# --- CONFIGURATION ---
AGENT_ID = 'XENWVOLGVL'
AGENT_ALIAS_ID = 'EMNUMIZC19'
REGION = 'eu-north-1'

st.set_page_config(page_title="Bitcoin Educator AI", page_icon="🧡")
st.title("🧡 Bitcoin Educator AI")
st.markdown("Ask me anything about the Bitcoin network, mining, or history.")

# Initialize Bedrock client
client = boto3.client('bedrock-agent-runtime', region_name=REGION)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is a block hash?"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.spinner("Thinking..."):
            response = client.invoke_agent(
                agentId=AGENT_ID,
                agentAliasId=AGENT_ALIAS_ID,
                sessionId="streamlit-session-123", # Can be dynamic
                inputText=prompt
            )

            # Parse the streaming response
            completion = ""
            for event in response.get("completion"):
                chunk = event.get("chunk")
                if chunk:
                    completion += chunk.get("bytes").decode("utf-8")

            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(completion)
            st.session_state.messages.append({"role": "assistant", "content": completion})

    except Exception as e:
        st.error(f"Error: {str(e)}")

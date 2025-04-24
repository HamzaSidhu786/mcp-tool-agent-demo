# import streamlit as st
# import requests

# st.set_page_config(page_title="MCP Chat", layout="centered")

# st.title("🧠 Chat with MCP + Gemini")

# prompt = st.text_input("Enter your question:", placeholder="e.g. What is the remainder if I divide 11 by 3?")

# if st.button("Ask"):
#     if prompt:
#         with st.spinner("Thinking..."):
#             try:
#                 response = requests.post(
#                     "http://0.0.0.0:8000/chat",
#                     params={"prompt": prompt}  # use this if your FastAPI expects prompt as query param
#                 )
#                 if response.status_code == 200:
#                     data = response.json()
#                     st.success("✅ Answer:")
#                     st.write(data["answer"])

#                     if data.get("tool_names"):
#                         st.info(f"🔧 Tool Used: `{data['tool_names']}`")
#                 else:
#                     st.error(f"❌ Failed with status code: {response.status_code}")
#             except Exception as e:
#                 st.error(f"⚠️ Error: {str(e)}")
#     else:
#         st.warning("Please enter a prompt before submitting.")

import streamlit as st
import asyncio
from mcp_client import MCPClient

server_script_path = "calculator_server.py"

async def query_mcp(prompt):
    client = MCPClient()
    await client.connect_to_server(server_script_path)
    response, tool_name = await client.process_query(prompt)
    await client.exit_stack.__aexit__(None, None, None)
    return response, tool_name

st.title("🛠️ MCP Server Chat")

prompt = st.text_input("Ask a question using a tool:")

if st.button("Submit"):
    if prompt:
        with st.spinner("Processing..."):
            try:
                response, tool_name = asyncio.run(query_mcp(prompt))
                st.success("✅ Answer")
                st.write(response)
                st.info(f"🔧 Tool used: {tool_name}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# 🛠️ MCP Tool Agent Demo

This project demonstrates how to build an interactive tool-based agent using the [MCP framework](https://github.com/microsoft/mcp). It integrates:
- ✅ **MCP Server**: Serves custom tools (like calculator functions)
- ✅ **MCP Client**: Sends prompts, detects required tools, and fetches results
- ✅ **Streamlit App**: Frontend UI to interact with the MCP-powered LLM

> 🚀 Great starting point for anyone exploring MCP + Streamlit for tool-based reasoning.

---

## 🧠 What's Inside?

| Component     | Description                                  |
|---------------|----------------------------------------------|
| `calculator.py` | Custom MCP server toolset (add, divide...)   |
| `client.py`     | Connects to MCP server and processes queries |
| `app.py`        | Streamlit UI for user interaction            |

---

## 📦 Installation

Make sure you have **Python 3.10+** and **virtualenv**.

```bash
# Clone the repository
git clone https://github.com/HamzaSidhu786/mcp-tool-agent-demo.git
cd mcp-tool-agent-demo

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Running the Demo

### 1. Start the Streamlit App

```bash
streamlit run app.py
```

### 2. Running the Client
```bash
uv run client.py calculator_server.py
```


This will automatically start the MCP client and connect to the MCP server.

Try this in the Streamlit app:


```
What is the reminder if I divide 11 by 3?
```

You'll get back:
```json
{
  "Answer": "2",
  "Tool Used": "divide"
}
```

---

## 👨‍💻 Author

- **Hamza Sidhu**
  - GitHub: [@HamzaSidhu786](https://github.com/HamzaSidhu786)
  - LinkedIn: [Muhammad Hamza](https://www.linkedin.com/in/muhammad-hamza-32622520b/)

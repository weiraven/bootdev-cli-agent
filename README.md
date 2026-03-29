# 🤖 AI Coding Agent (CLI)

A lightweight AI agent built with Python and the Gemini API that can:

- Inspect a codebase
- Read and modify files
- Execute Python programs
- Iteratively reason over results
- Fix bugs autonomously

This project demonstrates the core architecture behind modern tool-using AI agents.

---

## 🚀 Features

### 🔍 File system awareness
- List directories
- Read file contents

### 🛠️ Code execution
- Run Python scripts with arguments  
- Capture stdout/stderr  

### ✍️ Code modification
- Create and overwrite files safely  

### 🔁 Iterative reasoning loop
- Maintains conversation history  
- Uses tool outputs as feedback  
- Continues until a final answer is produced  

---

## 🧠 How It Works

The agent follows a loop similar to:
```
User → Model → Tool → Model → Tool → ... → Final Answer
```
**Tool schemas**  
Define available operations for the LLM  

**Function dispatcher (`call_function`)**  
Maps model-selected tools to Python functions  

**Conversation memory (`messages`)**  
Stores:
- user input  
- model responses  
- tool outputs  

**Agent loop**
- Calls the model repeatedly (max 20 iterations)  
- Executes tool calls  
- Feeds results back into the model  

---

## 📦 Project Structure
```
.
├── main.py                 # Agent loop + CLI entrypoint
├── call_function.py        # Tool dispatcher + schema registration
├── prompts.py              # System prompt
├── config.py               # Constants
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
└── calculator/             # Example project the agent can interact with
```

---

## ⚙️ Setup

### 1. Clone repo
```bash
git clone <your-repo-url>
cd <repo>
```

### 2. Create environment
```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
uv pip install -r requirements.txt
```

### 4. Add API key
Create a .env file:
```env
GEMINI_API_KEY=your_api_key_here
```

## ▶️ Usage

Run the agent from the project root:
```bash
uv run main.py "<your prompt>"
```
Optional verbose mode:
```bash
uv run main.py "<your prompt>" --verbose
```

## 🧪 Example: Autonomous Bug Fix

A bug was intentionally introduced in the calculator:
```bash
uv run calculator/main.py "3 + 7 * 2"
```
Incorrect result:
```json
{
  "expression": "3 + 7 * 2",
  "result": 20
}
```
Now let the agent fix it:
```bash
uv run main.py "Fix the bug in the calculator code. Right now calculator/main.py returns 20 for '3 + 7 * 2', but it should return 17. Inspect the code, fix it, and verify the fix by running the calculator."
```
Agent behavior:
```
 - Calling function: get_files_info
 - Calling function: get_file_content
 - Calling function: write_file
 - Calling function: run_python_file
```
Final result:
```bash
The bug has been fixed...
```
Verify:
```json
uv run calculator/main.py "3 + 7 * 2"
{
  "expression": "3 + 7 * 2",
  "result": 17
}
```

## ⚠️ Safety Notes

This agent can execute arbitrary Python code within a sandboxed directory.

Safeguards include:

- Restricted working directory
- Path validation
- 30-second execution timeout

Do not run untrusted prompts or code.

## 🧩 Future Improvements
- Smarter tool selection (reduce redundant calls)
- Streaming responses
- Web UI / chat interface
- Multi-file reasoning improvements
- Test-driven auto-fix loops

## 📚 Inspiration

This project mirrors the core ideas behind:

- OpenAI function-calling agents
- LangChain tools
- Cursor / IDE-integrated agents
- SWE-agent-style autonomous debugging systems

## 🏁 Summary

This project demonstrates how a simple combination of:

- structured tool schemas
- a function dispatcher
- and a feedback loop

can turn an LLM into a functional coding agent.
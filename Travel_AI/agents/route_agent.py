import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from Travel_AI.tools.flight_tool import avaitation_tool
from Travel_AI.tools.railway_tool import get_train_details
from langchain_groq import ChatGroq
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_agent
import asyncio
from dotenv import load_dotenv
from datetime import date

load_dotenv()

LLM = ChatOpenRouter(model = 'minimax/minimax-m2.7:free')

# Add one day to get tomorrow
today = date.today()

async def all_tools():
    avaitation = await avaitation_tool()
    railway = [get_train_details]

    all_tools = avaitation + railway
    return all_tools

ROUTE_SELECTION_PROMPT = """
You are a travel route planning agent.

The user will provide a travel request.

Read the user's message carefully and extract the information yourself.


IMPORTANT:
- Do NOT ask for information that is already present in the user message.
- If origin, destination, date, and transport mode are present, immediately use
  the appropriate tool to search for options.
- Only ask a clarification question when a required value is genuinely missing.
- If the user says "by flight", use the flight tool.
- If the user says "by train", use the railway tool (Only use the railway tool when the source and destination is in India.
- If the user is open to both or no preference, use both tools.
- Never invent transportation information.

The application may provide a default origin of New Delhi if the user does not
specify an origin.

After receiving tool results, compare the options and provide a concise
recommendation.
"""

prompt = PromptTemplate.from_template(ROUTE_SELECTION_PROMPT)


async def route_llm(state):
    tools = await all_tools()
    agent = create_agent(
        model = LLM,
        tools=  tools,
        system_prompt = ROUTE_SELECTION_PROMPT
    )

    response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": state['user_query']}]},
)
    print("===== Route Tool Responded =====")
    return {"route_selection" : str(response["messages"][-1].content)}

    # print("===== ALL MESSAGES =====")

    # for i, msg in enumerate(response["messages"]):
    #     print(f"\n--- {i} ---")
    #     print("TYPE:", type(msg).__name__)
    #     print("CONTENT:", repr(msg.content))
    #     print("TOOL CALLS:", getattr(msg, "tool_calls", None))




# if __name__ == "__main__":
#     asyncio.run(route_llm())
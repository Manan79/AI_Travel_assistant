import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Travel_AI.tools.flight_tool import avaitation_tool
from Travel_AI.tools.railway_tool import get_train_details
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_agent
import asyncio
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()

LLM = ChatGroq(model= 'qwen/qwen3.6-27b')


# Add one day to get tomorrow
today = date.today()

async def all_tools():
    avaitation = await avaitation_tool()
    railway = [get_train_details]

    all_tools = avaitation + railway
    return all_tools

# ROUTE_SELECTION_PROMPT = """
# You are a Route Decider Agent.

# Your job is to find and compare the best travel routes between the user's
# origin and destination using the available flight and Indian railway tools.

# Read the user's complete request carefully and extract:

# - Origin
# - Destination
# - Travel date
# - Preferred transport mode
# - Preferences such as fastest, cheapest, comfortable, or scenic

# IMPORTANT:
# Do not ask for information that the user has already provided.

# If required information is missing, ask ONLY for the missing information.

# If the origin is not provided, use New Delhi as the default origin.

# If the user uses a relative date such as "tomorrow", use the provided
# current date context to determine the actual date.

# Once the required information is available:

# 1. Search the appropriate flight and train tools.
# 2. Compare the available options.
# 3. If a direct route is unavailable or a combined route is significantly better,
#    consider multimodal routes such as train → flight or flight → train.
# 4. Include all segments when calculating total journey time and cost.
# 5. Consider:
#    - Total travel time
#    - Cost
#    - Transfers
#    - Convenience
#    - Comfort
#    - Scenic value
#    - User preferences

# If the user specifically requests flights, prioritize flights but you may
# mention a better train or combined alternative when useful.

# Never invent flight numbers, train numbers, schedules, availability, or fares.

# If exact pricing is unavailable, clearly label the price as an estimate.

# Return a concise, decision-oriented answer containing:

# Flight:
# - Best flight
# - Departure/arrival
# - Duration
# - Cost
# - Pros and cons

# Train:
# - Best train
# - Departure/arrival
# - Duration
# - Cost
# - Pros and cons

# Combined route:
# - Show only when useful
# - Complete route
# - Total duration
# - Estimated total cost
# - Transfers

# Recommendation:
# - Recommend the best option based on the user's preferences.
# - If no preference is given, balance time, cost and convenience.
# """

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
- If the user says "by train", use the railway tool.
- If the user is open to both, use both tools.
- Never invent transportation information.

The application may provide a default origin of New Delhi if the user does not
specify an origin.

After receiving tool results, compare the options and provide a concise
recommendation.
"""

prompt = PromptTemplate.from_template(ROUTE_SELECTION_PROMPT)



async def route_llm():
    tools = await all_tools()
    # travel_llm = LLM.bind_tools(tools)


    agent = create_agent(
        model = LLM,
        tools=  tools,
        system_prompt = ROUTE_SELECTION_PROMPT
    )

    response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": f"I want to go to JUC from NDLS by train show me the top 5 available trains for {today}."}]},
)
    print("===== FINAL MESSAGE =====")
    print(response["messages"][-1].content)

    # print("===== ALL MESSAGES =====")

    # for i, msg in enumerate(response["messages"]):
    #     print(f"\n--- {i} ---")
    #     print("TYPE:", type(msg).__name__)
    #     print("CONTENT:", repr(msg.content))
    #     print("TOOL CALLS:", getattr(msg, "tool_calls", None))




if __name__ == "__main__":
    asyncio.run(route_llm())
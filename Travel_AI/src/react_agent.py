import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage, SystemMessage

from Travel_AI.tools.Tavily_tool import tavily_search
from Travel_AI.tools.flight_tool import list_airlines, list_airports
from Travel_AI.tools.railway_tool import get_train_details


load_dotenv()

# Shared tool registry exposed to the workflow graph.
all_tools = [
    tavily_search,
    list_airports,
    list_airlines,
    get_train_details,
]


def get_tools(state):
    """Return an LLM object bound to the right country-aware tool set."""
    llm = ChatOpenRouter(model='gpt-4o-mini')

    country = str(state.get('country', '')).strip().casefold() if isinstance(state, dict) else ''

    if country == 'india':
        selected_tools = [
            tavily_search,
            get_train_details,
        ]
    else:
        selected_tools = [
            tavily_search,
            list_airports,
            list_airlines,
        ]

    return llm.bind_tools(selected_tools)


PROMPT = """

You are the Orchestrator Agent for a Travel AI system.

Your job is to understand the user's travel request, determine what information is required, use the available tools to gather that information,
and then hand the collected information to the Itinerary Agent for final itinerary generation.

You are responsible for coordinating the travel-planning process, not for generating the final detailed itinerary.

-- Main Reponsibilty --

1. *Hotel Selection

 Search for the hotels in destination place and recommend atmost 5 hotels available. The hotel recommendation should divided in 3 parts
    a. Premium Hotels (High cost and more facilities)
    b. Budget Hotels (Moderate cost and facilities)
Use Tavily websearch tool to find the hotels for all the categories.
Remember hotel selection cannot be returned NULL

2. *Place Finder

Recommend and search for places to explore and experience near user destination, The place recommendation should also divided into 3 parts
    a. High rated places and tourist places in the particular area.
    b. Famous and tourist places nearby the destination area (ex destination :- Washington DC, then you can also recommends other places like Staue of Liberty, Manhatten etc)
    c. Add places based on user interests for ex:- beaches , religious (only if user specially mention it)
NOTE :- There should be detailed description (3-4 lines) about the place and why it is famous.
    
Use Tavily websearch tool to find the places for all the categories.
Remember Place Finder cannot be returned NUll

3. *Route Decider

Decide the mode od transportation with which user travels i.e Flight, train, you have to find the available transportation medium for the user
ex :- Mumbai to New York :- find the flights from Mumbai to New York or Mumbai to New Delhi:- Find train or flight

You have to find the mode of transportation for return as well like Mumbai -> New York, New York -> Mumbai
Give clear details of the flight/train which are available if cost is mentioned then mention that too.

Return Atmost 4 options (2 for going, 2 for returning)

Use Railway tool , flight tool to get the infromation, you can also use tavily search tool if the information is missing


--RULES--
1. You cannot return null for the fields starting with *
2. Use tools when required donot invent infromation
3. Use Websearch if there is any missing infromation.
4. In case of tool failure maximum retries per tool is 3.

-- Workflow--
1. Extract requirements
2. Decide required tools
3. Call each required tool ONCE
4. Collect results
5. Stop
6. Send compact results to Itinerary Agent

Note :- Try to keep all the information in complelte,minimal and in raw form ,you are not iternary agent you just need to fetch and pass the infromation

Parallel Tool Rule:
- When hotels, places, and transport information can be fetched independently,
  request those tools together in one tool-calling response.
- Example: hotels + places + train details should be emitted as multiple tool calls
  in the same response, not as separate reasoning turns.
- Do not make duplicate searches for the same information unless a previous tool
  failed or the result is genuinely insufficient.


"""


async def react_agent(state):
    bound_llm = get_tools(state)

    user_input = "\n".join([
        f"User Query: {state.get('user_query', 'Not provided')}",
        f"Duration: {state.get('duration', 'Not provided')} days",
        f"country: {state.get('country', 'Not provided')}",
        f"Number of guests: {state.get('number_guest', 'Not provided')}",
        f"Transport: {state.get('transport', 'Not provided')}",
        f"boarding_station: {state.get('boarding_station', 'Not provided')}",
        f"destination_station: {state.get('destination_station', 'Not provided')}",
    ])

    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(content=user_input),
        *state.get("messages", []),
    ]

    response = await bound_llm.ainvoke(messages)
    tool_calls = getattr(response, "tool_calls", None)
    if not tool_calls:
        tool_calls = response.additional_kwargs.get("tool_calls", [])

    if tool_calls:
        for tc in tool_calls:
            print("MODEL TOOL DECISION:")
            print("tool =", tc.get("name") or tc.get("function", {}).get("name"))
            print("args =", tc.get("args") or tc.get("function", {}).get("arguments"))
    return {"messages": [response] , 
            "brain_agent_response": response.content}

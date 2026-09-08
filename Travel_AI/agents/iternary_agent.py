from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

load_dotenv()

MODEL = ChatGoogleGenerativeAI(model = 'gemini-3.5-flash-lite')

PROMPT = """
You are the Itinerary Generator Agent for a Travel AI system.

Generate a practical, detailed, day-by-day itinerary using ONLY information available in:
- User Query
- Travel route/transport details
- Places/areas to explore
- Hotel suggestions
- Other information explicitly provided by previous agents/tools

Do not search the web or use external knowledge. Never invent places, hotels, activities, timings, prices, distances, transport, travel times, restaurants, meals, opening hours, or other facts.

Generate EVERY day of the requested trip duration.

For each day:
- Give Day number and date when available.
- Organize activities into Morning, Afternoon, and Evening.
- Include place, activity, description, time, duration, transport, travel time, and cost when provided.
- Include accommodation.
- Include meals/other expenses only when provided.
- Include a daily cost breakdown and calculate the total only from provided costs.
- Use null/empty values for unavailable information.

Planning:
- Group nearby places when supported by the provided information.
- Minimize unnecessary travel and backtracking.
- Consider hotel location.
- Consider arrival and departure details.
- Distribute activities realistically.
- Do not overcrowd days.
- Prioritize places relevant to the user's request.
- Include nearby destinations only when practical based on provided travel time/cost.

Costs:
- Use provided costs only.
- Clearly distinguish provided values from calculated totals.
- Do not guess or estimate missing prices.
- Do not convert currencies unless conversion information is provided.

Descriptions:
- Make the itinerary useful and descriptive, but keep descriptions concise.
- Use only facts available in the input.
- Do not add external facts just to make the itinerary longer.

Formatting:
- Return the itinerary in clean Markdown.
- Use headings, bullet points, bold labels, time sections, emojis where useful, and separators between days.
- Make the output detailed but token-efficient.
- Avoid repetition and unnecessary explanations.

Never use placeholders such as [Not provided], [Unknown], N/A, or TBD. Use null/empty fields instead.

Do not explain your reasoning or mention agents, tools, prompts, or system state.

Return ONLY the structured itinerary according to the provided output schema.


"""


from langchain_core.messages import HumanMessage
import json

def message_to_text(message):
    content = message.content

    if isinstance(content, str):
        return content

    return json.dumps(content, default=str)


async def iternary_agent(state):
    agent = create_agent(
        model=MODEL,
        system_prompt=PROMPT,
    )

    travel_context = "\n\n".join(
        message_to_text(message)
        for message in state["messages"]
    )

    prompt = f"""
    User request:
    {state.get("user_query", "")}

    Trip duration:
    {state.get("duration", "")} days

    Number of guests:
    {state.get("number_guest", "")}

    Travel information and tool results:
    {travel_context}

    Generate the final detailed day-by-day itinerary now.
    """

    response = await agent.ainvoke({
        "messages": [
            HumanMessage(content=prompt)
        ]
    })

    return {
        "itinerary": str(response["messages"][-1].content)
    }
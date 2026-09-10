from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

MODEL = ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite')

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


async def iternary_generator(state):
    brain_agent_response = state.get('brain_agent_response', '')
    user_query = state.get('user_query', '')
    number_guest = state.get('number_guest', '')
    duration = state.get('duration', '')

    prompt = f"""
        You are an Expert Travel Guide and you have to generate simple but actionable day by day travel iternary for the user and
        you are given with previous agent response which include hotel suggestion , travel suggestion, places to explore etc.
        You have to convert raw/messy agent response to human readable beutiful response.

        Agent Response: {brain_agent_response}
        User_query: {user_query}
        number of guest : {number_guest}
        duration : {duration}

        Generate an day by day iternary from above data, a day in iternary should look like:
        Day 1:
        - morning and afternoon (timmings):
            - Activitiy
            - detailed description of the activitiy
            - Any suggestions (optional)
        (include food breaks)
        - Evening (timmings):
            - Activitiy
            - detailed description of the activitiy
            - Any suggestions (optional)
        ......

        NOTE:- You cannot show anything null to user, try to add gven infromation only, still if you didn't have enough infromation you can skip it or invent information based on your capabilities

        OUTPUT FORMAT:
        iternary should look like this
        1. Hotel Suggestions
        2. Travel (flight/train) suggestions
        3. Day by day iternary
        4. Extra suggestions
        5. Budget estimation (if you can)

    """
    result = await MODEL.ainvoke(prompt)
    return {'itinerary': result.content}

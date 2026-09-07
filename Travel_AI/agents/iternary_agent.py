from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent


load_dotenv()

MODEL = ChatGoogleGenerativeAI(model = 'gemini-3.5-flash-lite')

PROMPT = """
You are an itinerary generator for a Travel AI system.

Generate a practical and detailed day-by-day itinerary using ONLY the provided:

* User Query
* Travel route and transport details
* Areas/places to explore
* Hotel suggestions

Rules:

* Generate a plan for EVERY day of the trip duration.
* For each day, clearly mention:

  * Day number and date (if available)
  * Morning, afternoon, and evening activities
  * Places to visit
  * Transport between places, if provided
  * Travel time, if provided
  * Cost of each activity/transport, if provided
  * Hotel/accommodation
  * Meals or other expenses only when provided
  * Total estimated cost for that day
* Group nearby places together to minimize unnecessary travel.
* Consider the hotel location when organizing activities.
* Consider arrival and departure details when planning the first and last day.
* Distribute places realistically across the trip duration.
* Do not overcrowd any day.
* Prioritize the most relevant places.
* Include nearby destinations only when practical considering travel time and cost.
* Clearly distinguish between provided costs and approximate costs.
* Try to return costs in the user's currency when the currency can be determined from the provided information.
* Do not invent places, timings, prices, transport, travel times, or other information.
* Do not search for additional information.
* If required information is unavailable, leave the corresponding field empty/null according to the output schema.

Return ONLY the structured itinerary according to the provided output schema.

Also the Output should in markdown format


"""

async def iternary_agent(state):
    agent = create_agent(
            model = MODEL,
            system_prompt = PROMPT
        )
    itinerary_data = "\n".join([
        f"User Query: {state.get('user_query', 'Not provided')}",
        f"Duration: {state.get('duration', 'Not provided')} days",
        f"Number of guests: {state.get('number_guest', 'Not provided')}",
        f"Transport: {state.get('transport', 'Not provided')}",
        f"Route details: {state.get('route_selection', 'Not provided')}",
        f"Places to explore: {state.get('place_selection', 'Not provided')}",
        f"Hotel suggestions: {state.get('hotel_agent_response', 'Not provided')}",
    ])

    response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": itinerary_data }]},
    )
    print("===== Iternary Started Generating =====")
    return {"itinerary" : str(response["messages"][-1].content)}
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

MODEL = ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite')


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

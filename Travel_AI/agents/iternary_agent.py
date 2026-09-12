from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter


load_dotenv()

MODEL = ChatOpenRouter(
    model="qwen/qwen3.7-flash",
    temperature=0.2,
    max_tokens=2500,
)

# print(MODEL.invoke("Hi My name is Manan"))
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
            - detailed description of the activitiy(max 2-3 lines)
            - Any suggestions (optional)
        (include food breaks)
        - Evening (timmings):
            - Activitiy
            - detailed description of the activitiy(max 2-3 lines)
            - Any suggestions (optional)
        ......

        NOTE:- You cannot show anything null to user, try to add gven infromation only, still if you didn't have enough infromation you can skip it or invent information based on your capabilities

        OUTPUT FORMAT:
        iternary should look like this
        ## 1. Hotel Suggestions
            - Give 2-3 useful hotel options from the research.
            - Include short reason/details only when available.
        ## 2. Travel Suggestions
            - Give the best available flight/train option(s).
            - Include departure/arrival or other useful details only when provided.
        ## 3. Day by day iternary
        ## 4. Extra Suggestions
        - 3-5 concise practical tips.
        ## 5. Budget Estimation
        - Provide an estimate only if the research contains enough information.
        - Clearly separate known prices from approximate estimate

    """
    result = await MODEL.ainvoke(prompt)
    return {'itinerary': result.content}

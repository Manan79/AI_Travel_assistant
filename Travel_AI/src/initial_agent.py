from langchain_groq import ChatGroq
import asyncio
from dotenv import load_dotenv
from pydantic import Field, BaseModel 
from langchain_core.prompts import PromptTemplate
from typing import Literal , List
load_dotenv()



LLM = ChatGroq(model='openai/gpt-oss-120b')

class StructuredLLM(BaseModel):
    boarding_station: str = Field(
        description="Boarding station/city from the user query"
    )
    destination_station: str = Field(
        description="Destination station/city from the user query"
    )
    number_guest: int = Field(
        description="Number of people travelling"
    )
    duration: int = Field(
        description="Duration of the trip in days"
    )
    transport: str = Field(
        description="Mode of travelling"
    )
    country: str = Field(
        description="Which country is the user travelling to"
    )


structured_llm_response = LLM.with_structured_output(
    StructuredLLM,
    method='json_schema',
)


async def processing_query(state):
    prompt = PromptTemplate.from_template("""
    You are an expert travel assistant, you have to break the user query into
    1. boarding_station
    2. destination_station
    3. number_guest
    4. duration
    5. mode_of_transport
    6. country

    User_query: {user_query}

    The application may provide a default origin of New Delhi if the user does not specify an origin.

    ##Rule
    1. Remove the suffix if any like: Jalandhar city -> Jalandhar
    2. If the user mention state or country in destination, then you can return str containing (Capital or Famous places)
        -ex :- Make a plan from New Delhi to Punjab, Return :- Amritsar
        -ex :- Make a plan from New Delhi to Goa, Return :- Panaji
        (You can make decision on your own based if there is Ambiguity)

    3. If user does not clearly specify the source then take the capital city of the place
        - ex:- Make an plan from punjab to Rameshwaram, Source = 'Chandigarh'

    4. If the boarding_station and destination_station lies in India then set the country to India,
       otherwise set the country Abroad.

    5. If the source and destination is in India, then you can use the railway tool.
    """)
    message = prompt.format(user_query=state.get('user_query', ''))
    response = await structured_llm_response.ainvoke(message)
    print("Intital Agent Responded")
    return response.model_dump()

from langchain_groq import ChatGroq
import asyncio
from dotenv import load_dotenv
from pydantic import Field, BaseModel 
from langchain_core.prompts import PromptTemplate
from typing import Literal , List
load_dotenv()



LLM = ChatGroq(model= 'qwen/qwen3.6-27b')

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
        default='Train',
        description= "Mode of travelling"
    )


structured_llm_response = LLM.with_structured_output(StructuredLLM)


async def processing_query(state):
    prompt = PromptTemplate.from_template("""
    You are an expert travel assistant, you have to broke the user query into 
    1. boarding_station
    2. destination_station
    3. number_guest
    4. duration
    5. Mode of transport (default Train)

    User_query: {user_query}

    The application may provide a default origin of New Delhi if the user does not specify an origin.

    ##Rule
    1. Remove the suffix if any like: Jalandhar city -> Jalandhar
    2. If the user mention state or country in destination, then you can return str containing (Capital or Famous places)
        -ex :- Make a plan from New Delhi to Punjab, Retrun :- Amritsar
        -ex :- Make a plan from New Delhi to Goa, Retrun :- Panaji
        (You can make decision on your own based if there is Ambiguity)

    3. If user donot clearly specify the source then take the capital city of the place
        - ex:- Make an plan from punjab to Rameshwaram, Source = 'Chandigarh'
""")
    message = prompt.format(user_query = state['user_query'])
    response = await structured_llm_response.ainvoke(message)
    return response.model_dump()

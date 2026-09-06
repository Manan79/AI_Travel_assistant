from langchain_groq import ChatGroq
import asyncio
from dotenv import load_dotenv
from pydantic import Field, BaseModel
from langchain_core.prompts import PromptTemplate

load_dotenv()



LLM = ChatGroq(model= 'qwen/qwen3.8-27b')

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


structured_llm_response = LLM.with_structured_output(StructuredLLM)


async def processing_query(state):
    prompt = PromptTemplate.from_template("""
    You are an expert travel assistant, you have to broke the user query into 
    1. boarding_station
    2. destination_station
    3. number_guest
    4. duration

    User_query: {user_query}


    ##Rule
    1. Remove the suffix if any like: Jalandhar city -> Jalandhar
""")
    message = prompt.format(user_query = state['user_query'])
    response = await structured_llm_response.ainvoke(message)

    return response




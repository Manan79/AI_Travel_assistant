import uvicorn
from fastapi.responses import HTMLResponse , JSONResponse
from fastapi import FastAPI , Request
from pydantic import BaseModel
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates


import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Travel_AI.src.run_workflow import workflow_invoke

app = FastAPI(
    title= 'AI Travel Planner',
    description='Langgraph app for designing AI based travel iternary',
    version="1.0.0"
)

class TravelRequest(BaseModel):
    message: str
    thread_id : str

@app.get("/health")
async def health():
    return{
        
        "Status": "ok",
        "message": "AI Travel Planner" 
    }

# @app.post("/api/travel")
# async def travel_planeer(request_data: TravelRequest):
#     try: 
#         user_data = request_data.message.strip()
#         if not user_data:
#             return JSONResponse(
#                 status_code=400
#             )
#         result = await workflow_invoke(
#             user_query = user_data,
#             config = request_data.thread_id
#         )

#         # return JSONResponse(content = {
#         #     "sucess": True,
#         #     "thread_id": result['thread_id'],
#         #     "answer": result


#         # })
#         return result
#     except Exception as e:
#         print(e)
@app.post("/api/travel")
async def travel_planner(request_data: TravelRequest):
    try:
        user_data = request_data.message.strip()
        if not user_data:
            return JSONResponse(status_code=400)


        result = await workflow_invoke(
            user_query=user_data,
            thread_id= request_data.thread_id
        )
        

        return {
            "success": True,
            "thread_id": request_data.thread_id,
            "answer": result.get("itinerary", "")
        }
    except Exception as e:
        print(e)
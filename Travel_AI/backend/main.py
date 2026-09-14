import uvicorn
from fastapi.responses import HTMLResponse , JSONResponse
from fastapi import FastAPI , Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
# from fastapi.templating import Jinja2Templates

import sys
from pathlib import Path
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Travel_AI.src.run_workflow import workflow_invoke

STATIC_DIR = Path(__file__).resolve().parents[2] / "static"

app = FastAPI(
    title= 'AI Travel Planner',
    description='Langgraph app for designing AI based travel iternary',
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def index():
    index_file = STATIC_DIR / "index.html"
    return HTMLResponse(index_file.read_text(encoding="utf-8"))

@app.get("/chat")
async def chat_page():
    chat_file = STATIC_DIR / "chat.html"
    return HTMLResponse(chat_file.read_text(encoding="utf-8"))

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
            return JSONResponse(content={"detail": "empty message"}, status_code=400)

        result = await workflow_invoke(
            user_query=user_data,
            thread_id=request_data.thread_id,
        )

        itinerary = result.get("itinerary", "") if isinstance(result, dict) else str(result)
        if not itinerary:
            itinerary = ""

        return JSONResponse(content={
            "success": True,
            "thread_id": request_data.thread_id,
            "answer": itinerary,
        })
    except Exception as e:
        print(e)
        return JSONResponse(content={
            "success": False,
            "thread_id": request_data.thread_id,
            "answer": f"Unable to generate itinerary: {str(e)}"
        }, status_code=500)
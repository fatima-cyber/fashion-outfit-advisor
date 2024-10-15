from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import UploadFile, File
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from chat.conversation_engine import conversational_agent_executor
from langchain_core.messages import HumanMessage
from chat.session_manager import SessionManager
from schemas import UserInput

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Fashion Recommendation App",
    description="An API for generating fashion recommendations based on user inputs and image analysis.",
    version="1.0.0"
)

# Initialize the SessionManager
SessionManager = SessionManager()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # You can add more checks here, like database connectivity
        return JSONResponse(content={"status": "healthy"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Chat endpoint
@app.post("/chat")
async def chat(user_input: UserInput, session_id: int):
    try:
        # Send the user input to the LLM
        response = conversational_agent_executor.invoke(
            {"messages": [HumanMessage(content=user_input.message)]},
            {"configurable": {"session_id": str(session_id)}},
        )
        
        # Extract the AI's response
        ai_response = response["output"]
        
        return JSONResponse(content={"response": ai_response}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Clear chat endpoint
@app.post("/clear-chat")
async def clear_chat():
    try:
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Create session ID endpoint
@app.post("/create-session-id")
async def create_session_id():
    try:
        session_id = SessionManager.get_new_session_id()
        return JSONResponse(content={"session_id": session_id}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session ID: {str(e)}")

# Upload image endpoint
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(None)):  # Allow file to be None
    try:
        if file is None:
            return print("No file uploaded")
        else:
            image_bytes = await file.read()
            return {"image": image_bytes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
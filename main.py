from fastapi import FastAPI
from pydantic import BaseModel
import cohere
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get API key safely
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(COHERE_API_KEY)

class chatRequest(BaseModel):
    prompt: str

class chatResponse(BaseModel):
    response: str

app = FastAPI()


@app.get("/maths")
def calculation():
    answer = 1 + 1
    return {"answer": answer}

@app.get("/")
def root():
    return {"message": "Hello, World!"}
    
@app.post("/chat", response_model=chatResponse)
def chat(request: chatRequest):
    
    user_prompt = request.prompt
    
    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": user_prompt}],
    )

    final_response = response.message.content[0].text

    return chatResponse(response=f"Cohere said this: {final_response}")

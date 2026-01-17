from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import generate_questions

app = FastAPI()

class InterviewRequest(BaseModel):
    role: str
    skills: list
    level: str

@app.post("/generate-questions")
def get_questions(data: InterviewRequest):
    questions = generate_questions(data.role, data.skills, data.level)
    return {"questions": questions}

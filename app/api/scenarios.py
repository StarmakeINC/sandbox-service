from fastapi import APIRouter, Depends, HTTPException, Form
from ..schemas import ScenarioResponse, ScenarioCreate, UserMessage
import json
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import AuthService
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.services.sandbox_service import Sandbox

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/scenarios")
async def create_scenario(
    scenario_data: ScenarioCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = AuthService.handle_token(token)
    user_id = payload.get("user_id") 
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: user_id not found")
    if not scenario_data.text:
        raise HTTPException(status_code=400, detail="Текст сценария обязателен")
    scenario = Sandbox.create_scenario(db, user_id, scenario_data)
    return scenario

@router.get("/get_last_script")
def list_user_scenarios(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = AuthService.handle_token(token)
    user_id = payload.get("user_id") 
    return Sandbox.get_last_script(db, user_id)

import os
from openai import OpenAI
import asyncio

api_key = os.getenv('OPENAI_API_KEY') 
assistant_id = os.getenv('SCENARIO_ASSISTANT_ID') 
organization_id = os.getenv('ORGANIZATION_ID')  
project_id = os.getenv('PROJECT_ID')  

client = OpenAI(
    api_key=api_key,
    organization=organization_id,
    project=project_id,
)

async def wait_on_run(run, thread):
    while run.status in ["queued", "in_progress"]:
        await asyncio.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    return run

@router.post("/generate-response")
async def generate_response(
    data: UserMessage,
):
    user_message = data.user_message
    if not user_message:
        raise HTTPException(status_code=400, detail="Сообщение пользователя не может быть пустым.")
    thread = client.beta.threads.create()
    message_content = (
        f"Ответ в формате json: Ответь на русском языке. Напиши детальную идею для озвучки видео, "
        f"Вот задача: {user_message}"
    )
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_content
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    run = await wait_on_run(run, thread)
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = None
    for message in messages.data:
        if message.role == "assistant":
            assistant_response = message.content[0].text.value
            break
    if assistant_response:
        assistant_response = json.loads(assistant_response)
        variants = [
            [assistant_response["idea"], assistant_response["script"], "Теги: " + ", ".join(assistant_response["tags"])]
        ]
        return JSONResponse(content={"variants": variants})
    else:
        raise HTTPException(status_code=500, detail="Ответ ассистента не найден.")

import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from pydantic import BaseModel

app = FastAPI()

# TrueFoundry AI Gateway endpoint — handles routing, fallback, and auth.
# The model name is "<provider-account-name>/<integration-name>" from routing.yaml.
# Docs: https://docs.truefoundry.com/gateway/quick-start
client = ChatNVIDIA(
    model=os.environ["GATEWAY_MODEL"],        # nemotron-routing/nemotron
    api_key=os.environ["TFY_API_KEY"],        # TrueFoundry API key (PAT or VAT)
    base_url=os.environ["TFY_BASE_URL"] + "/api/llm/v1",
    temperature=1,
    top_p=0.95,
    max_completion_tokens=4096,
    model_kwargs={
        "reasoning_budget": 4096,
        "chat_template_kwargs": {"enable_thinking": True},
    },
)


class ChatRequest(BaseModel):
    message: str
    stream: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    messages = [{"role": "user", "content": req.message}]

    if req.stream:
        def generate():
            for chunk in client.stream(messages):
                # Nemotron Super returns reasoning tokens separately before the answer
                if chunk.additional_kwargs.get("reasoning_content"):
                    yield chunk.additional_kwargs["reasoning_content"]
                if chunk.content:
                    yield chunk.content
        return StreamingResponse(generate(), media_type="text/plain")

    thinking, answer = "", ""
    for chunk in client.stream(messages):
        if chunk.additional_kwargs.get("reasoning_content"):
            thinking += chunk.additional_kwargs["reasoning_content"]
        if chunk.content:
            answer += chunk.content

    return {"thinking": thinking or None, "response": answer}

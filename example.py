from langchain_nvidia_ai_endpoints import ChatNVIDIA

TFY_BASE_URL = "https://<your-org>.truefoundry.cloud"
TFY_API_KEY = "<your-tfy-token>"

client = ChatNVIDIA(
    model="nvidia/nemotron-super",   # or nvidia/nemotron-nano
    api_key=TFY_API_KEY,
    base_url=TFY_BASE_URL + "/api/llm/v1",
    temperature=1,
    top_p=0.95,
    max_completion_tokens=4096,
    model_kwargs={
        "reasoning_budget": 4096,
        "chat_template_kwargs": {"enable_thinking": True},
    },
)

thinking, answer = "", ""
for chunk in client.stream([{"role": "user", "content": "Which is greater: 9.8 or 9.11?"}]):
    if chunk.additional_kwargs.get("reasoning_content"):
        thinking += chunk.additional_kwargs["reasoning_content"]
    if chunk.content:
        answer += chunk.content

print("thinking:", thinking)
print("answer:", answer)

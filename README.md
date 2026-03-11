# Nemotron on TrueFoundry AI Gateway

Route traffic to **Nemotron 3 Super 120B** (primary) with automatic fallback to **Nemotron 3 Nano 30B** on errors — using [TrueFoundry AI Gateway](https://docs.truefoundry.com/gateway/intro-to-llm-gateway).

```
your app → TFY Gateway → Nemotron 3 Super 120B  (priority 1, 12B active, reasoning model)
                       ↘ Nemotron 3 Nano 30B    (fallback on 429 / 5xx, 3B active, fast)
```

## Files

| File | What it does |
|------|-------------|
| `gateway.yaml` | Registers NVIDIA's hosted API as a self-hosted model provider |
| `routing.yaml` | Creates a virtual model with priority routing Super → Nano |
| `main.py` | FastAPI service that calls the gateway |
| `truefoundry.yaml` | Deploys the FastAPI service on TrueFoundry |

## Deploy with Claude

You can use [TrueFoundry Agent Skills](https://github.com/truefoundry/tfy-agent-skills) with Claude to deploy this entirely via chat. Install the skills and set these three env vars:

```bash
TFY_HOST=https://<your-org>.truefoundry.cloud
TFY_BASE_URL=https://<your-org>.truefoundry.cloud
TFY_API_KEY=<your-tfy-token>
```

Then just ask Claude to apply the gateway config and deploy the service.

## Setup

### 1. Get an NVIDIA API key
Sign up at [build.nvidia.com](https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b) → avatar → **Get API Key**

### 2. Store secrets
Dashboard → **Secrets** → create a secret group → add your NVIDIA API key.
Reference format: `tfy-secret://<tenant>:<secret-group>:<key>` — [docs](https://docs.truefoundry.com/docs/manage-secrets)

Update `bearer_token` in `gateway.yaml` with your secret reference.

### 3. Apply gateway config

```bash
export TFY_HOST=https://<your-org>.truefoundry.cloud
export TFY_API_KEY=<your-tfy-token>

tfy apply -f gateway.yaml   # adds Nemotron Super + Nano as models
tfy apply -f routing.yaml   # sets up priority routing
```

See [routing docs](https://docs.truefoundry.com/gateway/load-balancing-overview) for weight-based and latency-based options.

### 4. Call the gateway directly

```python
from langchain_nvidia_ai_endpoints import ChatNVIDIA

client = ChatNVIDIA(
    model="nemotron-routing/nemotron",
    api_key="<your-tfy-token>",
    base_url="https://<your-org>.truefoundry.cloud/api/llm/v1",
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
```

### 5. (Optional) Deploy the FastAPI service

Fill in the placeholders in `truefoundry.yaml`, then:

```bash
tfy deploy -f truefoundry.yaml --no-wait
```

```bash
# Non-streaming
curl -X POST https://<your-service-url>/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Which is greater: 9.8 or 9.11?"}'

# Streaming
curl -X POST https://<your-service-url>/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum entanglement", "stream": true}'
```

## How the gateway auth works

The gateway uses your **TFY token** (PAT or VAT) for authentication — not the NVIDIA key directly.
The NVIDIA key is stored as a TFY secret and injected by the gateway as a `Bearer` token when calling NVIDIA's API.

For production, use a **Virtual Access Token (VAT)** scoped to only the models it needs — [docs](https://docs.truefoundry.com/docs/generating-truefoundry-api-keys).

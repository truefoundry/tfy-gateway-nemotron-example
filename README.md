# Nemotron 3 on TrueFoundry AI Gateway

[Nemotron 3 Super](https://research.nvidia.com/labs/nemotron/Nemotron-3/) is NVIDIA's latest open model — 120B parameters, 12B active at inference via a hybrid Mamba-Transformer MoE. 5x higher throughput than the previous generation.

🚀 [Sign up for TrueFoundry](https://www.truefoundry.com/register) &nbsp;·&nbsp; 🔑 [Get NVIDIA API key](https://build.nvidia.com)

---

## Option 1: UI

Add Nemotron to the gateway directly from the TrueFoundry dashboard — no code needed.

📺 [Watch the walkthrough](https://www.loom.com/share/5342a8be7e62444f810dcb9e2144c0c7)

---

## Option 2: CLI

**1. Store your NVIDIA API key as a TFY secret**

Dashboard → Secrets → create a group → add `NVIDIA-API-KEY = nvapi-...` — [docs](https://docs.truefoundry.com/docs/manage-secrets)

Update `bearer_token` in `gateway.yaml` with your secret reference.

**2. Apply**

```bash
export TFY_HOST=https://<your-org>.truefoundry.cloud
export TFY_API_KEY=<your-tfy-token>

tfy apply -f gateway.yaml
```

**3. Call the model**

Set `TFY_BASE_URL` and `TFY_API_KEY` in `example.py` and run it.

---

## Option 3: Claude + TrueFoundry Skills

Install [TrueFoundry Agent Skills](https://github.com/truefoundry/tfy-agent-skills), set these env vars:

```bash
TFY_HOST=https://<your-org>.truefoundry.cloud
TFY_BASE_URL=https://<your-org>.truefoundry.cloud
TFY_API_KEY=<your-tfy-token>
```

Then ask Claude:

> "Deploy Nemotron 3 thinking model to TrueFoundry"

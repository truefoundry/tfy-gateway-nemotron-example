# Nemotron 3 on TrueFoundry AI Gateway

[Nemotron 3 Super](https://research.nvidia.com/labs/nemotron/Nemotron-3/) is NVIDIA's latest open model — 120B parameters, 12B active at inference via a hybrid Mamba-Transformer MoE. 5x higher throughput than the previous generation.

This repo shows how to add Nemotron 3 Super and Nano to TrueFoundry AI Gateway in one YAML file.

📺 [Watch the video](#) &nbsp;·&nbsp; 🚀 [Sign up for TrueFoundry](https://www.truefoundry.com/register) &nbsp;·&nbsp; 🔑 [Get NVIDIA API key](https://build.nvidia.com)

---

**1. Store your NVIDIA API key as a TFY secret**

Dashboard → Secrets → create a group → add `NVIDIA-API-KEY = nvapi-...` — [docs](https://docs.truefoundry.com/docs/manage-secrets)

Update `bearer_token` in `gateway.yaml` with your secret reference.

**2. Apply**

```bash
export TFY_HOST=https://<your-org>.truefoundry.cloud
export TFY_API_KEY=<your-tfy-token>

tfy apply -f gateway.yaml
```

**3. Run `example.py`**

Set `TFY_BASE_URL` and `TFY_API_KEY` in `example.py` and run it.

---

## Deploy with Claude

Install [TrueFoundry Agent Skills](https://github.com/truefoundry/tfy-agent-skills), set `TFY_HOST`, `TFY_BASE_URL`, `TFY_API_KEY` and ask:

> "Deploy Nemotron 3 thinking model to TrueFoundry"

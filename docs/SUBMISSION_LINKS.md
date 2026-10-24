# Vortex OrderGuard — Submission Links

**Team:** Vortex  
**Project:** Vortex OrderGuard  
**Hackathon:** SDC Hackathon 2026 — Domain 2: Orbyte Smart SME Challenge

| Resource | Link | Status |
| --- | --- | --- |
| GitHub Repository | https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template | ✅ Ready |
| Live Demo | https://sdc-hackathon-submission-template.replit.app | ✅ Published |
| RunPod Serverless API | `POST https://api.runpod.ai/v2/ojf4e2o9yj00cy/runsync` | ✅ Authenticated API endpoint |
| RunPod Proof of Use | https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template/blob/vortex-orderguard-submission/docs/RUNPOD_PROOF_OF_USE.md | ✅ Evidence available |
| Slide Deck | Pending | ⏳ To complete |
| Demo Video | Pending | ⏳ To complete |

## Notes

- The live Replit deployment uses synthetic demo records only.
- The RunPod Serverless endpoint is an authenticated **POST API**, not a normal browser page. Opening the base URL in a browser sends a GET request and is not a valid endpoint test.
- RunPod authentication credentials/API keys are intentionally not included in this public repository.
- RunPod is used for GPU-assisted OCR inference. It does not approve or reject supplier cases.
- OCR output is treated as extraction input; OrderGuard applies deterministic comparison rules, the Trust Gate, and human approval before consequential actions.
- Slide Deck and Demo Video links will be added after the final pitch materials are completed.

## Proof of Use

- Replit proof: `docs/REPLIT_PROOF_OF_USE.md`
- RunPod proof: `docs/RUNPOD_PROOF_OF_USE.md`
- Live demo: https://sdc-hackathon-submission-template.replit.app

## RunPod invocation format

The Serverless endpoint is called server-side with authentication, for example:

```text
POST https://api.runpod.ai/v2/ojf4e2o9yj00cy/runsync
Authorization: Bearer <RUNPOD_API_KEY>
Content-Type: application/json
```

The API key is stored only as a server-side secret and must never be committed to GitHub or placed in public submission materials.

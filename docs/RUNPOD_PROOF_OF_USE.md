# RunPod Proof of Use — Vortex OrderGuard

Team: **Vortex**  
Project: **Vortex OrderGuard**  
Hackathon: **SDC Hackathon 2026**

## Verified RunPod evidence

The RunPod Serverless OCR worker was successfully built and executed for the OrderGuard prototype.

Verified execution result:

- Status: `COMPLETED`
- `ok`: `true`
- `gpu_used`: `true`
- GPU: `NVIDIA GeForce RTX 5090`
- Delay time: `9.33s`
- Execution time: `5.57s`
- OCR engine: EasyOCR
- Runtime: RunPod Serverless GPU worker

The GPU worker is used only for OCR/extraction. OrderGuard then applies deterministic comparison rules, the Trust Gate, and human approval before any consequential action.

## Synthetic test data

The test invoice is synthetic and uses the FreshFarm example created for the hackathon demo. No real supplier or customer production data is required for the proof-of-use flow.

## Submission PDF

Formal file name: `submission/SDC2026_Vortex_Runpod_POU.pdf`

The PDF contains the RunPod build evidence, completed GPU OCR request, GPU details, and the synthetic invoice evidence used in the demo.

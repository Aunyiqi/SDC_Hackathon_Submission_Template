# Replit Deployment Guide — Vortex OrderGuard

Replit is compulsory for the SDC Hackathon. This guide keeps the deployment aligned with the current OrderGuard codebase and avoids committing secrets to GitHub.

## 1. Import the repository

Import this repository into Replit:

`https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template`

The repository default branch is `vortex-orderguard-submission`, which is the competition version.

## 2. Verify the project files

After import, confirm these paths exist:

- `src/main.py`
- `src/app.py`
- `src/templates/`
- `src/static/`
- `requirements.txt`
- `.replit`

The included `.replit` file runs:

```bash
python src/main.py
```

## 3. Add Replit Secrets

Do not put real secrets in `.env`, README files, screenshots or Git commits.

For owner controls to work, configure both of these Replit Secrets:

```text
FLASK_SECRET_KEY=<at least 32 characters>
ORDERGUARD_OWNER_ACCESS_CODE=<at least 24 characters>
```

Recommended for the deployed HTTPS version:

```text
ORDERGUARD_COOKIE_SECURE=true
```

Optional AI extraction:

```text
DEEPSEEK_API_KEY=<your key>
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_API_URL=https://api.deepseek.com/chat/completions
```

If `DEEPSEEK_API_KEY` is absent, the manual structured-entry fallback still works.

## 4. Run the app

Press **Run** in Replit. The app listens on `0.0.0.0` and uses the `PORT` environment variable when Replit supplies one.

Expected first-use behavior:

1. Public/read-only pages can render safely.
2. Open **Owner access**.
3. Enter the value stored in `ORDERGUARD_OWNER_ACCESS_CODE`.
4. Create or run a synthetic demo case.
5. Confirm the Priority Action Queue, Trust Gate, human clarification, owner decision and audit/outbox flow.

## 5. Deployment proof to retain

Before submission, keep evidence that Replit was genuinely used:

- screenshot of the Replit workspace with this project open;
- screenshot of a successful running OrderGuard app;
- Replit project link;
- deployed/public prototype URL if available;
- project history or other usage evidence requested by the organizer.

Never include the owner access code, Flask secret key or DeepSeek API key in screenshots.

## 6. Judge demo sequence

For a short demo, use this order:

1. **Discrepancy** — shows quantity/price mismatch and Money at Risk.
2. **Repeat issue** — shows supplier pattern memory and raises the case in the Priority Action Queue.
3. **Ambiguous unit** — shows Trust Gate blocking a consequential action until a person clarifies the data.
4. **Clean match** — shows that OrderGuard does not create unnecessary actions.

## 7. RunPod note

The current prototype does not train, fine-tune or self-host a GPU model. DeepSeek is accessed as an external API. Do not claim RunPod usage unless the team actually adds and demonstrates a GPU workload.

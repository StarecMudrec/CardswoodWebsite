# Purchase Notify Service

Small service that receives the purchase webhook from the website backend and sends a Telegram message to the user via the game bot. **It does not grant items** — you handle that manually or in your bot.

## Environment

| Variable | Description |
|----------|-------------|
| `PURCHASE_NOTIFY_BOT_TOKEN` or `CW_BOT_TOKEN` | Game bot token (for sending the message). |
| `PURCHASE_WEBHOOK_SECRET` or `BOT_PURCHASE_WEBHOOK_SECRET` | Optional. If set, backend must send `Authorization: Bearer <secret>`. |
| `PORT` | HTTP port (default: 8081). |

## Endpoint

- **POST** `/webhook/purchase` — same JSON the backend sends: `event`, `user_id`, `items`, `total_amount`, `currency`, etc.

## Run locally

```bash
cd purchase_notify
pip install -r requirements.txt
export CW_BOT_TOKEN=your_bot_token
python app.py
```

## Docker

The `docker-compose.yml` in the repo root includes a `purchase_notify` service. Set `CW_BOT_TOKEN` (and optionally `BOT_PURCHASE_WEBHOOK_SECRET`) in your env or `.env`.

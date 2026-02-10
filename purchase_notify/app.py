"""
Purchase notify service: receives webhook from the website backend and sends
a Telegram message to the user via the game bot. Does not grant items.
"""
import os
import logging
from aiohttp import web
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("PURCHASE_NOTIFY_BOT_TOKEN") or os.getenv("CW_BOT_TOKEN")
WEBHOOK_SECRET = (os.getenv("PURCHASE_WEBHOOK_SECRET") or os.getenv("BOT_PURCHASE_WEBHOOK_SECRET") or "").strip()


async def handle_purchase(request: web.Request) -> web.Response:
    if request.method != "POST":
        return web.Response(status=405, text="Method not allowed")

    if WEBHOOK_SECRET:
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {WEBHOOK_SECRET}":
            logger.warning("Purchase webhook: invalid or missing Authorization")
            return web.Response(status=401, text="Unauthorized")

    try:
        data = await request.json()
    except Exception as e:
        logger.warning("Purchase webhook: invalid JSON: %s", e)
        return web.Response(status=400, text="Invalid JSON")

    event = data.get("event")
    user_id = data.get("user_id")
    items = data.get("items", [])
    total_amount = data.get("total_amount", "")
    currency = data.get("currency", "RUB")

    if event != "purchase_complete" or not user_id:
        logger.warning("Purchase webhook: invalid payload event=%s user_id=%s", event, user_id)
        return web.Response(status=400, text="Invalid payload")

    if not BOT_TOKEN:
        logger.error("PURCHASE_NOTIFY_BOT_TOKEN or CW_BOT_TOKEN not set")
        return web.Response(status=500, text="Bot not configured")

    # Build message
    lines = ["🎉 <b>Оплата прошла успешно!</b>\n"]
    lines.append("Ваш заказ оплачен. Выдачу товаров в боте обработают вручную или через вашу систему.\n")
    if items:
        lines.append("<b>Куплено:</b>")
        for it in items:
            name = it.get("name", "—")
            qty = int(it.get("quantity", 1))
            price = it.get("price")
            if qty > 1:
                lines.append(f"• {name} × {qty}")
            else:
                lines.append(f"• {name}")
        if total_amount:
            lines.append(f"\n<b>Сумма:</b> {total_amount} {currency}")

    text = "\n".join(lines)

    try:
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
        await bot.send_message(chat_id=user_id, text=text)
        await bot.session.close()
    except Exception as e:
        logger.exception("Failed to send Telegram message to %s: %s", user_id, e)
        return web.Response(status=500, text="Failed to send message")

    return web.Response(status=200, text="OK")


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/webhook/purchase", handle_purchase)
    return app


def main():
    port = int(os.getenv("PORT", "8081"))
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

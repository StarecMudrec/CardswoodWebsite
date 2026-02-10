import os
import hmac
from hashlib import sha256, md5
import uuid
from decimal import Decimal
from datetime import datetime
from urllib.parse import urlencode
import logging
import time
import random
from types import SimpleNamespace

import aiosqlite
from quart import Quart, request, redirect, url_for, make_response, jsonify, send_from_directory, session, render_template
from joserfc.errors import JoseError
from sqlalchemy import select, text
import httpx

from config import Config
from models import AuthToken, Card, Season, Comment, AllowedUser, Order
from async_db import get_async_session, get_sqlite_conn, SQLITE_DB_PATH

logging.basicConfig(level=logging.DEBUG)

app = Quart(__name__)
app.config.from_object(Config)
# Quart session (cookie-based)
try:
    from quart.sessions import SecureCookieSessionInterface
    app.session_interface = SecureCookieSessionInterface()
except Exception:
    pass


@app.route("/placeholder.jpg")
async def serve_placeholder():
    return await send_from_directory("public", "placeholder.jpg")


async def is_authenticated(req, sess):
    token = req.args.get("token") or req.cookies.get("token")
    if not token:
        logging.debug("No token found in request")
        return False, None
    try:
        async with get_async_session() as db_session:
            r = await db_session.execute(select(AuthToken).where(AuthToken.token == token))
            auth_token = r.scalar_one_or_none()
        if auth_token is None:
            logging.debug("Token not found in database")
            return False, None
        sess["user_id"] = auth_token.user_id
        logging.debug("Token is valid (database check)")
        return True, auth_token.user_id
    except Exception as e:
        logging.exception(f"Authentication error: {e}")
        return False, None


async def download_avatar(url, user_id):
    if not url:
        return None
    avatar_dir = "backend/avatars"
    os.makedirs(avatar_dir, exist_ok=True)
    filename = os.path.join(avatar_dir, f"{user_id}.jpg")
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            r.raise_for_status()
            with open(filename, "wb") as f:
                f.write(r.content)
        return filename
    except httpx.HTTPError as e:
        logging.error(f"Error downloading avatar from {url}: {e}")
        return None

# Telegram OAuth Callback Route
@app.route("/auth/telegram-callback")
async def telegram_callback():
    user_id = request.args.get("id", type=int)
    query_hash = request.args.get("hash")
    if user_id is None or query_hash is None:
        return "Invalid request", 400

    params = request.args.to_dict()
    data_check_string = "\n".join(sorted(f"{x}={y}" for x, y in params.items() if x not in ("hash", "next")))
    computed_hash = hmac.new(Config.BOT_TOKEN_HASH.digest(), data_check_string.encode(), sha256).hexdigest()
    if not hmac.compare_digest(computed_hash, query_hash):
        return "Authorization failed. Please try again", 401

    telegram_id = request.args.get("id", type=int)
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    username = request.args.get("username")
    photo_url = request.args.get("photo_url")
    session["telegram_id"] = telegram_id
    session["telegram_first_name"] = first_name
    session["telegram_last_name"] = last_name
    session["telegram_username"] = username
    session["telegram_photo_url"] = photo_url

    db_token = str(uuid.uuid4())
    auth_token = AuthToken(token=db_token, user_id=user_id)
    try:
        async with get_async_session() as db_session:
            db_session.add(auth_token)
        logging.debug(f"Stored token {db_token} for user {user_id} in database")
    except Exception as e:
        logging.exception(f"Database error saving token: {e}")
        return "Database error", 500

    response = await make_response(redirect(url_for("home")))
    response.set_cookie("token", db_token, httponly=True, secure=True)
    response.set_data(f"""
      <script>
        window.parent.postMessage('auth-success', 'http://localhost:5173');
      </script>
    """)
    return response


@app.route("/auth/logout", methods=["GET", "POST"])
async def logout():
    token = request.cookies.get("token")
    if token:
        try:
            async with get_async_session() as db_session:
                r = await db_session.execute(select(AuthToken).where(AuthToken.token == token))
                auth_token = r.scalar_one_or_none()
                if auth_token:
                    await db_session.delete(auth_token)
            logging.debug(f"Deleted token {token} from database")
        except Exception as e:
            logging.exception(f"Database error deleting token: {e}")
            return "Database error", 500

    session.clear()
    response = await make_response(jsonify({"status": "logged_out"}))
    response.delete_cookie("token")
    return response


@app.after_request
async def apply_csp(response):
    response.headers["Content-Security-Policy"] = (
        "frame-ancestors 'self' https://cardswood.ru; "
        "frame-src 'self' https://oauth.telegram.org;"
    )
    return response


@app.route("/")
async def return_home():
    return redirect(url_for("home"))


@app.route("/login")
async def login():
    is_auth, user_id = await is_authenticated(request, session)
    if is_auth:
        return redirect(url_for("home"))
    if request.args.get("check_auth"):
        is_auth, user_id = await is_authenticated(request, session)
        return jsonify({"type": "auth-status", "isAuthenticated": is_auth, "userId": user_id}), 200
    return jsonify({"type": "auth-status", "isAuthenticated": False, "userId": None}), 200


@app.route("/home")
async def home():
    is_auth, _ = await is_authenticated(request, session)
    return await render_template("homepage.html", is_auth=is_auth)



# API ROUTES

@app.route("/db-status")
async def db_status():
    try:
        async with get_async_session() as db_session:
            r = await db_session.execute(text("SELECT version()"))
            pg_version = r.scalar_one()
        async with get_sqlite_conn() as conn:
            cur = await conn.execute("SELECT sqlite_version()")
            row = await cur.fetchone()
            sqlite_version = row[0]
            cur2 = await conn.execute("SELECT COUNT(*) FROM cards")
            row2 = await cur2.fetchone()
            cards_count = row2[0]
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "postgres_version": pg_version,
        "sqlite_version": sqlite_version,
        "cards_count": cards_count,
    })


@app.route("/card_imgs/<filename>")
async def serve_card_image(filename):
    return await send_from_directory("card_imgs", filename)


@app.route("/api/seasons")
async def get_seasons():
    try:
        async with get_sqlite_conn() as conn:
            cur = await conn.execute("SELECT DISTINCT season FROM cards WHERE season IS NOT NULL")
            rows = await cur.fetchall()
            seasons = [row[0] for row in rows]
        return jsonify(sorted(seasons)), 200
    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({"error": "Failed to fetch seasons"}), 500

@app.route("/api/seasons", methods=["POST"])
async def add_season():
    is_auth, _ = await is_authenticated(request, session)
    if not is_auth:
        return jsonify({"error": "Unauthorized"}), 401
    current_user_username = session.get("telegram_username")
    async with get_async_session() as db_session:
        r = await db_session.execute(select(AllowedUser).where(AllowedUser.username == current_user_username))
        allowed_user = r.scalar_one_or_none()
    if not current_user_username or not allowed_user:
        return jsonify({"error": "You are not allowed to add seasons"}), 403
    new_season_uuid = str(uuid.uuid4())
    new_season = Season(uuid=new_season_uuid, name="_")
    async with get_async_session() as db_session:
        db_session.add(new_season)
    return jsonify({"message": "Season added successfully", "uuid": new_season_uuid, "name": new_season.name}), 201

@app.route("/api/seasons/<season_uuid>", methods=["PUT"])
async def update_season(season_uuid):
    is_auth, _ = await is_authenticated(request, session)
    if not is_auth:
        return jsonify({"error": "Unauthorized"}), 401
    current_user_username = session.get("telegram_username")
    async with get_async_session() as db_session:
        r = await db_session.execute(select(AllowedUser).where(AllowedUser.username == current_user_username))
        if not current_user_username or r.scalar_one_or_none() is None:
            return jsonify({"error": "You are not allowed to update seasons"}), 403
        s = await db_session.execute(select(Season).where(Season.uuid == season_uuid))
        season = s.scalar_one_or_none()
    if not season:
        return jsonify({"error": "Season not found"}), 404
    data = await request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        async with get_async_session() as db_session:
            s = await db_session.execute(select(Season).where(Season.uuid == season_uuid))
            season = s.scalar_one()
            if "name" in data:
                season.name = data["name"]
        return jsonify({"message": "Season updated successfully", "uuid": season.uuid, "name": season.name}), 200
    except Exception as e:
        logging.error(f"Error updating season: {e}")
        return jsonify({"error": "Error updating season"}), 500

@app.route("/api/seasons/<season_uuid>", methods=["DELETE"])
async def delete_season(season_uuid):
    is_auth, _ = await is_authenticated(request, session)
    if not is_auth:
        return jsonify({"error": "Unauthorized"}), 401
    current_user_username = session.get("telegram_username")
    async with get_async_session() as db_session:
        r = await db_session.execute(select(AllowedUser).where(AllowedUser.username == current_user_username))
        if not current_user_username or r.scalar_one_or_none() is None:
            return jsonify({"error": "You are not allowed to delete seasons"}), 403
        s = await db_session.execute(select(Season).where(Season.uuid == season_uuid))
        season = s.scalar_one_or_none()
        if not season:
            return jsonify({"error": "Season not found"}), 404
        await db_session.delete(season)
    return jsonify({"message": "Season deleted successfully"}), 200

@app.route("/api/cards/<season_id>")
async def get_cards(season_id):
    RARITY_ORDER = {
        "EPISODICAL": 1, "SECONDARY": 2, "FAMOUS": 3, "MAINCHARACTER": 4,
        "MOVIE": 5, "SERIES": 6, "ACHIEVEMENTS": 7,
    }
    try:
        sort_field = request.args.get("sort", "id")
        sort_direction = request.args.get("direction", "asc")
        async with get_sqlite_conn() as conn:
            if sort_field == "rarity":
                cur = await conn.execute(
                    "SELECT id, photo, name, rarity, points FROM cards WHERE season = ?",
                    (int(season_id),),
                )
                rows = await cur.fetchall()
                cards = [dict(zip(["id", "img", "name", "rarity", "points"], row)) for row in rows]
                cards.sort(key=lambda x: RARITY_ORDER.get(x["rarity"], 0))
                if sort_direction.lower() == "desc":
                    cards.reverse()
                return jsonify(cards), 200
            elif sort_field == "amount":
                query = """
                    SELECT c.id, c.photo, c.name, c.rarity, c.points, COUNT(f.card_id) as amount
                    FROM cards c LEFT JOIN filmstrips f ON c.id = f.card_id
                    WHERE c.season = ? GROUP BY c.id, c.photo, c.name, c.rarity, c.points
                    ORDER BY amount {}
                """.format(sort_direction)
                cur = await conn.execute(query, (int(season_id),))
                rows = await cur.fetchall()
                cards = [dict(zip(["id", "img", "name", "rarity", "points", "amount"], row)) for row in rows]
                return jsonify(cards), 200
            else:
                query = """
                    SELECT id, id as uuid, photo as img, name, rarity, points
                    FROM cards WHERE season = ? ORDER BY {} {}
                """.format(sort_field, sort_direction)
                cur = await conn.execute(query, (int(season_id),))
                rows = await cur.fetchall()
                cards = [dict(zip(["id", "uuid", "img", "name", "rarity", "points"], row)) for row in rows]
                return jsonify(cards), 200
    except ValueError:
        return jsonify({"error": "Invalid season ID"}), 400
    except Exception as e:
        logging.error(f"Error fetching cards: {str(e)}")
        return jsonify({"error": "Failed to fetch cards"}), 500

@app.route("/api/cards", methods=["POST"])
async def add_card():
    is_auth, _ = await is_authenticated(request, session)
    if not is_auth:
        return jsonify({"error": "Unauthorized"}), 401
    current_user_username = session.get("telegram_username")
    async with get_async_session() as db_session:
        r = await db_session.execute(select(AllowedUser).where(AllowedUser.username == current_user_username))
        if not current_user_username or r.scalar_one_or_none() is None:
            return jsonify({"error": "You are not allowed to add cards"}), 403
    form = await request.form
    files = await request.files
    card_uuid = form.get("uuid")
    category = form.get("category")
    name = form.get("name")
    description = form.get("description")
    season_id = form.get("season_id")
    img_file = files.get("img")
    img = None
    if img_file and getattr(img_file, "filename", None):
        allowed_extensions = {"png", "jpg", "jpeg", "gif"}
        if "." not in img_file.filename or img_file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
            return jsonify({"error": "Unsupported file type"}), 400
        img_filename = str(card_uuid) + os.path.splitext(img_file.filename)[1]
        img_path = os.path.join("card_imgs", img_filename)
        body = await img_file.read()
        with open(img_path, "wb") as f:
            f.write(body)
        img = img_filename
    if not all([card_uuid, img, category, name, description, season_id]):
        return jsonify({"error": "Missing required fields"}), 400
    new_card = Card(uuid=card_uuid, img=img, category=category, name=name, description=description, season_id=int(season_id))
    try:
        async with get_async_session() as db_session:
            db_session.add(new_card)
        return jsonify({"message": "Card added successfully", "uuid": new_card.uuid}), 201
    except Exception as e:
        logging.error(f"Error adding card: {e}")
        return jsonify({"error": "Error adding card"}), 500

@app.route("/api/cards/<card_id>", methods=["DELETE"])
async def delete_card(card_id):
    is_auth, _ = await is_authenticated(request, session)
    if not is_auth:
        return jsonify({"error": "Unauthorized"}), 401
    current_user_username = session.get("telegram_username")
    async with get_async_session() as db_session:
        r = await db_session.execute(select(AllowedUser).where(AllowedUser.username == current_user_username))
        if not current_user_username or r.scalar_one_or_none() is None:
            return jsonify({"error": "You are not allowed to delete cards"}), 403
        c = await db_session.execute(select(Card).where(Card.uuid == card_id))
        card = c.scalar_one_or_none()
        if card is None:
            return jsonify({"error": "Card not found"}), 404
        if card.img and os.path.exists(os.path.join("card_imgs", card.img)):
            os.remove(os.path.join("card_imgs", card.img))
        await db_session.delete(card)
    return jsonify({"message": "Card deleted successfully"}), 200

@app.route("/api/check_permission", methods=["GET"])
async def check_permission():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username not provided"}), 400
    async with get_async_session() as db_session:
        r = await db_session.execute(select(AllowedUser).where(AllowedUser.username == username))
        user = r.scalar_one_or_none()
    return jsonify({"is_allowed": user is not None})
    
@app.route("/api/card_info/<card_id>")
async def get_card_info(card_id):
    try:
        async with get_sqlite_conn() as conn:
            cur = await conn.execute(
                "SELECT photo, name, rarity, points, number, [drop], event, season FROM cards WHERE id = ?",
                (int(card_id),),
            )
            row = await cur.fetchone()
            if not row:
                return jsonify({"error": "Card not found"}), 404
            cur2 = await conn.execute("SELECT COUNT(*) FROM filmstrips WHERE card_id = ?", (card_id,))
            row2 = await cur2.fetchone()
            card_count = row2[0]
        return jsonify({
            "id": card_id, "uuid": card_id, "season_id": row[7], "img": row[0],
            "category": row[2], "name": row[1], "description": f"Amount: {card_count}",
        }), 200
    except ValueError:
        return jsonify({"error": "Invalid card ID"}), 400
    except Exception as e:
        logging.error(f"SQLite error: {str(e)}")
        return jsonify({"error": "Failed to fetch card info"}), 500

@app.route("/api/cards/<card_id>", methods=["PUT"])
async def update_card(card_id):
    is_auth, _ = await is_authenticated(request, session)
    if not is_auth:
        return jsonify({"error": "Unauthorized"}), 401
    data = await request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    async with get_async_session() as db_session:
        r = await db_session.execute(select(Card).where(Card.id == int(card_id)))
        card = r.scalar_one_or_none()
        if not card:
            return jsonify({"error": "Card not found"}), 404
        if "name" in data:
            card.name = data["name"]
        if "description" in data:
            card.description = data["description"]
        if "category" in data:
            card.category = data["category"]
        if "season_uuid" in data:
            s = await db_session.execute(select(Season).where(Season.uuid == data["season_uuid"]))
            season = s.scalar_one_or_none()
            if not season:
                return jsonify({"error": "Season not found"}), 404
            card.season_id = season.id
    return jsonify({"message": "Card updated successfully"}), 200
        
@app.route("/api/cards/<card_uuid>/image", methods=["PUT"])
async def update_card_image(card_uuid):
    is_auth, _ = await is_authenticated(request, session)
    if not is_auth:
        return jsonify({"error": "Unauthorized"}), 401
    current_user_username = session.get("telegram_username")
    async with get_async_session() as db_session:
        r = await db_session.execute(select(AllowedUser).where(AllowedUser.username == current_user_username))
        if not current_user_username or r.scalar_one_or_none() is None:
            return jsonify({"error": "You are not allowed to update card images"}), 403
        c = await db_session.execute(select(Card).where(Card.uuid == card_uuid))
        card = c.scalar_one_or_none()
    if not card:
        return jsonify({"error": "Card not found"}), 404
    files = await request.files
    if "image" not in files:
        return jsonify({"error": "No image file provided"}), 400
    img_file = files["image"]
    allowed_extensions = {"png", "jpg", "jpeg", "gif"}
    if "." not in img_file.filename or img_file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
        return jsonify({"error": "Unsupported file type"}), 400
    img_filename = str(card.uuid) + os.path.splitext(img_file.filename)[1].lower()
    img_path = os.path.join("card_imgs", img_filename)
    try:
        if card.img and os.path.exists(os.path.join("card_imgs", card.img)) and card.img != img_filename:
            os.remove(os.path.join("card_imgs", card.img))
        body = await img_file.read()
        with open(img_path, "wb") as f:
            f.write(body)
        async with get_async_session() as db_session:
            c = await db_session.execute(select(Card).where(Card.uuid == card_uuid))
            card = c.scalar_one()
            card.img = img_filename
        return jsonify({"message": "Card image updated successfully", "img": img_filename}), 200
    except Exception as e:
        logging.error(f"Error updating card image: {e}")
        return jsonify({"error": "Error updating card image"}), 500

@app.route("/api/season_info/<int:season_id>")
async def get_season_info(season_id):
    try:
        season_num = int(season_id)
        season_info = {"id": season_num, "uuid": season_num, "name": "Season " + str(season_num)}
        return jsonify(season_info), 200
    except ValueError:
        return jsonify({"error": "Invalid season ID format"}), 400
    except Exception as e:
        logging.error(f"Error fetching season info: {e}")
        return jsonify({"error": "Failed to fetch season info"}), 500


@app.route("/api/comments/<card_id>")
async def get_comments(card_id):
    async with get_async_session() as db_session:
        stmt = select(Comment).where(Comment.card_id == int(card_id)).order_by(Comment.id)
        r = await db_session.execute(stmt)
        comments = r.scalars().all()
    comments_data = [c.present() for c in comments]
    return jsonify(comments_data), 200


@app.route("/api/check_auth")
async def check_auth():
    is_auth, user_id = await is_authenticated(request, session)
    return jsonify({"isAuthenticated": is_auth, "userId": user_id}), 200


@app.route("/api/user", methods=["GET"])
async def get_user_info():
    user_id = session.get("user_id")
    if user_id:
        user_data = {
            "id": session.get("telegram_id"),
            "first_name": session.get("telegram_first_name"),
            "last_name": session.get("telegram_last_name"),
            "photo_url": session.get("telegram_photo_url"),
            "username": session.get("telegram_username"),
        }
        return jsonify(user_data), 200
    return jsonify({"error": "User not authenticated"}), 401


# --- PayAnyWay (MONETA.Assistant) payment ---
# Формирование подписи в запросе на оплату (документация PayAnyWay, служба сопровождения):
# MNT_SIGNATURE = MD5(MNT_ID + MNT_TRANSACTION_ID + MNT_AMOUNT + MNT_CURRENCY_CODE + MNT_SUBSCRIBER_ID + ТЕСТОВЫЙ_РЕЖИМ + КОД_ПРОВЕРКИ_ЦЕЛОСТНОСТИ_ДАННЫХ)
# Важно: MNT_AMOUNT — с двумя десятичными знаками, точка («1.23», «123.00»); MNT_SUBSCRIBER_ID при отсутствии — пустая строка; ТЕСТОВЫЙ РЕЖИМ — «1» или «0».
# Всегда передаём MNT_TEST_MODE в форме («1»/«0») и используем то же значение в подписи (пример поддержки: ...RUB012345 — перед ключом «0»).
# Включить лог: PAYANYWAY_DEBUG_SIGNATURE=1 (в env или docker-compose).
#
# Если «Неправильная подпись» остаётся при верной формуле — проверить: (1) код проверки в ЛК = PAYANYWAY_MNT_INTEGRITY_CODE без кавычек/пробелов/BOM;
# (2) ключ только ASCII; (3) PAYANYWAY_PAYMENT_URL — тот же домен, что в ЛК (payanyway.ru vs assistant.moneta.ru); (4) в ЛК магазин привязан к тому же MNT_ID.
def _payanyway_form_signature(mnt_id, mnt_transaction_id, mnt_amount, mnt_currency_code, key, mnt_subscriber_id="", test_mode=None):
    key = (key or "").strip().strip("\"'").strip("\ufeff")
    if test_mode is None:
        test_mode = "1" if getattr(Config, "PAYANYWAY_TEST_MODE", False) else "0"
    test_mode = "1" if test_mode in (True, "1", 1) else "0"
    try:
        amt = f"{float(mnt_amount):.2f}"
    except (ValueError, TypeError):
        amt = str(mnt_amount) if mnt_amount else ""
    mnt_id = str(mnt_id).strip()
    mnt_transaction_id = str(mnt_transaction_id).strip()
    mnt_currency_code = (mnt_currency_code or "").strip()
    mnt_subscriber_id = (mnt_subscriber_id or "").strip()
    raw = f"{mnt_id}{mnt_transaction_id}{amt}{mnt_currency_code}{mnt_subscriber_id}{test_mode}{key}"
    signature = md5(raw.encode("utf-8")).hexdigest()
    if os.environ.get("PAYANYWAY_DEBUG_SIGNATURE"):
        try:
            key.encode("ascii")
        except UnicodeEncodeError:
            logging.warning("PayAnyWay: ключ содержит не-ASCII символы — возможна ошибка кодировки (ЛК vs UTF-8)")
        logging.info(
            "PayAnyWay form signature debug: MNT_ID=%r MNT_TRANSACTION_ID=%r MNT_AMOUNT=%r MNT_CURRENCY_CODE=%r "
            "MNT_SUBSCRIBER_ID=%r MNT_TEST_MODE=%r key_len=%d | строка_без_ключа=%r | MNT_SIGNATURE=%s",
            mnt_id, mnt_transaction_id, amt, mnt_currency_code,
            mnt_subscriber_id, test_mode, len(key), raw[: -len(key)] if key else raw, signature,
        )
    return signature


# Официальная формула (Check URL / callback): MNT_SIGNATURE = MD5(MNT_COMMAND + MNT_ID + MNT_TRANSACTION_ID + MNT_OPERATION_ID + MNT_AMOUNT + MNT_CURRENCY_CODE + MNT_SUBSCRIBER_ID + MNT_TEST_MODE + КОД_ПРОВЕРКИ). Отсутствующие параметры — пустая строка.
def _payanyway_signature(mnt_id, mnt_transaction_id, mnt_amount, mnt_currency_code, key, mnt_command="", mnt_operation_id="", mnt_subscriber_id="", mnt_test_mode=None):
    """Подпись для callback (Check URL): порядок полей фиксирован, отсутствующие = ''."""
    if mnt_test_mode is None:
        mnt_test_mode = "1" if getattr(Config, "PAYANYWAY_TEST_MODE", False) else ""
    if mnt_amount:
        try:
            amt = f"{float(mnt_amount):.2f}"
        except (ValueError, TypeError):
            amt = str(mnt_amount)
    else:
        amt = ""
    raw = f"{mnt_command or ''}{mnt_id}{mnt_transaction_id}{mnt_operation_id or ''}{amt}{mnt_currency_code}{mnt_subscriber_id or ''}{mnt_test_mode}{key}"
    return md5(raw.encode("utf-8")).hexdigest()


@app.route("/api/orders", methods=["POST"])
async def create_order():
    is_auth, user_id = await is_authenticated(request, session)
    if not is_auth:
        return jsonify({"error": "Войдите в аккаунт, чтобы совершить покупку"}), 401
    data = await request.get_json()
    if not data or "items" not in data:
        return jsonify({"error": "Missing items"}), 400
    items = data["items"]
    if not items:
        return jsonify({"error": "Cart is empty"}), 400
    mnt_id = (Config.PAYANYWAY_MNT_ID or "").strip().strip("\ufeff")
    key = (Config.PAYANYWAY_SIGNATURE_KEY or "").strip().strip("\"'").strip("\ufeff")
    if not mnt_id or not key:
        logging.warning("PayAnyWay not configured")
        return jsonify({"error": "Payment system is not configured"}), 503
    total = sum(Decimal(str(it["price"])) * int(it.get("quantity", 1)) for it in items)
    order_number = str(uuid.uuid4()).replace("-", "")[:32]
    amount_str = f"{total:.2f}"
    currency = "RUB"
    description = "Cardswood shop" if not items else items[0].get("name", "Order") + (" + ..." if len(items) > 1 else "")
    try:
        order = Order(
            order_number=order_number,
            user_id=user_id,
            amount=total,
            currency=currency,
            status="pending",
            items=items,
        )
        async with get_async_session() as db_session:
            db_session.add(order)
            await db_session.flush()
            order_id = order.id
    except Exception as e:
        logging.exception(f"Create order error: {e}")
        return jsonify({"error": "Failed to create order"}), 500
    mnt_test_mode = "1" if getattr(Config, "PAYANYWAY_TEST_MODE", False) else "0"
    signature = _payanyway_form_signature(
        mnt_id, order_number, amount_str, currency, key,
        mnt_subscriber_id="", test_mode=mnt_test_mode
    )
    payment_url = Config.PAYANYWAY_PAYMENT_URL
    params = {
        "MNT_ID": mnt_id,
        "MNT_TRANSACTION_ID": order_number,
        "MNT_AMOUNT": amount_str,
        "MNT_CURRENCY_CODE": currency,
        "MNT_DESCRIPTION": description[:255],
        "MNT_SIGNATURE": signature,
        "MNT_SUCCESS_URL": Config.PAYANYWAY_SUCCESS_URL,
        "MNT_FAIL_URL": Config.PAYANYWAY_FAIL_URL,
        "MNT_TEST_MODE": mnt_test_mode,
    }
    if getattr(Config, "PAYANYWAY_CHECK_URL", None):
        params["MNT_CHECK_URL"] = Config.PAYANYWAY_CHECK_URL
    payment_url_with_params = f"{payment_url}?{urlencode(params)}"
    return jsonify({
        "order_id": order_id,
        "order_number": order_number,
        "payment_url": payment_url_with_params,
        "form_fields": params,
    }), 201


def _payanyway_callback_verify(data, key):
    """Проверка подписи callback по официальной формуле: MD5(MNT_COMMAND + MNT_ID + MNT_TRANSACTION_ID + MNT_OPERATION_ID + MNT_AMOUNT + MNT_CURRENCY_CODE + MNT_SUBSCRIBER_ID + MNT_TEST_MODE + key). Отсутствующие параметры — пустая строка."""
    def get(k, default=""):
        v = data.get(k)
        return (v or "").strip() if v is not None else default
    mnt_command = get("MNT_COMMAND")
    mnt_id = get("MNT_ID")
    mnt_transaction_id = get("MNT_TRANSACTION_ID")
    mnt_operation_id = get("MNT_OPERATION_ID")
    mnt_amount = get("MNT_AMOUNT")
    mnt_currency_code = get("MNT_CURRENCY_CODE")
    mnt_subscriber_id = get("MNT_SUBSCRIBER_ID")
    mnt_test_mode = get("MNT_TEST_MODE")
    return _payanyway_signature(
        mnt_id, mnt_transaction_id, mnt_amount, mnt_currency_code, key,
        mnt_command=mnt_command, mnt_operation_id=mnt_operation_id,
        mnt_subscriber_id=mnt_subscriber_id, mnt_test_mode=mnt_test_mode
    )


async def _notify_bot_purchase(order, max_retries=3):
    """
    Notify purchase_notify service about completed order.
    Retries up to max_retries times with exponential backoff.
    Returns (notification_status, notification_error) for persistence.
    """
    url = getattr(Config, "BOT_PURCHASE_NOTIFY_URL", None)
    if not url:
        logging.info(f"Order {order.order_number}: BOT_PURCHASE_NOTIFY_URL not set, skipping notification")
        return "skipped", None

    payload = {
        "event": "purchase_complete",
        "order_id": order.id,
        "order_number": order.order_number,
        "user_id": order.user_id,
        "items": [
            {"id": it.get("id"), "name": it.get("name"), "price": float(it.get("price", 0)), "quantity": int(it.get("quantity", 1))}
            for it in (order.items or [])
        ],
        "total_amount": str(order.amount),
        "currency": order.currency or "RUB",
        "completed_at": datetime.utcnow().isoformat() + "Z",
    }
    headers = {}
    if getattr(Config, "BOT_PURCHASE_WEBHOOK_SECRET", None):
        headers["Authorization"] = f"Bearer {Config.BOT_PURCHASE_WEBHOOK_SECRET}"
    
    import asyncio
    last_error = None
    
    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(url, json=payload, headers=headers, timeout=10.0)
                if r.status_code < 400:
                    logging.info(f"Order {order.order_number}: Notification sent successfully (attempt {attempt})")
                    return "sent", None
                else:
                    last_error = f"HTTP {r.status_code}: {r.text[:200]}"
                    logging.warning(f"Order {order.order_number}: Notification failed (attempt {attempt}/{max_retries}): {last_error}")
        except httpx.HTTPError as e:
            last_error = str(e)
            logging.warning(f"Order {order.order_number}: Notification failed (attempt {attempt}/{max_retries}): {last_error}")
        except Exception as e:
            last_error = str(e)
            logging.exception(f"Order {order.order_number}: Unexpected error during notification (attempt {attempt}/{max_retries}): {e}")
        
        if attempt < max_retries:
            wait_time = 2 ** attempt  # Exponential backoff: 2s, 4s, 8s
            logging.info(f"Order {order.order_number}: Retrying notification in {wait_time}s...")
            await asyncio.sleep(wait_time)
    
    # All retries failed
    error_msg = (last_error or "unknown")[:512]
    logging.error(
        f"Order {order.order_number} (user_id={order.user_id}, amount={order.amount} {order.currency}): "
        f"Failed to send notification after {max_retries} attempts. Last error: {last_error}. "
        f"Order is marked as PAID but user may not have received Telegram notification. "
        f"Manual intervention may be required to grant items or notify user."
    )
    return "failed", error_msg


async def _grant_test_item(conn: "aiosqlite.Connection", tg_id: int):
    """Тестовый товар: просто выдаёт карту с id=1."""
    try:
        await conn.execute(
            "INSERT INTO filmstrips (tg_id, card_id) VALUES (?, ?)",
            (tg_id, 1),
        )
        logging.info("Grant: test item -> card_id=1 to tg_id=%s", tg_id)
    except Exception as e:
        logging.exception("Grant: failed to give test card to tg_id=%s: %s", tg_id, e)


async def _grant_subscription(conn: "aiosqlite.Connection", tg_id: int, premium: bool = False):
    """
    Выдача подписки:
    - устанавливаем subs=True и days=текущее время (как делает rq.changesubs в боте).
    - для премиум-подписки дополнительно начисляем немного очков магазина.
    """
    now_ts = int(time.time())
    try:
        cur = await conn.execute("SELECT subs, days, shoppoints FROM users WHERE tg_id = ?", (tg_id,))
        row = await cur.fetchone()
        if not row:
            logging.warning("Grant: subscription — user tg_id=%s not found in users table", tg_id)
            return
        subs, days, shoppoints = row[0], row[1], row[2]
        # Если подписка уже есть, просто обновим отсчёт 30 дней с текущего момента
        new_subs = 1
        new_days = now_ts
        new_shops = shoppoints
        if premium:
            # Премиум даёт дополнительный буст очков магазина
            bonus = 50000
            new_shops = (shoppoints or 0) + bonus
            logging.info("Grant: premium subscription -> +%s shoppoints to tg_id=%s", bonus, tg_id)
        await conn.execute(
            "UPDATE users SET subs = ?, days = ?, shoppoints = ? WHERE tg_id = ?",
            (new_subs, new_days, new_shops, tg_id),
        )
        logging.info(
            "Grant: %s subscription set for tg_id=%s (subs=%s, days=%s, shoppoints=%s)",
            "premium" if premium else "basic",
            tg_id,
            new_subs,
            new_days,
            new_shops,
        )
    except Exception as e:
        logging.exception("Grant: failed to set subscription for tg_id=%s: %s", tg_id, e)


async def _get_random_card_ids_by_rarity(conn: "aiosqlite.Connection", rarities, count: int):
    """Возвращает список случайных card_id указанной редкости/редкостей."""
    if not rarities or count <= 0:
        return []
    placeholders = ",".join("?" for _ in rarities)
    try:
        cur = await conn.execute(f"SELECT id FROM cards WHERE rarity IN ({placeholders})", tuple(rarities))
        rows = await cur.fetchall()
        ids = [r[0] for r in rows]
        if not ids:
            logging.warning("Grant: no cards found for rarities=%r", rarities)
            return []
        return [random.choice(ids) for _ in range(count)]
    except Exception as e:
        logging.exception("Grant: failed to select cards by rarity %r: %s", rarities, e)
        return []


async def _get_random_card_ids_any(conn: "aiosqlite.Connection", count: int):
    """Случайные карты любой редкости."""
    if count <= 0:
        return []
    try:
        cur = await conn.execute("SELECT id FROM cards")
        rows = await cur.fetchall()
        ids = [r[0] for r in rows]
        if not ids:
            logging.warning("Grant: no cards found in cards table")
            return []
        return [random.choice(ids) for _ in range(count)]
    except Exception as e:
        logging.exception("Grant: failed to select random cards: %s", e)
        return []


async def _insert_cards_for_user(conn: "aiosqlite.Connection", tg_id: int, card_ids):
    """Добавляет пользователю указанные карты в таблицу filmstrips."""
    if not card_ids:
        return
    try:
        await conn.executemany(
            "INSERT INTO filmstrips (tg_id, card_id) VALUES (?, ?)",
            [(tg_id, cid) for cid in card_ids],
        )
        logging.info("Grant: added cards %r to tg_id=%s", card_ids, tg_id)
    except Exception as e:
        logging.exception("Grant: failed to insert cards %r for tg_id=%s: %s", card_ids, tg_id, e)


async def _grant_pack(conn: "aiosqlite.Connection", tg_id: int, pack_type: str):
    """
    Выдаёт награду за покупку пака:
    - regular: 3 карты EPISODICAL/SECONDARY/FAMOUS, 1 любая карта, 1 MOVIE/SERIES
    - rare:    4 любых карты, 1 MOVIE/SERIES
    - epic:    2 любых карты, 3 MOVIE/SERIES
    """
    try:
        if pack_type == "regular":
            ids_main = await _get_random_card_ids_by_rarity(conn, ["EPISODICAL", "SECONDARY", "FAMOUS"], 3)
            ids_any = await _get_random_card_ids_any(conn, 1)
            ids_movie = await _get_random_card_ids_by_rarity(conn, ["MOVIE", "SERIES"], 1)
            await _insert_cards_for_user(conn, tg_id, ids_main + ids_any + ids_movie)
        elif pack_type == "rare":
            ids_any = await _get_random_card_ids_any(conn, 4)
            ids_movie = await _get_random_card_ids_by_rarity(conn, ["MOVIE", "SERIES"], 1)
            await _insert_cards_for_user(conn, tg_id, ids_any + ids_movie)
        elif pack_type == "epic":
            ids_any = await _get_random_card_ids_any(conn, 2)
            ids_movie = await _get_random_card_ids_by_rarity(conn, ["MOVIE", "SERIES"], 3)
            await _insert_cards_for_user(conn, tg_id, ids_any + ids_movie)
        else:
            logging.warning("Grant: unknown pack_type=%r for tg_id=%s", pack_type, tg_id)
    except Exception as e:
        logging.exception("Grant: failed to grant pack %r for tg_id=%s: %s", pack_type, tg_id, e)


async def _grant_movie_home_alone(conn: "aiosqlite.Connection", tg_id: int):
    """
    Выдаёт пользователю карту фильма HOME ALONE.
    Если такой карты нет в таблице cards — выдаём карту id=1.
    """
    card_id = None
    try:
        cur = await conn.execute(
            "SELECT id FROM cards WHERE name LIKE ? LIMIT 1",
            ("%HOME ALONE%",),
        )
        row = await cur.fetchone()
        if row:
            card_id = row[0]
        else:
            logging.warning("Grant: HOME ALONE card not found, fallback to card_id=1")
            card_id = 1
    except Exception as e:
        logging.exception("Grant: failed to find HOME ALONE card: %s", e)
        card_id = 1

    try:
        await conn.execute(
            "INSERT INTO filmstrips (tg_id, card_id) VALUES (?, ?)",
            (tg_id, card_id),
        )
        logging.info("Grant: HOME ALONE card_id=%s granted to tg_id=%s", card_id, tg_id)
    except Exception as e:
        logging.exception("Grant: failed to insert HOME ALONE card for tg_id=%s: %s", tg_id, e)


async def _grant_career_level(conn: "aiosqlite.Connection", tg_id: int, level: str):
    """
    Уровни карьеры (учёба/бизнес) пока не интегрированы в бота напрямую,
    поэтому реализуем их как заметный бонус очков магазина.
    """
    bonus = 0
    if level == "study":
        bonus = 100000
    elif level == "business":
        bonus = 200000
    else:
        logging.warning("Grant: unknown career level %r", level)
        return

    try:
        cur = await conn.execute("SELECT shoppoints FROM users WHERE tg_id = ?", (tg_id,))
        row = await cur.fetchone()
        if not row:
            logging.warning("Grant: career %s — user tg_id=%s not found", level, tg_id)
            return
        shoppoints = row[0] or 0
        new_shops = shoppoints + bonus
        await conn.execute(
            "UPDATE users SET shoppoints = ? WHERE tg_id = ?",
            (new_shops, tg_id),
        )
        logging.info(
            "Grant: career %s -> +%s shoppoints to tg_id=%s (total=%s)",
            level,
            bonus,
            tg_id,
            new_shops,
        )
    except Exception as e:
        logging.exception("Grant: failed to grant career %s for tg_id=%s: %s", level, tg_id, e)


async def _grant_items_for_order(order):
    """
    Выдаёт внутриигровые награды за оплаченный заказ.
    Привязка по order.user_id (tg_id из бота) и item.id из Shop.vue.
    """
    tg_id = order.user_id
    if not tg_id:
        logging.warning("Grant: order %s has no user_id, skipping", order.order_number)
        return

    items = order.items or []
    if not items:
        logging.info("Grant: order %s has no items, nothing to grant", order.order_number)
        return

    logging.info("Grant: starting grant for order %s, tg_id=%s, items=%r", order.order_number, tg_id, items)

    # Открываем отдельно R/W соединение к той же БД, что использует бот
    conn = await aiosqlite.connect(SQLITE_DB_PATH)
    try:
        for it in items:
            pid = it.get("id")
            if pid is None:
                continue
            try:
                pid_int = int(pid)
            except (TypeError, ValueError):
                logging.warning("Grant: invalid product id %r in order %s", pid, order.order_number)
                continue

            if pid_int == 7:
                await _grant_test_item(conn, tg_id)
            elif pid_int == 1:
                await _grant_subscription(conn, tg_id, premium=False)
            elif pid_int == 2:
                await _grant_subscription(conn, tg_id, premium=True)
            elif pid_int == 3:
                await _grant_pack(conn, tg_id, "regular")
            elif pid_int == 4:
                await _grant_pack(conn, tg_id, "rare")
            elif pid_int == 6:
                await _grant_pack(conn, tg_id, "epic")
            elif pid_int == 5:
                await _grant_movie_home_alone(conn, tg_id)
            elif pid_int == 8:
                await _grant_career_level(conn, tg_id, "study")
            elif pid_int == 9:
                await _grant_career_level(conn, tg_id, "business")
            else:
                logging.info("Grant: unknown product id %s in order %s, skipping", pid_int, order.order_number)

        await conn.commit()
    except Exception as e:
        logging.exception("Grant: unexpected error while processing order %s: %s", order.order_number, e)
        try:
            await conn.rollback()
        except Exception:
            pass
    finally:
        await conn.close()


@app.route("/api/dev/test-grant", methods=["POST"])
async def dev_test_grant():
    """
    Тестовый эндпоинт для локальной выдачи товаров БЕЗ оплаты.
    Работает только в режиме PAYANYWAY_TEST_MODE (см. .env).

    Запрос: POST /api/dev/test-grant
    {
      "product_id": 7
    }
    """
    # Защита: только в тестовом режиме
    if not getattr(Config, "PAYANYWAY_TEST_MODE", False):
        return jsonify({"error": "Test grant disabled in non-test mode"}), 403

    is_auth, user_id = await is_authenticated(request, session)
    if not is_auth or not user_id:
        return jsonify({"error": "Войдите в аккаунт, чтобы тестировать выдачу"}), 401

    try:
        data = await request.get_json()
    except Exception:
        data = None
    if not data or "product_id" not in data:
        return jsonify({"error": "Missing product_id"}), 400

    try:
        product_id = int(data["product_id"])
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid product_id"}), 400

    # Эмулируем заказ с одним товаром
    dummy_order = SimpleNamespace(
        id=0,  # фейковый id заказа
        user_id=user_id,
        order_number=f"TEST-{uuid.uuid4().hex[:12]}",
        amount=Decimal("0.00"),
        currency="RUB",
        items=[{"id": product_id, "name": f"TEST_PRODUCT_{product_id}", "price": 0}],
    )

    logging.info(
        "DEV TEST GRANT: user_id=%s product_id=%s order_number=%s",
        user_id,
        product_id,
        dummy_order.order_number,
    )

    try:
        # Выдаём предметы так же, как при реальной оплате
        await _grant_items_for_order(dummy_order)
        # И шлём уведомление в purchase_notify / бота
        status, err = await _notify_bot_purchase(dummy_order)
        logging.info(
            "DEV TEST GRANT: notification status=%s err=%r for order %s",
            status,
            err,
            dummy_order.order_number,
        )
    except Exception as e:
        logging.exception("DEV TEST GRANT: error while granting items: %s", e)
        return jsonify({"error": "Grant failed"}), 500

    return jsonify({
        "status": "ok",
        "message": "Test grant executed",
        "user_id": user_id,
        "product_id": product_id,
    }), 200


async def _fulfill_order(order):
    logging.info(f"Order {order.order_number} fulfilled (items: {order.items})")

    # 1. Выдаём внутриигровые награды
    try:
        await _grant_items_for_order(order)
    except Exception as e:
        logging.exception("Order %s: error while granting items: %s", order.order_number, e)

    # 2. Уведомляем purchase_notify сервис / бота (Telegram-уведомление пользователю)
    status, err = await _notify_bot_purchase(order)
    try:
        async with get_async_session() as db_session:
            r = await db_session.execute(select(Order).where(Order.id == order.id))
            o = r.scalar_one_or_none()
            if o:
                o.notification_status = status
                o.notification_error = err
    except Exception as e:
        logging.warning(f"Order {order.order_number}: Could not save notification_status: {e}")


@app.route("/api/payment/payanyway/callback", methods=["POST", "GET"])
async def payanyway_callback():
    # Максимально подробное логирование входящего callback
    logging.info("PayAnyWay callback: incoming request method=%s path=%s", request.method, request.path)
    try:
        safe_headers = {k: v for k, v in request.headers.items() if k.lower() not in ("cookie", "authorization")}
        logging.info("PayAnyWay callback: headers=%r", safe_headers)
    except Exception as e:
        logging.warning("PayAnyWay callback: failed to log headers: %s", e)

    key = (Config.PAYANYWAY_SIGNATURE_KEY or "").strip().strip("\"'").strip("\ufeff")
    if not key:
        logging.warning("PayAnyWay callback: PAYANYWAY_MNT_INTEGRITY_CODE not set")
        return "CONFIG_ERROR", 500

    if request.method == "POST":
        data = await request.form
    else:
        data = request.args

    try:
        logged_data = {k: v for k, v in data.items()}
        logging.info("PayAnyWay callback: raw data=%r", logged_data)
    except Exception as e:
        logging.warning("PayAnyWay callback: failed to log data: %s", e)

    mnt_transaction_id = (data.get("MNT_TRANSACTION_ID") or "").strip()
    mnt_signature = (data.get("MNT_SIGNATURE") or "").strip()
    mnt_status = data.get("MNT_STATUS", "")
    logging.info(
        "PayAnyWay callback: MNT_TRANSACTION_ID=%r MNT_STATUS=%r received_signature=%r",
        mnt_transaction_id,
        mnt_status,
        mnt_signature,
    )
    if not mnt_transaction_id or not mnt_signature:
        logging.warning("PayAnyWay callback: missing MNT_TRANSACTION_ID or MNT_SIGNATURE")
        return "MISSING_PARAMS", 400

    expected_sig = _payanyway_callback_verify(data, key)
    logging.info("PayAnyWay callback: expected_signature=%r", expected_sig)

    if not hmac.compare_digest(expected_sig.lower(), mnt_signature.lower()):
        logging.warning("PayAnyWay callback: invalid signature (expected=%s, got=%s)", expected_sig, mnt_signature)
        return "INVALID_SIGNATURE", 400

    async with get_async_session() as db_session:
        r = await db_session.execute(select(Order).where(Order.order_number == mnt_transaction_id))
        order = r.scalar_one_or_none()

    if not order:
        logging.warning("PayAnyWay callback: order not found %r", mnt_transaction_id)
        # Сообщаем MONETA.Assistant об ошибке, чтобы он мог повторить уведомление
        return "FAIL", 200

    logging.info(
        "PayAnyWay callback: loaded order id=%s number=%s status=%s amount=%s currency=%s",
        order.id,
        order.order_number,
        order.status,
        getattr(order, "amount", None),
        getattr(order, "currency", None),
    )

    if order.status == "paid":
        # Повторное уведомление о уже оплаченном заказе — просто подтверждаем SUCCESS,
        # чтобы MONETA.Assistant прекратил ретраи.
        logging.info("PayAnyWay callback: order %s already paid, returning SUCCESS", order.order_number)
        return "SUCCESS", 200

    # Документация MONETA.Assistant: Pay URL получает отчёт о УЖЕ обработанном платеже,
    # без поля MNT_STATUS. Сам факт прихода отчёта с валидной подписью означает успешный платёж.
    logging.info("PayAnyWay callback: treating processed payment report as successful for order %s", mnt_transaction_id)
    try:
        async with get_async_session() as db_session:
            r = await db_session.execute(select(Order).where(Order.order_number == mnt_transaction_id))
            order = r.scalar_one()
            order.status = "paid"
            order.payanyway_payment_id = data.get("MNT_OPERATION_ID") or data.get("MNT_ID")
            order.updated_at = datetime.utcnow()
        logging.info(
            "PayAnyWay callback: order %s marked as paid (payanyway_payment_id=%r)",
            order.order_number,
            order.payanyway_payment_id,
        )
        # NOTE: Order is marked "paid" BEFORE notification. If notification fails,
        # the order remains paid (money already processed by PayAnyWay).
        # No automatic refunds - monitor logs for notification failures and handle manually.
        await _fulfill_order(order)
    except Exception as e:
        logging.exception("PayAnyWay callback commit error for order %r: %s", mnt_transaction_id, e)
        # В случае внутренней ошибки просим MONETA повторить уведомление.
        return "FAIL", 200

    # Важно: для Pay URL текстовым ответом должен быть SUCCESS или FAIL.
    # SUCCESS говорит MONETA.Assistant, что отчёт получен и деньги можно окончательно зачислить.
    return "SUCCESS", 200


if __name__ == "__main__":
    import hypercorn
    hypercorn.run(app, bind="0.0.0.0:8000")


@app.route("/avatars/<int:user_id>")
async def serve_avatar(user_id):
    avatar_dir = "backend/avatars"
    filename = f"{user_id}.jpg"
    try:
        return await send_from_directory(avatar_dir, filename)
    except FileNotFoundError:
        return "Avatar not found", 404


@app.route("/proxy/avatar")
async def proxy_avatar():
    url = request.args.get("url")
    logging.debug(f"Proxying avatar from URL: {url}")
    if not url:
        return "Missing image URL", 400
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            r.raise_for_status()
        return r.content, r.status_code, {"Content-Type": r.headers.get("Content-Type", "image/jpeg")}
    except httpx.HTTPError as e:
        logging.error(f"Error proxying avatar from {url}: {e}")
        return "Image not found or could not be downloaded.", 404
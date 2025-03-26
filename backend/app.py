import os
import hmac
from hashlib import sha256
import uuid  # For generating unique tokens

from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_migrate import Migrate
import jwt
from joserfc.errors import JoseError
import logging
from flask_sqlalchemy import SQLAlchemy  # Database integration
from models import db, AuthToken, Card, Season, Comment
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

db.init_app(app)

migrate = Migrate(app, db)

# Create the database tables
with app.app_context():
    db.create_all()


# Authentication Helper Function
def is_authenticated(request):
    token = request.args.get("token") or request.cookies.get("token")
    if not token:
        logging.debug("No token found in request")
        return False, None

    try:
        auth_token = AuthToken.query.filter_by(token=token).first()
        if auth_token is None:
            logging.debug("Token not found in database")
            return False, None

        logging.debug("Token is valid (database check)")
        return True, auth_token.user_id

    except Exception as e:
        logging.exception(f"Authentication error: {e}")
        return False, None


# Telegram OAuth Callback Route
@app.route("/auth/telegram-callback")
def telegram_callback():
    user_id = request.args.get("id", type=int)
    auth_date = request.args.get("auth_date")
    query_hash = request.args.get("hash")
    print(query_hash)

    if user_id is None or query_hash is None:
        return "Invalid request", 400

    # Extract parameters and sort them
    params = request.args.to_dict()
    data_check_string = "\n".join(sorted(f"{x}={y}" for x, y in params.items() if x not in ("hash", "next")))

    # Compute HMAC hash using BOT_TOKEN_HASH
    computed_hash = hmac.new(Config.BOT_TOKEN_HASH.digest(), data_check_string.encode(), sha256).hexdigest()

    if not hmac.compare_digest(computed_hash, query_hash):
        return "Authorization failed. Please try again", 401

    # Generate a unique token and store it in the database
    db_token = str(uuid.uuid4())
    auth_token = AuthToken(token=db_token, user_id=user_id)

    try:
        db.session.add(auth_token)
        db.session.commit()
        logging.debug(f"Stored token {db_token} for user {user_id} in database")

    except Exception as e:
        db.session.rollback()
        logging.exception(f"Database error saving token: {e}")
        return "Database error", 500

    # Redirect to home, setting the token in a cookie
    response = make_response(redirect(url_for("home")))
    response.set_cookie("token", db_token, httponly=True, secure=True)
    return response


# Logout Route (Clears the Token)
@app.route("/auth/logout")
def logout():
    token = request.cookies.get("token")

    if token:
        try:
            auth_token = AuthToken.query.filter_by(token=token).first()
            if auth_token:
                db.session.delete(auth_token)
                db.session.commit()
                logging.debug(f"Deleted token {token} from database")

        except Exception as e:
            db.session.rollback()
            logging.exception(f"Database error deleting token: {e}")
            return "Database error", 500

    response = redirect(url_for("home"))
    response.delete_cookie("token")
    return response


# Main Route (Checks for Authentication)
@app.route("/")
def return_home():
    return redirect(url_for("home"))
    
# Main Route (Checks for Authentication)
@app.route("/login")
def login():
    is_auth, _ = is_authenticated(request)
    if is_auth:
        return redirect(url_for("home"))
    else:
        return render_template("login.html")


# Home Route (Protected Page)
@app.route("/home")
def home():
    is_auth, _ = is_authenticated(request)
    return render_template("homepage.html", is_auth=is_auth)



#API ROUTES
@app.route("/api/seasons")
def get_seasons():
    seasons = Season.query.all()
    season_uuids = [season.uuid for season in seasons]
    # print(season_names)
    return jsonify(season_uuids), 200 

@app.route("/api/cards/<season_id>")
def get_cards(season_id):  
    season = Season.query.filter_by(uuid=season_id).first_or_404()
    cards = (season.cards)
    cards_uuids = [card.uuid for card in cards]
    return jsonify(cards_uuids), 200

@app.route("/api/card_info/<card_id>")
def get_card_info(card_id):  
    print(card_id)
    card = Card.query.filter_by(uuid=card_id).first_or_404()
    return jsonify(card.present()), 200

if __name__ == "__main__":
    app.run(debug=True, port=80)

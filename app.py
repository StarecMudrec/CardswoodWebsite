import os
import urllib.parse
import hmac
from hashlib import sha256
import uuid  # For generating unique tokens

from flask import Flask, render_template, request, redirect, url_for
import jwt
from joserfc.errors import JoseError
import logging
from flask_sqlalchemy import SQLAlchemy  # Database integration

# Configuration
JWT_SECRET_KEY = "COOL"  # Replace with your actual secret key
BOT_TOKEN_HASH = sha256("7505659847:AAF3AoBU0HFInjsPPOqz4KaPmX3M15l9f1U".encode())  # Replace with your actual token
DATABASE_URI = 'sqlite:///tokens.db'  # Example: SQLite database file
# If you are not using SQLite, you will need to install a database package and configure the dialect. For example, to use PostgreSQL, install the psycopg2 package with pip install psycopg2, and set the DATABASE_URI to postgresql://username:password@host:port/database_name.
# This can be configured with other databases like Postgres, MySQL, etc.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking for better performance

db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)


# Database Model
class AuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Store user ID from Telegram
    # Add other fields if needed, like expiration timestamp


    def __repr__(self):
        return f'<AuthToken token={self.token} user_id={self.user_id}>'


# Create the database tables (run this once)
with app.app_context():
    db.create_all() # create all tables if they do not exist


# Authentication Helper Function (Database-Based)
def is_authenticated(request):
    token = request.args.get('token')  # Get token from query parameter (or header)
    if not token:
        logging.debug("No token found in request")
        return False, None

    try:
        # Query the database for the token
        auth_token = AuthToken.query.filter_by(token=token).first()

        if auth_token is None:
            logging.debug("Token not found in database")
            return False, None

        # Verify JWT (optional - you can skip this if you trust the database)
        # token_parts = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        token_parts = jwt.decode(token, JWT_SECRET_KEY)
        # user_id = token_parts.get('k')
        # Optional: Check if the user ID from the token matches the user ID in the database
        # if auth_token.user_id != user_id:
        #    logging.warning("User ID mismatch between token and database")
        #    return False, None

        logging.debug("Token is valid (database check)")
        return True, token_parts

    except JoseError as e:
        logging.error(f"JWT Decode Error: {e}")
        return False, None
    except Exception as e:
        logging.exception(f"Authentication error: {e}")
        return False, None



# Routes for Authentication
@app.route('/auth/telegram-callback')
def telegram_callback():
    user_id = request.args.get('id', type=int)
    query_hash = request.args.get('hash')
    next_url = '/home'

    if user_id is None or query_hash is None:
        return "Invalid request", 400

    params = request.args.to_dict()
    data_check_string = '\n'.join(sorted(f'{x}={y}' for x, y in params.items() if x not in ('hash', 'next')))

    computed_hash = hmac.new(BOT_TOKEN_HASH.digest(), data_check_string.encode(), 'sha256').hexdigest()
    is_correct = hmac.compare_digest(computed_hash, query_hash)

    if not is_correct:
        return "Authorization failed. Please try again", 401

    # 1. Create the JWT
    token_payload = {'k': user_id}
    jwt_token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm="HS256")

    # 2. Generate a unique token to store in the database
    db_token = str(uuid.uuid4())  # Generate a unique ID

    # 3. Store token in database (do *not* store the JWT in DB)
    auth_token = AuthToken(token=db_token, user_id=user_id)

    try:
        db.session.add(auth_token)
        db.session.commit()
        logging.debug(f"Stored token {db_token} for user {user_id} in database")

    except Exception as e:
        db.session.rollback()
        logging.exception(f"Database error saving token: {e}")
        return "Database error", 500

    # Redirect to the /home route, passing the database token as a query parameter
    return redirect(url_for('home', token=db_token))


@app.route('/auth/logout')
def logout():
    token = request.args.get('token')

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
    # Redirect to the login page after logging out
    return redirect(url_for('index'))


# Main route
@app.route('/')
def index():
    is_auth, _ = is_authenticated(request)
    if is_auth:
        return redirect(url_for('home', token=request.args.get('token')))
    else:
        return render_template('login.html')


# Home route (protected)
@app.route('/home')
def home():
    is_auth, _ = is_authenticated(request)
    if is_auth:
        return render_template('page.html')
    else:
        return redirect(url_for('index'))

# Static files
@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(os.path.join('site', path))


if __name__ == '__main__':
    app.run(debug=True, port=80)
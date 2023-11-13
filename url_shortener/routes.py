from flask import Blueprint, request, jsonify, redirect, abort
from .models import db, URL, User
from .utils import generate_short_link, check_rate_limit

bp = Blueprint('api', __name__)
    
@bp.route('/api/shorten', methods=['POST'])
                
def shorten_url():
    data = request.json
    user_id = data.get('user_id')

    # Ensuring that the user id is given
    if not user_id:
        return jsonify({'error': 'User ID not provided'}), 400

    # This handles the rate limit
    @check_rate_limit(user_id)
    def _internal_shorten_url():
        original_url = data.get('original_url')
        custom_short_link = data.get('custom_short_link')

        # Checking if the custom link is given
        if custom_short_link:
            existing_url = URL.query.filter_by(short_url=custom_short_link).first()
            if existing_url:
                return jsonify({"error": "Custom short link is already in use"}), 409

            short_url = custom_short_link
        else:
            short_url = generate_short_link()

        new_url = URL(original_url=original_url, short_url=short_url, user_id=user_id)
        db.session.add(new_url)
        db.session.commit()

        return jsonify({"short_url": request.host_url + short_url}), 201

    # Calling the main function
    return _internal_shorten_url()




@bp.route('/api/history/<int:user_id>', methods=['GET'])
def get_user_history(user_id):
    # Getting the user
    user = User.query.get(user_id)
    if user:
        urls = URL.query.filter_by(user_id=user_id).all()
        history = [{"long_url": url.original_url, "short_url": request.host_url + url.short_url} for url in urls]
        return jsonify(history)
    else:
        return jsonify({"error": "User not found"}), 404

@bp.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.original_url)
    else:
        return abort(404)  # error message if the program cannot find the url

@bp.route('/')
def index():
    return 'Welcome to my URL shortener!'

@bp.route('/api/create_user', methods=['POST'])
def create_user():
    data = request.json
    user_id = data.get('user_id')
    tier = data.get('tier')

    # Checking if the parameters are given
    if user_id is None or tier is None:
        return jsonify({"error": "Invalid user data. 'id' and 'tier' are required."}), 400
    
    # Checking for invalid tier
    if (tier != 1 and tier != 2):
        return jsonify({"error": "Invalid user data. invalid 'tier'."}), 400

    # Checking if there is already a user with this id
    existing_user = User.query.filter_by(id=user_id).first()
    if existing_user:
        return jsonify({"error": "User with the same 'id' already exists."}), 409

    # Creating the user and adding their id and tier to the database
    new_user = User(id=user_id, tier=tier)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201



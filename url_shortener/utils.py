import string
import random
import functools
from flask import jsonify, request
from .models import User, URL

# Following the assignment's rate limits
RATE_LIMITS = {
    'Tier 1': 1000,
    'Tier 2': 100
}

def generate_short_link(num_chars=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num_chars))


def check_rate_limit(user_id):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            tier = user.tier
            request_count = URL.query.filter_by(user_id=user_id).count()

            if request_count > RATE_LIMITS[f'Tier {tier}']:
                return jsonify({'error': 'Rate limit exceeded'}), 429

            print(f"User {user_id} has made {request_count} requests out of {RATE_LIMITS[f'Tier {tier}']} allowed.")

            return f(*args, **kwargs)
        return decorated_function
    return decorator


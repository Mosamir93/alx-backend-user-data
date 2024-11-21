#!/usr/bin/env python3
"""Flask app."""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/users", methods=["POST"])
def register_user():
    """Registers a new user."""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify(
            {"email": email, "message": "user created"}
        ), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/", methods=["GET"])
def index():
    """Returns a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Logs a user in and creates a new session."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logout by session_id cookie."""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None or session_id is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None or session_id is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Generates a token."""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password",  methods=["PUT"], strict_slashes=False)
def update_password():
    """Updates the password."""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

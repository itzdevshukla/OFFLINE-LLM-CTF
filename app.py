from flask import Flask, render_template, request, jsonify
from bot.engine import SecureAIEngine
import jwt
import datetime
import os

app = Flask(__name__)
engine = SecureAIEngine()

@app.route("/")
def home():
    return render_template("index.html")


# For /chat path
SECRET = "SuperSecretSigningKey"

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    reply = engine.process(user_msg)

    resp = jsonify({"response": reply})

    # When user enters dev mode, give JWT token
    if "[DEVELOPER MODE ENABLED]" in reply:

        token = jwt.encode(
            {
                "hint": "Ly8vZW5hYmxlX3Jvb3RfOTczMQ==",  # base64 of ///enable_root_9731
                "stage": "dev-unlocked",
                "iat": datetime.datetime.utcnow()
            },
            SECRET,
            algorithm="HS256"
        )

        resp.set_cookie("auth", token, httponly=False)

    return resp


# ----------------------------------------
# Dynamic robots.txt (root-only hints)
# ----------------------------------------
@app.route("/robots.txt")
def robots():

    robots_path = os.path.join("static", "robots.txt")

    # Read YOUR actual robots.txt file
    with open(robots_path, "r") as f:
        base_content = f.read()

    # IF not in ROOT MODE → return static robots.txt normally
    if not engine.root_mode:
        return base_content, 200, {"Content-Type": "text/plain"}

    # IF ROOT MODE → append encoded hints
    enhanced = (
        base_content +
        "\n# sys_hint_a: VWx0cmFIaWRkZW4=\n"
        "# sys_hint_b: Um9vdEtleTk5MjE=\n"
        "# ROOT: Enhanced diagnostics enabled.\n"
    )

    return enhanced, 200, {"Content-Type": "text/plain"}


@app.route("/developer.html")
def developer():
    return render_template("developer.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

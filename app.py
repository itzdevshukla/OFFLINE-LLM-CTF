from flask import Flask, render_template, request, jsonify, session
from bot.engine import SecureAIEngine
import jwt
import datetime
import os

app = Flask(__name__)
app.secret_key = "VeryStrongSecretKeyForSessions"   # IMPORTANT FOR SESSION SECURITY

engine = SecureAIEngine()

SECRET = "SuperSecretSigningKey"


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/chat", methods=["POST"])
def chat():

    user_msg = request.json.get("message", "")

    # Read per-user session state
    dev_mode = session.get("dev", False)
    root_mode = session.get("root", False)

    # Pass states into engine
    reply = engine.process(user_msg, dev_mode, root_mode)

    resp = jsonify({"response": reply})

    # When dev mode activates
    if "[DEVELOPER MODE ENABLED]" in reply:

        # store dev access per-user
        session["dev"] = True

        # send JWT (harmless hint)
        token = jwt.encode(
            {
                "hint": "Ly8vZW5hYmxlX3Jvb3RfOTczMQ==",
                "stage": "dev-unlocked",
                "iat": datetime.datetime.utcnow()
            },
            SECRET,
            algorithm="HS256"
        )

        resp.set_cookie("auth", token, httponly=False)

    # When ROOT MODE activates
    if "__ROOT_MODE_ACTIVATED__" in reply:
        session["root"] = True      # PER-USER ROOT ACCESS

    return resp



# ----------------------------------------
# DYNAMIC robots.txt (root mode only)
# ----------------------------------------
@app.route("/robots.txt")
def robots():

    robots_path = os.path.join("static", "robots.txt")

    with open(robots_path, "r") as f:
        base_content = f.read()

    # If NOT root → return normal robots.txt
    if not session.get("root", False):
        return base_content, 200, {"Content-Type": "text/plain"}

    # If ROOT → return hints
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

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

    user_msg = request.json.get("message", "").strip().lower()

    # Load per-user mode states
    dev_mode = session.get("dev", False)
    root_mode = session.get("root", False)

    # -------------------------------------
    # FIRST: Handle EXIT for root/dev modes
    # -------------------------------------
    if user_msg == "exit":
        if root_mode:
            session["root"] = False
            return jsonify({"response": "Root mode disabled."})

        if dev_mode:
            session["dev"] = False
            return jsonify({"response": "Developer mode disabled."})

    # -------------------------------------
    # Process normally
    # -------------------------------------
    reply = engine.process(user_msg, dev_mode, root_mode)
    resp = jsonify({"response": reply})

    # -------------------------------------
    # Developer mode activation
    # -------------------------------------
    if "[DEVELOPER MODE ENABLED]" in reply:
        session["dev"] = True

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

    # -------------------------------------
    # Root mode activation
    # -------------------------------------
    if "__ROOT_MODE_ACTIVATED__" in reply:
        session["root"] = True

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

    # If ROOT → append hints
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

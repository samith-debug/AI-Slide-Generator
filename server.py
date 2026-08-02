from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
import os
import re

from generate_ppt import generate_ppt_api

app = Flask(
    __name__,
    static_folder="static_site",
    static_url_path=""
)

# Allow frontend to call backend
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=False
)


# -------------------------------
# Clean filename for download
# -------------------------------
def clean_filename(text: str):
    text = text.strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:60] or "presentation"


# -------------------------------
# HEALTH CHECK (optional)
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}, 200


# -------------------------------
# SERVE BUILT FRONTEND
# -------------------------------
@app.route("/")
def serve_frontend():
    return send_from_directory("static_site", "index.html")


@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("static_site", path)


# -------------------------------
# GENERATE PPT
# Supports:
#  POST /generate
#  POST /api/generate
# -------------------------------
@app.post("/generate")
@app.post("/api/generate")
def generate():
    try:
        # --- Parse data ---
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        topic = data.get("topic")
        groq_key = data.get("groq_api_key")
        serp_key = data.get("serp_api_key")

        slides = int(data.get("slides", 7))
        slides = max(1, min(slides, 15))   # 🔒 limit slides between 1–15

        if not topic or not groq_key:
            return jsonify({"error": "Missing topic or API key"}), 400

        model_name = "llama-3.3-70b-versatile"

        # --- Create presentation ---
        file_path = generate_ppt_api(
            topic=topic,
            api_name="groq",
            model_name=model_name,
            num_slides=slides,
            api_key=groq_key,
            serp_api_key=serp_key
        )

        filename = f"{clean_filename(topic)}.pptx"

        return send_file(
            file_path,
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print("\n❌ ERROR:", e, "\n")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Debug mode only for development
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

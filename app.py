"""
Living Ink — Flask Application

Transforms nature photographs into artistic ink illustrations.
Upload a photo, choose a style, receive art + poetry.
"""

import os
import uuid

from flask import Flask, render_template, request, jsonify, send_file

from processors import PatternAnalyzer, StyleTransformer, PoetryGenerator

# ------------------------------------------------------------------ app setup

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

UPLOAD_DIR = os.path.join(app.static_folder, "uploads")
OUTPUT_DIR = os.path.join(app.static_folder, "outputs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

ALLOWED_EXT = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}

analyzer = PatternAnalyzer()
transformer = StyleTransformer()
poet = PoetryGenerator()


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# -------------------------------------------------------------------- routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/process", methods=["POST"])
def process_image():
    """
    Accepts multipart form:
        image  – uploaded file
        style  – one of: tattoo, abstract, sacred_geometry,
                 minimalist, dark_botanical, living_sketch
    Returns JSON with analysis, artwork URL, and poetry.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400
    if not _allowed(file.filename):
        return jsonify({"error": f"Unsupported format. Use: {', '.join(ALLOWED_EXT)}"}), 400

    style = request.form.get("style", "tattoo")
    if style not in StyleTransformer.STYLES:
        return jsonify({"error": f"Unknown style '{style}'. Options: {list(StyleTransformer.STYLES.keys())}"}), 400

    # Save upload
    ext = file.filename.rsplit(".", 1)[1].lower()
    uid = uuid.uuid4().hex[:12]
    filename = f"{uid}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)

    try:
        # 1. Analyze patterns
        analysis = analyzer.analyze(filepath)

        # 2. Transform
        output_path = transformer.transform(filepath, style, analysis)

        # 3. Generate poetry
        poetry = poet.generate(analysis, style)

        return jsonify({
            "success": True,
            "analysis": analysis,
            "original_url": f"/static/uploads/{filename}",
            "artwork_url": f"/static/outputs/{os.path.basename(output_path)}",
            "poetry": poetry,
            "style": style,
            "style_name": StyleTransformer.STYLES[style],
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/download/<path:filename>")
def download(filename):
    """Download a generated artwork file."""
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.isfile(path):
        return jsonify({"error": "File not found."}), 404
    return send_file(path, as_attachment=True, download_name=filename)


# ---------------------------------------------------------------------- main

if __name__ == "__main__":
    print("\n  🖋️  Living Ink is running at http://localhost:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000)

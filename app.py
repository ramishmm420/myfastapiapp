from flask import Flask, render_template, request, redirect, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = "your_secret_key"

DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url").strip()

        if not url:
            flash("Please enter a valid video URL", "error")
            return redirect("/")

        if "youtube.com" in url or "youtu.be" in url:
            cmd = [
                "yt-dlp",
                "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "--write-sub",
                "--sub-lang", "en",
                "--convert-subs", "srt",
                "--embed-subs",
                "-o", f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
                url
            ]
        else:
            cmd = [
                "yt-dlp",
                "-f", "best",
                "-o", f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
                url
            ]

        try:
            subprocess.run(cmd, check=True)
            flash("✅ Download started. Check the downloads folder.", "success")
        except Exception as e:
            flash(f"❌ Error during download: {str(e)}", "error")

        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

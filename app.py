from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        format_code = request.form.get("format")
        uid = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_DIR, f"{uid}.%(ext)s")
        ydl_opts = {
            "format": format_code,
            "outtmpl": output_path,
            "quiet": True,
            "noplaylist": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                ext = info['ext']
                file_path = output_path.replace("%(ext)s", ext)
                return send_file(file_path, as_attachment=True)
        except Exception as e:
            return f"<p style='color:red'>Error: {e}</p>"
    return render_template_string(open("index.html").read())

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
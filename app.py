from flask import Flask, render_template_string, request, redirect
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Video Downloader</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; color: #333; }
        .container { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.2); width: 100%; max-width: 400px; text-align: center; }
        h2 { color: #ff0000; margin-bottom: 25px; font-size: 28px; }
        input[type="text"], select { width: 100%; padding: 15px; margin: 12px 0; border: 2px solid #eee; border-radius: 10px; font-size: 16px; transition: 0.3s; }
        input:focus { border-color: #ff0000; outline: none; }
        button { width: 100%; padding: 15px; background: #ff0000; color: white; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        button:hover { background: #cc0000; transform: translateY(-2px); }
        .footer { margin-top: 25px; font-size: 13px; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Video Downloader</h2>
        <form action="/get_download" method="get">
            <input type="text" name="url" placeholder="ভিডিও লিঙ্ক এখানে পেস্ট করুন..." required>
            <select name="format">
                <option value="mp4_720">MP4 Video (720p)</option>
                <option value="mp4_360">MP4 Video (360p)</option>
                <option value="mp3">MP3 Audio (High Quality)</option>
            </select>
            <button type="submit">ডাউনলোড শুরু করুন</button>
        </form>
        <div class="footer">© 2026 | All Rights Reserved</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_download')
def get_download():
    video_url = request.args.get('url')
    download_format = request.args.get('format')
    if not video_url: return "লিঙ্ক প্রয়োজন!", 400

    if download_format == 'mp3':
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True}
    elif download_format == 'mp4_720':
        ydl_opts = {'format': 'best[height<=720]', 'quiet': True, 'noplaylist': True}
    else:
        ydl_opts = {'format': 'best[height<=360]', 'quiet': True, 'noplaylist': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return redirect(info.get('url'))
    except Exception as e:
        return f"দুঃখিত, সমস্যা হয়েছে: {str(e)}", 500

if __name__ == '__main__':
    app.run()

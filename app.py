from flask import Flask, render_template_string, request, redirect
import yt_dlp

app = Flask(__name__)

# ইন্টারফেস ডিজাইন (UI)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Video Downloader</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; color: #333; }
        .container { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.3); width: 90%; max-width: 400px; text-align: center; }
        h2 { color: #cc0000; margin-bottom: 25px; }
        input[type="text"], select { width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #ddd; border-radius: 10px; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; padding: 15px; background: #ff0000; color: white; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        button:hover { background: #990000; transform: translateY(-2px); }
        .footer { margin-top: 25px; font-size: 12px; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Video Downloader</h2>
        <form action="/download" method="get">
            <input type="text" name="url" placeholder="ভিডিও লিঙ্ক এখানে পেস্ট করুন..." required>
            <select name="format">
                <option value="mp4_720">MP4 - 720p (High Quality)</option>
                <option value="mp4_360">MP4 - 360p (Normal Quality)</option>
                <option value="mp3">MP3 - Audio Only</option>
            </select>
            <button type="submit">ডাউনলোড শুরু করুন</button>
        </form>
        <div class="footer">© 2026 | Safe & Fast Downloader</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    selected_format = request.args.get('format')

    if not video_url:
        return "দয়া করে ভিডিওর লিঙ্ক দিন!", 400

    # yt-dlp সেটিংস (কুকিজ ফাইলসহ)
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt', # আপনার তৈরি করা কুকি ফাইল
    }

    if selected_format == 'mp3':
        ydl_opts['format'] = 'bestaudio/best'
    elif selected_format == 'mp4_720':
        ydl_opts['format'] = 'best[height<=720]'
    else:
        ydl_opts['format'] = 'best[height<=360]'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return redirect(info.get('url'))
    except Exception as e:
        return f"দুঃখিত! সমস্যাটি হলো: {str(e)}", 500

if __name__ == "__main__":
    app.run()
    

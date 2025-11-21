from fastapi import FastAPI, HTTPException, Query
from yt_dlp import YoutubeDL

app = FastAPI(title="FastTube API")

ydl_opts_info = {
    'quiet': True,
    'skip_download': True,
    'force_generic_extractor': True
}

ydl_opts_download = {
    'quiet': True,
    'format': 'best'
}

@app.get("/info")
def get_video_info(url: str = Query(..., description="رابط الفيديو على YouTube")):
    try:
        with YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "id": info.get("id"),
                "uploader": info.get("uploader"),
                "duration": info.get("duration"),
                "formats": [
                    {
                        "format_id": f.get("format_id"),
                        "ext": f.get("ext"),
                        "resolution": f.get("resolution"),
                        "url": f.get("url")
                    }
                    for f in info.get("formats", [])
                ]
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download")
def download_video(url: str = Query(..., description="رابط الفيديو على YouTube")):
    try:
        with YoutubeDL(ydl_opts_download) as ydl:
            info = ydl.extract_info(url, download=False)
            best_format = info.get("url")
            return {"download_url": best_format}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 

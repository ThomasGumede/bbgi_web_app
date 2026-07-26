import subprocess
import json, logging
from pathlib import Path
from celery import shared_task
from django.core.files import File
from bbgistore.models.webinar import WebinarVideo

logger = logging.getLogger("tasks")

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_video(self, video_id):
    try:
        webinar_video = WebinarVideo.objects.get(id=video_id)
        video_path = webinar_video.video.path
        if video_path:
            results = subprocess.run([
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                video_path,
            ], capture_output=True, text=True, check=True)
            info = json.loads(results.stdout)
            duration = int(float(info['format']['duration']))
            webinar_video.duration = duration
            webinar_video.save(update_fields=['duration'])
            return {'duration': duration}
        else:
            logger.info(f'Video path not found')
            return {'duration': 'unkown'}
    except WebinarVideo.DoesNotExist:
        logger.error(f"Webinar video not found : id {video_id}")
        return
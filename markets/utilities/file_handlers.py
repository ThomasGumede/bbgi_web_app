import uuid

def handle_service_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"business/{filename}"
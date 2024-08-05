import uuid

def handle_business_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"business/{filename}"

def handle_business_verification_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"business/verification/{filename}"
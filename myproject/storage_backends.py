"""
Custom Cloudinary storage backend for Django.
Replaces django-cloudinary-storage which is incompatible with Django 4+/5+.
Configure by setting CLOUDINARY_URL environment variable:
  cloudinary://API_KEY:API_SECRET@CLOUD_NAME
"""
import os
import cloudinary
import cloudinary.uploader
from django.core.files.storage import Storage


_IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.tiff', '.ico'}
_VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.ogv'}


def _resource_type(name):
    ext = os.path.splitext(name)[1].lower()
    if ext in _IMAGE_EXTS:
        return 'image'
    if ext in _VIDEO_EXTS:
        return 'video'
    return 'raw'


class CloudinaryStorage(Storage):

    def _save(self, name, content):
        name = name.replace('\\', '/')
        rtype = _resource_type(name)
        ext = os.path.splitext(name)[1]

        # Images: strip extension from public_id (Cloudinary manages format)
        # Raw/Video: keep extension as part of public_id
        public_id = os.path.splitext(name)[0] if rtype == 'image' else name

        try:
            content.seek(0)
        except Exception:
            pass

        result = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            resource_type=rtype,
            overwrite=True,
        )

        stored = result.get('public_id', public_id)

        # Always persist the extension so _resource_type works on retrieval
        if ext and not stored.endswith(ext):
            stored = stored + ext
        return stored

    def url(self, name):
        if not name:
            return ''
        if name.startswith(('http://', 'https://')):
            return name
        rtype = _resource_type(name)
        # Images: strip extension; Cloudinary CDN serves without it
        public_id = os.path.splitext(name)[0] if rtype == 'image' else name
        from cloudinary.utils import cloudinary_url
        url, _ = cloudinary_url(public_id, resource_type=rtype, secure=True)
        return url

    def exists(self, name):
        return False  # Always let Cloudinary handle duplicates via overwrite

    def delete(self, name):
        if not name or name.startswith(('http://', 'https://')):
            return
        rtype = _resource_type(name)
        public_id = os.path.splitext(name)[0] if rtype == 'image' else name
        try:
            cloudinary.uploader.destroy(public_id, resource_type=rtype)
        except Exception:
            pass

    def size(self, name):
        return 0

    def _open(self, name, mode='rb'):
        raise NotImplementedError('CloudinaryStorage does not support local file open.')

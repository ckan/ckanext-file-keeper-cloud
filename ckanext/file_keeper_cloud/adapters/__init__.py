import contextlib

with contextlib.suppress(ImportError):
    from .libcloud import LibCloudStorage

with contextlib.suppress(ImportError):
    from .azure_blob import AzureBlobStorage

with contextlib.suppress(ImportError):
    from .gcs import GoogleCloudStorage

with contextlib.suppress(ImportError):
    from .s3 import S3Storage


__all__ = [
    "AzureBlobStorage",
    "GoogleCloudStorage",
    "LibCloudStorage",
    "S3Storage",
]

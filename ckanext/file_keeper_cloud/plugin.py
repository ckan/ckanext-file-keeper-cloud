from __future__ import annotations
import ckan.plugins as p
from typing_extensions import override
from ckan.lib.files import Storage
from . import adapters


class FileKeeperCloudPlugin(p.IFiles, p.SingletonPlugin):
    @override
    def files_get_storage_adapters(self):
        result: dict[str, type[Storage]] = {}

        if adapter := getattr(adapters, "LibCloudStorage", None):
            result["ckan:libcloud"] = adapter

        if adapter := getattr(adapters, "AzureBlobStorage", None):
            result["ckan:azure_blob"] = adapter

        if adapter := getattr(adapters, "GoogleCloudStorage", None):
            result["ckan:gcs"] = adapter

        if adapter := getattr(adapters, "S3Storage", None):
            result["ckan:s3"] = adapter

        return result

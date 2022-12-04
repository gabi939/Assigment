from decouple import config as cf
import json
from azure.storage.blob import BlobServiceClient
import argparse


class MOCK_PostgresRecoverJob:
    def __init__(self, config: dict):
        self.name = config["name"]
        self.namespace = config["namespace"]
        self.manifest = Manifest(config["manifest"])

    def run_job(self):
        # TODO some how run this job
        if self.manifest.valid():
            self.manifest.manifest()


class Manifest:
    def __init__(self, config: dict):
        self._manifest = {
            "schedule": "0 4 * * *",
            "container": Container(
                config=config["container"],
            ),
            "service_account_name": "custom-sa-postgres-backup-dev"
        }

    def valid(self):
        return self._manifest["container"].validate()

    def manifest(self):
        # TODO somehow manifest
        pass


class Container:
    def __init__(
            self,
            config: dict
    ):
        for i in ["POSTGRES_USER", "POSTGRES_PASSWORD"]:
            config[i] = cf(i, default='')
        self._container_config = config.copy()

    def validate(self) -> bool:
        assert self._container_config["image"]
        assert self._container_config["AZURE_STORAGE_BACKUP_PATH"]

        try:
            print("Azure Blob Storage Python quickstart sample")
            blob_service_client = BlobServiceClient(
                account_url=self._container_config["AZURE_STORAGE_BACKUP_PATH"]
            )

            # Quickstart code goes here

        except Exception as ex:
            print('Exception:')
            return False

        return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str)

    args = parser.parse_args()
    with open(args.config,'r') as f:
        config = json.load(f)
    MOCK_PostgresRecoverJob(config=config).run_job()

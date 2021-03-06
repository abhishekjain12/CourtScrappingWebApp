import logging
import traceback

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def transfer_to_bucket(folder_name, filename):
    try:
        if filename is not None:
            credentials = GoogleCredentials.get_application_default()
            service = discovery.build('storage', 'v1', credentials=credentials)

            bucket = 'ecl-original'
            # bucket = 'test_original'

            body = {'name': str(folder_name) + '/' + str(filename[filename.rfind("/")+1:])}
            req = service.objects().insert(bucket=bucket, body=body, media_body=filename)
            resp = req.execute()

            return True
        else:
            logging.error("Filename is None.")
            return False

    except Exception as e:
        logging.error("Failed to transfer! %s", e)
        traceback.print_exc()
        return False

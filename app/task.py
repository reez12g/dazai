from google.cloud import tasks_v2
import os
import json

project_id = os.getenv("PROJECT_ID", "XXXXXXX")
queue_id = os.getenv("QUEUE_ID", "XXXXXXX")
location_id = os.getenv("LOCATION_ID", "XXXXXXX")
url = os.getenv("DAZAI_PREDICTIVE_SENTENCES_URL", "http://localhost:8080")
service_account_email = os.getenv("SERVICE_ACCOUNT_EMAIL", "aaaaa@aaaaa.com")
audience = os.getenv("DAZAI_ENDPOINT", "http://localhost:8080")

class Task:
    def __init__(self) -> None:
        self.client = tasks_v2.CloudTasksClient()

    def create_task(self, text, response_url):
        parent = self.client.queue_path(project_id, location_id, queue_id)

        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": url,
                "oidc_token": {
                    "service_account_email": service_account_email,
                    "audience": audience,
                },
            }
        }

        payload = json.dumps({
            "text": text,
            "response_url": response_url
        })
        task["http_request"]["headers"] = {"Content-type": "application/json"}

        converted_payload = payload.encode()
        task["http_request"]["body"] = converted_payload

        response = self.client.create_task(request={"parent": parent, "task": task})

        print("Created task {}".format(response.name))
        return response

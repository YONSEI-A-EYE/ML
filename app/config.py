import os
import firebase_admin
from firebase_admin import credentials
# from google.cloud import secretmanager


def fcm_conf():
    current_working_directory = os.getcwd()
    print(f"{current_working_directory}/app/fcm-secret.json")
    cred = credentials.Certificate(f"{current_working_directory}/app/fcm-secret.json")
    print(cred)
    firebase_admin.initialize_app(cred)
#
# # Import the Secret Manager client library.
# from google.cloud import secretmanager
#
# # GCP project in which to store secrets in Secret Manager.
# project_id = "a-eye-381414"
#
# # ID of the secret to create.
# secret_id = "fcm-secret"
#
# # Create the Secret Manager client.
# client = secretmanager.SecretManagerServiceClient()
#
# # Build the parent name from the project.
# parent = f"projects/{project_id}"
#
# # Create the parent secret.
# secret = client.create_secret(
#     request={
#         "parent": parent,
#         "secret_id": secret_id,
#         "secret": {"replication": {"automatic": {}}},
#     }
# )
#
# # Add the secret version.
# version = client.add_secret_version(
#     request={"parent": secret.name, "payload": {"data": b"hello world!"}}
# )
#
# # Access the secret version.
# response = client.access_secret_version(request={"name": version.name})
#
# # Print the secret payload.
# #
# # WARNING: Do not print the secret in a production environment - this
# # snippet is showing how to access the secret material.
# payload = response.payload.data.decode("UTF-8")

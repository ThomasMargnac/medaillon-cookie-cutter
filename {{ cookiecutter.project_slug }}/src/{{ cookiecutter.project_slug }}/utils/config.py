import os

if os.getenv(key="ENV", default="dev") == "dev":
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="dev.env")

STORAGE_OPTIONS = {
    "AWS_ACCESS_KEY_ID": os.getenv("MINIO_SERVER_ROOT_USER"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("MINIO_SERVER_ROOT_PASSWORD"),
    "AWS_REGION": "us-east-1",
    "AWS_ENDPOINT_URL": f"http://{os.getenv("MINIO_SERVER_NAME")}:9000",
    'AWS_ALLOW_HTTP': 'true',
    'aws_conditional_put': 'etag'
}
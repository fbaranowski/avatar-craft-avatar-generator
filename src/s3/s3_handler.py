import logging

from botocore.exceptions import ClientError

from s3.s3_client import connect_client
from s3.settings import AWSSettings


async def upload_file_to_s3(file_uuid: str, img_bytes: bytes) -> bool:
    try:
        async with await connect_client() as client:
            await client.put_object(
                Bucket=AWSSettings.BUCKET_NAME, Key=f"{file_uuid}.jpg", Body=img_bytes
            )
    except ClientError as e:
        logging.error(f"Error while uploading file to S3: {e}")
        return False
    return True

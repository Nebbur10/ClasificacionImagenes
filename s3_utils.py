import boto3
import uuid

BUCKET_NAME = "clasficacionimg"

s3 = boto3.client("s3", region_name="us-east-1")

def subir_imagen_a_s3(file_bytes: bytes, filename: str) -> str:
    
    nombre_unico = f"{uuid.uuid4()}_{filename}"
    s3.put_object(Bucket=BUCKET_NAME, Key=nombre_unico, Body=file_bytes)
    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{nombre_unico}"
    return url

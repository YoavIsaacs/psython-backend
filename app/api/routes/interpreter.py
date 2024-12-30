from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.interpreter import ConfigEncoder, KeywordValidator
import logging

endpoints = APIRouter()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@endpoints.get("/")
def healthcheck() -> dict:
    return {"message": "Hello, world!"}

class KeywordConfig(BaseModel):
    keywords: dict

class EncodedConfig(BaseModel):
    code: str


@endpoints.post("/encode")
async def encode_config(config: KeywordConfig) -> dict:
    logger.info(f"Received encode request with config: {config}")
    try:
        encoded = ConfigEncoder.encode_config(config.keywords)
        logger.info(f"Successfully encoded config")
        return {"Encoded config": encoded}
    except Exception as e:
        logger.error(f"Error encoding config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@endpoints.post("/decode")
def decode_config(code: EncodedConfig) -> dict:
    logger.info(f"Received decode request with code: {code}")
    try:
        decoded = ConfigEncoder.decode_config(code.code)
        logger.info(f"Successfully decoded config")
        return {"Decoded keywords": decoded}
    except Exception as e:
        logger.error(f"Error decoding config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@endpoints.post("/validate_keywords")
async def validate_keywords(config: KeywordConfig) -> dict:
    logger.info(f"Validating keyword configuration: {config.keywords}")

    validator = KeywordValidator()
    is_valid, errors = validator.validate_mapping(config.keywords)

    if not is_valid:
        return {
            "valid": False,
            "errors": errors
        }

    return {
        "valid": True,
        "message": "Configuration is valid"
    }




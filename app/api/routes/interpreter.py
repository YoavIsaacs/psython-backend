from fastapi import APIRouter, HTTPException

from app.core.translator_validator import CustomKeywordParser
from app.schemas.config import KeywordConfig, EncodedConfig, CodeExecutionRequest
from app.core.interpreter import ConfigEncoder, KeywordValidator
import logging

endpoints = APIRouter()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@endpoints.get("/")
def healthcheck() -> dict:
    return {"message": "Hello, world!"}



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

@endpoints.post("/translate")
async def translate_code(request: CodeExecutionRequest) -> dict:
    logger.info(f"Received translation request with code length: {len(request.code)}")
    try:
        parser = CustomKeywordParser(request.config)
        try:
            translated_code = parser.translate_to_python(request.code)
            logger.info(f"Translated code: {repr(translated_code)}")
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                "success": False,
                "errors": [f"Translation error: {str(e)}"]
            }

        is_valid , errors = parser.validate_custom_code(request.code)
        if not is_valid:
            return {
                "success": False,
                "errors": errors
            }

        translated_code = parser.translate_to_python(request.code)
        return {
            "success": True,
            "translated_code": translated_code
        }
    except Exception as e:
        logger.error(f"Error in code translation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



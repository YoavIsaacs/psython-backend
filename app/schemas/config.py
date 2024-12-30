from pydantic import BaseModel

class KeywordConfig(BaseModel):
    keywords: dict

class EncodedConfig(BaseModel):
    code: str

class CodeExecutionRequest(BaseModel):
    code: str
    config: dict[str, str]
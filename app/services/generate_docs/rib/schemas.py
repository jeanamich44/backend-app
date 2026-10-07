from pydantic import BaseModel, ConfigDict


class RibGenerateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

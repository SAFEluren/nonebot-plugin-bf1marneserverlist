from pydantic import BaseModel


class Config(BaseModel):
    marne_url: str
    marne_plugin_enabled: bool = True

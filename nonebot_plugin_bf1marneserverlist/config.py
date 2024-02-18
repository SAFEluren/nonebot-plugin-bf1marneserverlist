from pydantic import BaseModel

class Config(BaseModel):
    marne_url: str
    marne_plugin_enabled: bool = True
    marne_data_dir: str = './data/marne_data/'
    class Config:
        extra = "ignore"
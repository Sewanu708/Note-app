from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url:str
    algorithm:str
    secret_key:str
    expiry_time:int
    
    class Config:   
        env_file ='.env'
        
settings = Settings()
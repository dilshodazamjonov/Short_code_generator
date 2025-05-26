from pydantic import BaseModel, HttpUrl




class URLRequest(BaseModel):
    original_url: HttpUrl

class URLResponse(BaseModel):
    short_url: str


class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None

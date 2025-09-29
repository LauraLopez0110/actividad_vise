from pydantic import BaseModel, EmailStr

# Para recibir datos de registro
class ClientCreate(BaseModel):
    email: EmailStr
    password: str

# Para mostrar datos de cliente (sin password)
class ClientResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# Para login
class ClientLogin(BaseModel):
    email: EmailStr
    password: str

# Para respuesta JWT
class Token(BaseModel):
    access_token: str
    token_type: str

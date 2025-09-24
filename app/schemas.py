from pydantic import BaseModel, EmailStr

# Participación de [Persona 2]: schemas de Cliente

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

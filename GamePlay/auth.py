
from fastapi import status, HTTPException, Security
from fastapi.security import APIKeyHeader


# holding the key for now
### It should be placed in environment variables or key vaults
secrets = ["Copywrite @ Chinmay Routray"]     

api_key_header = APIKeyHeader(name= 'X-API-Key')

# for security
def get_api_key(api_key_header : str = Security(api_key_header)):
    if api_key_header in secrets:
        return api_key_header
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid key...")
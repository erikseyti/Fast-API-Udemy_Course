from fastapi import Header, HTTPException

import os
from dotenv import load_dotenv

load_dotenv()

secret_token = os.getenv('secret_token')
print(secret_token)

async def get_token_header(internal_token: str=Header(...)):
  if internal_token !=  secret_token:
    raise HTTPException(status_code=400, detail='Internal-Token header invalid')
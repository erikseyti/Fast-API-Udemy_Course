from fastapi import FastAPI
import models
from database import  engine
from routers import auth, todos
from company import companyapis

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(
  companyapis.router,
  prefix='/companyapis',
  tags=['companyapis'],
  responses={410: {'description': 'Internal Use Only :"( '}}
)

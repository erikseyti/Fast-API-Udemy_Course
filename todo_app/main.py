from fastapi import FastAPI, Depends
import models
from database import  engine
from routers import auth, todos, users_instructor
from company import companyapis, dependencies
from todo_app.routers import users_my_solution

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users_my_solution.router)
app.include_router(users_instructor.router)

app.include_router(
  companyapis.router,
  prefix='/companyapis',
  tags=['companyapis'],
  dependencies=[Depends(dependencies.get_token_header)],
  responses={410: {'description': 'Internal Use Only :"( '}}
)

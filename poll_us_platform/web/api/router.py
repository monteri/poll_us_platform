from fastapi.routing import APIRouter

from poll_us_platform.web.api import auth, monitoring, questions, user_answers

api_router = APIRouter()
api_router.include_router(monitoring.router, tags=["Test"])
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(questions.router, tags=["Questions"])
api_router.include_router(user_answers.router, tags=["User Answers"])

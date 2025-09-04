from fastapi import FastAPI, Depends, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.settings import Settings, get_settings
from app.models import AppGenericException, MessageResponse
from app.exceptions import ValidationError


def create_app():
    app = FastAPI()

    # cors middleware
    origins = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/test/message")
    async def get_test_message():
        return {'message': "Test message"}

    @app.get("/api/version")
    async def get_test_message(config: Settings = Depends(get_settings)):
        return {'version': config.version}

    from .modules import auth
    from .modules.users import user
    from .modules import vehicles
    from .modules.rites import rites

    app.include_router(auth.router, prefix="/auth", tags=['auth'])
    app.include_router(user.router, tags=['users'])
    app.include_router(vehicles.router, tags=['vehicles'])
    app.include_router(rites.router, tags=['rites'])

    @app.exception_handler(AppGenericException)
    async def app_generic_exception_handler(request: Request, exc: AppGenericException):
        return JSONResponse(
            status_code=exc.http_response_status_code,
            content=MessageResponse(code=exc.code, message=exc.message).dict(),
        )


    return app

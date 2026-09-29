from fastapi import FastAPI
from settings import settings
from routers.products import router as products_router


app = FastAPI(title=settings.APP_NAME)

app.include_router(products_router)

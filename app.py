from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from delivery.api.adapters.http_ad.views import ROUTER_OBJ


app = FastAPI(docs_url="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ROUTER_OBJ, prefix="/api/v1/", tags=["use-cases"])

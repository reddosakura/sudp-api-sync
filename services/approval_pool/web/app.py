from fastapi import FastAPI
from starlette.responses import RedirectResponse
from .api.api import router

app = FastAPI(
    debug=True,
    docs_url="/docs/approval-pool",
    title = "VACS/СУДП",
    version = "3.0.1",
)

app.include_router(router, prefix="/api/v3")


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url='/docs/approval-pool')

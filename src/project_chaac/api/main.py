from fastapi import FastAPI

from project_chaac.api.routes import jobs

app = FastAPI(title="project_chaac")

app.include_router(jobs.router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
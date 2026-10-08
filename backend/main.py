
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.app import protected_router,public_router
from mcp_server.server import mcp_app

app = FastAPI(
    title="Resume Matcher API",
    description="An API for matching resumes to job descriptions.",
    lifespan=mcp_app.lifespan,
)


app.include_router(protected_router, prefix="/api")
app.include_router(public_router, prefix="/api")
app.mount("/mcp", mcp_app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI

from routes.ticketRoutes import router as ticketRouter
from routes.chatRoutes import router as chatRouter

from pathlib import Path
from fastapi.responses import FileResponse

from routes.analyticsRoutes import router as analyticsRouter


app = FastAPI(
    title="NovaTech AI Customer Support API",
    version="1.0.0",
    description=(
        "AI Customer Support Agent using FastAPI, "
        "LangGraph, RAG, ChromaDB, SQLite and n8n."
    )
)


app.include_router(ticketRouter)
app.include_router(chatRouter)

app.include_router(analyticsRouter)


@app.get("/health", tags=["System"])
def HealthCheck():

    return {
        "status": "healthy",
        "service": "ai-customer-support-agent"
    }




BASE_DIR = Path(__file__).resolve().parent


@app.get("/", include_in_schema=False)
def CustomerSupportPage():

    return FileResponse(
        BASE_DIR / "static" / "index.html"
    )



@app.get("/admin", include_in_schema=False)
def SupportAdminPage():

    return FileResponse(
        BASE_DIR / "static" / "admin.html"
    )



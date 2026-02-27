"""Monopoly API application entry point."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    """Return a greeting message from the API root endpoint."""
    return {"message": "Hello World"}

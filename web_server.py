"""
FastAPI web server for the chatbot web interface.
"""

import json
import os
from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from web_interface import WebInterface
from query_engine import QueryEngine
import config


# Pydantic models for API requests/responses
class ChatMessage(BaseModel):
    query: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    success: bool
    session_id: str
    message: Optional[dict] = None
    error: Optional[str] = None


class SessionInfo(BaseModel):
    session_id: str
    created_at: str
    last_activity: str
    message_count: int


# Global web interface instance
web_interface: Optional[WebInterface] = None


def create_app(query_engine: QueryEngine) -> FastAPI:
    """Create and configure the FastAPI application."""
    global web_interface

    # Initialize web interface
    web_interface = WebInterface(query_engine)

    # Create FastAPI app
    app = FastAPI(
        title=f"{config.CHATBOT_NAME} Web Interface",
        description="Web-based chat interface for the local RAG chatbot",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup static files and templates
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    # Create directories if they don't exist
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(templates_dir, exist_ok=True)

    # Mount static files
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Setup templates
    templates = Jinja2Templates(directory=templates_dir)

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Serve the main chat interface."""
        return templates.TemplateResponse("index.html", {
            "request": request,
            "chatbot_name": config.CHATBOT_NAME,
            "welcome_message": config.WELCOME_MESSAGE
        })

    @app.post("/api/chat", response_model=ChatResponse)
    async def chat_endpoint(message: ChatMessage):
        """Handle chat messages via REST API."""
        if not web_interface:
            raise HTTPException(status_code=500, detail="Web interface not initialized")

        # Create session if not provided
        session_id = message.session_id
        if not session_id:
            session_id = web_interface.create_session()
        elif not web_interface.get_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found")

        # Process query
        result = await web_interface.process_query_async(session_id, message.query)

        if "error" in result:
            return ChatResponse(
                success=False,
                session_id=session_id,
                error=result["error"]
            )

        return ChatResponse(
            success=True,
            session_id=session_id,
            message=result.get("assistant_message")
        )

    @app.post("/api/sessions")
    async def create_session():
        """Create a new chat session."""
        if not web_interface:
            raise HTTPException(status_code=500, detail="Web interface not initialized")

        session_id = web_interface.create_session()
        return {"session_id": session_id}

    @app.get("/api/sessions/{session_id}", response_model=SessionInfo)
    async def get_session_info(session_id: str):
        """Get information about a specific session."""
        if not web_interface:
            raise HTTPException(status_code=500, detail="Web interface not initialized")

        session_info = web_interface.get_session_info(session_id)
        if not session_info:
            raise HTTPException(status_code=404, detail="Session not found")

        return SessionInfo(**session_info)

    @app.get("/api/sessions/{session_id}/history")
    async def get_session_history(session_id: str, limit: Optional[int] = None):
        """Get the message history for a session."""
        if not web_interface:
            raise HTTPException(status_code=500, detail="Web interface not initialized")

        if not web_interface.get_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found")

        history = web_interface.get_session_history(session_id, limit)
        return {"session_id": session_id, "messages": history}

    @app.websocket("/ws/{session_id}")
    async def websocket_endpoint(websocket: WebSocket, session_id: str):
        """WebSocket endpoint for real-time chat."""
        if not web_interface:
            await websocket.close(code=1011, reason="Web interface not initialized")
            return

        # Accept connection
        await websocket.accept()

        # Create session if it doesn't exist
        if not web_interface.get_session(session_id):
            web_interface.create_session()
            # Override the generated session ID with the one from URL
            if session_id not in web_interface.sessions:
                from web_interface import WebChatSession
                web_interface.sessions[session_id] = WebChatSession(session_id)

        # Add connection to session
        web_interface.add_connection(session_id, websocket)

        try:
            # Send session info
            session_info = web_interface.get_session_info(session_id)
            await websocket.send_text(json.dumps({
                "type": "session_info",
                "data": session_info
            }))

            # Send chat history
            history = web_interface.get_session_history(session_id)
            await websocket.send_text(json.dumps({
                "type": "history",
                "data": history
            }))

            # Listen for messages
            while True:
                data = await websocket.receive_text()
                message_data = json.loads(data)

                if message_data.get("type") == "chat":
                    query = message_data.get("message", "").strip()
                    if query:
                        # Process query asynchronously
                        await web_interface.process_query_async(session_id, query)

        except WebSocketDisconnect:
            # Remove connection when client disconnects
            web_interface.remove_connection(session_id, websocket)
        except Exception as e:
            print(f"WebSocket error: {e}")
            web_interface.remove_connection(session_id, websocket)

    @app.get("/api/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "chatbot_name": config.CHATBOT_NAME,
            "model": config.OLLAMA_MODEL
        }

    return app


def run_server(query_engine: QueryEngine):
    """Run the web server."""
    import uvicorn

    app = create_app(query_engine)

    print(f"Starting {config.CHATBOT_NAME} web interface...")
    print(f"Server will be available at: http://{config.WEB_HOST}:{config.WEB_PORT}")

    uvicorn.run(
        app,
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        log_level="debug" if config.WEB_DEBUG else "info"
    )

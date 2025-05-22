"""
Web interface module for handling web-based chat interactions.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from query_engine import QueryEngine
import config


class WebChatSession:
    """Represents a single chat session with history."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.messages: List[Dict] = []
        self.last_activity = datetime.now()
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to the session history."""
        message = {
            "id": str(uuid.uuid4()),
            "role": role,  # "user" or "assistant"
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.messages.append(message)
        self.last_activity = datetime.now()
        return message
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get message history, optionally limited to recent messages."""
        if limit:
            return self.messages[-limit:]
        return self.messages.copy()


class WebInterface:
    """
    Web-based chat interface for the chatbot.
    Manages multiple chat sessions and provides async query processing.
    """
    
    def __init__(self, query_engine: QueryEngine):
        """
        Initialize the web interface.
        
        Args:
            query_engine (QueryEngine): The query engine to use for processing queries
        """
        self.query_engine = query_engine
        self.sessions: Dict[str, WebChatSession] = {}
        self.active_connections: Dict[str, List] = {}  # session_id -> list of websockets
    
    def create_session(self) -> str:
        """Create a new chat session and return its ID."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = WebChatSession(session_id)
        self.active_connections[session_id] = []
        return session_id
    
    def get_session(self, session_id: str) -> Optional[WebChatSession]:
        """Get a chat session by ID."""
        return self.sessions.get(session_id)
    
    def add_connection(self, session_id: str, websocket):
        """Add a WebSocket connection to a session."""
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
    
    def remove_connection(self, session_id: str, websocket):
        """Remove a WebSocket connection from a session."""
        if session_id in self.active_connections:
            try:
                self.active_connections[session_id].remove(websocket)
            except ValueError:
                pass  # Connection not in list
    
    async def broadcast_to_session(self, session_id: str, message: Dict):
        """Broadcast a message to all connections in a session."""
        if session_id not in self.active_connections:
            return
        
        # Remove closed connections
        active_connections = []
        for websocket in self.active_connections[session_id]:
            try:
                await websocket.send_text(json.dumps(message))
                active_connections.append(websocket)
            except Exception:
                # Connection is closed, skip it
                pass
        
        self.active_connections[session_id] = active_connections
    
    async def process_query_async(self, session_id: str, query: str) -> Dict:
        """
        Process a query asynchronously and return the response.
        
        Args:
            session_id (str): The session ID
            query (str): The user's query
            
        Returns:
            Dict: Response containing the answer and metadata
        """
        session = self.get_session(session_id)
        if not session:
            return {
                "error": "Session not found",
                "session_id": session_id
            }
        
        try:
            # Add user message to history
            user_message = session.add_message("user", query)
            
            # Broadcast user message to all connections in session
            await self.broadcast_to_session(session_id, {
                "type": "message",
                "message": user_message
            })
            
            # Broadcast typing indicator
            await self.broadcast_to_session(session_id, {
                "type": "typing",
                "is_typing": True
            })
            
            # Process query in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            response_text = await loop.run_in_executor(
                None, 
                self.query_engine.query, 
                query
            )
            
            # Add assistant response to history
            assistant_message = session.add_message(
                "assistant", 
                response_text,
                metadata={
                    "model": config.OLLAMA_MODEL,
                    "top_k": config.TOP_K
                }
            )
            
            # Stop typing indicator
            await self.broadcast_to_session(session_id, {
                "type": "typing",
                "is_typing": False
            })
            
            # Broadcast assistant response
            await self.broadcast_to_session(session_id, {
                "type": "message",
                "message": assistant_message
            })
            
            return {
                "success": True,
                "session_id": session_id,
                "user_message": user_message,
                "assistant_message": assistant_message
            }
            
        except Exception as e:
            # Stop typing indicator on error
            await self.broadcast_to_session(session_id, {
                "type": "typing",
                "is_typing": False
            })
            
            error_message = f"Error processing query: {str(e)}"
            error_response = session.add_message(
                "assistant", 
                error_message,
                metadata={"error": True}
            )
            
            # Broadcast error message
            await self.broadcast_to_session(session_id, {
                "type": "message",
                "message": error_response
            })
            
            return {
                "error": error_message,
                "session_id": session_id
            }
    
    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict]:
        """Get the message history for a session."""
        session = self.get_session(session_id)
        if not session:
            return []
        return session.get_history(limit)
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get information about a session."""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session.session_id,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "message_count": len(session.messages)
        }
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Remove sessions older than the specified age."""
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        sessions_to_remove = []
        
        for session_id, session in self.sessions.items():
            if session.last_activity < cutoff_time:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
            if session_id in self.active_connections:
                del self.active_connections[session_id]
        
        return len(sessions_to_remove)

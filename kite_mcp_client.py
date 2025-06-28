import httpx
import uuid

class KiteMCPClient:
    """
    Minimal Kite MCP client using SSE protocol.
    """

    def __init__(self, server_url: str = "https://mcp.kite.trade/sse"):
        self.server_url = server_url
        self.kite_session = None

    def login(self) -> str:
        """
        Initiates a browser login via Kite MCP.
        Returns the URL user must visit to authorize Kite access.
        """
        params = {
            "id": str(uuid.uuid4()),
            "method": "login",
            "params": {}
        }
        resp = httpx.post(self.server_url, json=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        token = data.get("login_url")
        if not token:
            raise ValueError("Failed to get login URL from Kite MCP")
        return token

    def set_session(self, session_token: str):
        """Stores Kite-access token returned after login."""
        self.kite_session = session_token

    def query(self, prompt: str) -> str:
        """
        Sends a query to Kite MCP and returns the assistant response.
        """
        if not self.kite_session:
            raise RuntimeError("Kite session not set. Please login first.")
        payload = {
            "id": str(uuid.uuid4()),
            "method": "query",
            "params": {
                "kite_session": self.kite_session,
                "input": prompt
            }
        }
        resp = httpx.post(self.server_url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "No response returned")

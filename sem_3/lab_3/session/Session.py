
from datetime import datetime, timedelta

class Session:
    def __init__(self, user_id: int, ip_address: str, user_agent: str):
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(hours=24)
        self.is_active = True
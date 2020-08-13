from app.entities.DB2ConnectionEntity import DB2ConnectionEntity


class DB2QueryEntity(DB2ConnectionEntity):
    def __init__(self, state: dict):
        super().__init__(state)
        self.interval = state.get("interval") or 10



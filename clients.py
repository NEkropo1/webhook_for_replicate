class ClientsDB:
    def __init__(self):
        self.clients = {}

    def __contains__(self, item):
        return item in self.clients

    def add_clients(self, payload: dict = None) -> dict:
        device_id = payload.get("device_id")
        _id = payload.get("id")
        self.clients[_id] = device_id
        return {_id: device_id}

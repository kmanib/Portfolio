class Intent:
    def __init__(self, action=None, uri=None):
        self.action = action
        self.uri = uri
        self.extras = {}

    def putExtra(self, key, value):
        self.extras[key] = value
        return self

    def getExtra(self, key):
        return self.extras.get(key)

class IntentSystem:
    def __init__(self):
        self.broadcasts = []

    def sendBroadcast(self, intent):
        self.broadcasts.append(intent)
        print(f"[IntentSystem] Broadcast sent: {intent.action}")
        return True

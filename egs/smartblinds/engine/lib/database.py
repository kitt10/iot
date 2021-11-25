

class Database:
    
    def __init__(self, app):
        self.app = app
        self.cfg = app.cfg
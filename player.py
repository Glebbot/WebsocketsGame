


class Player:
    def __init__(self, num, max_turns=5):
        self.num = num
        self.score = 0
        self.turns = max_turns
        self.client = None

    def is_player_for_client(self, client):
        return self.client == client

    def define_client(self, client):
        self.client = client

    def undefine_client(self):
        self.client = None



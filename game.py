from player import Player
from box import Box

N = 15
K = 5
S1 = 0
S2 = 10

class Game:
    def __init__(self, box_count=N, num_turns = K, min_value = S1, max_value = S2):
        self.first_player = Player(1, max_turns=num_turns)
        self.second_player = Player(2, max_turns=num_turns)
        self.boxes = [Box(s1=min_value, s2=max_value) for _ in range(box_count)]

    def define_player(self, client):
        if self.first_player.client is None:
            self.first_player.define_client(client)
            print('Player 1 is defined')
        elif self.second_player.client is None:
            self.second_player.define_client(client)
            print('Player 2 is defined')
        else:
            return False
        return True

    def undefine_player(self, client):
        if self.first_player.client is not None and self.first_player.is_player_for_client(client):
            self.first_player.undefine_client()
            print('Player 1 disconnected')
        elif self.second_player.client is not None and self.second_player.is_player_for_client(client):
            self.second_player.undefine_client()
            print('Player 2 disconnected')

    def get_player(self, client):
        if self.first_player.client is not None and self.first_player.is_player_for_client(client):
            return self.first_player
        elif self.second_player.client is not None and self.second_player.is_player_for_client(client):
            return self.second_player
        return None

    def open_box(self, box_num):
        try:
            box_num = int(box_num)
        except ValueError:
            return None
        if box_num < 0 or box_num >= N:
            return None
        return self.boxes[box_num].open()

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
        self.turn = 1
        self.available_score = 0
        self.gamestate = 'wait'
        self.save_gamestate = 'wait'
        self.started = False

    def define_player(self, client):
        if self.first_player.client is None:
            self.first_player.define_client(client)
            print('Player 1 is defined')
        elif self.second_player.client is None:
            self.second_player.define_client(client)
            print('Player 2 is defined')
        else:
            return False
        self.start_game()
        return True

    def undefine_player(self, client):
        if self.first_player.client is not None and self.first_player.is_player_for_client(client):
            self.first_player.undefine_client()
            self.pause_game()
            print('Player 1 disconnected')
        elif self.second_player.client is not None and self.second_player.is_player_for_client(client):
            self.second_player.undefine_client()
            self.pause_game()
            print('Player 2 disconnected')

    def start_game(self):
        if self.is_ready():
            if not self.started:
                self.gamestate = 'open'
                self.started = True
            else:
                self.gamestate = self.save_gamestate
            print('Game is ready')

    def pause_game(self):
        self.save_gamestate = self.gamestate
        self.gamestate = 'wait'
        print('Game is paused')

    def is_ready(self):
        if self.first_player.client is not None and self.second_player.client is not None:
            return True
        return False

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

    def next_turn(self, player):
        self.available_score = 0
        self.gamestate = 'open'
        if player.num == 1 and self.second_player.turns > 0:
            self.turn = 2
        elif player.num == 2 and self.first_player.turns > 0:
            self.turn = 1

    def withdraw(self, player):
        player.score += self.available_score
        player.turns = 0
        self.next_turn(player)

    def player_turn_open(self, client, box_num):
        if self.gamestate == 'wait':
            return -7, 0
        player = self.get_player(client)
        if player is None:
            return -2, 0
        elif player.num != self.turn:
            return -3, 0
        elif player.turns <= 0:
            return -5, 0
        elif self.gamestate != 'open':
            return -6, 0
        score = self.open_box(box_num)
        if score is not None:
            player.turns -= 1
            self.available_score = score
            self.gamestate = 'decide'
            return -1, score
        return -4, 0

    def player_turn_skip(self, client):
        if self.gamestate == 'wait':
            return -7, 0
        player = self.get_player(client)
        if player is None:
            return -2, 0
        elif player.num != self.turn:
            return -3, 0
        elif self.gamestate != 'decide':
            return -6, 0
        elif player.turns > 0:
            self.next_turn(player)
            return -1, 0
        self.withdraw(player)
        return 0, player.score

    def player_turn_withdraw(self, client):
        if self.gamestate == 'wait':
            return -7, 0
        player = self.get_player(client)
        if player is None:
            return -2, 0
        elif player.num != self.turn:
            return -3, 0
        if self.gamestate != 'decide':
            return -6, 0
        self.withdraw(player)
        return -1, player.score



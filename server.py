import websockets
import asyncio
from game import Game
from exceptions import TooManyPlayersError

MESSAGE_CODES = {
    -1: 'success',
    -2: 'player_not_found',
    -3: 'not_your_turn',
    -4: 'box_num_error',
    -5: 'no_more_turns',
    -6: 'not_available_now',
    -7: 'game_not_started'
}

class ServerApp:
    def __init__(self, host: str = 'localhost', port: int = 8889):
        self.host = host
        self.port = port
        self.server = websockets.serve(self.connection_handler, host, port)
        self.connected = []
        self.game = Game()

    async def connection_handler(self, connection, path):
        self.connected.append(connection)
        print('Client connected')
        can_connect = self.game.define_player(connection)

        while True:
            try:
                message = await connection.recv()
                if not can_connect:
                    print('Too many players')
                    raise TooManyPlayersError
                print(f'Message from client: {message}')
                print('Connected clients:', self.connected)
                await self.message_handler(message, connection)

            except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError, TooManyPlayersError):
                if self.close_connection(connection):
                    break

    async def send_message_open(self, connection, box_num, score):
        for client in self.connected:
            if client != connection:
                await client.send(f'other open {box_num}')
            else:
                await client.send(f'opened {box_num} {score}')

    async def send_message_skip(self, connection):
        for client in self.connected:
            if client != connection:
                await client.send('other skip')
            else:
                await client.send('skipped')

    async def send_message_withdraw(self, connection, score):
        for client in self.connected:
            if client != connection:
                await client.send(f'other withdraw')
            else:
                await client.send(f'withdraw {score}')

    async def message_handler(self, message, connection):
        if message.startswith('open '):
            box_num = message.split()[1]
            code, score = self.game.player_turn_open(connection, box_num)
            if code == -1:
                await self.send_message_open(connection, box_num, score)
            else:
                await connection.send(MESSAGE_CODES[code])
        elif message == 'skip':
            code, score = self.game.player_turn_skip(connection)
            if code == -1:
                await self.send_message_skip(connection)
            elif code == 0:
                await self.send_message_withdraw(connection, score)
            else:
                await connection.send(MESSAGE_CODES[code])
        elif message == 'withdraw':
            code, score = self.game.player_turn_withdraw(connection)
            if code == -1:
                await self.send_message_withdraw(connection, score)
            else:
                await connection.send(MESSAGE_CODES[code])
        elif message == "I'm feeling high,rat!":
            await connection.send(f'player {self.game.get_player(connection).num}')
        else:
            await connection.send('Unknown command')

    def close_connection(self, connection):
        try:
            self.connected.remove(connection)
            self.game.undefine_player(connection)
        except ValueError:
            return True
        print('Client disconnected')
        return False

    async def start(self):
        print(f'Server started at {self.host}:{self.port}')
        await self.server


if __name__ == "__main__":
    server = ServerApp()
    asyncio.get_event_loop().run_until_complete(server.start())
    asyncio.get_event_loop().run_forever()

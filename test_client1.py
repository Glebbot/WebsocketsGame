import asyncio
import websockets


class ClientCommunicator:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = "ws://" + host + ":" + str(port)
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def send_message(self, message):
        if not self.websocket:
            await self.connect()

        await self.websocket.send(message)
        response = await self.websocket.recv()
        print("Получено от сервера:", response)


client = ClientCommunicator('localhost', 8889)
asyncio.get_event_loop().run_until_complete(client.connect())

while True:
    message = input("Введите сообщение: ")
    asyncio.get_event_loop().run_until_complete(client.send_message(message))

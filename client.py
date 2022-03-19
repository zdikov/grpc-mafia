import asyncio
import copy

import google.protobuf.empty_pb2
import google.protobuf.json_format

from mafia_pb2_grpc import *
from mafia_pb2 import *


class Mafia:
    def __init__(self, addr, username):
        self._server_addr = addr
        self._username = username

    def consume(self, message):
        if message.type == RESPONSE:
            response = message.response
            print(response.message)
        elif message.type == LEAVE:
            print('leave:', message.username)
        elif message.type == JOIN:
            print('join:', message.username)

    async def join(self):
        async with grpc.aio.insecure_channel(self._server_addr) as channel:
            stub = MafiaStub(channel)
            req = JoinRequest(username=self._username)
            async for response in stub.Join(req):
                self.consume(response)

    async def leave(self):
        async with grpc.aio.insecure_channel(self._server_addr) as channel:
            stub = MafiaStub(channel)
            _ = await stub.Leave(LeaveRequest(username=self._username))


async def read_command(mafia):
    while True:
        command = input('Type leave to exit or anything else to continue game loop-->')
        if command == 'leave':
            await mafia.leave()
            exit(0)
        else:
            await asyncio.sleep(0)


async def main():
    username = input('Enter username --> ')
    address = input('Enter server address --> ')
    if not address:
        address = '127.0.1.1:8080'
    mafia = Mafia(address, username)
    await asyncio.gather(mafia.join(), read_command(mafia))


if __name__ == '__main__':
    asyncio.run(main())

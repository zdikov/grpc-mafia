import os
import grpc.aio
import asyncio

from mafia_pb2_grpc import *
from mafia_pb2 import *


class Mafia(MafiaServicer):
    def __init__(self):
        self._queues = {}
        self._players = set()

    async def Join(self, request, context):
        for username, queue in self._queues.items():
            event = Event()
            event.type = JOIN
            event.username = request.username
            queue.put_nowait(event)

        self._players.add(request.username)
        if request.username not in self._queues:
            self._queues[request.username] = asyncio.Queue()
        response = Event()
        response.type = RESPONSE
        response.response.message = str(self._players)

        await context.write(response)
        while request.username in self._players:
            event = await self._queues[request.username].get()
            await context.write(event)

    async def Leave(self, request, context):
        self._players.remove(request.username)
        del self._queues[request.username]
        for username, queue in self._queues.items():
            event = Event()
            event.type = LEAVE
            event.username = username
            queue.put_nowait(event)
        return LeaveResponse()


async def run_server(port):
    server = grpc.aio.server()
    add_MafiaServicer_to_server(Mafia(), server)
    server.add_insecure_port('[::]:' + port)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    server_port = '8080'
    asyncio.run(run_server(server_port))

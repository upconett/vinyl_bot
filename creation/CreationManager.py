from dataclasses import dataclass
from enum import Enum
import asyncio

from creation.asyncio import *


class VinylTypes(Enum):
    PHOTO= 'photo'
    VIDEO = 'video'


@dataclass
class Creation:
    user_id: int
    unique_id: int


@dataclass
class Vinyl(Creation):
    template: int
    type: VinylTypes
    audio_path: str
    cover_path: str
    offset: str
    speed: int
    noise: bool

    def __repr__(self):
        return f'Vinyl {self.user_id, self.unique_id}'


@dataclass
class Player(Creation):
    template: int


@dataclass
class Album(Creation):
    template: int
    first_path: str
    second_path: str | None


@dataclass
class Result(Creation):
    output_path: str | tuple[str, str]

    def __init__(self, creation: Vinyl | Album | Player):
        self.unique_id = creation.unique_id
        self.user_id = creation.user_id

    def __repr__(self):
        return f'Result {self.user_id, self.unique_id}'

class CreationManager():
    def __init__(self):
        self.queue: list[Vinyl | Album | Player] = []
        self.tasks: list[asyncio.Task] = []
        self.creating: list[Vinyl | Album | Player] = []
        self.result: list[Result] = []


    async def start(self):
        print("Creation Manager started!")
        while True:
            print(self.queue, self.creating, self.result)
            if len(self.queue) > 0 and len(self.creating) < 2:
                creation = self.queue.pop(0)
                if isinstance(creation, Vinyl):
                    task = asyncio.create_task(self.make_vinyl(creation))
                if isinstance(creation, Player):
                    task = asyncio.create_task(self.make_player(creation))
                if isinstance(creation, Album):
                    task = asyncio.create_task(asyncio.sleep(10))
                self.creating.append(creation)
                self.tasks.append(task)

            to_remove = []
            for c in self.creating:
                for r in self.result:
                    if c.unique_id == r.unique_id:
                        to_remove.append(c)
            for r in to_remove:
                self.creating.remove(r)

            await asyncio.sleep(1)


    async def createVinyl(self, vinyl: Vinyl) -> tuple[str, str]:
        self.queue.append(vinyl)
        await asyncio.sleep(1)
        while vinyl in self.queue or vinyl in self.creating:
            await asyncio.sleep(1)
        await asyncio.sleep(1)
        for r in self.result:
            if r.user_id == vinyl.user_id and r.unique_id == vinyl.unique_id:
                my = r
                break
        else:
            raise Exception("NOTHING V RESULTE")
        self.result = [r for r in self.result if r != my]
        return r.output_path


    async def make_vinyl(self, vinyl: Vinyl):
        result = Result(vinyl)
        print('Started vinyl CREATION')
        try:
            match vinyl.type:
                case VinylTypes.PHOTO:
                    result.output_path = await make_classic_vinyl(
                        vinyl.unique_id,
                        vinyl.cover_path,
                        vinyl.audio_path,
                        vinyl.template,
                        vinyl.offset,
                        vinyl.speed,
                        vinyl.noise
                    )
                case VinylTypes.VIDEO:
                    result.output_path = await make_video_vinyl(
                        vinyl.unique_id,
                        vinyl.cover_path,
                        vinyl.audio_path,
                        vinyl.template,
                        vinyl.offset,
                        vinyl.speed,
                        vinyl.noise
                    )
        finally:
            self.result.append(result)
            self.creating.remove(vinyl)
            self.tasks = [t for t in self.tasks if not t.done()]
            print('FINISHED vinyl CREATION')
            

    async def make_player(self, player: Player):
        result = Result(player)
        try:
            return await make_player_vinyl(
                player.unique_id,
                player.template
            )
        finally:
            self.result.append(result)
            self.creating.remove(player)
            self.tasks = [t for t in self.tasks if not t.done()]


    async def make_album(self, album: Album):
        pass

    
    def in_player_queue(self, user_id: int):
        for c in self.queue:
            if c.user_id == user_id and isinstance(c, Player):
                return True
        for c in self.creating:
            if c.user_id == user_id and isinstance(c, Player):
                return True
        return False


    def in_vinyl_queue(self, user_id: int):
        for c in self.queue:
            if c.user_id == user_id and isinstance(c, Vinyl):
                return True
        for c in self.creating:
            if c.user_id == user_id and isinstance(c, Vinyl):
                return True
        return False


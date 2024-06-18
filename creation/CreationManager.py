from dataclasses import dataclass
from enum import Enum
import asyncio, os

from creation.asyncio import *
from utility.exceptions import NoResFolder


class VinylTypes(Enum):
    PHOTO= 'photo'
    VIDEO = 'video'


@dataclass
class Creation():
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

    def __repr__(self):
        return f'Player {self.user_id, self.unique_id}'


@dataclass
class Album(Creation):
    template: int
    first_path: str
    second_path: str | None

    def __repr__(self):
        return f'Album {self.user_id, self.unique_id}'


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
        self.queueVinyl: list[Vinyl] = []
        self.tasksVinyl: list[asyncio.Task] = []
        self.creatingVinyl: list[Vinyl] = []
        self.resultVinyl: list[Result] = []

        self.queuePlayer: list[Player] = []
        self.tasksPlayer: list[asyncio.Task] = []
        self.creatingPlayer: list[Player] = []
        self.resultPlayer: list[Result] = []

        for f in ['img/', 'audio/', 'users_video/', 'video/', 'res/']:
            if not os.path.isdir(f'creation/{f}'):
                if f == 'res/': raise NoResFolder('\nThere is no <creation/res/> folder!\nPaste contents of res archive to <creation/res>/\n')
                os.makedirs(f'creation/{f}')


    async def startVinyl(self):
        print("Creation Manager started creating vinyl!")
        while True:
            # print(self.queueVinyl, self.creatingVinyl, self.resultVinyl)
            if len(self.queueVinyl) > 0 and len(self.creatingVinyl) < 2:
                creation = self.queueVinyl.pop(0)
                if isinstance(creation, Vinyl):
                    task = asyncio.create_task(self.make_vinyl(creation))
                if isinstance(creation, Player):
                    task = asyncio.create_task(self.make_player(creation))
                if isinstance(creation, Album):
                    task = asyncio.create_task(asyncio.sleep(10))
                self.creatingVinyl.append(creation)
                self.tasksVinyl.append(task)

            to_remove = []
            for c in self.creatingVinyl:
                for r in self.resultVinyl:
                    if c.unique_id == r.unique_id:
                        to_remove.append(c)
            for r in to_remove:
                self.creatingVinyl.remove(r)

            await asyncio.sleep(1)


    async def startPlayer(self):
        print("Creation Manager started creating players!")
        while True:
            # print(self.queuePlayer, self.creatingPlayer, self.resultPlayer)
            if len(self.queuePlayer) > 0 and len(self.creatingPlayer) < 2:
                creation = self.queuePlayer.pop(0)
                if isinstance(creation, Vinyl):
                    task = asyncio.create_task(self.make_vinyl(creation))
                if isinstance(creation, Player):
                    task = asyncio.create_task(self.make_player(creation))
                if isinstance(creation, Album):
                    task = asyncio.create_task(asyncio.sleep(10))
                self.creatingPlayer.append(creation)
                self.tasksPlayer.append(task)

            to_remove = []
            for c in self.creatingPlayer:
                for r in self.resultPlayer:
                    if c.unique_id == r.unique_id:
                        to_remove.append(c)
            for r in to_remove:
                self.creatingPlayer.remove(r)

            await asyncio.sleep(1)


    async def createVinyl(self, vinyl: Vinyl) -> tuple[str, str]:
        self.queueVinyl.append(vinyl)
        await asyncio.sleep(1)
        while vinyl in self.queueVinyl or vinyl in self.creatingVinyl:
            await asyncio.sleep(1)
        await asyncio.sleep(1)
        for r in self.resultVinyl:
            if r.user_id == vinyl.user_id and r.unique_id == vinyl.unique_id:
                my = r
                break
        else:
            raise Exception("NOTHING V RESULTE")
        self.resultVinyl = [r for r in self.resultVinyl if r != my]
        return r.output_path

    
    async def createPlayer(self, player: Player) -> tuple[str, str]:
        self.queuePlayer.append(player)
        await asyncio.sleep(1)
        while player in self.queuePlayer or player in self.creatingPlayer:
            await asyncio.sleep(1)
        await asyncio.sleep(1)
        for r in self.resultPlayer:
            if r.user_id == player.user_id and r.unique_id == player.unique_id:
                my = r
                break
        else:
            raise Exception("NOTHING V RESULTE")
        self.resultPlayer = [r for r in self.resultPlayer if r != my]
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
            self.resultVinyl.append(result)
            self.creatingVinyl.remove(vinyl)
            self.tasksVinyl = [t for t in self.tasksVinyl if not t.done()]
            print('FINISHED vinyl CREATION')
            

    async def make_player(self, player: Player):
        result = Result(player)
        try:
            result.output_path = await make_player_vinyl(
                player.unique_id,
                player.template
            )
        finally:
            self.resultPlayer.append(result)
            self.creatingPlayer.remove(player)
            self.tasksPlayer = [t for t in self.tasksPlayer if not t.done()]


    async def make_album(self, album: Album):
        pass

    
    def in_player_queue(self, user_id: int):
        for c in self.queuePlayer:
            if c.user_id == user_id and isinstance(c, Player):
                return True
        for c in self.creatingPlayer:
            if c.user_id == user_id and isinstance(c, Player):
                return True
        return False


    def in_vinyl_queue(self, user_id: int):
        for c in self.queueVinyl:
            if c.user_id == user_id and isinstance(c, Vinyl):
                return True
        for c in self.creatingVinyl:
            if c.user_id == user_id and isinstance(c, Vinyl):
                return True
        return False


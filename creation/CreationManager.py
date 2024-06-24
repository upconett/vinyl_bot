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
    second_path: str = None

    def __repr__(self):
        return f'Album {self.user_id, self.unique_id}'


@dataclass
class Result(Creation):
    output_path: str | tuple[str, str]
    exception: str | None

    def __init__(self, creation: Vinyl | Album | Player, exception: str = None):
        self.unique_id = creation.unique_id
        self.user_id = creation.user_id
        self.exception = exception

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

        self.queueAlbum: list[Album] = []
        self.tasksAlbum: list[asyncio.Task] = []
        self.creatingAlbum: list[Album] = []
        self.resultAlbum: list[Result] = []

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
                task = asyncio.create_task(self.make_vinyl(creation))
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
                task = asyncio.create_task(self.make_player(creation))
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

    
    async def startAlbum(self):
        print("Creation Manager started creating albums!")
        while True:
            if len(self.queueAlbum) > 0 and len(self.creatingAlbum) < 2:
                creation = self.queueAlbum.pop(0)
                task = asyncio.create_task(self.make_album(creation))
                self.creatingAlbum.append(creation)
                self.tasksAlbum.append(task)
            
            to_remove = []
            for c in self.creatingAlbum:
                for r in self.resultAlbum:
                    if c.unique_id == r.unique_id:
                        to_remove.append(c)
            for r in to_remove:
                self.creatingAlbum.remove(r)

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
        if r.exception: raise r.exception
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
        if r.exception: raise r.exception
        self.resultPlayer = [r for r in self.resultPlayer if r != my]
        return r.output_path


    async def createAlbum(self, album: Album) -> str:
        self.queueAlbum.append(album)
        await asyncio.sleep(1)
        while album in self.queueAlbum or album in self.creatingAlbum:
            await asyncio.sleep(1)
        await asyncio.sleep(1)
        for r in self.resultAlbum:
            if r.user_id == album.user_id and r.unique_id == album.unique_id:
                my = r
                break
        else:
            raise Exception("NOTHING V RESULTE")
        if r.exception: raise r.exception
        self.resultAlbum = [r for r in self.resultAlbum if r != my]
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
        except Exception as e: result.exception = e
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
        except Exception as e: result.exception = e
        finally:
            self.resultPlayer.append(result)
            self.creatingPlayer.remove(player)
            self.tasksPlayer = [t for t in self.tasksPlayer if not t.done()]


    async def make_album(self, album: Album):
        result = Result(album)
        try:
            result.output_path = await make_album(
                album.unique_id,
                album.template,
                album.first_path,
                album.second_path
            )
        except Exception as e: result.exception = e
        finally:
            self.resultAlbum.append(result)
            self.creatingAlbum.remove(album)
            self.tasksAlbum = [t for t in self.tasksAlbum if not t.done()]

    
    async def in_player_queue(self, user_id: int):
        for c in self.queuePlayer:
            if c.user_id == user_id: return True
        for c in self.creatingPlayer:
            if c.user_id == user_id: return True
        return False

    
    async def count_player_queue(self) -> tuple[int, int]:
        count = len(self.queuePlayer)
        wait = 0
        for e in self.queuePlayer:
            wait += 20
        return count, wait


    async def in_vinyl_queue(self, user_id: int):
        for c in self.queueVinyl:
            if c.user_id == user_id: return True
        for c in self.creatingVinyl:
            if c.user_id == user_id: return True
        return False

    
    async def count_vinyl_queue(self) -> tuple[int, int]:
        count = len(self.queueVinyl)
        wait = 0
        for e in self.queueVinyl:
            if e.type == VinylTypes.PHOTO:
                if e.template == 3: wait += 90
                else: wait += 45
            else:
                if e.template == 3: wait += 60 * 6
                else: wait += 60 * 3
        return count, wait


    async def in_album_queue(self, user_id: int):
        for c in self.queueAlbum:
            if c.user_id == user_id: return True
        for c in self.creatingAlbum:
            if c.user_id == user_id: return True
        return False

    
    async def count_album_queue(self) -> tuple[int, int]:
        count = len(self.queueAlbum)
        wait = 0
        for e in self.queueAlbum:
            if e.template == 1: wait += 20
            else: wait += 45
        return count, wait

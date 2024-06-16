class CreationManager():
    def __init__(self):
        self.queue_vinyl = []
        self.queue_album = []
        self.queue_player = []

    def queue_vinyl_add(self, user_id: int):
        self.queue_vinyl.append(user_id)

    def in_vinyl_queue(self, user_id: int):
        return user_id in self.queue_vinyl

    def queue_vinyl_rem(self, user_id: int):
        self.queue_vinyl.remove(user_id)

    def queue_album_add(self, user_id: int):
        self.queue_album.append(user_id)

    def in_album_queue(self, user_id: int):
        return user_id in self.queue_album

    def queue_album_rem(self, user_id: int):
        self.queue_album.remove(user_id)

    def queue_player_add(self, user_id: int):
        self.queue_player.append(user_id)

    def in_player_queue(self, user_id: int):
        return user_id in self.queue_player

    def queue_player_rem(self, user_id: int):
        self.queue_player.remove(user_id)

class User:
    def __init__(self, id):
        self.id = id
        self.friends = []
        self.preferences = []

    def add_friend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)

    def set_preferences(self, preference):
        self.preferences = preference
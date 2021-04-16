class User:
    def __init__(self, u_name, p_hash, p_salt, u_profile):
        self.username = u_name
        self.password_hash = p_hash
        self.password_salt = p_salt
        self.profile = u_profile
        self.watched = [] # watched list
        self.liked = [] # liked list
    def get_username(self):
        return self.username
    def get_password(self):
        pass
    def get_liked(self):
        return self.liked
    def get_watched(self):
        return self.watched

    def set_liked(self, id, title):
        self.liked.append((id, title))
    def set_watched(self, id, title):
        self.liked.append((id, title))

    def removed_liked(self, id):
        for i,j in self.liked:
            if i == id:
                self.liked.remove((i,j))
    
    def removed_watched(self, id):
        for i,j in self.watched:
            if i == id:
                self.watched.remove((i,j))

    
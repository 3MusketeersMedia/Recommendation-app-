class User:
    def __init__(self, u_name, p_hash, p_salt, u_profile):
        self.username = u_name
        self.password_hash = p_hash
        self.password_salt = p_salt
        self.profile = u_profile
    def get_username(self):
        return self.username
    def get_password(self):
        return self.pass
        
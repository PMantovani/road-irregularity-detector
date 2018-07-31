class GsmApnConfiguration(object):

    def __init__(self, apn, user, password):
        self.apn = apn
        self.user = user
        self.password = password

    def get_apn(self):
        return self.apn
    
    def get_user(self):
        return self.user

    def get_password(self):
        return self.password
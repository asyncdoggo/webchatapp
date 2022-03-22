import random


class Users():
    def __init__(self,uname,id) -> None:
        self.uname = uname
        self.id = id
        self.tempid = random.randint(100000,999999)

    def getuname(self):
        return self.uname

    def getid(self):
        return self.id


    def getkey(self):
        return str(self.tempid)
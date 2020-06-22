class gameGroup():
    def __init__(self, FirstId: str, gameName: str):
        self.gameName = gameName
        self.myFriends = list()
        FirstId = f"[CQ:at,qq={FirstId}]"
        self.myFriends.append(FirstId)

    def getGmaersNum(self):
        return len(self.myFriends)

    def removeGamer(self, id):
        id = f"[CQ:at,qq={id}]"
        self.myFriends.remove(id)

    def addFriend(self, id: str):
        id = f"[CQ:at,qq={id}]"
        for i in self.myFriends:
            if i == id:
                return f"你已经加入了游戏{self.gameName}"
        self.myFriends.append(id)
        return f"加入游戏{self.gameName}成功"

    def printGamer(self):
        src = ''
        for i in self.myFriends:
            src += i
        return src

    def getThis(self):
        return self


gameList = list()


def addGame(game: gameGroup):
    gameList.append(game)


def deleteGmae(game: gameGroup):
    gameList.remove(game)

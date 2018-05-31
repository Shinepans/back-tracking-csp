class Matching():

    def __init__(self):

        self.Author = 'Author: Shang'
        self.Time = 'Time: 2018-5-30'
        self.Github = 'Github: https://github.com/Shinepans'
        self.Desc = 'Desc:\n It is a stranger matching algorithm, It produce double person, and each record is different ' \
                    'that every one met another one, and it would not repeat'
        self.TeamNumber = 8
        self.Team = []
        self.AllCase = []
        self.TempRes = []
        self.Res = []
        self.Keys = []
        self.keyidx = -1

    def showDesc(self):
        print('###############################################\n|',
              self.Author, '|\n|',
              self.Time, '|\n|',
              self.Github, '|')
        print(self.Desc, '\n###############################################')

    def initTeam(self):
        self.TeamNumber = self.TeamNumber
        for i in range(0, self.TeamNumber):
            self.Team.append(i)
        print('Team inited, It is', self.Team)

    def findCase(self):
        for i in range(len(self.Team) - 1):
            OneCase = []
            for j in range(i + 1, len(self.Team)):
                Group = []
                Group.append(self.Team[i])
                Group.append(self.Team[j])
                OneCase.append(Group)
            self.AllCase.append(OneCase)
        print('All case was found')
        for one in self.AllCase:
            self.Keys.append(-2)
            print(one)

    def initKeys(self):
        self.Keys = []
        for one in self.AllCase:
            self.Keys.append(-2)
        print(self.Keys)

    def getEachItem(self, Que):
        eachItems = []
        for eachItem in Que:
            eachItems.append(eachItem[0])
            eachItems.append(eachItem[1])
        return eachItems

    def findRes(self, Que):
        TempResItems = self.getEachItem(self.TempRes)
        rangeStart = self.Keys[self.keyidx] if self.Keys[self.keyidx] != -2 else 0
        print('**START** Find\n    keyidx = ', self.keyidx,
              '\n    Keys[keyidx] = ', self.Keys[self.keyidx],
              '\n    Que =', Que,
              '\n    rangStart=', rangeStart)
        for eachIdx in range(rangeStart, len(Que)):
            PresentItems = []
            PresentItems.append(Que[eachIdx][0])
            PresentItems.append(Que[eachIdx][1])
            inters = list(set(TempResItems).intersection(set(PresentItems)))
            if (eachIdx == len(Que) - 1 and len(inters) > 0):
                self.Keys[self.AllCase.index(Que)] = -1   ## not found
                return self.handleAnswer(False)           ## jump or backtracking
            if len(inters) == 0:
                self.Keys[self.AllCase.index(Que)] = eachIdx  ## found one
                self.TempRes.append(Que[eachIdx])
                return self.handleAnswer(True)


    def handleAnswer(self, answer):
        if not answer:
            if self.keyidx == len(self.Keys) - 1:
                self.TempRes.pop()
                for k in range(len(self.Keys)):     ## 横向深度
                    preidx = len(self.Keys) - 1 - k
                    print('**←** BackTrackingNoAnswer\n    preidx = ', preidx, '\n    Keys[preidx] = ', self.Keys[preidx])
                    if self.Keys[preidx] != -1:
                        self.keyidx = preidx
                        kidx = self.Keys[preidx]+1   ## 纵向梯度下降
                        if kidx == len(self.AllCase[preidx]):
                            continue
                        else:
                            self.Keys[preidx] += 1
                            for newk in range(preidx + 1, len(self.Keys)):
                                self.Keys[newk] = -2
                            break
            else:
                self.Keys[self.keyidx] = -1
                self.keyidx += 1
            Que = self.AllCase[self.keyidx]
            print('**RES** Not Found')
            self.findRes(Que)
        else:
            print('**RES** Found One\n    TempRes:', self.TempRes)
            if self.isRightRes():
                return self.removeUsed()
            if self.keyidx == len(self.Keys) - 1:  ## 回溯向上
                self.TempRes.pop()
                for k in range(len(self.Keys)):    ## 横向深度
                    preidx = len(self.Keys) - 1 - k
                    if self.Keys[preidx] != -1:
                        self.keyidx = preidx
                        kidx = self.Keys[preidx]+1 ## 纵向梯度下降
                        if kidx == len(self.AllCase[preidx]) - 1:
                            continue
                        else:
                            self.Keys[preidx] += 1
                            for newk in range(preidx + 1, len(self.Keys)):
                                self.Keys[newk] = -2
                            break
                Que = self.AllCase[self.keyidx]
                print('**←** Backtracking')
                self.findRes(Que)
            else:
                self.keyidx += 1
                Que = self.AllCase[self.keyidx]
                print('**↓** Deep Search')
                self.findRes(Que)

    def pushAnswer(self):
        self.keyidx = -1 ## 横向查找
        if len(self.TempRes) == 0:
            self.keyidx = 0
            Que = self.AllCase[0]
            self.Keys[0] = 0
            self.handleAnswer(self.findRes(Que))
        else:
            for k in range(len(self.Keys)):
                if self.Keys[k] == -2:
                    self.keyidx = k
                    self.handleAnswer(self.findRes(self.AllCase[k]))
                    break

    def isRightRes(self):
        print('**Found All?**\n    ', len(self.TempRes) == self.TeamNumber / 2)
        return len(self.TempRes) == self.TeamNumber / 2

    def isAllResed(self):
        return len(start.Res) == start.TeamNumber - 1

    def removeUsed(self):
        self.Res.append(self.TempRes)
        if self.isAllResed():
            print('All is found, case : ', len(self.Res))
            for row in self.Res:
                print(row)
            exit()
        else:
            for item in self.TempRes:
                for row in self.AllCase:
                    for col in row:
                        if col == item:
                            row.remove(col)
            for row in self.AllCase:
                if row == []:
                    self.AllCase.remove(row)
            self.TempRes = []
            self.initKeys()
            self.pushAnswer()

start = Matching()
start.showDesc()
start.initTeam()
start.findCase()
start.pushAnswer()


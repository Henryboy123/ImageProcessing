class Letter:
    def __init__(self,coords,dims,number):
        self.id = number
        self.x = coords[0]
        self.y = coords[1]
        self.dimen = dims
        self.myCoor = [self.x,self.y]
        self.val = ""

    def getID(self):
        return self.id

    def getY(self):
        return self.y

    def getX(self):
        return self.x

    def getCoords(self):
        return self.myCoor

    def getHeight(self):
        return self.dimen[0]

    def getWidth(self):
        return self.dimen[1]

    def getDimension(self):
        return self.dimen

    def getValue(self):
        return self.val

    def getRight(self):
        return self.right

    def getLeft(self):
        return self.left

    def getArea(self):
        return self.dimen[0]*self.dimen[1]

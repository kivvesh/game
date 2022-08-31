from utils import randbool,randcell,randcell2
import os
CELL_TYPES = "🟩🌲🌊🏥🏦🔥"
TREE_BONUS=100
UP_COST = 500
LIFE_COST = 500
class Map:

    def __init__(self, w , h):
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.w = w
        self.h = h
        self.generate_forest(3,10)
        self.generate_river(5)
        self.generate_river(5)
        self.generate_river(5)
        self.generate_shop()
        self.generate_hospital()

    def print_Map(self,helico,clouds):
        print("⬛" * (self.w+2))
        for ri in range(self.h):
            print("⬛",end="")
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if clouds.cells[ri][ci]==1:
                    print("💭",end = "")
                elif clouds.cells[ri][ci]==2:
                    print("⚡",end = "")
                elif (helico.x == ri and helico.y ==ci):
                    print("🚁",end = "")
                elif (cell>=0 or cell <len(CELL_TYPES)):
                    print(CELL_TYPES[cell],end="")
                
            print("⬛")
        print("⬛" * (self.w+2))

    def check_box(self,x,y):
        if (x<0 or y<0 or x>=self.h or y>=self.w):
            return False
        else:
            return True

    def generate_river(self,l):
        rc = randcell(self.w,self.h)
        rx,ry=rc[0],rc[1]
        self.cells[rx][ry] = 2
        while l > 1:
            x,y = randcell2(rx,ry) 
            if self.check_box(x,y) and self.cells[x][y]!=2:
                self.cells[x][y] = 2
                rx,ry = x,y
                l-=1
    def generate_forest(self,r,mxr):
        for i in range(self.h):
            for j in range(self.w):
                if randbool(r,mxr):
                    self.cells[i][j]=1
    def generate_tree(self):
        cx,cy = randcell (self.w,self.h)
        if (self.check_box(cx,cy) and self.cells[cx][cy]==0):
            self.cells[cx][cy]==1
    def generate_shop(self):
        cx,cy = randcell(self.w,self.h)
        self.cells[cx][cy]=4

    def generate_hospital(self):
        cx,cy = randcell(self.w,self.h)
        if self.cells[cx][cy]!=4:
            self.cells[cx][cy]=3
        else:
            self.generate_hospital()
        

    def add_fire(self):
        cx,cy = randcell (self.w,self.h)
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] =5

    def update_fires(self):
        for i in range (self.h):
            for j in range(self.w):
                cell =self.cells[i][j]
                if cell == 5:
                    self.cells[i][j]=0
        for i in range(10):
            self.add_fire()

    def process_holicopter(self,helico,clouds):
        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        if ( c==2):
            helico.tank = helico.mxtank
        if (c==5 and helico.tank>0):
            helico.tank -=1
            self.cells[helico.x][helico.y]=1
            helico.score += TREE_BONUS
        if (c==4 and helico.score>=UP_COST):
            helico.mxtank+=1
            helico.score-=UP_COST
        if (c==3 and helico.score>=LIFE_COST):
            helico.lives+=10
            helico.score-=LIFE_COST
        if (d==2):
            helico.lives -=1
            if helico.lives ==0:
                helico.game_over()
    def export_data(self):
        return {"cells":self.cells}
    def import_data(self,data):
        self.cells = data["cells"] or [[0 for i in range(w)] for j in range(h)]
   

import tkinter as tk
import tkinter.font as font

white=0
black=1
class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.numstr="12345678"
        self.alpstr="abcdefgh"

        self.title("othello")
        self.geometry("560x420")

        self.player=black
        self.was_passed=False
        self.tag2pos={}
        self.z2tag={}
        self.cells={}

        self.font1=font.Font(family="Times New Roman",size=14)

        self.button=tk.Button(self,text="Restart",command=self.reset)
        self.button.place(x=470,y=350)

        self.text1=tk.StringVar()
        self.text2=tk.StringVar()
        self.text3=tk.StringVar()
        self.text1.set("")
        self.text2.set("")
        self.text3.set("")
        self.label1=tk.Label(self,textvariable=self.text1,font=self.font1)
        self.label1.place(x=425,y=5)
        self.label2=tk.Label(self,textvariable=self.text2,font=self.font1)
        self.label2.place(x=425,y=25)
        self.label3=tk.Label(self,textvariable=self.text3,font=self.font1)
        self.label3.place(x=425,y=50)

    def put_disk(self,tag):
        if self.cells[tag] is not None:
            return False
        
        flippable=self.list_flippable_disks(tag)
        if flippable==[]:
            return False

        self.cells[tag]=self.player
        for rtag in flippable:
            self.cells[rtag]=self.player

        return True

    def list_flippable_disks(self,tag):
        direction=[-1,0,1]
        flippable=[]
        z=self.z_coordinate(tag)

        for dx in direction:
            for dy in direction:
                if dx==0 and dy==0:
                    continue
                
                tmp=[]
                depth=0

                while(True):
                    depth+=1
                    rz=z+(dy*depth*10)+(dx*depth)

                    if 0<rz%10<=8 and 1<=rz/10<9:
                        rtag=self.z2tag[rz]
                        request=self.cells[rtag]

                        if request is None:
                            break

                        if request==self.player:
                            if tmp!=[]:
                                flippable.extend(tmp)
                            
                            break

                        else:
                            tmp.append((rtag))
                    
                    else:
                        break

        return flippable

    def z_coordinate(self,tag):
        x=self.alpstr.index(tag[1])+1
        y=self.numstr.index(tag[0])+1
        return y*10+x

    def list_possible_cells(self):
        self.possible=[]
        for tag in self.cells.keys():
            if self.cells[tag] is not None:
                continue
            if self.list_flippable_disks(tag)==[]:
                continue
            else:
                self.possible.append((tag))

        if self.possible==[]:
            if self.was_passed:
                self.finish_game()
            else:
                self.was_passed=True
                self.shift_player()
                self.list_possible_cells()

    def get_next_player(self):
        return white if self.player==black else black

    def shift_player(self):
        self.player=self.get_next_player()

    def update_board(self):
        for tag in self.cells.keys():
            if self.cells[tag]==white:
                self.board.create_oval(*self.tag2pos[tag],fill="white",tags="t"+tag)
            elif self.cells[tag]==black:
                self.board.create_oval(*self.tag2pos[tag],fill="black",tags="t"+tag)


        self.list_possible_cells()
        self.switch_board(1)

    def set_board(self):
        self.board=tk.Canvas(self, bg="lime green", width=420, height=420)
        self.board.place(x=0, y=0)
        for i,y in zip(self.numstr,range(10,420,50)):
            for j,x in zip(self.alpstr,range(10,420,50)):
                pos=x,y,x+50,y+50
                tag=i+j
                self.tag2pos[tag]=pos
                self.board.create_rectangle(*pos,fill="lime green",tags=tag)
                self.z2tag[self.z_coordinate(tag)]=tag
                self.board.tag_bind(tag,"<ButtonPress-1>",self.pressed)
                self.cells[tag]=None

        self.cells["4d"]=white
        self.cells["4e"]=black
        self.cells["5d"]=black
        self.cells["5e"]=white
        
        self.update_board()

    def pressed(self,event):
        item_id=self.board.find_closest(event.x,event.y)
        tag=self.board.gettags(item_id[0])[0]
        if self.put_disk(tag):
            self.was_passed=False
            self.shift_player()
            self.switch_board(0)
            self.update_board()
        else:
            return False

    def switch_board(self,t):
        for tag in self.possible:
            self.board.itemconfig(tag, fill=["lime green","lawn green"][t])

    def finish_game(self):
        self.get_disk_map()
        White=self.disks[white]
        Black=self.disks[black]
        self.text1.set("{}: {}".format("BLACK", self.disks[black]))
        self.text2.set("{}: {}".format("WHITE", self.disks[white]))
        if White<Black:
            self.text3.set("Winner: BLACK")
        elif Black<White:
            self.text3.set("Winner: WHITE")
        else:
            self.text3.set("DRAW")

    def get_disk_map(self):
        self.disks={white:0,black:0}
        for tag in self.cells.keys():
            if self.cells[tag]==white:
                self.disks[white]+=1
            elif self.cells[tag]==black:
                self.disks[black]+=1
    
    def reset(self):
        self.player=black
        self.was_passed=False
        self.switch_board(0)
        self.text1.set("")
        self.text2.set("")
        self.text3.set("")
        for tag in self.cells.keys():
            if self.cells[tag] is not None:
                self.board.delete("t"+tag)
                self.cells[tag]=None

        self.cells["4d"]=white
        self.cells["4e"]=black
        self.cells["5d"]=black
        self.cells["5e"]=white
        
        self.update_board()

if __name__=="__main__":
    game=Game()
    game.set_board()
    game.mainloop()
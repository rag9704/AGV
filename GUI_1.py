import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure 
#from graph_editer import graph_editor
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from Main import main,main_1
import json
from test_1 import test_visualize
from tkinter.filedialog import asksaveasfile


class Main(tk.Tk):

    def __init__(self,*args,**kwargs):   #args -->arguement(open ended), kwargs-->key word araguement, dictinoary

        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.title(self,'AGV Route Optimization')
        container = tk.Frame(self)

        container.pack(side = "top",fill = "both",expand = True)

        container.grid_rowconfigure(0,weight = 1)
        container.grid_columnconfigure(0,weight = 1)

        self.frames = {}

        for F in (StartPage,PageOne,PageTwo,PageJson):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row= 0,column = 0,sticky = "nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()

def graph_map(grid= True,grid_N = 30):
    global n,e,p
    plt.ion() # interactive mode !
    fig, ax = plt.subplots()
    
    ticks = np.linspace(0,1,grid_N)
    
    def init_ax():
        ax.clear()
        ax.set_xlim(0,1)
        ax.set_xticks(ticks)
        ax.set_xticklabels([])
        ax.set_ylim(0,1)
        ax.set_yticks(ticks)
        ax.set_yticklabels([])
        if grid:
            ax.grid()
    
    
    # 1st STEP
    
    print ("Place the nodes and press enter")
    init_ax()
    fig.canvas.draw
    nodes_pos = plt.ginput(-1,timeout=-1)
    
    if grid:
        # project the points on the nearest grid sections
        nodes_pos = [
            [
                ticks[np.argmin([abs(u-t) for t in ticks])]
                for u in (x,y)
            ]
            for x,y in nodes_pos
        ]
    nodes_posx, nodes_posy = zip(*nodes_pos)
    
    nodes = range(len(nodes_pos))
    
    
    # 2nd STEP
    
    print ("Place the edges and press enter")
    fig.canvas.draw()
    edges = []
    
    while True:
        # This loops goes as the user selects edges, and breaks when the
        # user presses enter without having selected an edge.
                
        # plot the current nodes and edges
        init_ax()
        for i,j in edges:
            x1,y1 = nodes_pos[i]
            x2,y2 = nodes_pos[j]
            ax.plot([x1,x2],(y1,y2),lw=2,c='k')
        ax.scatter(nodes_posx, nodes_posy, s=30)
        fig.canvas.draw()
        
        l = plt.ginput(2,timeout=-1)
        if len(l) == 0: # Enter has been pressed with no selection: end.
            break
        elif len(l) == 1: # only one point has been selected
            (x1,y1),(x2,y2) = nodes_pos[edges[-1][1]], l[0]
        else:  # only one point has been selected
            (x1,y1),(x2,y2) = l
        
        # find the nodes nearest from the positions of the clicks
        n1 = nodes[np.argmin([(x1-x)**2+(y1-y)**2 for x,y in nodes_pos])]
        n2 = nodes[np.argmin([(x2-x)**2+(y2-y)**2 for x,y in nodes_pos])]
        
        if (n1,n2) in edges: # a re-selection of an edge : remove
            edges.remove((n1,n2))
        else:
            edges.append((n1,n2)) # yeah ! one new edge in the graph
            
    plt.ioff()
    plt.close()

    n = nodes
    e = edges
    p = nodes_pos

    
    return n,e,p
    
    

class StartPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Automated Guided Vehicle Route Optimization Platform")
        label.pack(pady=10, padx = 10)

        button = tk.Button(self,text = "Enter Map",command = lambda:[graph_map(),controller.show_frame(PageOne)] )
        button.pack()

        label = tk.Label(self,text="Or")
        label.pack(pady=10, padx = 10)

        button1 = tk.Button(self,text = "Enter JSON File",command = lambda: controller.show_frame(PageJson)) # lambda: controller.show_frame(PageOne))
        button1.pack()


class PageOne(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self,text="Page 1 ")
        label.pack(pady=10, padx = 10)

        button1 = tk.Button(self,text = "Start Page",command = lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Display Map",
                            command= lambda: self.map_display(source,destination)) #self.map_display(n,e,p))
        button2.pack()

        button3 = tk.Button(self, text="Calculations",
                            command= lambda: self.calculate(n,e,p,source,destination,qc)) #self.map_display(n,e,p))
        button3.pack()

        label2 = tk.Label(self,text="Enter the Starting points (comma seperated) ")
        label2.pack(pady=10, padx = 10)
        source = tk.StringVar()
        nameEntered = tk.Entry(self, width=20, textvariable=source )
        nameEntered.pack()
        nameEntered.focus()

        label3 = tk.Label(self,text="Enter the Destination points (comma seperated) ")
        label3.pack(pady=10, padx = 10)

        destination = tk.StringVar()
        nameEntered = tk.Entry(self, width=20, textvariable=destination )
        nameEntered.pack()
        nameEntered.focus()
        
        qc = tk.IntVar()
        labelC = tk.Label(self, text="Method of computation: ")
        labelC.pack(pady=10, padx = 10)

        # Radio Button 1
        tabu = tk.Radiobutton(self, text="SASampler ", variable=qc, value=False)
        tabu.pack(pady=10, padx = 10)

        # Radio Button 2
        dwave = tk.Radiobutton(self, text="D-Wave Sampler", variable=qc, value=True)
        dwave.pack(pady=10, padx = 10)

        
        label = tk.Label(self, text="Time taken to solve QUBO instance (in seconds): ")
        label.pack()

        self.QUBO_time = tk.StringVar()
        self.T_0 = tk.Label(self, height=2, width=30, text="")
        self.T_0.pack()
        

    def map_display(self,source,destination):
            G = nx.Graph()
            G.add_nodes_from(n)
            G.add_edges_from(e)
            fig, ax = plt.subplots(1,figsize=(15,15))
            print(source)
            if source != None :
                s = source.get()
                d = destination.get()
                source_ = list(map(int,s.split(',')))
                destination_ = list(map(int,d.split(',')))
                color_map = []
                for no in G:
                    if no in source_:
                         color_map.append("green")
                    elif no in destination_ :
                         color_map.append("red")
                    else:
                         color_map.append("blue")
                nx.draw(G, p,node_color=color_map, ax=ax,with_labels = True )
            else:
                nx.draw(G, p, ax=ax,with_labels = True )
            canvas = FigureCanvasTkAgg(fig,self)
            canvas.draw()
            canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

            toolbar = NavigationToolbar2Tk(canvas,self)
            toolbar.update()
            canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

            button1 = tk.Button(self,text = "Start Page")
            button1.pack()
            #print(n)
            #print(e)
            #print(p)
            self.pos = {i:tuple(p[i]) for i in n}
            #mapss={"nodes":[]}
            mapss={"nodes":list(set(n)),"edges":e}
            #print('edges:::',e)
            with open('map_file.json','w') as f:
                json.dump(mapss,f)
                
            

    def calculate(self,n,e,p,source,destination,qc):
            s = source.get()
            d = destination.get()
            source_ = list(map(int,s.split(',')))
            destination_ = list(map(int,d.split(',')))
            
            #r = 3
            self.best,QUBO_time_ =main_1(n,e,p,source_,destination_,qc)
            print("best :",self.best)

            self.QUBO_time.set(QUBO_time_)
            self.T_0.config(text=self.QUBO_time.get())
            test_visualize(n,e,p,self.best)
        
        
    
class PageTwo(tk.Frame):

    def __init__(self,parent,controller):
        #
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self,text="Page 2 ")
        label.pack(pady=10, padx = 10)
        
        

    

    def map_display(self):
            G = nx.Graph()
            G.add_nodes_from(n)
            G.add_edges_from(e)
            fig, ax = plt.subplots(1)
            nx.draw(G, p, ax=ax,with_labels = True )
            canvas = FigureCanvasTkAgg(fig,self)
            canvas.draw()
            canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

            toolbar = NavigationToolbar2Tk(canvas,self)
            toolbar.update()
            canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

            button1 = tk.Button(self,text = "Start Page")
            button1.pack()

class PageJson(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self,text="Page 1 ")
        label.pack(pady=10, padx = 10)

        button1 = tk.Button(self,text = "Start Page",command = lambda: controller.show_frame(StartPage))
        button1.pack()

        label = tk.Label(self,text="Entering the address of in JSON file")
        label.pack()

        address = tk.StringVar()
        nameEntered = tk.Entry(self, width=20, textvariable=address )
        nameEntered.pack()
        nameEntered.focus()

        label2 = tk.Label(self,text="Enter the Starting points (comma seperated) ")
        label2.pack(pady=10, padx = 10)

        source = tk.StringVar()
        nameEntered = tk.Entry(self, width=20, textvariable=source )
        nameEntered.pack()
        nameEntered.focus()

        label3 = tk.Label(self,text="Enter the Starting points (comma seperated) ")
        label3.pack(pady=10, padx = 10)

        destination = tk.StringVar()
        nameEntered = tk.Entry(self, width=20, textvariable=destination )
        nameEntered.pack()
        nameEntered.focus()

        button2 = tk.Button(self, text="Display Map",
                            command= lambda: self.display_graph(address,source,destination)) #self.map_display(n,e,p))
        button2.pack(pady=10, padx = 10)

        qc = tk.IntVar()
        labelC = tk.Label(self, text="Method of computation: ")
        labelC.pack(pady=10, padx = 10)

        # Radio Button 1
        tabu = tk.Radiobutton(self, text="SASampler ", variable=qc, value=False)
        tabu.pack(pady=10, padx = 10)

        # Radio Button 2
        dwave = tk.Radiobutton(self, text="D-Wave ", variable=qc, value=True)
        dwave.pack(pady=10, padx = 10)

        button3 = tk.Button(self, text="Calculations",
                            command= lambda: self.Calulations(address,source,destination,qc)) #self.map_display(n,e,p))
        button3.pack(pady=10, padx = 10)

        label = tk.Label(self, text="Time taken to solve QUBO instance (in seconds): ")
        label.pack(pady=10, padx = 10)

        self.QUBO_time = tk.StringVar()
        self.T_0 = tk.Label(self, height=2, width=30, text="")
        self.T_0.pack()

        self.nodes = []
        self.edges = []
        self.pos = {}

    def display_graph(self,address,source,destination):
            s = source.get()
            d = destination.get()
            source_ = list(map(int,s.split(',')))
            destination_ = list(map(int,d.split(',')))
            with open(address.get()) as f:
                instance = json.load(f)
            self.nodes = instance["nodes"]
            print(self.nodes)

            self.edges = instance["edges"]
            self.edges = [tuple(e) for e in self.edges]

            pos_1 = instance["pos"]
            self.pos = {int(n): tuple(pos_1[n]) for n in pos_1}

            G = nx.Graph()
            G.add_nodes_from(self.nodes)
            G.add_edges_from(self.edges)
            color_map = []
            for no in G:
                if no in source_:
                    color_map.append("green")
                elif no in destination_:
                    color_map.append("red")
                else:
                    color_map.append("blue")
                                     
                
            fig, ax = plt.subplots(1,figsize=(15,15))
            nx.draw(G, self.pos,node_color=color_map ,ax=ax,with_labels = True )
            canvas = FigureCanvasTkAgg(fig,self)
            canvas.draw()
            canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

            toolbar = NavigationToolbar2Tk(canvas,self)
            toolbar.update()
            canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

    def Calulations(self,address,source,destination,qc):
            s = source.get()
            d = destination.get()
            source_ = list(map(int,s.split(',')))
            destination_ = list(map(int,d.split(',')))
            address_ = address.get()
            print(qc.get())
            r = 3
            self.best,QUBO_time_ =main(len(source_),r,address_,source_,destination_,qc)
            print("best :",self.best)

            self.QUBO_time.set(QUBO_time_)
            self.T_0.config(text=self.QUBO_time.get())
    
            with open(address_) as f:
                instance = json.load(f)
            self.nodes = instance["nodes"]
            print(self.nodes)

            self.edges = instance["edges"]
            self.edges = [tuple(e) for e in self.edges]

            pos_1 = instance["pos"]
            self.pos = {int(n): tuple(pos_1[n]) for n in pos_1}
            test_visualize(self.nodes,self.edges,self.pos,self.best)

            

            


app = Main()
app.mainloop()
        

# "C:\Users\Rag9704\Desktop\jija pd\AGV\Original\Final\GUI"

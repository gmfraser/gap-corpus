import getpass, datetime, sqlite3, pygame, time, csv, platform
import tkinter.simpledialog as tkSimpleDialog
import tkinter.filedialog as tkFileDialog
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

from tkinter import *

from PIL import Image, ImageTk, ImageWin


import numpy
import nltk#; nltk.download('punkt')

from sklearn import datasets, linear_model, metrics
from sklearn.metrics import confusion_matrix

#import convokit
        
print(platform.system())

if platform.system() == 'Windows':
    print("You are using Windows!")
    DASH = '\\'
    OS = "Windows"
else:
    DASH = '//'
    OS = "Linux"
    
## Saved for later
##import matplotlib
##matplotlib.use("TkAgg")
##from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
##from matplotlib.figure import Figure

##KNOWN BUGS
    
# Try loading when data already loaded bug

VERSION = '1.3.0'
UPDATED = 'July 23/2020'
PROGID = "BCORPUS"
AUTHOR = 'Jeremy Wright'
ADVISOR = 'Gabriel Murray'
USERNAME = getpass.getuser()
LOGDATE = datetime.date.today()
DATABASE = "Database"+DASH+"Corpus.db"
FILTERS = []

MAINCOLOUR = "WHITE"
SECCOLOUR = "WHITE"
GUIBLUE = "#bbddff"

VISIBLE = []

AUDIOFILE = ""
# Saved for later
##XPLOT = [5,6,1,3,8,9,3,5]
##YPLOT = [1,2,3,4,5,6,7,8]

class Main:

    def __init__(self, master):
        print("HERE1")
        self.master = master

        ##### GUI SETUP #####

        self.menubar = Menu(root)
        self.padding = 5
        self.paddingBut = 2.5
        self.defaultW = 85 #Table column width
        self.defaultMinW = 60
        
        self.tipsOn = 1
        self.autoRunJob = None

        
        self.filemenu = Menu(self.menubar, tearoff=0)
        #self.filemenu.add_command(label="TEST", command=lambda: self.chooseColumns(self.detTree))
        self.filemenu.add_command(label="Exit", command=self.exitGUI)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
            
        root.config(menu=self.menubar)

        #### START TABS

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=0, fill=BOTH)
        self.tabs.bind('<Button-1>', self.tabClick)
        
        self.tab1Frame = Frame(self.tabs, bg=MAINCOLOUR)
        self.tab1Frame.pack(side=TOP, expand=1, fill=BOTH)

        self.tab2Frame = Frame(self.tabs, bg=MAINCOLOUR)
        self.tab2Frame.pack(side=TOP, expand=1, fill=BOTH)

        self.tab3Frame = Frame(self.tabs, bg=MAINCOLOUR)
        self.tab3Frame.pack(side=TOP, expand=1, fill=BOTH)

        self.tabs.add(self.tab1Frame, text="Browse")
        self.tabs.add(self.tab2Frame, text="Annotations")
        self.tabs.add(self.tab3Frame, text="Learn")

        
        
#### TAB 1 Browse

        
        self.mainFrame  = Frame(root, bg=MAINCOLOUR)#, bg="GREEN")
        self.mainFrame.pack(expand=1, fill=BOTH)

        self.footerFrame = Frame(root, height=20, bg=MAINCOLOUR)#, bg="WHITE")
        self.footerFrame.pack(side=BOTTOM, expand=0, fill=X)

        self.userLabelLabel = Label(self.footerFrame, text="Username: ", bg=MAINCOLOUR)
        self.userLabelLabel.pack(side=LEFT)
        
        self.userText = StringVar()
        self.userText.set(USERNAME)
        self.userLabel = Label(self.footerFrame, textvariable=self.userText, bg=MAINCOLOUR)
        self.userLabel.pack(side=LEFT)
        

        ######### MEETING LISTS FRAME
        self.ltFrame = Frame(self.mainFrame, bg=MAINCOLOUR)#,  bg="BLUE")
        self.ltFrame.pack(side=LEFT, expand=1, pady=self.padding, padx=self.padding, fill=BOTH)

##        ################ MEETING LIST BUTTONS
##        self.ltBtnFrame = Frame(self.tab1Frame, bg=MAINCOLOUR)#, bg="BLACK") # Has the notebook in it
##        self.ltBtnFrame.pack(side=TOP, expand=0, pady=self.padding, padx=self.padding,  fill=BOTH)

        ##
        self.ltListFrame = Frame(self.ltFrame, bg=MAINCOLOUR)#, bg="WHITE")
        self.ltListFrame.pack(side=BOTTOM, expand=1, pady=self.padding, padx=self.padding,  fill=BOTH)

        ##         # MEETING LIST MASTER
        self.ltMtFrame = Frame(self.ltListFrame, bg=MAINCOLOUR)#, bg="DARK GREEN")
        self.ltMtFrame.pack(side=LEFT, expand=0, pady=self.padding, padx=self.padding, fill=BOTH)

##         # MEETING LIST MASTER
        self.ltMt2Frame = Frame(self.ltListFrame, width=200, bg=MAINCOLOUR)#, bg="ORANGE")
        self.ltMt2Frame.pack(side=RIGHT, expand=1, pady=self.padding, padx=self.padding, fill=BOTH)


        ### MEETING LIST DETAIL
        self.ltMtDtlFrame = Frame(self.ltMt2Frame, bg=MAINCOLOUR)#, bg="DARK BLUE")
        self.ltMtDtlFrame.pack(side=TOP, expand=1, pady=self.padding, padx=self.padding,  fill=BOTH)


##          # Footer below annotation list
        self.ltFootAFrame = Frame(self.ltMt2Frame, bg=MAINCOLOUR)#, bg="YELLOW")
        self.ltFootAFrame.pack(side=TOP, expand=0, pady=self.padding, padx=self.padding, fill=X)
        

##          # Footer below annotation list
        self.ltFootBFrame = Frame(self.ltMt2Frame, bg=MAINCOLOUR)#, bg="YELLOW")
        self.ltFootBFrame.pack(side=TOP, expand=0, pady=self.padding, padx=self.padding, fill=X)

##                #Label frame
        self.ltFootCFrame = Frame(self.ltMt2Frame, bg=MAINCOLOUR)
        self.ltFootCFrame.pack(side=TOP, expand=1, pady=self.padding, padx=self.padding, fill=BOTH)
        
        
        # DETAIL FRAME
        self.dtlFrame = Frame(self.mainFrame, bg=MAINCOLOUR)#, bg="PURPLE")
        self.dtlFrame.pack(side=RIGHT, expand=0, pady=self.padding, padx=self.padding, fill=BOTH)

        ##            # MEETING STATS FRAME
        self.dtlStatsFrame = Frame(self.dtlFrame, bg=MAINCOLOUR)#,  bg="GREY")
        self.dtlStatsFrame.pack(side=TOP, expand=1, pady=self.padding, padx=self.padding,  fill=BOTH)

        


        
##     # PARTICIPANTS FRAME
        self.dtlParFrame = Frame(self.dtlFrame, bg=MAINCOLOUR)#, bg="BROWN")
        self.dtlParFrame.pack(side=TOP, expand=1, pady=self.padding, padx=self.padding,  fill=BOTH)

        ##            # SHOWS AUDIO VISUALS AND BUTTONS
        self.dtlAudioFrame = Frame(self.dtlFrame, bg=MAINCOLOUR)#, bg="YELLOW")
        self.dtlAudioFrame.pack(side=TOP, expand=1, pady=self.padding, padx=self.padding, fill=BOTH)

        self.dtlAudioAFrame = Frame(self.dtlAudioFrame, bg=MAINCOLOUR)#, bg="RED")
        self.dtlAudioAFrame.pack(side=TOP, expand=1, pady=self.padding, padx=self.padding, fill=BOTH)
        
        self.dtlAudioBFrame = Frame(self.dtlAudioFrame, bg=MAINCOLOUR)#, bg="RED")
        self.dtlAudioBFrame.pack(side=BOTTOM, expand=1, pady=self.padding, padx=self.padding, fill=BOTH)


        self.featFrame = Frame(self.mainFrame, bg=MAINCOLOUR)#, bg="PURPLE")
        #self.featFrame.pack(side=RIGHT, expand=0, pady=self.padding, padx=self.padding, fill=BOTH)
        

##        # LOAD DATABASE BUTTON
##
##        image = Image.open("Required"+DASH+"table_go.png")
##        self.photo = ImageTk.PhotoImage(image)
##        self.conButPic = self.photo
##        self.conBut = Button(self.tab1Frame, image=self.conButPic, relief=FLAT, command=self.getDatabase, bg=SECCOLOUR)
##        self.conBut.pack(side=LEFT, pady=self.paddingBut, padx=self.paddingBut)
##        TT = ToolTip(self.conBut, "Choose database.")


                # LOAD DATA BUTTON

        image = Image.open("Required"+DASH+"table_go.png")
        self.photo = ImageTk.PhotoImage(image)
        self.loadButPic = self.photo
        self.loadBut = Button(self.tab1Frame, image=self.loadButPic, relief=FLAT, command=self.loadData, bg=SECCOLOUR)
        self.loadBut.pack(side=LEFT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.loadBut, "Load master meeting data.")


         # FILTER BUTTON

        image = Image.open("Required"+DASH+"table_refresh.png")
        self.photo = ImageTk.PhotoImage(image)
        self.refreshPic = self.photo
        self.refreshBut = Button(self.tab1Frame, image=self.refreshPic,  relief=FLAT, command=self.refresh, bg=SECCOLOUR)
        self.refreshBut.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.refreshBut, "Refresh meeting data.")
        

        # SEARCH BUTTON

        image = Image.open("Required"+DASH+"search.png")
        self.photo = ImageTk.PhotoImage(image)
        self.searchPic = self.photo
        self.searchBut = Button(self.tab1Frame, image=self.searchPic,  relief=FLAT, command=self.findItem, bg=SECCOLOUR)
        self.searchBut.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.searchBut, "Search meeting data for keywords.")
        

        self.searchFrame = Frame(self.tab1Frame, bg=MAINCOLOUR)
        self.searchFrame.pack(side=RIGHT, expand=0, padx=5, pady=5, fill=Y)
        
##        self.searchLabel = Label(self.searchFrame, text="Find Item: ", width=9, bg=MAINCOLOUR)
##        self.searchLabel.pack(side=LEFT)

        self.searchEnter = Entry(self.searchFrame)
        self.searchEnter.pack(side=LEFT, expand=1, fill=X)
        self.searchEnter.bind("<Return>", self.findItem)
        TT = ToolTip(self.searchEnter, "Enter keywords to search, search is compounded.")

        
        image = Image.open("Required"+DASH+"info.png")
        self.photo = ImageTk.PhotoImage(image)
        self.infoPic = self.photo
        self.filterLabel = Label(self.searchFrame, text="Filters", image=self.infoPic, bg=MAINCOLOUR)
        self.filterLabel.pack(side=LEFT)
        IV = InfoView(self.filterLabel, FILTERS)
        
        
    

                # CHOOSE VISIBLE COLUMNS
        image = Image.open("Required"+DASH+"table_gear.png")
        self.photo = ImageTk.PhotoImage(image)
        self.hideColumnPic = self.photo
        self.hideColBut = Button(self.tab1Frame, image=self.hideColumnPic, relief=FLAT, command=self.setColumns, bg=SECCOLOUR)
        self.hideColBut.pack(side=LEFT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.hideColBut, "Hide/Show columns.")

        image = Image.open("Required"+DASH+"excel.png")
        self.photo = ImageTk.PhotoImage(image)
        self.toExcelPic = self.photo
        self.toExcel = Button(self.tab1Frame, image=self.toExcelPic, relief=FLAT, command=self.exportExcel, bg=SECCOLOUR)
        self.toExcel.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.toExcel, "Export all to CSV file.")


                 # ADD ANNOTATION COLUMN BUTTON

        image = Image.open("Required"+DASH+"table_col_add.png")
        self.photo = ImageTk.PhotoImage(image)
        self.addColPicTAB2 = self.photo
        self.addColButTAB2 = Button(self.tab2Frame, image=self.addColPicTAB2, relief=FLAT, command=self.addCol, bg=SECCOLOUR)
        self.addColButTAB2.pack(side=LEFT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.addColButTAB2, "Add a column.")

        
        image = Image.open("Required"+DASH+"table_col_delete.png")
        self.photo = ImageTk.PhotoImage(image)
        self.remColPicTAB2 = self.photo
        self.remColButTAB2 = Button(self.tab2Frame, image=self.remColPicTAB2, relief=FLAT, command=self.remCol, bg=SECCOLOUR)
        self.remColButTAB2.pack(side=LEFT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.remColButTAB2, "Remove a column.")
        

        image = Image.open("Required"+DASH+"excel.png")
        self.photo = ImageTk.PhotoImage(image)
        self.toExcelPicTAB2 = self.photo
        self.toExcelTAB2 = Button(self.tab2Frame, image=self.toExcelPicTAB2, relief=FLAT, command=self.exportExcel, bg=SECCOLOUR)
        self.toExcelTAB2.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.toExcelTAB2, "Export all to CSV file.")
        
### TAB 2
        # DELETE ANNOTATION COLUMN BUTTON

        

        self.setFrame = LabelFrame(self.tab3Frame, bg="WHITE")
        self.setFrame.pack(side=RIGHT, expand=0, fill=BOTH)

        self.setFrame1 = Frame(self.setFrame, bg="WHITE")
        self.setFrame1.pack(side=TOP, expand=0, fill=BOTH)

        self.setFrame2 = Frame(self.setFrame, bg="WHITE")
        self.setFrame2.pack(side=BOTTOM, expand=0, fill=BOTH)

        self.balFrame = Frame(self.setFrame1, bg=MAINCOLOUR)
        self.balFrame.pack(side=BOTTOM, expand=1, padx=5, pady=5, fill=BOTH)
        
        self.balLabel = Label(self.setFrame1, width=25, anchor="w", text="Balanced class weight:", bg="WHITE")
        self.balLabel.pack(side=LEFT, padx=2.5, pady=2.5)
        TT = ToolTip(self.balLabel, "Use balanced class weight?")
    
        #Do you want to use balanced class weight?
        MODES = [("No", "0"), ("Yes", "1")]

        self.balanceClass = StringVar()
        self.balanceClass.set("1") # initialize

        for text, mode in MODES:
            b = Radiobutton(self.setFrame1, text=text, variable=self.balanceClass, value=mode, bg="WHITE")
            b.pack(side=LEFT, fill=X)
            TT = ToolTip(b, "Use balanced class weight?")
        
        self.trainPerLabel = Label(self.setFrame2, width=10, anchor="w", text="Train %", bg="WHITE")
        self.trainPerLabel.pack(side=LEFT, padx=2.5, pady=2.5)
        TT = ToolTip(self.trainPerLabel, "What percentage of the entire dataset should be for training?")
        
        self.trainPerEntry = Entry(self.setFrame2, text="Train %", bg="WHITE", foreground="BLACK", relief='solid', borderwidth=1)
        self.trainPerEntry.pack(side=LEFT, padx=2.5, pady=2.5)
        self.trainPerEntry.insert(END, '50')
        self.trainPerEntry.bind("<FocusOut>",self.balancePer)
        self.trainPerEntry.bind("<Enter>",self.balancePer)
        self.trainPerEntry.bind("<Return>",self.balancePer)
        
        self.testPerLabel = Label(self.setFrame2, width=10, anchor="w", text="Test %", bg="WHITE")
        self.testPerLabel.pack(side=LEFT, padx=2.5, pady=2.5)
        TT = ToolTip(self.testPerLabel, "What percentage of the entire dataset should be for testing?")
        
        self.testPerEntry = Entry(self.setFrame2, text="Test %", bg="WHITE", foreground="BLACK", relief='solid', borderwidth=1)
        self.testPerEntry.pack(side=LEFT, padx=2.5, pady=2.5)
        self.testPerEntry.insert(END, '50')
        self.testPerEntry.configure(state='disabled')
    

        
        image = Image.open("Required"+DASH+"wand.png")
        self.photo = ImageTk.PhotoImage(image)
        self.wandPic = self.photo
        self.wandBut = Button(self.tab3Frame, image=self.wandPic, relief=FLAT, command=self.logReg, bg=SECCOLOUR)
        self.wandBut.pack(side=LEFT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.wandBut, "Wave the magic logistic regression wand.")
        

        image = Image.open("Required"+DASH+"excel.png")
        self.photo = ImageTk.PhotoImage(image)
        self.dataDumpPic = self.photo
        self.dataDumpBut = Button(self.tab3Frame, image=self.dataDumpPic, relief=FLAT, command=lambda dumpOnly="Y": self.logReg(dumpOnly), bg=SECCOLOUR)
        self.dataDumpBut.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.dataDumpBut, "Data dump for use in other ML applications.")
        
        
        image = Image.open("Required"+DASH+"brick_delete.png")
        self.photo = ImageTk.PhotoImage(image)
        self.remFPic = self.photo
        self.remFBut = Button(self.tab3Frame, image=self.remFPic, relief=FLAT, command=self.remFeature, bg=SECCOLOUR)
        self.remFBut.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.remFBut, "Remove feature.")

        
        image = Image.open("Required"+DASH+"brick_add.png")
        self.photo = ImageTk.PhotoImage(image)
        self.addFButPic = self.photo
        self.addFBut = Button(self.tab3Frame, image=self.addFButPic, relief=FLAT, command=self.addFeature, bg=SECCOLOUR)
        self.addFBut.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.addFBut, "Add feature.")

        print("HERE2")
        ###### GET VARIABLE TABLE COLUMNS

        alldem = self.getTableColumns("AnnotationMaster")
        
        self.detColumns = []
        for i in alldem:
            self.detColumns.append(i[1])
      
        ################
        self.values = [""]
        self.tChoice = StringVar()
        self.tChoice.set("Outcome Variable")
        self.tChoice.trace("w", self.variableSelect)
        if len(self.detColumns) == 0:
            self.tList = OptionMenu(self.tab3Frame, self.tChoice, *self.detColumns, state="disabled")
        else:
            self.tList = OptionMenu(self.tab3Frame, self.tChoice, *self.detColumns)
        self.tList.config(bg = "White", width=25)
        self.tList.pack(side=LEFT, padx=3, pady=2, ipadx=5, ipady=2)
            
        self.vChoice = StringVar()
        self.vChoice.set("Positive Class")
        self.vChoice.trace("w", self.loadFeatures)
        #self.vChoice.trace("w", self.classSelect)
        self.vList = OptionMenu(self.tab3Frame, self.vChoice, *self.values)
        self.vList.config(bg = "White", width=25)
        self.vList.pack(side=LEFT, padx=3, pady=2, ipadx=5, ipady=2)

        print("HERE3")
        
    ###### GET VARIABLE TABLE COLUMNS

        alldem = self.getTableColumns("MeetingMaster")

        self.mastColumns = []
        for i in alldem[0:3]:
            self.mastColumns.append(i[1])

 ################
        print("HERE4")
            # Master Group/Meeting List

        self.mastbarY = Scrollbar(self.ltMtFrame)
        self.mastbarY.pack(side=RIGHT, fill=Y)
        self.mastbarX = Scrollbar(self.ltMtFrame, orient=HORIZONTAL)
        self.mastbarX.pack(side=BOTTOM, fill=X)
        
        self.mastTree = ttk.Treeview(self.ltMtFrame, columns=self.mastColumns, yscrollcommand=self.mastbarY.set, xscrollcommand=self.mastbarX.set)
        TT = ToolTip(self.mastTree, "List of unique meetings.")

        for col in self.mastColumns:
            self.mastTree.heading(col, text=col, command=lambda x=col: self.sortCol(self.mastTree, x, False))
            self.mastTree.column(col, width=self.defaultW, minwidth=self.defaultMinW, anchor="center")

        self.mastTree.pack(side=BOTTOM, ipady=self.padding, ipadx=self.padding,  pady=self.padding, padx=self.padding, expand=1, fill=BOTH)

        self.mastTree['show'] = 'headings'
        
        self.mastTree.bind('<ButtonPress-1>', self.mastItemClick)
        self.mastTree.bind('<MouseWheel>', self.onMouseWheelMast)
        
        self.mastbarY.config(command=self.mastTree.yview)
        self.mastbarX.config(command=self.mastTree.xview)

        print("HERE4.5")
        self.detbarY = Scrollbar(self.ltMtDtlFrame)
        self.detbarY.pack(side=RIGHT, fill=Y)
        self.detbarX = Scrollbar(self.ltMtDtlFrame, orient=HORIZONTAL)
        self.detbarX.pack(side=BOTTOM, fill=X)
        
        self.detTree = ttk.Treeview(self.ltMtDtlFrame, columns=self.detColumns, yscrollcommand=self.detbarY.set, xscrollcommand=self.detbarX.set)
        TT = ToolTip(self.detTree, "List of selected meeting annotations.")

        if len(self.detColumns) == 0:
            wid = (root.winfo_width()/5)
        else:   
            wid = (root.winfo_width()/len(self.detColumns))/2
        
        for col in self.detColumns:
            self.detTree.heading(col, text=col, command=lambda x=col: self.sortCol(self.detTree, x, False))
            self.detTree.column(col, width=int(wid), minwidth=10, anchor="center")
        
        print("HERE5")
        self.detTree.pack(side=TOP, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding, expand=1, fill=BOTH)
        ttk.Style().configure("Treeview", rowheight=25, foreground="BLACK", font="Arial 8")

        self.detTree['show'] = 'headings'

        root.update()
        for col in self.detColumns:
            self.detTree.column(col, width=self.defaultW, minwidth=self.defaultMinW, anchor="center")
            VISIBLE.append((col,"1"))
                           
        self.detbarY.config(command=self.detTree.yview)
        self.detbarX.config(command=self.detTree.xview)

        self.detTree.bind('<ButtonPress-1>', self.detItemClick)
        self.detTree.bind('<MouseWheel>', self.onMouseWheelDet)
        self.detTree.bind('<Button-3>', self.popupMenu)
        self.detTree.bind('<Double-1>', self.editLine)



        image = Image.open("Required"+DASH+"next.png")
        self.photo = ImageTk.PhotoImage(image)
        self.nextPic = self.photo
        self.nextBut = Button(self.ltFootAFrame, image=self.nextPic, relief=FLAT, command=self.nextMeeting, bg=SECCOLOUR)
        self.nextBut.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.nextBut, "Move to next meeting.")

        image = Image.open("Required"+DASH+"back.png")
        self.photo = ImageTk.PhotoImage(image)
        self.backPic = self.photo
        self.backBut = Button(self.ltFootAFrame, image=self.backPic, relief=FLAT, command=self.prevMeeting, bg=SECCOLOUR)
        self.backBut.pack(side=LEFT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.backBut, "Move to previous meeting.")

        
        ## Details about clicked line
        self.clickVar = StringVar()
        self.clickVar.set('')

        self.clickLab = Label(self.ltFootBFrame, text="Column: ", bg=MAINCOLOUR)
        self.clickLab.pack(side=LEFT, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding)
        
        self.clickVarLab = Label(self.ltFootBFrame, textvar=self.clickVar,  bg=MAINCOLOUR)
        self.clickVarLab.pack(side=LEFT, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding)

        self.valueVar = StringVar()
        self.valueVar.set('')

        self.valueLab = Label(self.ltFootBFrame, text="Search Value: ", bg=MAINCOLOUR)
        self.valueLab.pack(side=LEFT, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding)
        
        self.valueVarLab = Label(self.ltFootBFrame, textvar=self.valueVar,  bg=MAINCOLOUR)
        self.valueVarLab.pack(side=LEFT, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding)

        self.countVar = StringVar()
        self.countVar.set('')

        self.countLab = Label(self.ltFootBFrame, text="Occurrences: ", bg=MAINCOLOUR)
        self.countLab.pack(side=LEFT, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding)
        
        self.countVarLab = Label(self.ltFootBFrame, textvar=self.countVar,  bg=MAINCOLOUR)
        self.countVarLab.pack(side=LEFT, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding)
        
        self.sep = ttk.Separator(self.ltFootCFrame, orient=HORIZONTAL)
        self.sep.pack(side=TOP, fill=X, expand=1)

        self.valueLab = Label(self.ltFootCFrame, text="To add features, double click or highlight any word(s) and right click to add it to the feature list.", bg=MAINCOLOUR)
        self.valueLab.pack(side=BOTTOM, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding)
        
        
        self.infoText = Text(self.ltFootCFrame, height=1, width=15, borderwidth=0, bg=MAINCOLOUR) #TEXT SO PEOPLE CAN COPY PASTE IT
        self.infoText.pack(side=BOTTOM, fill=BOTH, expand=1)
        self.infoText.insert('0.0', "None")
        self.infoText.configure(state="disabled")
        self.infoText.bind("<Button-3>",self.addFeature)





        #Label above meeting table
        self.mtnLabel = Label(self.dtlStatsFrame, text="Meeting Information")
        self.mtnLabel.pack(side=TOP, expand=0, fill=X)

        # Variables for the meeting
        self.columns = ["Variable", "Value"]

        self.statsTree = ttk.Treeview(self.dtlStatsFrame, columns=self.columns)

        for col in self.columns:
            self.statsTree.heading(col, text=col)
            
        self.statsTree.column("Variable",width=150, minwidth=self.defaultMinW, anchor="w")
        self.statsTree.column("Value",width=150, minwidth=self.defaultMinW, anchor="w")

        self.statsTree.pack(side=TOP, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding, expand=1, fill=BOTH)

        self.statsTree['show'] = 'headings'



        self.parLabel = Label(self.dtlParFrame, text="Participant Information")
        self.parLabel.pack(fill=X)
        
                # Variables for the meeting
        self.columns = ["Variable", "Value"]

        self.parTree = ttk.Treeview(self.dtlParFrame, columns=self.columns)

        for col in self.columns:
            self.parTree.heading(col, text=col)
            
        self.parTree.column("Variable",width=150, minwidth=self.defaultMinW, anchor="w")
        self.parTree.column("Value",width=150, minwidth=self.defaultMinW, anchor="w")
        
        self.parTree.pack(side=TOP, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding, expand=1, fill=BOTH)

        self.parTree['show'] = 'headings'


        # Start, End, Duration variables and the labels
        self.stimeVar = StringVar()
        self.stimeVar.set(0.0)

        self.stimeLab = Label(self.dtlAudioAFrame, text="Start Time: ", bg=MAINCOLOUR)
        self.stimeLab.pack(side=LEFT)
        
        self.stimeVarLab = Label(self.dtlAudioAFrame, textvar=self.stimeVar,  bg=MAINCOLOUR)
        self.stimeVarLab.pack(side=LEFT)

        self.etimeVar = StringVar()
        self.etimeVar.set(0.0)

        self.etimeLab = Label(self.dtlAudioAFrame, text="End Time: ", bg=MAINCOLOUR)
        self.etimeLab.pack(side=LEFT)
        
        self.etimeVarLab = Label(self.dtlAudioAFrame, textvar=self.etimeVar,  bg=MAINCOLOUR)
        self.etimeVarLab.pack(side=LEFT)

        self.dtimeVar = StringVar()
        self.dtimeVar.set(0.0)

        self.dtimeLab = Label(self.dtlAudioAFrame, text="Duration: ", bg=MAINCOLOUR)
        self.dtimeLab.pack(side=LEFT)
        
        self.dtimeVarLab = Label(self.dtlAudioAFrame, textvar=self.dtimeVar,  bg=MAINCOLOUR)
        self.dtimeVarLab.pack(side=LEFT)

        ## Audio control buttons

        image = Image.open("Required"+DASH+"play.png")
        self.photo = ImageTk.PhotoImage(image)
        self.playPic = self.photo
        self.playBut = Button(self.dtlAudioBFrame, image=self.playPic, relief=FLAT, command=self.playAudioClip, bg=SECCOLOUR)
        self.playBut.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.playBut, "Play meeting recording.")

##             # NEXT BUTTON
##        self.button = Button(self.dtlAudioBFrame, text="NEXT", command=None)
##        self.button.pack(side=RIGHT, expand=1,  fill=BOTH)


        image = Image.open("Required"+DASH+"pause.png")
        self.photo = ImageTk.PhotoImage(image)
        self.pausePic = self.photo
        self.pauseBut = Button(self.dtlAudioBFrame, image=self.pausePic, relief=FLAT, command=self.stopAudioClip, bg=SECCOLOUR)
        self.pauseBut.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
        TT = ToolTip(self.pauseBut, "Stop meeting recording.")

##
##        image = Image.open("Required"+DASH+"repeat.png")
##        self.photo = ImageTk.PhotoImage(image)
##        self.rePic = self.photo
##        self.reBut = Button(self.dtlAudioBFrame, image=self.rePic, relief=FLAT, command=self.firstAudioClip, bg=SECCOLOUR)
##        self.reBut.pack(side=RIGHT, pady=self.paddingBut, padx=self.paddingBut)
##        TT = ToolTip(self.reBut, "Stop meeting recording.")
        
##             # BACK BUTTON
##        self.button = Button(self.dtlAudioBFrame, text="BACK",  command=None)
##        self.button.pack(side=RIGHT, expand=1,  fill=BOTH)


                ###### GET VARIABLE TABLE COLUMNS

        alldem = self.getTableColumns("FeatureMaster")

        self.featColumns = []
        for i in alldem:
            self.featColumns.append(i[1])

 ################

            # Master Group/Meeting List

        self.featbarY = Scrollbar(self.featFrame)
        self.featbarY.pack(side=RIGHT, fill=Y)
        self.featbarX = Scrollbar(self.featFrame, orient=HORIZONTAL)
        self.featbarX.pack(side=BOTTOM, fill=X)
        
        self.featTree = ttk.Treeview(self.featFrame, columns=self.featColumns, yscrollcommand=self.featbarY.set, xscrollcommand=self.featbarX.set)
        TT = ToolTip(self.featTree, "List of selected features.")
        
        for col in self.featColumns:
            self.featTree.heading(col, text=col, command=lambda x=col: self.sortCol(self.featTree, x, False))
            self.featTree.column(col, width=self.defaultW, minwidth=self.defaultMinW, anchor="center")

        self.featTree.pack(side=BOTTOM, ipady=self.padding, ipadx=self.padding,  pady=self.padding, padx=self.padding, expand=1, fill=BOTH)

        self.featTree['show'] = 'headings'
        
        #self.featTree.bind('<ButtonPress-1>', self.featItemClick)
        self.featTree.bind('<MouseWheel>', self.onMouseWheelfeat)
        
        self.featbarY.config(command=self.featTree.yview)
        self.featbarX.config(command=self.featTree.xview)
        

        
        
        #Color tags for treeviews
        self.detTree.tag_configure("even", foreground="black", background="WHITE")
        self.detTree.tag_configure("odd", foreground="black", background=GUIBLUE)
        self.detTree.tag_configure("found", foreground="white", background="BLACK")
        self.mastTree.tag_configure("even", foreground="black", background="WHITE")
        self.mastTree.tag_configure("odd", foreground="black", background=GUIBLUE)
        self.statsTree.tag_configure("even", foreground="black", background="WHITE")
        self.statsTree.tag_configure("odd", foreground="black", background=GUIBLUE)
        self.parTree.tag_configure("even", foreground="black", background="WHITE")
        self.parTree.tag_configure("odd", foreground="black", background=GUIBLUE)
        self.featTree.tag_configure("even", foreground="black", background="WHITE")
        self.featTree.tag_configure("odd", foreground="black", background=GUIBLUE)

        
        self.popup = Menu(root, tearoff=0)
        self.popup.add_command(label="Hide Column", command=self.setColumns)
        
### Preloaded images
        image = Image.open("Required"+DASH+"cancel.png")
        self.photo = ImageTk.PhotoImage(image)
        self.cancelPic = self.photo

        
        image = Image.open("Required"+DASH+"save.png")
        self.photo = ImageTk.PhotoImage(image)
        self.savePic = self.photo
#########
        print("HERE6")
    def balancePer(self, e=''):

        tr = int(self.trainPerEntry.get())
        if tr < 100:
            self.testPerEntry.configure(state='normal')
            te = 100-tr
            self.testPerEntry.delete(0,END)
            self.testPerEntry.insert(END,str(te))
            self.testPerEntry.configure(state='disabled')
        else:

            tkMessageBox.showinfo("Oops!", "Training data percentage must be an integer less than 100!")
            
    ## Saved for later
##    def plot(self):
##
##        global XPLOT, YPLOT
##
##        #If the plot isn't showing, show it, else, clear it and rebuild it.
##        try:
##            self.canvas.get_tk_widget().pack_forget()
##            self.canvas._tkcanvas.pack_forget()
##        except:
##            pass
##        
##        f = Figure(figsize=(5,5), dpi=100)
##        self.a = f.add_subplot(111)
##        self.a.plot(XPLOT,YPLOT)
##
##        self.canvas = FigureCanvasTkAgg(f, self.graphFrame)
##        self.canvas.draw()
##        self.canvas.get_tk_widget().pack(side=BOTTOM, expand=True)
##
##        XPLOT = [1,2,3,4,5,6,7,8]
##        YPLOT = [2,3,4,5,6,7,7,7]
##
        

    def logReg(self, dumpOnly = 'N'):

        global CONN, CURSOR

        logistic = ''
        balChoice = ''
        
        if self.balanceClass.get() == '1':
            logistic = linear_model.LogisticRegression(max_iter=1000, random_state=42, solver='liblinear', class_weight='balanced')
            balChoice = "balanced"
        else:
            logistic = linear_model.LogisticRegression(max_iter=1000, random_state=42, solver='liblinear')
            balChoice = "not balanced"
            
        #column = tkSimpleDialog.askstring("Column","Enter column to predict:", parent=root)
        column = self.tChoice.get()
        
        if column != None:

            #predField = tkSimpleDialog.askstring("Value","Enter value to predict:", parent=root)
            predField = self.vChoice.get()
            #column = "Sentiment"
            #predField = "Positive"

            if predField != None:
            
                    
                features = ["I", "my", "uh", "$"]

                self.connect()
                
                Q = 'SELECT Feature FROM "FeatureMaster" WHERE OutcomeVariable = "{}" AND PositiveClass = "{}"'.format(str(column), str(predField))

                CURSOR = CONN.cursor()
                CURSOR.execute(Q)

                alldem = CURSOR.fetchall()
                print(Q)
                print(alldem)
                features = []
                for i in list(alldem):
                    features.append(str(i[0]))
                #features = list(alldem)
                print(list(alldem))
                
                xtrain = []
                ytrain = []
                xtest = []
                ytest = []

                posCountTrain = 0
                posCountTest = 0

                ##GET TOTAL ROW COUNT
                self.connect()
                
                Q = 'SELECT COUNT(ID) FROM "AnnotationMaster"'

                CURSOR = CONN.cursor()
                CURSOR.execute(Q)

                alldem = CURSOR.fetchall()

                self.disconnect()

                ## IF ANY ROWS EXIST, MOVE ON
                if len(alldem) > 0:

                    print("TRAIN%", self.trainPerEntry.get())
                    print("TEST%", self.testPerEntry.get())
                    ## GET TOTAL ROWS, DIVIDE BY TWO FOR TRAIN/TEST SETS
                    rowCount = int(alldem[0][0])
                    
                    print(rowCount, "ROWS")
                    print("Train", (rowCount * int(self.trainPerEntry.get())/100))
                    print("Test", (rowCount * int(self.testPerEntry.get())/100))
                    
                    trainAmount = (rowCount * int(self.trainPerEntry.get())/100)
                    testAmount = (rowCount * int(self.testPerEntry.get())/100)
                    
                    rowCountHalf = int(alldem[0][0])/2
                    
                   # print "Count = ", rowCount, rowCountHalf

                    self.connect()
                    ## GET TOP "rowCountHalf" ROWS FROM DB
                    Q = 'SELECT {}, Sentence FROM "AnnotationMaster" ORDER BY ID ASC LIMIT {}'.format(str(column), int(trainAmount))

                    CURSOR = CONN.cursor()
                    CURSOR.execute(Q)

                    alldem = CURSOR.fetchall()

                    self.disconnect()

                    trainSent = []
                    testSent = []

                    if len(alldem) > 0:

                        # LOOP ALL RETURNED ROWS FOR TRAINING
                        for i in alldem:

                            # CONVERT PREDICTEDFIELD TO 1 OR 0
                            #POSITIVE = POSITIVE?
                            
                            
                            if str(i[0]).upper() == str(predField).upper():
                                ytrain.append([1])
                                posCountTrain += 1
                            else:
                                ytrain.append([0])

                            # CONVERT FEATURES TO 1 OR 0 (1 = IN SENTENCE; 0 = NOT IN SENTENCE)
                            featureScore = []

                            sent = str(i[1]).upper()
                            trainSent.append(sent)
                            
                            for j in features:
                               # print str(j).upper(), str(i[1]).upper(), str(j).upper() in str(i[1]).upper()
                               #CHECK FOR THE FEATURE IN THE SENTENCE AND TRUE = 1 FALSE = 0
                                words = sent.strip('"').strip('.').strip(',').split(" ")
                                found = 0
                                for n in words:
                                    if str(j).upper() == n:
                                        found = 1

                                if found == 1:
                                    featureScore.append(1)
                                    #print("Found 1")
                                else:
                                    featureScore.append(0)

                            xtrain.append(featureScore)
                            
                          #  print "xt", xtrain


                ############ GET TEST DATA
                    self.connect()

                    ### GET BOTTOM "rowCountHalf" FROM THE DATABASE
                    Q = 'SELECT {}, Sentence FROM "AnnotationMaster" ORDER BY ID DESC LIMIT {}'.format(str(column), int(testAmount))

                    CURSOR = CONN.cursor()
                    CURSOR.execute(Q)

                    alldem = CURSOR.fetchall()

                    self.disconnect()

                    if len(alldem) > 0:

                        for i in alldem:
                            #POSITIVE = POSITIVE?
                            if str(i[0]).upper() == str(predField).upper():
                                ytest.append([1])
                                posCountTest += 1
                            else:
                                ytest.append([0])
                            #CHECK FOR THE FEATURE IN THE SENTENCE AND TRUE = 1 FALSE = 0
                            featureScore = []
                            
                            testSent.append(str(i[1]).upper())
                            
                            for j in features:
                                sent = str(i[1]).upper()
                                words = sent.strip('"').strip('.').strip(',').split(" ")
                                found = 0
                                for n in words:
                                    if str(j).upper() == n:
                                        found = 1

                                if found == 1:
                                    featureScore.append(1)
                                    #print("found in test")
                                else:
                                    featureScore.append(0)
                                    #print("not found in test")



                            xtest.append(featureScore)
                            
                    ## Y SETS NEED TO BE FLATTENED FOR THE FUNCTION TO WORK
                    ytrain = numpy.ravel(ytrain)
                    ytest = numpy.ravel(ytest)
                    

                    if dumpOnly == 'N':
                        ## GET FIT AND SCORE
                        lf = logistic.fit(xtest,ytest)
                        #print lf, "lf"
                        probs = lf.predict_proba(xtest)
                        preds = lf.predict(xtest)
                        #print probs
                        #class1_1 = [pr[0] for pr in probs]
                        #print class1_1

                        #print features
                        #print "xTrain", xtrain[0:15]
                        #print "yTrain", ytrain[0:15]
                        
                        score = lf.score(xtest,ytest)
                        tn, fp, fn, tp = confusion_matrix(ytest, preds).ravel()
                        
                        ####
                        # PRINT THE SCORE..
                        output = ''
                        output = output + "Your accuracy score: "+ str(score)
                        output = output + "\n\n"
                        output = output + "Baseline Accuracy: " + str(100 - int(float(posCountTest)/float(testAmount) *100))+ "%"
                        output = output + "\n\n"
                        output = output + str(posCountTrain) + "/" + str(trainAmount) + " Positives in Training Data"
                        output = output + "\n\n"
                        output = output + str(posCountTest) + "/" + str(testAmount) + " Positives in Testing Data"
                        output = output + "\n\n"
                        output = output + "Also, this class_weight was " + str(balChoice) + "!"
                        output = output + "\n\n"
                        output = output + "\n\n"

                        
                    
                        ##print confusion_matrix(ytest, preds)
                        output = output + "Confusion Matrix:"
                        output = output + "\n\n"
                        output = output + "TP"+"\t|\t"+"FP"
                        output = output + "\n\n"
                        output = output + str(tp)+"\t|\t"+str(fp)
                        output = output + "\n\n"
                        output = output + "------------------------------------------"
                        output = output + "\n\n"
                        output = output + "FN"+"\t|\t"+"TN"
                        output = output + "\n\n"
                        output = output + str(fn)+"\t|\t"+str(tn)

                        tkMessageBox.showinfo("Woohoo!", output)


                        ans = tkMessageBox.askyesno("Save Data","Save raw data for later?")

                    else:
                        ans = 1



                    if ans == 1:
                        x = xtrain + xtest
                        y = []
                        for n in ytrain:
                            y.append(n)
                        for m in ytest:
                            y.append(m)
                        #y = ytrain + ytest
                    
                        sen = trainSent + testSent
                       # print "LENGTHS"
                       # print len(x),len(y),len(sen)
                        self.exportDataDump(features, x, y, sen, predField)

                        
                    
                else:
                    tkMessageBox.showinfo("Oops", "Please enter a value to predict!")
                    
            else:
                tkMessageBox.showinfo("Oops", "Please enter a column!")
    ############


    def exportDataDump(self, columns, xdata, ydata, sentList, outcome):

        
        filename = tkFileDialog.asksaveasfilename(defaultextension=".csv")
        if filename == '':
            tkMessageBox.showinfo("Bad Filename", "This was not saved!")
        else:
            savefile = open(filename, 'wb')
            doc = csv.writer(savefile, lineterminator='\n')

            cols = columns
            cols.append(outcome)
            cols.append("Sentence")
            cols.append("\n")
            #print "Columns!"
            #print cols
            
            doc.writerow(tuple(cols))

            loopData = list(xdata)
            for i in range(0, len(loopData)):
               
                values = list(loopData[i])
                values.append(ydata[i])
                values.append(sentList[i])
                #values.append("\n")

                #print values  
                doc.writerow(tuple(values))

            tkMessageBox.showinfo("Export Successful", "Congratulations, you made a data dump!")


            

               
    def findItem(self, event=''):

        global FILTERS
        
        found = 0
        foundList = []
        
        item = self.searchEnter.get()

        if item == '':

            self.refresh()
                      
        else:

            FILTERS.append(item)
            for j in self.detTree.get_children():

                for i in list(self.detTree.item(j).values())[2]:
 
                    if str(i).find(str(item)) >= 0:
                                      
                        foundList.append(j)
                        found = 1
            
            if found == 1:
                for j in self.detTree.get_children():
                    if j not in foundList:
                        self.detTree.delete(j)
            
            else:
                tkMessageBox.showinfo("Not Found", "Item "+item+" not found.")



    def refresh(self):

        global FILTERS
       # print "Next!"

        FILTERS = []
        try:
            current = self.mastTree.selection()[0]
            
            if self.mastTree.selection() != '' and self.mastTree.selection() != [] and self.mastTree.selection() != ():
                values = list(self.mastTree.item(current).values())[2]
                valueCount = len(values)

                ## Find column regardless of index
                for c in range(0, valueCount):
                    if self.mastTree.heading(c, "text") == "MeetingId":
                        meetId = values[c]
            
                self.mastItemClick(auto='Y',rowid=current,values=values,valueCount=valueCount)
        except:
            tkMessageBox.showinfo("Not Found", "Sorry, I lost your meeting!")


   
        
    def popupMenu(self, event=''):#NDC

        global CLICKX, CLICKY

##        print self.detTree.winfo_pointerx() - root.winfo_x()
##        print event.x_root
##
        CLICKX = self.detTree.winfo_pointerx() - root.winfo_x()#event.x_root
        CLICKY = self.detTree.winfo_pointery() - root.winfo_y()
        
        if self.detTree.selection() != '' and self.detTree.selection() != [] and self.detTree.selection() != ():
            try:
                self.popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                self.popup.grab_release()



    def tabClick(self, e=''):

        clicked = self.tabs.tk.call(self.tabs._w, "identify", "tab", e.x, e.y)
      #  print clicked

        if clicked == 0:
          #  print "Browse"
            self.ltMtFrame.pack(side=LEFT, expand=0, pady=self.padding, padx=self.padding, fill=BOTH)
            self.dtlFrame.pack(side=RIGHT, expand=1, pady=self.padding, padx=self.padding, fill=BOTH)
            self.featFrame.pack_forget()
            
        elif clicked == 1:
           # print "Annotation"
            self.ltMtFrame.pack_forget()
            self.dtlFrame.pack_forget()
            self.featFrame.pack_forget()
            
        elif clicked == 2:
          #  print "Learn"
            self.ltMtFrame.pack_forget()
            self.dtlFrame.pack_forget()
            self.featFrame.pack(side=RIGHT, expand=0, pady=self.padding, padx=self.padding, fill=BOTH)
            ##self.loadFeatures()
            self.colorLines(self.featTree)
            

    def exportExcel(self):

        filename = tkFileDialog.asksaveasfilename(defaultextension=".csv")
        if filename == '':
            tkMessageBox.showinfo("Bad Filename", "Please save as a csv..")
        else:
            savefile = open(filename, 'wb')
            doc = csv.writer(savefile, lineterminator='\n')

            cols = self.detColumns
            cols.append("\n")
            
            doc.writerow(tuple(cols))

                  
            for item in list(self.detTree.get_children()):
               
                values = list(self.detTree.item(item).values())[2]
                values.append("\n")
                     
                doc.writerow(tuple(values))

            tkMessageBox.showinfo("Export Successful", "Congratulations, you made a data dump!")
        
        

    def getTableColumns(self, table):

        ###### GET VARIABLE TABLE COLUMNS

        self.connect()

        Q = '''PRAGMA table_info({})'''.format(table)
  
        CURSOR = CONN.cursor()
        CURSOR.execute(Q)

        alldem = CURSOR.fetchall()

        self.disconnect()

        return alldem
        
 ################


         
    def addCol(self):

        this = tkSimpleDialog.askstring("New Annotation Column","Enter new column name:", parent=root, initialvalue="New Column")

        if this != None:

            self.connect()

            Q = 'ALTER TABLE "AnnotationMaster" ADD {}'.format(str(this))
            
            CURSOR = CONN.cursor()
            CURSOR.execute(Q)
            CONN.commit()

            self.disconnect()

            self.rebuildDetTree()
            
            tkMessageBox.showinfo("Add Column", "Welcome, new column!")


    def remCol(self):

        

        this = tkSimpleDialog.askstring("Delete Column", "Enter column name:", parent=root)

        if this != None:

            sure = tkMessageBox.askyesno("Confirm", "Are you sure you want to delete this column and all of the data in it? This is VERY permanent!")

            if sure == True:

                alldem = self.getTableColumns("AnnotationMaster")
##
##                print this, alldem
##                print this is alldem
                cont = 0

                for i in alldem:
                    if str(i[1]) == str(this):
                        cont = 1
                
                if cont == 1:


                    colText = ""
                    colOnlyText = ""
                    
                    ## Add column to exclude

                    for i in range(1,len(alldem)):
                        
                        if alldem[i][1] != str(this): # Not the column you want to remove
                            colText = colText + str(alldem[i][1]) + "\t" + str(alldem[i][2]) + "\tDEFAULT " + str(alldem[i][4])
                            colOnlyText = colOnlyText + str(alldem[i][1])

                            if i != len(alldem)-1:
                                colText = colText + ",\n"
                                colOnlyText = colOnlyText + ",\n"

                        else:
                            if i == len(alldem)-1: #If the column you remove is last, remove the last comma.
                                colText = colText.rsplit(",",1)[0]
                                colOnlyText = colOnlyText.rsplit(",",1)[0]
                            
                                
##                    print colText
##                    print colOnlyText
                    
                    statements = ['PRAGMA foreign_keys = 0;',
                                  'CREATE TABLE tempTable AS SELECT * FROM "AnnotationMaster";',
                                  'DROP TABLE "AnnotationMaster";',
                                  'CREATE TABLE AnnotationMaster (ID INTEGER PRIMARY KEY AUTOINCREMENT, {});'.format(colText),
                                  'INSERT INTO AnnotationMaster (ID, {}) SELECT ID,{} FROM tempTable;'.format(colOnlyText,colOnlyText),
                                  'DROP TABLE tempTable;',
                                  'PRAGMA foreign_keys = 1;' ]


                    for Q in statements:

                        self.connect()
                        
                        CURSOR = CONN.cursor()
                        CURSOR.execute(Q)
                        CONN.commit()

                        self.disconnect()


                    self.rebuildDetTree()

                    tkMessageBox.showinfo("Delete Column", "Gone, but not forgotten!")

                    
                else:
                    tkMessageBox.showinfo("Delete Column", "Column Name '" + str(this) + "' Not Found!")
            
            else:
                tkMessageBox.showinfo("Delete Column", "PHEW, that was close!")
                
        

    def rebuildDetTree(self):

            global VISIBLE

            self.detTree.destroy()
            
    ###### GET VARIABLE TABLE COLUMNS

            alldem = self.getTableColumns("AnnotationMaster")

            VISIBLE = []
            self.detColumns = []
            for i in alldem:
                self.detColumns.append(i[1])
          
     ################


            
            self.detTree = ttk.Treeview(self.ltMtDtlFrame, columns=self.detColumns, yscrollcommand=self.detbarY.set, xscrollcommand=self.detbarX.set)
            TT = ToolTip(self.detTree, "List of selected meeting annotations.")

            wid = (root.winfo_width()/len(self.detColumns))/2
            
            for col in self.detColumns:
                self.detTree.heading(col, text=col, command=lambda x=col: self.sortCol(self.detTree, x, False))
                self.detTree.column(col, width=int(wid), minwidth=10, anchor="center")
            

            self.detTree.pack(side=TOP, ipady=self.padding, ipadx=self.padding, padx=self.padding, pady=self.padding, expand=1, fill=BOTH)

            self.detTree['show'] = 'headings'

            root.update()
            for col in self.detColumns:
                self.detTree.column(col, width=self.defaultW, minwidth=self.defaultMinW, anchor="center")
                VISIBLE.append((col,"1"))
                               
            self.detbarY.config(command=self.detTree.yview)
            self.detbarX.config(command=self.detTree.xview)

            self.detTree.bind('<ButtonPress-1>', self.detItemClick)
            self.detTree.bind('<MouseWheel>', self.onMouseWheelDet)
            self.detTree.bind('<Button-3>', self.popupMenu)
            self.detTree.bind('<Double-1>', self.editLine)

            self.detTree.tag_configure("even", foreground="black", background="WHITE")
            self.detTree.tag_configure("odd", foreground="black", background=GUIBLUE)
            self.detTree.tag_configure("found", foreground="white", background="BLACK")
        
            self.colorLines(self.detTree)

            self.refresh()




    def variableSelect(self, *args):

        #self.vList["menu"].config(state="normal")
        self.vList["menu"].delete(0,END)

        Q = 'SELECT DISTINCT {} FROM "AnnotationMaster"'.format(str(self.tChoice.get()))
        
        self.connect()
        
        CURSOR = CONN.cursor()
        CURSOR.execute(Q)

        alldem = CURSOR.fetchall()
        
        self.disconnect()
        if len(alldem) > 0:
            self.values = alldem

            for i in self.values:
                # Filter out blank entries
                if i[0] != '' and i[0] != ' ':
                    self.vList["menu"].add_command(label=i, command=lambda item=i[0]: self.vChoice.set(str(item)))

            self.vChoice.set(str(""))
            
        else:
            pass
        
        self.loadFeatures()
        

    def editLine(self, event):
        
        # what row and column was clicked on
        rowid = self.detTree.identify_row(event.y)
        column = self.detTree.identify_column(event.x)
        heading = self.detTree.heading(column, "text")
        num = self.detColumns.index(heading)
        
        parent = self.detTree.parent(rowid)

        if rowid == '' or column == '#0':
            return

        
        values = list(self.detTree.item(rowid).values())[2]
        
        try:
            defaultText = values[num]        
        except:
            defaultText = ''

        TextEntry(str(defaultText), values, num, heading, rowid)




    def removeLine(self, line):
        
        
        self.detTree.delete(line)
            
        #self.colorLines(self.detTree)





    def addLine(self, options, index=END):
       
        ## REMOVE WHITESPACE
        options = list(options)
        for i in range(0, len(options)):
            options[i] = str(options[i]).rstrip()
        options = tuple(options)

        self.detTree.insert('',0,index, values=options)
        self.sortCol(self.detTree,0,0)
        self.colorLines(self.detTree)


    
    def updateDatabase(self, db, ID, col, value):

        self.connect()

        Q = '''UPDATE "{}"
            SET {} = "{}"
            WHERE ID = {}'''.format(db,col,value,ID)
        
        CURSOR = CONN.cursor()
        CURSOR.execute(Q)
        CONN.commit()

        self.disconnect()

        

                 
    def connect(self):

        global CONN, DATABASE
        
        try:
            CONN = sqlite3.connect(DATABASE)
            print("Connected!")
        except:
            tkMessageBox.showinfo("Connection Error", "Error connecting to SQLite3 database: " + DATABASE)




    def disconnect(self):

        global CONN
        
        try:
            CONN.close()
            print("Disconnected!")
        except:
            pass

            

    def loadData(self):

        global CONN

        self.connect()

        Q = 'SELECT MeetingId, MeetingSize, MeetingMin FROM "MeetingMaster"'

        CURSOR = CONN.cursor()
        CURSOR.execute(Q)

        alldem = CURSOR.fetchall()

        self.disconnect()
        
        if len(alldem) > 0:

            index = 0

            #Loop through results and insert into master table (index is a unique identifier)
            for i in alldem:
            
                self.mastTree.insert('', 'end', str(index), values=tuple(i))

                index+=1
        
            self.colorLines(self.mastTree)




    def detItemClick(self, event='', auto='N', rowid=0):

        #Click a mast item and load meeting details where MeetingId = column 1 of mastTable

        column = ''

        if auto == 'N':
            rowid = self.detTree.identify_row(event.y)
            column = self.detTree.identify_column(event.x)
            head = self.detTree.heading(column, "text")
            num = self.detColumns.index(self.detTree.heading(column, "text"))

        try:
            self.detTree.selection_set(rowid)
            
            if self.detTree.selection() != '' and self.detTree.selection() != [] and self.detTree.selection() != ():
                values = list(self.detTree.item(rowid).values())[2]
                valueCount = len(values)
                

        ####
        #####
        ## Figure out how to check index of column on the fly #self.detTree.heading(column, "text") = "Column Text"
                
               # num = self.detColumns.index(self.detTree.heading(column, "text"))

                #print "Head", self.detTree.heading(column, "text")
                #print "Index", self.detColumns.index(self.detTree.heading(column, "text"))

                ## Find column regardless of index
                for c in range(0, valueCount):
                    if self.detTree.heading(c, "text") == "ID":
                        thisId = values[c]
                    if self.detTree.heading(c, "text") == "ParticipantId":
                        partId = values[c]
                    if self.detTree.heading(c, "text") == "MeetingId":
                        meetId = values[c]
                    if self.detTree.heading(c, "text") == "Sentence":
                        sent = values[c]
                    
                #Participant ID
    ##            partId = values[1]
    ##            meetId = values[0]
    ##            sent = values[6]

                if auto == 'N':
                    findValue = values[num]
                    if findValue != '':
                        foundCount = 0
                        self.colorLines(self.detTree)
                        for n in self.detTree.get_children():
                            if list(self.detTree.item(n).values())[2][num] == findValue:
                                
                                self.detTree.item(n, tags="found")
                                foundCount +=1
                   
                        self.clickVar.set(str(head))
                        self.valueVar.set(str(findValue))
                        self.countVar.set(str(foundCount))
                
                # Fill in the participant table
                self.connect()

                Q = '''PRAGMA table_info("ParticipantMaster")'''
          
                CURSOR = CONN.cursor()
                CURSOR.execute(Q)

                alldem = CURSOR.fetchall()

                headers = []
                for i in alldem:
                    headers.append(i[1])
                    
                Q2 = '''SELECT *
                    FROM "ParticipantMaster"
                    WHERE ParticipantId = "{}"'''.format(str(partId))
                CURSOR = CONN.cursor()
                CURSOR.execute(Q2)

                alldem2 = CURSOR.fetchall()

                values = []
                for i in alldem2[0]:
                    values.append(i)
                
                self.disconnect()
                
                if len(headers) > 0 and len(values) > 0:

                    combo = zip(headers, values)

                    self.clearTable(self.parTree)
                        
                    index = 0

                    #Loop through results and insert into master table (index is a unique identifier)
                    for i in combo:
                    
                        self.parTree.insert('', 'end', str(index), values=tuple(i))

                        index+=1

                self.infoText.configure(state="normal")
                self.infoText.delete('0.0',END)
                self.infoText.insert('0.0', str(sent))
                self.infoText.configure(state="disabled")
            
                self.colorLines(self.parTree)
                self.getAudioPosition(meetId, sent, thisId, auto)
        except:
            self.stopAudioClip()



    def setColumns(self):

        global VISIBLE
        
        ColumnView(root, VISIBLE)

        


    def hideColumns(self, columns):

        toDisplay = []
        for i in columns:
            if i[1] == '1' or i[1] == 1:
                toDisplay.append(i[0])

        
        wid = (root.winfo_width()/len(self.detColumns))/2
        for col in self.detColumns:
            self.detTree.column(col, width=int(wid), minwidth=10, anchor="center")
            
        self.detTree["displaycolumns"] = (tuple(toDisplay))

        root.update()

        for col in self.detColumns:
            self.detTree.column(col, width=self.defaultW, minwidth=self.defaultMinW, anchor="center")
              



    def getRowValues(self, tree, y):

        rowid = tree.identify_row(y)
        
        tree.selection_set(rowid)

        if tree.selection() != '' and tree.selection() != [] and tree.selection() != ():
            
            values = list(tree.item(rowid).values())[2] #Edit for PYTHON3.8
            valueCount = len(values)

        else:
            values = 'N'
            valueCount = -1
            
        return rowid, values, valueCount



    def nextMeeting(self):

        try:
            current = self.mastTree.selection()[0]
            nextItem = int(current)+1
            rowid = str(nextItem)
            
            self.mastTree.selection_set(rowid)
            
            if self.mastTree.selection() != '' and self.mastTree.selection() != [] and self.mastTree.selection() != ():
                values = list(self.mastTree.item(rowid).values())[2]
                valueCount = len(values)

                ## Find column regardless of index
                for c in range(0, valueCount):
                    if self.mastTree.heading(c, "text") == "MeetingId":
                        meetId = values[c]
            
                self.mastItemClick(auto='Y',rowid=rowid,values=values,valueCount=valueCount)
        except:
            #print("Out of meetings!")
            pass



    def prevMeeting(self):

        current = self.mastTree.selection()[0]
        prevItem = int(current)-1
        rowid = str(prevItem)

        try:
            self.mastTree.selection_set(rowid)
            
            if self.mastTree.selection() != '' and self.mastTree.selection() != [] and self.mastTree.selection() != ():
                values = list(self.mastTree.item(rowid).values())[2]
                valueCount = len(values)

                ## Find column regardless of index
                for c in range(0, valueCount):
                    if self.mastTree.heading(c, "text") == "MeetingId":
                        meetId = values[c]
            
                self.mastItemClick(auto='Y',rowid=rowid,values=values,valueCount=valueCount)
        except:
            pass
            
        
    def mastItemClick(self, event='', auto='N', rowid=0, values='', valueCount=-1):

        global AUDIOFILE
        
        #Click a mast item and load meeting details where MeetingId = column 1 of mastTable
        if auto == 'N': 
            rowid, values, valueCount = self.getRowValues(self.mastTree, event.y)
        else:
            pass
        
        if valueCount != -1:     
            for c in range(0, valueCount):
                if self.mastTree.heading(c, "text") == "MeetingId":
                    meetId = values[c]
                    
            
            self.connect()

            Q = '''SELECT *
                    FROM "AnnotationMaster"
                    WHERE MeetingId = "{}"'''.format(str(meetId))

            CURSOR = CONN.cursor()
            CURSOR.execute(Q)

            alldem = CURSOR.fetchall()

            self.disconnect()
            
            if len(alldem) > 0:

                self.clearTable(self.detTree)
                    
                index = 0

                #Loop through results and insert into master table (index is a unique identifier)
                for i in alldem:
                
                    self.detTree.insert('', 'end', str(index), values=tuple(i))

                    index+=1

            # Fill in the variable table
            self.connect()

            Q = '''PRAGMA table_info("MeetingMaster")'''
      
            CURSOR = CONN.cursor()
            CURSOR.execute(Q)

            alldem = CURSOR.fetchall()

            headers = []
            for i in alldem:
                headers.append(i[1])
                
            Q2 = '''SELECT *
                FROM "MeetingMaster"
                WHERE MeetingId = "{}"'''.format(str(meetId))
            
            CURSOR = CONN.cursor()
            CURSOR.execute(Q2)

            alldem2 = CURSOR.fetchall()

            values = []
            for i in alldem2[0]:
                values.append(i)
            
            self.disconnect()
            
            if len(headers) > 0 and len(values) > 0:

                if OS == 'Windows':
                    AUDIOFILE = values[11]
                else:
                    AUDIOFILE = values[11].replace("\\",DASH)
                combo = zip(headers, values)

                self.clearTable(self.statsTree)
                    
                index = 0

                #Loop through results and insert into master table (index is a unique identifier)
                for i in combo:
                
                    self.statsTree.insert('', 'end', str(index), values=tuple(i))

                    index+=1
            
            self.colorLines(self.detTree)
            self.colorLines(self.statsTree)
            



    def clearTable(self, table):
        
        for i in table.get_children():
            table.delete(i)
            
            

    def colorLines(self, table):
 
        index = 0

        for i in table.get_children():
            
            #Remove current tags
            table.item(i, tags=())
                
            #if a remainder = 0, it means the line is even, else, it is odd
            if index%2 == 0:            
                table.item(i, tags="even")
            else:
                table.item(i, tags="odd")

            index+=1

            
            
    def onMouseWheelMast(self, event=''):
        self.mastTree.yview_scroll(int(-1*(event.delta/120)), "units")

    def onMouseWheelDet(self, event=''):
        self.detTree.yview_scroll(int(-1*(event.delta/120)), "units")

    def onMouseWheelfeat(self, event=''):
        self.featTree.yview_scroll(int(-1*(event.delta/120)), "units") 




    def getAudioPosition(self, meetId, sent, thisID, auto='N'):

        global CONN
        
        self.connect()

        Q = '''SELECT StartTime, Duration, EndTime FROM "AnnotationMaster"
                WHERE ID = '{}'
                AND MeetingId = "{}"
                AND Sentence = ""{}""'''.format(str(thisID), str(meetId), str(sent))
        CURSOR = CONN.cursor()
        CURSOR.execute(Q)

        alldem = CURSOR.fetchall()

        self.disconnect()
        
       # print alldem[0][0]

        #Take StartTime Time format, and convert to seconds
        stime = alldem[0][0]
        dtime = alldem[0][1]
        etime = alldem[0][2]

        date = datetime. datetime.strptime(stime, "%M:%S.%f") #Format 00:00.0
        delta = date - datetime.datetime(1900, 1, 1)#get proper date
        startSec = delta.total_seconds() #StartTime

        date = datetime. datetime.strptime(dtime, "%M:%S.%f") #Format 00:00.0
        delta = date - datetime.datetime(1900, 1, 1)#get proper date
        durSec = delta.total_seconds() #Duration

        date = datetime. datetime.strptime(etime, "%M:%S.%f") #Format 00:00.0
        delta = date - datetime.datetime(1900, 1, 1)#get proper date
        endSec = delta.total_seconds() #Duration

        
        self.stimeVar.set(str(startSec))
        self.etimeVar.set(str(endSec))
        self.dtimeVar.set(str(durSec))

        if auto == 'Y':
            self.playAudioClip()
      

        

    ##Takes start and duration times and plays an MP3 file.
    ##startSec and durSec must be in seconds.
    def playAudioClip(self):

        global AUDIOFILE
        
        startSec = float(self.stimeVar.get())
        durSec = float(self.dtimeVar.get())
        
        pygame.mixer.init()

        pygame.mixer.music.load(AUDIOFILE)
        
        #Start at position
        pygame.mixer.music.play(0,startSec)
        
        #Pause to hear sentence
        ########self.autoRunJob = root.after(int(durSec*1000), self.nextAudioClip)
 


    def stopAudioClip(self):

        ########root.after_cancel(self.autoRunJob)
        ########self.autoRunJob = None
        pygame.mixer.music.stop()
      

            
##    def firstAudioClip(self): #not working becuase of the subprocess
##        pygame.mixer.music.stop()
##        #self.detTree.selection_set(0)
##        self.detItemClick(auto='Y',rowid=str(0))
    
        

    ########def nextAudioClip(self):

        ########pygame.mixer.music.stop()
        ########current = self.detTree.selection()[0]
        ########nextItem = int(current)+1
        ########print nextItem

        ########self.detItemClick(auto='Y',rowid=str(nextItem))
                     


        

    ## SORTS BY COLUMN col IN SPECIFIED TREEVIEW tv (Clicking again reverses this)
    def sortCol(self, tv, col, reverse):#NDC

        try: 
            l = [(float(tv.set(k, col)), k) for k in tv.get_children('')]
        except:
            l = [(tv.set(k, col), k) for k in tv.get_children('')]

        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.sortCol(tv, col, not reverse))

        self.colorLines(tv)




    def loadFeatures(self, *args):

        column = self.tChoice.get()
        
        if column != None:

            predField = self.vChoice.get()
            
            if predField != None:
                
                self.connect()

                Q = 'SELECT * FROM "FeatureMaster" WHERE OutcomeVariable = "{}" AND PositiveClass = "{}"'.format(str(column), str(predField))
                
                CURSOR = CONN.cursor()
                CURSOR.execute(Q)

                alldem = CURSOR.fetchall()

                self.disconnect()

                self.clearTable(self.featTree)
                
                if len(alldem) > 0:

                    
                        
                    index = 0

                    #Loop through results and insert into master table (index is a unique identifier)
                    for i in alldem:
                    
                        self.featTree.insert('', 'end', str(index), values=tuple(i))

                        index+=1

                    self.colorLines(self.featTree)

            


    def addFeature(self, e=''):


        #AddFeat(root)
        column = self.tChoice.get()
        posClass = self.vChoice.get()
        
        if column != "Outcome Variable":
   
            if posClass != "Positive Class":

                try:
                    that = self.infoText.selection_get()
                
                except:
                    
                    that = tkSimpleDialog.askstring("Add Feature","Enter new feature:", parent=root, initialvalue="Feature")
                    
                if that != None:
                
                    self.connect()

                    Q = '''INSERT INTO "FeatureMaster"
                        (OutcomeVariable, PositiveClass, Feature)
                        VALUES ("{}","{}","{}")'''.format(str(column), str(posClass).rstrip(),str(that))
                    
                    CURSOR = CONN.cursor()
                    CURSOR.execute(Q)
                    CONN.commit()

                    self.disconnect()

                    self.loadFeatures()

        else:
            tkMessageBox.showinfo("Error", "Please select an Outcome Variable and a Positive Class from the drop down menus!.")

    def remFeature(self):


        rowid = self.featTree.selection()[0]
        
        if self.featTree.selection() != '' and self.featTree.selection() != [] and self.featTree.selection() != ():
            values = list(self.featTree.item(rowid).values())[2]
            valueCount = len(values)

            ## Find column regardless of index
            for c in range(0, valueCount):
                if self.featTree.heading(c, "text") == "ID":
                    ID = values[c]

            self.connect()

            Q = '''DELETE FROM "FeatureMaster"
                WHERE ID = "{}"'''.format(str(ID))
            
            CURSOR = CONN.cursor()
            CURSOR.execute(Q)
            CONN.commit()

            self.disconnect()

            self.loadFeatures()
        
        

    def exitGUI(self):

        try:
            root.after_cancel(self.autoRunJob)
        except:
            pass
        try:
            self.autoRunJob = None
        except:
            pass
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
        root.destroy()




class ToolTip():

    def __init__(self, widget, msg=''):

        self.widget = widget
        self.msg = msg
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
        
    def enter(self, e=''):
        
        if Main.tipsOn == 1:
            # ENSURE THE LABEL NEVER GOES OFF SCREEN
            if root.winfo_pointerxy()[0] < root.winfo_width()/2:
                
                x = self.widget.winfo_rootx() + e.x + 10
                y = self.widget.winfo_rooty() + e.y + 10
            else:
                x = self.widget.winfo_rootx() + e.x - len(self.msg)*6
                y = self.widget.winfo_rooty() + e.y + 10

            self.topw = Toplevel(self.widget)
            
            # Removes the top window
            self.topw.wm_overrideredirect(True)
            self.topw.wm_geometry("+%d+%d" % (x, y))
            
            label = Label(self.topw, text=self.msg, bg="WHITE", foreground="BLACK", relief='solid', borderwidth=1)
            label.pack(ipadx=2)

        else:
            pass
        
    def close(self, e=''):
        try: 
            if Main.tipsOn == 1:    
                if self.topw:
                    self.topw.destroy()
            else:
                pass
        except:
            pass


class InfoView():

    def __init__(self, widget, itemList):

        self.widget = widget
        self.items = itemList
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
        
    def enter(self, e=''):

        text = ""
        for i in self.items:
            text = text + str(i) + "\n"
        
        x = Main.searchEnter.winfo_rootx() 
        y = Main.searchEnter.winfo_rooty() + 25

        self.topw = Toplevel(self.widget)
        
        # Removes the top window
        self.topw.wm_overrideredirect(True)
        self.topw.wm_geometry("+%d+%d" % (x, y))
        
        label = Label(self.topw, text=text, bg="WHITE", foreground="BLACK", relief='solid', borderwidth=1)
        label.pack(ipadx=5)
        
        
    def close(self, e=''):
        try: 
             
            if self.topw:
                self.topw.destroy()
        except:
            pass

        
        

class TextEntry():
 

    def __init__(self, msg, values, num, heading, rowid):

        self.msg = msg
        self.values = values
        self.col = heading
        self.num = num
        self.rowid = rowid
        
        x = root.winfo_pointerxy()[0] - len(self.msg)*6
        y = root.winfo_pointerxy()[1] - 10

        self.topw = Toplevel(root)
        
        # Removes the top window
        self.topw.wm_overrideredirect(True)
        self.topw.wm_geometry("%dx%d+%d+%d" % (Main.defaultW, 20, x, y))

        self.entry = Entry(self.topw, text=self.msg, bg="WHITE", foreground="BLACK", relief='solid', borderwidth=1)
        self.entry.pack(ipadx=2)
        self.entry.focus_set()
        
        self.entry.bind("<Return>", self.save)
        self.entry.bind("<Escape>", self.close)
        root.bind("<Button-1>", self.close)


    def save(self, e=''):

        this = self.entry.get()
        
        if this == None:
            return
        
        if this.upper() == "NONE" or this == '': #prevent case sensitivity
            this = "None"

      
        self.values[self.num] = this

        inx = Main.detTree.index(self.rowid)   

        #def updateDatabase(self, db, ID, col, value)
        Main.updateDatabase("AnnotationMaster", self.values[0], self.col, this)
        
        Main.removeLine(self.rowid)
        Main.addLine(self.values, index=inx)

        self.close()
        
        
    def close(self, e=''):

        if self.topw:
            self.entry.delete(0,END)
            self.topw.destroy()
      
        




### Class to hide, unhide columns in detTree


class ColumnView:

    def __init__(self, parent, columns):

        global VISIBLE
        
        top = self.top = Toplevel(parent, bg=MAINCOLOUR)
        top.focus_force()
        self.columns = columns
        self.parent = parent

        
        top.geometry('{}x{}'.format(200, 400))
        top.resizable(0,0)
        topFrame = Frame(top, bg=MAINCOLOUR)
        topFrame.pack(side=TOP, fill=BOTH, expand=1)

        
        sorLbarY = Scrollbar(topFrame)
        sorLbarY.pack(side=RIGHT, fill=Y)

        self.canvas = Canvas(topFrame, bd=0, highlightthickness=0, width=100, height=100, yscrollcommand=sorLbarY.set, scrollregion=(0,0,0,1000), bg=MAINCOLOUR)
        self.inner = Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.inner, anchor="nw")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.top.bind('<MouseWheel>', self.onMouseWheel)

        self.vars = []
    
        for i in VISIBLE:
            textv = i[0]
            inew = IntVar()
            inew.set(i[1])
            new = Checkbutton(self.inner, text=textv, variable=inew, anchor="w", bg=MAINCOLOUR)
            self.vars.append(inew)
            new.pack(expand=1,fill=BOTH)


        sorLbarY.config(command=self.canvas.yview)


        b = Button(top, text="Cancel", image=Main.cancelPic, relief=FLAT, borderwidth=1, bg=MAINCOLOUR, command=self.done)
        b.pack(side=RIGHT, pady=2,ipady=2,ipadx=2,padx=2)
        
        b = Button(top, text="OK", image=Main.savePic, relief=FLAT, borderwidth=1, bg=MAINCOLOUR, command=self.save)
        b.pack(side=RIGHT, pady=2,ipady=2,ipadx=2,padx=2)



    def onMouseWheel(self, event=''):
        
        self.canvas.yview_scroll(-1*(event.delta/120), "units")

        
    
    def save(self):

        global VISIBLE
        
        states = []
        for i in self.vars:
            states.append(i.get())

        newC = []
        for i in self.columns:
            newC.append(i[0])

        zipper = zip(newC, states)

        VISIBLE = zipper

        Main.hideColumns(VISIBLE)
        
        self.done()


        
    def done(self, event=''):

        self.top.destroy()



root = Tk()

if platform.system() == 'Windows':
    root.iconbitmap(default='Required'+DASH+'box.ico')
else:
    pass

root.geometry('{}x{}'.format(1350, 900))
#root.resizable(width=False, height=False)
root.minsize(width=750, height=500)
root.title("Corpus Browser - v" + str(VERSION))
root.configure(bg="BLACK")
root.update()

Main = Main(root)
root.protocol("WM_DELETE_WINDOW", Main.exitGUI)
root.mainloop()


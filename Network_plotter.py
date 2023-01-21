from tkinter import *
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from DAlgorithm import DPath
from FAlgorithm import FPath
from math import *
from random import *
import time
import webbrowser
import os
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Imported algorithm modules
def Shortest():
    if root.ResultTxt == "":
        SubmitBtn.config(state=DISABLED)                                                           # Disabled to prevent user from messing up the
        LinkList = []                                                                              # inputted data
        for ind in range(len(root.EntList)):                                                       # Getting the link names and values from entries
            Lbl = root.LblList2[ind].cget("text")
            nodeA = Lbl[0]
            nodeB = Lbl[len(DirOptions[0])+1]
            direction = Lbl[1:len(DirOptions[0])+1]
            value = round(float(root.EntList[ind].get()), 1)                                       # Maximum 2dp
            LinkList.append([nodeA, nodeB, value, direction])
        if root.Algorithm == "D":                                                                  # Using Dijkstra's algorithm
            NodeList = [[chr(i + 65), -1] for i in range(len(root.NodeList))]
            Path, Min = DPath(NodeList, LinkList, root.StartNode, root.TargetNode)
        elif root.Algorithm == "F":                                                                # Using Floyd's algorithm
            NumOfNodes = len(root.NodeList)
            Path, Min = FPath(NumOfNodes, LinkList, root.StartNode, root.TargetNode)
        if Min == "N/A": mb.showerror('Error', 'Disconnected parts found')
        else:
            ind = 0
            PathNodes = Path.split(" -> ")
            Letter = PathNodes[0]                                                                  # Starting node
            Node = root.NodeList[ord(Letter) - 65]
            Ax, Ay = GetCoords(Node)
            Num, Refresh_rate = 50, 0.01                                                           # Set animation speed
            LineW = ChangeLineW()
            while ind < len(PathNodes) - 1:                                                        # Animation
                Letter = PathNodes[ind + 1]
                Node2 = root.NodeList[ord(Letter) - 65]
                Bx, By = GetCoords(Node2)
                for i in range(1, Num):
                    Line = cnv.create_line(Ax, Ay, (Bx - Ax) * i / Num + Ax,
                                           (By - Ay) * i / Num + Ay,
                                           fill=root.Line2Bg, width=LineW)                         # Fake lines for animation
                    for item in (Node, Node2, root.LblList1[root.NodeList.index(Node)],
                                 root.LblList1[root.NodeList.index(Node2)]):
                        cnv.tag_raise(item)
                    time.sleep(Refresh_rate)                                                       # A pause to make the animation effect
                    root.update()
                    cnv.delete(Line)
                direct = "=="
                for Link in LinkList:
                    if Link == [PathNodes[ind], Letter, Link[2], "=>"]: direct = "=>"
                if direct == "==":                                                                 # The actual line
                    Line = cnv.create_line(Ax, Ay, Bx, By, fill=root.Line2Bg, width=LineW)         # Bi-directional
                else:
                    B2x, B2y = DrawArrow(Ax, Ay, Bx, By)
                    Line = cnv.create_line(Ax, Ay, B2x, B2y, fill=root.Line2Bg, width=LineW,       # Directed
                                           arrow=LAST, arrowshape=ArrowShape)
                for item in (Node, Node2, root.LblList1[root.NodeList.index(Node)],
                                 root.LblList1[root.NodeList.index(Node2)]):
                        cnv.tag_raise(item)
                root.SolLinks.append(Line)                                                         # Saved so it can be deleted
                Ax, Ay = Bx, By
                Node = Node2
                ind += 1
        Text = "Path: {},   Minimum: {}".format(Path, str(Min))
        if root.ResultTxt != "":
            cnv.delete(root.ResultTxt)                                                             # Prevent creating two labels
        root.ResultTxt = cnv.create_text(10, root.Height * 3 // 4 - 60, text=Text,
                                         font=Lbl4Font, anchor=SW)                                 # Result label
    SubmitBtn.config(state=NORMAL)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Miscellaneous / Repetitive functions
def GetCoords(item):                                                                               # Get the coordinates of the item in canvas
    x1, y1, x2, y2 = cnv.coords(item)
    x3, y3 = (x1 + x2) // 2, (y1 + y2) // 2
    return x3, y3

def ArrowStatus():                                                                                 # Change the status of the arrow buttons
    if len(root.LinkList) - root.CurrentPage <= 2: state = DISABLED
    else: state = NORMAL
    RightBtn.config(state=state)
    LeftBtn.config(state=DISABLED)

def ClearLinkLbl():                                                                                # Clear the link label
    root.LinkA = ""
    root.LinkB = ""
    AddLinkLbl.config(text="Link: ")

def Deselect():                                                                                    # Item back to normal when gets deselected
    if root.SelectedItem in root.LinkList:
        cnv.itemconfig(root.SelectedItem, fill=root.LineBg, activefill=None)
    elif root.SelectedItem != "":
        cnv.itemconfig(root.SelectedItem, width=2, activefill=None)
    root.SelectedItem = ""

def Highlight(Item):                                                                               # Item highlighted when gets selected
    if Item in root.LinkList: cnv.itemconfig(Item, fill=root.Line2Bg)
    else: cnv.itemconfig(Item, width=5)

def EditNodes(command):                                                                            # Change nodes, can also choose to bind command
    for Node in root.NodeList:
        cnv.itemconfig(Node, width=2)
        cnv.tag_unbind(Node, "<Button-1>")
        if command is None: cnv.itemconfig(Node, activefill=root.NodeBg)
        else:
            cnv.tag_bind(Node, "<Button-1>", command)
            cnv.itemconfig(Node, activefill=root.NodeAf)

def ChangeLinks(command):                                                                          # Change links, can also choose to bind command
    for Link in root.LinkList:
        cnv.tag_unbind(Link, "<Button-1>")
        if command == None:
            cnv.itemconfig(Link, fill=root.LineBg, activefill=root.LineBg)
        else:
            cnv.tag_bind(Link, "<Button-1>", command)
            cnv.itemconfig(Link, fill=root.LineBg, activefill=root.LineAf)

def ButtonRelief(item):                                                                            # Change the button reliefs
    AddLinkBtn.config(relief=RAISED)                                                               # Raises all buttons
    SelBtn.config(relief=RAISED)
    AddNodeBtn.config(relief=RAISED)
    if item != None: item.config(relief=SUNKEN)                                                    # An option to make a button sunken

def ChangeLineW():                                                                                 # Change line width according
    LineW = len(root.NodeList) * -0.5 + 20                                                         # to number of nodes
    return LineW

def UpdateAlgLbl():                                                                                # Update algorithm label
    if root.Algorithm == "D": alg = "Dijkstra's"
    else: alg = "Floyd's"
    cnv.itemconfig(AlgLbl, text="Current algorithm: " + alg)

def DrawArrow(Ax, Ay, Bx, By):
    dist = 15
    if Bx - Ax == 0: angle = pi / 2
    else: angle = atan((By - Ay)/(Bx - Ax))                                                       # Decrease in line length
    dx, dy = cos(angle) * dist, sin(angle) * dist                                                 # Change in x and y
    if Bx - Ax > 0:
        Bx -= dx
        By -= dy
    else:
        Bx += dx
        By += dy
    return Bx, By
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Delete everything in the graph
def DelAll(Ok, DelPic):
    if not Ok:                                                                                     # Confirmation
        Ok = mb.askyesno("Warning", "Confirm clear all?")
    if Ok:
        root.Saved = True
        root.SelectedItem = ""
        for l in (root.NodeList, root.LblList1, root.LinkList,
                  root.EntList, root.LblList2):                                                    # Clear all lists
            for item in l:
                if l in (root.EntList, root.LblList2): item.destroy()
                else: cnv.delete(item)
        root.NodeList = []
        root.LblList1 = []
        root.LinkList = []
        root.EntList = []
        root.LblList2 = []
        ArrowStatus()                                                                              # Sync the arrow buttons
        root.CurrentPage = 0                                                                       # Reset
        ClearLinkLbl()
        ButtonRelief(None)                                                                         # Means no buttons selected
        if root.Pic != "" and DelPic: cnv.delete(root.Pic)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Delete selected button
def Reorganise():                                                                                  # Reorder entries
    page = root.CurrentPage
    for ind in range(len(root.EntList)):                                                           # Remove all widgets from the grid method
        Lbl = root.LblList2[ind]
        Lbl.grid_remove()
        Ent = root.EntList[ind]
        Ent.grid_remove()
    ind = 0                                                                                        # Place them back on the grid
    while (ind + page < len(root.EntList) and ind < 10):                                           # Make sure not go out of the list and max 10
        if ind % 2 == 0: row = 0
        else: row = 1
        column = ind // 2 * 2
        root.LblList2[ind + page].grid(row=row, column=column, sticky="NE")
        root.EntList[ind + page].grid(row=row, column=column + 1, sticky="NW")
        ind += 1

def DelSel():
    def DelLink(Link, Lbl, Ent):
        cnv.delete(Link)
        root.LinkList.remove(Link)
        Ent.destroy()
        root.EntList.remove(Ent)
        Lbl.destroy()
        root.LblList2.remove(Lbl)

    def Relabel():                                                                                 # Relabels all nodes according to the order in the
        for count, Label in enumerate(root.LblList1):                                              # list
            Letter = chr(count + 65)
            cnv.itemconfig(Label, text=Letter)
        
    def DelEntries(ind):                                                                           # Delete the links connected to the node
        Letter = chr(ind + 65)
        i = 0
        while i < len(root.LblList2):                                                              # Check which link should be deleted
            Lbl = root.LblList2[i]
            text = Lbl.cget("text")[0:-1]                                                          # Labels are in the form of "_=x_:"
            if Letter in text: 
                Ent = root.EntList[i]
                Link = root.LinkList[i]
                DelLink(Link, Lbl, Ent)
            else:                                                                                  # When the link is not directly linked to the
                NewTxt = ""                                                                        # deleted node
                for letter in text:
                    if ind < ord(letter) - 65: NewTxt += chr(ord(letter) - 1)                      # Either move down a letter
                    else: NewTxt += letter                                                         # Or same letter
                Lbl.config(text=NewTxt + ":")
                i += 1                                                                             # Dont need to add if deleted
    
    if len(root.NodeList) > 0 and root.SelectedItem != "":
        root.Saved = False
        Item = root.SelectedItem
        ClearLinkLbl()
        root.CurrentPage = 0
        if Item in root.LinkList:                                                                  # A link
            ind = root.LinkList.index(Item)
            Ent = root.EntList[ind]
            Lbl = root.LblList2[ind]
            DelLink(Item, Lbl, Ent)
        else:                                                                                      # A node
            ind = root.NodeList.index(Item)
            cnv.delete(Item)
            root.NodeList.remove(Item)                                                             # Delete node
            Label = root.LblList1[ind]
            root.LblList1.pop(ind)                                                                 # Delete label for the node
            cnv.delete(Label)
            Relabel()                                                                              # Need to replace the missing letter
            DelEntries(ind)
        Reorganise()
        ArrowStatus()
        root.SelectedItem = ""
        LineW = ChangeLineW()                                                                      # Update line width
        for Link in root.LinkList:
            cnv.itemconfig(Link, width=LineW)
    else: mb.showerror("Error", "No items selected")

def DelSelKey(Event):                                                                              # Delete item with the "DELETE" key
    DelSel()
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Select item button
def Select():
    def SelectItem(Event):
        Deselect()
        x, y = Event.x, Event.y                                                                    # Get coords of the click
        Item = int(cnv.find_closest(x, y)[0])                                                      # Search for closest node or link
        root.SelectedItem = Item
        Highlight(Item)
    ButtonRelief(SelBtn)
    ClearLinkLbl()
    cnv.unbind("<Button-1>")
    EditNodes(SelectItem)                                                                          # Binding the function to nodes and links
    ChangeLinks(SelectItem)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Make new node
def CreateNode(x, y):
    root.Saved = False
    Node = cnv.create_oval(x - NodeR, y - NodeR, x + NodeR, y + NodeR,
                           fill=root.NodeBg, outline=root.NodeBd, width=5)                         # Create node
    root.NodeList.append(Node)                                                                     # Save it so it can be accessed for changes
    Letter = chr(len(root.LblList1) + 65)
    Label = cnv.create_text(x, y - 30, text=Letter, font=Lbl1Font, fill=root.Fg)                   # Corresponding letter
    root.LblList1.append(Label)
    return Node

def AddNode():
    def ValidSpace(x, y):
        Space = 20
        for Node in root.NodeList:
            x3, y3 = GetCoords(Node)
            if x3 - 40 < x < x3 + 40 and y3 - 60 < y < y3 + 40: return False                       # Check any nodes nearby
        if x < Space or x > CnvW - Space or y < Space + 20 or y > CnvH - Space:                    # Not out of canvas
            if len(root.Nodelist) >= 26: return False                                              # Max 26 nodes
        return True

    def LocateNode(Event):
        x, y = Event.x, Event.y                                                                    # Coords of click
        if ValidSpace(x, y):
            if len(root.NodeList) > 0:
                Deselect()
            Node = CreateNode(x, y)
            LineW = ChangeLineW()
            for Link in root.LinkList:                                                             # Update the lines' width
                cnv.itemconfig(Link, width=LineW)
            root.SelectedItem = Node

    ButtonRelief(AddNodeBtn)
    EditNodes(None)                                                                                # Change nodes and
    ChangeLinks(None)                                                                              # Links back to normal
    cnv.bind("<Button-1>", LocateNode)
    ClearLinkLbl()
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Make new links
def DrawLine(LinkA, LinkB, text):
    root.Saved = False
    if len(root.EntList) % 2 == 0: row = 0
    else: row = 1
    column = (len(root.EntList) - root.CurrentPage) // 2 * 2                                       # Calculate the rows and columns
    Lbl = Label(root, text=text, width=Lbl1W, bg=root.RootBg, fg=root.Fg, font=Lbl4Font)
    Ent = Entry(root, width=EntW, bg=root.EntBg, fg=root.Fg, font=EntFont)                         # Create corresponding label and entry
    if len(root.EntList) - root.CurrentPage < 10:                                                  # If entries not full (less than 10)
        Lbl.grid(row=row, column=column, sticky="E")
        Ent.grid(row=row, column=column + 1, sticky="W")
        if len(root.EntList) - root.CurrentPage >= 2: RightBtn.config(state=NORMAL)                # If there are more than 2 entries presented
    root.LblList2.append(Lbl)
    root.EntList.append(Ent)
    Ax, Ay = GetCoords(LinkA)                                                                      # Get coords of the 2 nodes
    Bx, By = GetCoords(LinkB)
    LineW = ChangeLineW()
    if text[1:3] == "=>":                                                                          # Directed line
        Bx, By = DrawArrow(Ax, Ay, Bx, By)
        Line = cnv.create_line(Ax, Ay, Bx, By, fill=root.LineBg, width=LineW,
                               arrow=LAST, arrowshape=ArrowShape)
    else: Line = cnv.create_line(Ax, Ay, Bx, By, fill=root.LineBg, width=LineW)                    # Bi-directional line
    cnv.tag_lower(Line)
    if root.Pic != "": cnv.tag_raise(Line, root.Pic)
    root.LinkList.append(Line)
    for Link in root.LinkList:
        cnv.itemconfig(Link, width=LineW)

def AddLink():
    def LinkNodes(Event):                                                                          # Dealing with the add link label
        x, y = Event.x, Event.y                                                                    # Coords of click
        Node = cnv.find_closest(x, y)[0]                                                           # Get coord of the nearest node
        if Node in root.NodeList:
            if root.LinkA == "" or root.LinkB == "": cnv.itemconfig(Node, width=5)
            text = AddLinkLbl.cget("text")
            letter = chr(root.NodeList.index(Node) + 65)                                           # Convert into letter
            if root.LinkA == "":                                                                   # When no nodes are selected
                root.LinkA = Node
                text = "Link: " + letter + text[-1]
            elif root.LinkA == Node:                                                               # Remove the selected node
                root.LinkA = ""
                text = "Link:  " + text[-1]
                cnv.itemconfig(Node, width=2)
            elif root.LinkB == "":                                                                 # When one node is selected
                root.LinkB = Node
                text = text[0:-1] + letter
            elif root.LinkB == Node:                                                               # Remove the selected node
                root.LinkB = ""
                text = text[0:-1] + " "
                cnv.itemconfig(Node, width=2)
            AddLinkLbl.config(text=text)
            if root.LinkA != "" and root.LinkB != "":                                              # When two nodes are selected
                AddLinkBtn.config(relief=RAISED)                                                   # Link ready to be created
            else:
                AddLinkBtn.config(relief=SUNKEN)                                                   # User still picking nodes
    
    def CreateLink():
        text = AddLinkLbl.cget("text")[-2:]
        repeat = False
        for Lbl in root.LblList2:                                                                  # Check is that a repeating link
            LblTxt = Lbl.cget("text")
            i = len(DirOptions[0]) + 1
            a = LblTxt[0] + LblTxt[i]
            b = LblTxt[i] + LblTxt[0]
            if text == a or text == b: repeat = True
        if not repeat:                                                                             # Check is link already present
            text = text[0] + DirBtn.cget("text") + text[1] + ":"
            DrawLine(root.LinkA, root.LinkB, text)                                                 # Creating line in cnv
        else: mb.showerror("Error", "Link already present")
        EditNodes(None)
    
    ButtonRelief(AddLinkBtn)                                                                       # Stay selected
    cnv.unbind("<Button-1>")
    if not (root.LinkA == "" or root.LinkB == ""):                                                 # When two diff nodes are selected
        CreateLink()
        ClearLinkLbl()
        Deselect()
        EditNodes(LinkNodes)
        ChangeLinks(None)
    elif root.LinkA == "" and root.LinkB == "":                                                    # When no nodes are selected
        Deselect()
        EditNodes(LinkNodes)
        ChangeLinks(None)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Arrow buttons
def RightPage():
    if len(root.EntList) - root.CurrentPage <= 4: RightBtn.config(state=DISABLED)                  # Only 2 entries visible
    if root.CurrentPage >= 0: LeftBtn.config(state=NORMAL)                                         # All left button
    root.CurrentPage += 2
    Reorganise()

def LeftPage():
    if root.CurrentPage == 2: LeftBtn.config(state=DISABLED)                                       # Already the leftest
    if len(root.EntList) - root.CurrentPage >= 0: RightBtn.config(state=NORMAL)
    root.CurrentPage -= 2
    Reorganise()
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def ChangeDir():                                                                                   # Change direction in dir button
    direction = DirBtn.cget("text")
    ind = DirOptions.index(direction) + 1
    ind %= 2
    DirBtn.config(text = DirOptions[ind])
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Error checking
def Submit():
    def Check():
        errors = []                                                                                # Used to save all errors
        l = []
        x = len(DirOptions[0]) + 1
        for Lbl in root.LblList2:                                                                  # Check any disconnected node
            text = Lbl.cget("text")
            for i in range(0, x+1, x):
                letter = text[i]
                if letter not in l: l.append(letter)
        if len(l) < len(root.NodeList): errors.append("Disconnected nodes")
        for Ent in root.EntList:
            try:
                value = Ent.get()                                                                  # Get inputs in entries
                if float(value) > 0:                                                               # Check for characters and numbers > 0
                    pass
                else: errors.append("Only positive real numbers")                                  # Negative float value
            except: errors.append("Invalid link value(s)")
        NumOfNodes = len(root.NodeList)
        root.StartNode = StartNodeEnt.get().upper()                                                # Get uppercase values
        root.TargetNode = TargetNodeEnt.get().upper()
        for item in (root.StartNode, root.TargetNode):
            if len(item) != 1:                                                                     # Length should be 1
                if item == root.StartNode.upper(): txt = "start"
                else: txt = "target"
                errors.append("Invalid {} node".format(txt))
            else:
                num = ord(item)
                if NumOfNodes + 64 < num or num < 65:
                    errors.append("{} node not in range".format(txt))
        return errors
    
    if SubmitBtn.cget("text") != "Unlock":
        errors = Check()
        if len(errors) == 0:                                                                       # Disabling everything
            cnv.unbind("<Button-1>")
            EditNodes(None)
            ChangeLinks(None)
            for Ent in root.EntList:
                Ent.config(state=DISABLED)
            root.SelectedItem = ""
            ClearLinkLbl()
            ButtonRelief(None)
            for item in SideList:
                item.config(state=DISABLED)
            SubmitBtn.config(text="Unlock")
            SubmitBtn.config(state=NORMAL)
            ShortestBtn.config(state=NORMAL)
            for item in (root.SettingsArea, root.SettingsShape, root.SettingsCircle):
                SettingsCnv.tag_unbind(item, "<Button-1>")
        else:
            message = ""
            for error in errors:
                message += error + "\n"
            mb.showerror("Error", message)                                                         # List errors
    else:
        for Ent in root.EntList:                                                                   # Everything back to normal
            Ent.config(state=NORMAL)
        for item in SideList:
            item.config(state=NORMAL)
        for item in root.SolLinks:
            cnv.delete(item)
        root.SolLinks = []
        for item in (root.SettingsArea, root.SettingsShape, root.SettingsCircle):
            SettingsCnv.tag_bind(item, "<Button-1>", SettingsWindow)
        SubmitBtn.config(text="Submit")
        ShortestBtn.config(state=DISABLED)
        cnv.delete(root.ResultTxt)
        root.ResultTxt = ""
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# SETTINGS WINDOW
def SettingsIcon():
    def ShapeList(x, y, ratio):                                                                    # Function not used
        l = [0,10, 2,10, 2,7.4, 7.1-1.4-2.12,7.1+1.4-2.12, 7.1-1.4, 7.1+1.4]
        for ind in range(0, 10):                                                                   # Reflect in y=x
            l.append(l[10 - 1 - ind])
        for ind in range(0, 10 * 2, 2):                                                            # Reflect in x-axis
            l.append(l[10 * 2 - 1 - ind - 1])
            l.append(l[10 * 2 - 1 - ind] * -1)
        for ind in range(0, 10 * 4, 2):                                                            # Reflect in y-axis
            l.append(l[10 * 4 - 1 - ind - 1] * -1)
            l.append(l[10 * 4 - 1 - ind])
        for ind in range(len(l)):
            if ind % 2 == 0: a = l[ind] * ratio + x
            else: a = l[ind] * ratio + y
            a = round(a, 1)
            l[ind] = a
        print(l)
    
    x = 185                                                                                        # The x and y distance away from the origin of the
    y = 30                                                                                         # canvas
    ratio = 2                                                                                      # Enlarge by the ratio
    #ShapeList(x, y, ratio)                                                                        # Generate and print the coordinates
    root.SettingsShape = SettingsCnv.create_polygon(185,50, 189,50, 189,44.8, 192.2,42.8,
                                                    196.4,47.0, 202.0,41.4, 197.8,37.2, 199.8,34,
                                                    205,34, 205,30, 205,30, 205,26,
                                                    199.8,26, 197.8,22.8, 202.0,18.6, 196.4,13.0,
                                                    192.2,17.2, 189,15.2, 189,10, 185,10,
                                                    185,10, 181,10, 181,15.2, 177.8,17.2,
                                                    173.6,13.0, 168.0,18.6, 172.2,22.8, 170.2,26,
                                                    165,26, 165,30, 165,30, 165,34,
                                                    170.2,34, 172.2,37.2, 168.0,41.4, 173.6,47.0,
                                                    177.8,42.8, 181,44.8, 181,50, 185,50,
                                                    fill=root.RootBg,)                             # Create the outer settings icon
    ratio *= 5
    root.SettingsCircle = SettingsCnv.create_oval(x-ratio, y-ratio, x+ratio, y+ratio,
                                                  fill=root.IconBg, width=0)                       # Create the inner settings icon
    SettingsCnv.tag_bind(root.SettingsShape, "<Button-1>", SettingsWindow)
    SettingsCnv.tag_bind(root.SettingsCircle, "<Button-1>", SettingsWindow)
# -------------------------------------------------------------------------------------------------
def ClearList(Settings):                                                                           # Clear all widgets in settings
    for item in Settings.l:
        item.destroy()
    Settings.l = []
# -----------------------------------------------
# File menu
def FilePage(Settings):                                                                            # Create the file page
    def NewFile(Settings):
        if root.Saved:                                                                             # Clear everything if saved
            DelAll(True, True)
            ClearList(Settings)
            Settings.destroy()
        else:                                                                                      # If not saved
            Ok = mb.askyesno("Warning", "File not saved\nDo you still want to clear?")
            if Ok:                                                                                 # Don't want to save
                DelAll(True, True)
                ClearList(Settings)
                Settings.destroy()
            else: SaveFile(Settings)

    def OpenFile(Settings):
        FilePath = fd.askopenfilename(filetype=TxtFT)                                              # Get filename
        ClearList(Settings)
        Settings.destroy()
        if FilePath != "":                                                                         # Didn't select a file (Closed that window)
            Ok = mb.askyesno("Warning", "Everything will be cleared,\nAre you sure?")
        else: Ok = False
        if Ok:
            DelAll(True, False)
            cnv.itemconfig(Filename, text="File: "+FilePath)
            File = open(FilePath, "r")
            Lines = File.readlines()                                                               # Get every line from file
            ind = 0
            Line = Lines[ind][0:-1].split(",")
            root.RootBg = Line[0]
            ChangeWidgets(root.RootBg)                                                             # Change the window bg
            ind += 2
            Line = Lines[ind][0:-1].split(",")
            while Line != ["---"]:                                                                 # "---" is to split the data
                x = float(Line[0])                                                                 # Get the coords x and y
                y = float(Line[1])
                CreateNode(x, y)
                ind += 1
                Line = Lines[ind][0:-1].split(",")
            for node in root.NodeList:
                cnv.itemconfig(node, width=2)
            ind += 1
            Line = Lines[ind][0:-1].split(",")
            while Line != ["---"]:
                [Nodes, Value] = Line[0:2]
                NodeA = Nodes[0]                                                                   # Get links with linkA and
                NodeB = Nodes[len(DirOptions[0])+1]                                                # linkB with the value
                NodeA = root.NodeList[ord(NodeA) - 65]
                NodeB = root.NodeList[ord(NodeB) - 65]
                DrawLine(NodeA, NodeB, Nodes + ":")
                if Value != " ":
                    for i, Lbl in enumerate(root.LblList2):                                        # Insert values into entries
                        Text = Lbl.cget("text")[0:-1]
                        if Text == Nodes: root.EntList[i].insert(0, Value)
                ind += 1
                Line = Lines[ind][0:-1].split(",")
            l = []
            for i in range(3):                                                                     # Get the last 3 data
                ind += 1
                Line = Lines[ind][0:-1].split(",")
                l.append(Line[0])
            StartNodeEnt.delete(0, END)
            TargetNodeEnt.delete(0, END)
            StartNodeEnt.insert(0, l[0])                                                           # Starting node value
            TargetNodeEnt.insert(0, l[1])                                                          # Target node value
            root.Algorithm = l[2]                                                                  # Algorithm saved
            UpdateAlgLbl()
            File.close()

    def SaveFile(Settings):
        FilePath = fd.asksaveasfilename(filetype=TxtFT)                                            # Get file name
        if FilePath[-4:] != ".txt": FilePath += ".txt"                                             # User enter file name
        if FilePath != ".txt":                                                                     # User didn't select
            cnv.itemconfig(Filename, text="File:")                                                  # Close file path text
            root.Saved = True                                                                      # File saved
            try:
                File = open(FilePath, "x")                                                         # Create file, returns error if exists
                mb.showinfo("Info", "File saved")
            except:
                mb.showinfo("Info", "File replaced")                                               # Overwrite if exists
                File = open(FilePath, "w")
            File.write(root.RootBg + "\n---\n")                                                    # "---" to separate
            text = ""
            for Node in root.NodeList:
                Coords = GetCoords(Node)                                                           # Get the coordinates of the node
                text = "{},{}".format(str(Coords[0]), str(Coords[1]))
                File.write(text + "\n")                                                            # Save the coords
            File.write("---\n")
            for ind, Ent in enumerate(root.EntList):
                Text = root.LblList2[ind].cget("text")[:len(DirOptions[0])+2]                      # Get the nodes of the link
                Value = Ent.get()                                                                  # Get the value of the link (could be blank)
                File.write("{},{}\n".format(Text, Value))
            File.write("---\n")
            File.write(StartNodeEnt.get() + "\n")                                                  # Save the starting and target node (can be blank)
            File.write(TargetNodeEnt.get() + "\n")
            File.write(root.Algorithm + "\n")                                                      # The lastest selected algorithm
            File.close()
    
    ClearList(Settings)
    lbl1 = Label(Settings, text="Files", width=SettingsLblW - 5, bg=root.RootBg,
                 fg=root.Fg, font=SettingsTitleFont)
    lbl1.grid(row=0, column=0, pady=10)
    Settings.l.append(lbl1)
    lbl2 = Label(Settings, text="New:", width=SettingsLblW, bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl2.grid(row=1, column=0)
    Settings.l.append(lbl2)
    btn1 = Button(Settings, text="New file", width=SettingsBtnW, bg=root.BtnBg, fg=root.Fg,
                  activebackground=root.BtnBg, command=lambda: NewFile(Settings))
    btn1.grid(row=2, column=0)
    Settings.l.append(btn1)
    lbl3 = Label(Settings, text="Open:", width=SettingsLblW, bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl3.grid(row=3, column=0)
    Settings.l.append(lbl3)
    btn2 = Button(Settings, text="Open file", width=SettingsBtnW, bg=root.BtnBg, fg=root.Fg,
                  activebackground=root.BtnBg, command=lambda: OpenFile(Settings))
    btn2.grid(row=4, column=0)
    Settings.l.append(btn2)
    lbl4 = Label(Settings, text="Save as:", width=SettingsLblW, bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl4.grid(row=5, column=0)
    Settings.l.append(lbl4)
    btn3 = Button(Settings, text="Save file", width=SettingsBtnW, bg=root.BtnBg, fg=root.Fg,
                  activebackground=root.BtnBg, command=lambda: SaveFile(Settings))
    btn3.grid(row=6, column=0)
    Settings.l.append(btn3)
    if root.Saved:
        btn3.config(state=DISABLED)
# -----------------------------------------------
def MakeGraphPage(Settings):                                                                       # Creatae the generate graph page
    def GenerateGraph(NumOfNodes, Option):                                                         # Create graph
        Radius = NumOfNodes * 10 + 70                                                              # Radius of the graph of ndoes
        Angle = 2 * pi / NumOfNodes                                                                # The angle between each node
        for num in range(NumOfNodes):
            x = root.Width / 2 + Radius * sin(Angle * num)
            y = CnvH / 2 - Radius * cos(Angle * num)
            CreateNode(x, y)                                                                       # Make nodes
        if Option != 0:                                                                            # No links
            ind1, ind2 = 0, 1
            while ind1 < len(root.NodeList) - 1:                                                   # Go through all pairs of nodes
                ind2 = ind1 + 1
                while ind2 < len(root.NodeList):
                    text = ""
                    text = chr(ind1 + 65) + DirOptions[0]
                    text += chr(ind2 + 65)
                    chance = NumOfNodes // 4 + 1                                                   # More nodes -> smaller chance for random links
                    if Option == 2 or randint(1, chance) == 1:                                     # Random links
                        text += ":"
                        DrawLine(root.NodeList[ind1], root.NodeList[ind2], text)
                    ind2 += 1
                ind1 += 1
    
    def GraphDetails(Settings, v):
        ent1 = Settings.l[2]                                                                       # Get the number of nodes user want
        NumOfNodes = ent1.get()
        try:
            NumOfNodes = int(NumOfNodes)
            if NumOfNodes >= 2 and NumOfNodes <= 26:                                               # Only 2 - 26 nodes allowed
                Ok = mb.askyesno("Warning", "Everything will be cleared!")
            else:
                Ok = False
                mb.showerror("Error", "Only 2 to 26 nodes allowed")
        except:
            Ok = False
            mb.showerror("Error", "Invalid number of nodes")
        if Ok:
            ClearList(Settings)
            Settings.destroy()
            DelAll(True, False)
            Option = v.get()
            GenerateGraph(NumOfNodes, Option)
            for node in root.NodeList:
                cnv.itemconfig(node, width=2)
    
    ClearList(Settings)
    PadxDist = 12
    lbl1 = Label(Settings, text="Make graph", bg=root.RootBg,
                 fg=root.Fg, font=SettingsTitleFont)
    lbl1.grid(row=0, column=0, columnspan=2, pady=10)
    Settings.l.append(lbl1)
    lbl2 = Label(Settings, text="No of nodes:", bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl2.grid(row=1, column=0, padx=PadxDist, sticky="E")
    Settings.l.append(lbl2)
    ent1 = Entry(Settings, width=EntW, fg=root.Fg, font=SettingsFont)
    ent1.grid(row=1, column=1, sticky="W")
    Settings.l.append(ent1)
    lbl3 = Label(Settings, text="Style:", bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl3.grid(row=2, column=0, padx=PadxDist, sticky="E")
    Settings.l.append(lbl3)
    v = IntVar()
    v.set(0)                                                                                       # Default select first option
    for row, (Option, Val) in enumerate(GraphOptions):                                            # Choose which type of graph
        rdb = Radiobutton(Settings, text=Option, variable=v, value=Val, bg=root.RootBg,
                          fg=root.Fg, activebackground=root.RootBg)
        rdb.grid(row=row+2, column=1, sticky="W")
        Settings.l.append(rdb)
    btn1 = Button(Settings, text="Generate graph!", bg=root.BtnBg, fg=root.Fg, font=SettingsFont,
                  activebackground=root.BtnBg, command=lambda: GraphDetails(Settings, v))
    btn1.grid(row=5, column=0, columnspan=2, pady=20)
    Settings.l.append(btn1)
# -------------------------------------------------------------------------------------------------
def AlgorithmPage(Settings):                                                                       # Create algorithm page
    def ChangeAlg(Settings, v):                                                                    # Change algorithm
        if root.Algorithm != v.get():
            root.Algorithm = v.get()
            UpdateAlgLbl()
        ClearList(Settings)
        Settings.destroy()
    
    ClearList(Settings)
    root.Saved = False
    lbl1 = Label(Settings, text="Algorithms", bg=root.RootBg, fg=root.Fg, font=SettingsTitleFont)
    lbl1.grid(row=0, column=0, padx=10, pady=10, sticky="W")
    Settings.l.append(lbl1)
    lbl2 = Label(Settings, text="Choose algorithm:", bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl2.grid(row=1, column=0, columnspan=len(ColourOptions), padx=10, sticky="W")
    Settings.l.append(lbl2)
    v = StringVar()
    v.set(root.Algorithm)
    for row, (Name, Val) in enumerate(Algorithms):                                                 # Algorithm options
        rdb = Radiobutton(Settings, text=Name, variable=v, value=Val,
                          bg=root.RootBg, activebackground=root.RootBg)
        rdb.grid(row=row+2, column=0, padx=20, sticky="W")
        Settings.l.append(rdb)
    btn1 = Button(Settings, text="Change algorithm", bg=root.BtnBg, fg=root.Fg,
                  font=SettingsFont, command=lambda: ChangeAlg(Settings, v))
    btn1.grid(row=4, column=0, columnspan=len(ColourOptions), padx=10, pady=10)
    Settings.l.append(btn1)
# -----------------------------------------------
def OutlinePage(Settings):                                                                         # Create outline page
    def LbxDisplay(lbx, btn1, btn2):
        if btn1.cget("text") == "Links":                                                           # Display links
            ind = lbx.curselection()                                                               # Get user selection (could be blank)
            if ind != ():                                                                          # If not blank
                ind = ind[0] - 1                                                                   # Left one line for the title
                if ind != -1:
                    btn1.config(text="Back")
                    btn2.config(state=DISABLED)
                    Node = chr(ind + 65)
                    lbx.delete(0, END)
                    lbx.insert(0, "Link(s) from node " + Node)
                    for lbl in root.LblList2:
                        NodeA = lbl.cget("text")[0]
                        NodeB = lbl.cget("text")[len(DirOptions[0])+1]
                        if Node == NodeA:
                            lbx.insert(END, " -To node " + NodeB)
                        elif Node == NodeB:
                            lbx.insert(END, " -To node " + NodeA)
            else: mb.showerror("Error", "No nodes selected")
        else:                                                                                      # Display nodes
            btn2.config(state=NORMAL)
            btn1.config(text="Links")
            lbx.delete(0, len(root.LinkList))
            lbx.insert(0, "Nodes:")
            for num in range(len(root.NodeList)):
                lbx.insert(num + 1, " -Node {}".format(chr(num + 65)))

    def LbxDelSel(lbx):                                                                            # Delete selected
        ind = lbx.curselection()
        if ind != ():
            ind = int(ind[0] - 1)
            if ind != -1:
                Item = root.NodeList[ind]
                Deselect()
                root.SelectedItem = Item
                DelSel()
                lbx.delete(len(root.NodeList) + 1)
        else: mb.showerror("Error", "No nodes selected")
    
    ClearList(Settings)
    lbl1 = Label(Settings, text="Outline", bg=root.RootBg,
                 fg=root.Fg, font=SettingsTitleFont)
    lbl1.grid(row=0, column=0, columnspan=2, pady=5)
    Settings.l.append(lbl1)
    NodeFrame = Frame(Settings, bg=root.RootBg)
    NodeFrame.grid(row=1, column=0, padx=10)
    Settings.l.append(NodeFrame)
    lbx = Listbox(NodeFrame, width=18, height=11, bg=root.RootBg,
                  fg=root.Fg, selectbackground=root.LbxTxtFill)
    if len(root.NodeList) == 0:
        lbx.insert(0, "------ Empty ------")
        status = DISABLED
    else:
        lbx.insert(0, "NODES:")
        for num in range(len(root.NodeList)):
            lbx.insert(END, " -Node {}".format(chr(num + 65)))
        status = NORMAL
    lbx.grid(row=0, column=0)
    Settings.l.append(lbx)
    sb = Scrollbar(NodeFrame, command=lbx.yview)
    sb.grid(row=0, column=1, ipady=85)
    lbx.config(yscrollcommand=sb.set)
    BtnFrame = Frame(Settings, bg=root.RootBg)
    BtnFrame.grid(row=1, column=1, padx=5, sticky="N")
    Settings.l.append(BtnFrame)
    btn1 = Button(BtnFrame, text="Links", width=SettingsBtnW, bg=root.BtnBg, fg=root.Fg, state=status,
                  activebackground=root.BtnBg, command=lambda: LbxDisplay(lbx, btn1, btn2))
    btn1.grid(row=0, column=0, pady=5)
    btn2 = Button(BtnFrame, text="Delete item", width=SettingsBtnW, bg=root.BtnBg, fg=root.Fg,
                  state=status, activebackground=root.BtnBg, command=lambda: LbxDelSel(lbx))
    btn2.grid(row=1, column=0, pady=5)
# -----------------------------------------------
def EntriesPage(Settings):
    def FillEnt(Settings, Option):                                                                 # Fill empty entries
        Ok = mb.askyesno("Warning",
                         "Empty entries will be filled with {}\nAre you sure?".format(Option))
        if Ok:
            ClearList(Settings)
            Settings.destroy()
            for Ent in root.EntList:
                if Ent.get() == "":
                    if Option == "1s": Txt = "1"                                                   # Fill with 1s
                    else: Txt = str(randint(1, 10))                                                 # Fill with random integers (1-10)
                    Ent.insert(0, Txt)

    def DistEnt(Settings):
        Ok = mb.askyesno("Warning", "All entries will be cleared\nAre you sure?")
        if Ok:
            for ind in range(len(root.LblList2)):
                txt = root.LblList2[ind].cget("text")
                x1, y1 = GetCoords(root.NodeList[ord(txt[0]) - 65])
                x2, y2 = GetCoords(root.NodeList[ord(txt[2]) - 65])
                Dist = int(sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)) // 10
                root.EntList[ind].delete(0, END)
                root.EntList[ind].insert(0, Dist)

    def ClearEnt():                                                                                # Clear all entries
        Ok = mb.askyesno("Warning", "All entries will be cleared\nAre you sure?")
        if Ok:
            for Ent in root.EntList:
                Ent.delete(0, END)
    
    ClearList(Settings)
    root.Saved = False
    if len(root.EntList) == 0: state = DISABLED
    else: state = NORMAL
    lbl1 = Label(Settings, text="Entries", bg=root.RootBg,
                 fg=root.Fg, font=SettingsTitleFont)
    lbl1.grid(row=0, column=0, pady=5, columnspan=2)
    Settings.l.append(lbl1)
    lbl2 = Label(Settings, text="Assing 1s:", bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl2.grid(row=1, column=0, pady=5, sticky="E", padx=10)
    Settings.l.append(lbl2)
    btn1 = Button(Settings, text="1s", width=SettingsBtnW, bg=root.BtnBg, fg=root.Fg, state=state,
                  activebackground=root.BtnBg, command=lambda: FillEnt(Settings, "1s"))
    btn1.grid(row=1, column=1, pady=5)
    Settings.l.append(btn1)
    lbl3 = Label(Settings, text="Random values:", bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl3.grid(row=2, column=0, pady=5, sticky="E", padx=10)
    Settings.l.append(lbl3)
    btn2 = Button(Settings, text="Random", width=SettingsBtnW, bg=root.BtnBg, fg=root.Fg, state=state,
                  activebackground=root.BtnBg, command=lambda: FillEnt(Settings, "random values"))
    btn2.grid(row=2, column=1, pady=5)
    Settings.l.append(btn2)
    lbl4 = Label(Settings, text="Distance:", bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl4.grid(row=3, column=0, pady=5, sticky="E", padx=10)
    Settings.l.append(lbl4)
    btn3 = Button(Settings, text="Distance", width=SettingsBtnW, bg=root.BtnBg, fg=root.Fg, state=state,
                 activebackground=root.BtnBg, command=lambda: DistEnt(Settings))
    btn3. grid(row=3, column=1, pady=5)
    Settings.l.append(btn3)
    lbl5 = Label(Settings, text="Clear entries:", bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl5.grid(row=4, column=0, pady=5, sticky="E", padx=10)
    Settings.l.append(lbl5)
    btn4 = Button(Settings, text="Clear", width=SettingsBtnW, bg=root.BtnBg, fg=root.Fg, state=state,
                  activebackground=root.BtnBg, command=ClearEnt)
    btn4.grid(row=4, column=1, pady=5)
    Settings.l.append(btn4)
# -----------------------------------------------
def ImagePage(Settings):
    def AddBgPic(Settings):
        FilePath = fd.askopenfilename(filetype=ImgFT)
        root.img = tk.PhotoImage(file=FilePath)
        if root.Pic != "": cnv.delete(root.Pic)
        root.Pic = cnv.create_image(CnvW/2, CnvH/2, image=root.img)
        cnv.tag_lower(root.Pic)
        ClearList(Settings)
        Settings.destroy()
    
    ClearList(Settings)
    lbl1 = Label(Settings, text="Image", bg=root.RootBg, fg=root.Fg, font=SettingsTitleFont)
    lbl1.grid(row=0, column=0, pady=5)
    Settings.l.append(lbl1)
    lbl2 = Label(Settings, text="Import image as background", bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl2.grid(row=1, column=0, pady=5, padx=8)
    Settings.l.append(lbl2)
    btn1 = Button(Settings, text="Image", bg=root.BtnBg, fg=root.Fg,
                  font=SettingsFont, command=lambda: AddBgPic(Settings))
    btn1.grid(row=2, column=0)
    Settings.l.append(btn1)
# -----------------------------------------------
def MakeColour(r, g, b, no):                                                                       # Make the colour
    def DecHex(num):                                                                               # Convert from Dec to Hex
        a = num // 16
        b = num % 16
        if a >= 10: a = chr(a + 55)
        if b >= 10: b = chr(b + 55)
        a, b = str(a), str(b)
        return a + b
    
    start = [r, g, b]
    end = ["", "", ""]
    ind = start.index(min(start))
    end[ind] = start[ind] + Widgets[no][0]
    ind2 = start.index(max(start))
    end[ind2] = start[ind2] + Widgets[no][2]
    start.pop(ind)
    if ind < ind2: start.pop(ind2 - 1)
    else: start.pop(ind2)
    for i in range(len(end)):
        if end[i] == "":
            end[i] = start[0] + Widgets[no][1]
    for i in range(len(end)):
        if end[i] > 255: end[i] = 255
        if end[i] < 0: end[i] = 0
    Colour = "#{}{}{}".format(DecHex(end[0]), DecHex(end[1]), DecHex(end[2]))
    return Colour

def ChangeColour(Colour):                                                                          # Get the main colours
    def HexDec(num):                                                                               # Convert from Hex to Dec
        try: a = int(num[0]) * 16
        except: a = (ord(num[0]) - 55) * 16
        try: b = int(num[1])
        except: b = ord(num[1]) - 55
        return a + b
    
    R, G, B = HexDec(Colour[1:3]), HexDec(Colour[3:5]), HexDec(Colour[5:7])
    root.Fg = MakeColour(R, G, B, 0)
    root.CnvBg = MakeColour(R, G, B, 1)
    root.BtnBg = MakeColour(R, G, B, 2)
    root.EntBg = MakeColour(R, G, B, 3)
    root.ArrowBg = MakeColour(R, G, B, 4)
    root.LineBg = MakeColour(R, G, B, 5)
    root.NodeBg = MakeColour(R, G, B, 6)
    root.LbxTxtFill = MakeColour(R, G, B, 7)
    root.Line2Bg = MakeColour(R, G, B, 8)

def ChangeWidgets(Colour):                                                                         # Change all widget colours
    root.Saved = False
    root.RootBg = Colour
    root.config(bg=root.RootBg)
    SettingsCnv.config(bg=root.RootBg)
    SideFrame.config(bg=root.RootBg)
    SettingsCnv.itemconfig(root.SettingsShape, fill=root.RootBg)
    ChangeColour(Colour)
    root.IconBg = root.Fg
    cnv.itemconfig(Filename, fill=root.Fg)
    cnv.itemconfig(AlgLbl, fill=root.Fg)
    SettingsCnv.itemconfig(root.SettingsArea, fill=root.IconBg)
    SettingsCnv.itemconfig(root.SettingsCircle, fill=root.IconBg)
    StartNodeLbl.config(bg=root.RootBg, fg=root.Fg)
    TargetNodeLbl.config(bg=root.RootBg, fg=root.Fg)
    cnv.config(bg=root.CnvBg)
    for item in SideList:
        if item in (StartNodeEnt, TargetNodeEnt): item.config(bg=root.EntBg, fg=root.Fg)
        elif item in (AddLinkLbl, Space, Space2): item.config(bg=root.RootBg, fg=root.Fg)
        else:
            item.config(bg=root.BtnBg, fg=root.Fg,
                        activebackground=root.BtnBg,
                        activeforeground=root.Fg,)
    root.LineAf = root.ArrowBg
    root.NodeAf = root.ArrowBg
    LeftBtn.config(bg=root.ArrowBg, fg=root.Fg)
    RightBtn.config(bg=root.ArrowBg, fg=root.Fg)
    for Node in root.NodeList:
        cnv.itemconfig(Node, fill=root.NodeBg, outline=root.NodeBd)
    for Link in root.LinkList:
        cnv.itemconfig(Link, fill=root.LineBg)
    for Lbl in root.LblList1:
        cnv.itemconfig(Lbl, fill=root.Fg)
    for Lbl in root.LblList2:
        Lbl.config(bg=root.RootBg, fg=root.Fg)
    for Ent in root.EntList:
        Ent.config(bg=root.EntBg, fg=root.Fg)

def ThemePage(Settings):                                                                           # Create change colour page
    def GetColour(Settings, v):                                                                    # Get colour choice
        Colour = v.get()
        ChangeWidgets(Colour)
        ClearList(Settings)
        Settings.destroy()
    
    ClearList(Settings)
    lbl1 = Label(Settings, text="Colour theme", bg=root.RootBg, fg=root.Fg, font=SettingsTitleFont)
    lbl1.grid(row=0, column=0, columnspan=len(ColourOptions), pady=5)
    Settings.l.append(lbl1)
    lbl2 = Label(Settings, text="Choose a colour:", bg=root.RootBg,
                 fg=root.Fg, font=SettingsFont)
    lbl2.grid(row=1, column=0, columnspan=len(ColourOptions), sticky="W")
    Settings.l.append(lbl2)
    v = StringVar()
    v.set(root.RootBg)
    for column, Colour in enumerate(ColourOptions):
        rdb = tk.Radiobutton(Settings, width=RdbtnW, variable=v, value=Colour, indicator=0,
                             border=3, bg=Colour, activebackground=Colour, selectcolor=Colour)
        rdb.grid(row=2, column=column, padx=8, pady=5, sticky="W")
        Settings.l.append(rdb)
    btn1 = Button(Settings, text="Change colour", bg=root.BtnBg, fg=root.Fg,
                  font=SettingsFont, command=lambda: GetColour(Settings, v))
    btn1.grid(row=3, column=0, columnspan=len(ColourOptions), pady=10)
    Settings.l.append(btn1)
# -------------------------------------------------------------------------------------------------
def TutorialPage(Settings):
    def YoutubeVideo():
        webbrowser.open('https://youtu.be/cLq0w-xvmsU')                                            # Link to YouTube
    
    ClearList(Settings)
    lbl1 = Label(Settings, text="Tutorial", bg=root.RootBg,
                 fg=root.Fg, font=SettingsTitleFont)
    lbl1.grid(row=0, column=0)
    Settings.l.append(lbl1)
    cnv = Canvas(Settings, width=300, height = 200, bg=root.RootBg)
    cnv.grid(row=1, column=0)
    Settings.l.append(cnv)
    local_dir = os.path.dirname(__file__)
    file_path = os.path.join(local_dir, "Tutorial_cover.ppm")
    Settings.img = tk.PhotoImage(file=file_path)
    Settings.Pic = cnv.create_image(0, 0, image=Settings.img, anchor=NW)
    btn1 = Button(Settings, text="Link to video ->", bg=root.BtnBg,
                  fg=root.Fg, font=SettingsFont, command=YoutubeVideo)
    btn1.grid(row=2, column=0)
    Settings.l.append(btn1)
# -------------------------------------------------------------------------------------------------
def RunMenuBar(Settings):                                                                          # Menu bar in settings page
    MenuBar = Menu(Settings)
    GeneralMenu = Menu(MenuBar, tearoff=0)
    GeneralMenu.add_command(label="Manage files", command=lambda: FilePage(Settings))
    GeneralMenu.add_command(label="Make graph", command=lambda: MakeGraphPage(Settings))
    MenuBar.add_cascade(label="General", menu=GeneralMenu)

    ViewMenu = Menu(MenuBar, tearoff=0)
    ViewMenu.add_command(label="Algorithms", command=lambda: AlgorithmPage(Settings))
    ViewMenu.add_command(label="Outline", command=lambda: OutlinePage(Settings))
    ViewMenu.add_command(label="Entries", command=lambda: EntriesPage(Settings))
    ViewMenu.add_command(label="Image", command=lambda: ImagePage(Settings))
    ViewMenu.add_command(label="Change theme", command=lambda: ThemePage(Settings))
    MenuBar.add_cascade(label="View", menu=ViewMenu)

    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label="Tutorial", command=lambda: TutorialPage(Settings))
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    Settings.config(menu=MenuBar)
# -------------------------------------------------------------------------------------------------
def SettingsWindow(Event):                                                                         # Create settings window
    Settings = Toplevel()
    Settings.title("Settings")
    x, y = 300, 300
    Settings.geometry("{}x{}+{}+{}".format(x, y, root.Width // 2 - x // 2,
                                           root.Height // 2 - y // 2 - 50))
    Settings.configure(background=root.RootBg)
    Settings.focus()
    Settings.resizable(False, False)
    Settings.grab_set()
    Settings.l = []
    RunMenuBar(Settings)
    FilePage(Settings)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def ToggleFullScreen(event):                                                                       # F11 toggle full screen
    if root.FullScreen:
        root.attributes("-fullscreen", False)
        root.geometry(str(root.Width) + "x" + str(root.Height))
        root.FullScreen = False
    else:
        root.attributes("-fullscreen", True)
        root.FullScreen = True
# -------------------------------------------------------------------------------------------------
def ExitWindow(Event): # Close window
    if root.Saved: # File saved
        quit()
    else:
        Leave = mb.askyesno("Warning", "Leave without saving?\nEverything will be lost!")
        if Leave:
            quit()
# -------------------------------------------------------------------------------------------------
def SideBtn():                                                                                     # Lay out the side buttons
    for row, item in enumerate(SideList):
        PadyDist = 3
        if item == AddLinkLbl:
            item.grid(row=row, column=0, sticky="W", pady=15)
            DirBtn.grid(row=row, column=0, sticky="E")
        elif item == StartNodeEnt:
            item.grid(row=row, column=0, sticky="E", pady=PadyDist)
            StartNodeLbl.grid(row=row, column=0, sticky="W", pady=PadyDist)
        elif item == TargetNodeEnt:
            item.grid(row=row, column=0, sticky="E", pady=PadyDist)
            TargetNodeLbl.grid(row=row, column=0, sticky="W", pady=PadyDist)
        elif item.cget("text") == SpaceTxt:
            item.grid(row=row, column=0)
        elif item != DirBtn:
            item.grid(row=row, column=0, pady=PadyDist)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------
root = tk.Tk()
root.title("Shortest path finder")                                                                 # Window name
root.attributes("-fullscreen", True)                                                               # Full screen
root.bind("<Escape>", ExitWindow)
root.Saved = True
root.Width = root.winfo_screenwidth()
root.Height = root.winfo_screenheight()
root.RootBg = "#C8E4F9"
root.configure(bg=root.RootBg)
root.FullScreen = True
root.bind("<F11>", ToggleFullScreen)
root.minsize(root.Width, root.Height)
# -------------------------------------------------------------------------------------------------
# Variables that changes throughout the program
root.NodeList = []
root.LblList1 = []
root.LblList2 = []
root.EntList = []
root.LinkList = []
root.SolLinks = []
root.Algorithm = "D"
root.CurrentPage = 0
root.LinkA = root.LinkB = ""
root.SelectedItem = ""
root.ResultTxt = ""
root.Pic = ""
# Fixed data for reference
DirOptions = ["==", "=>"]
GraphOptions = [("No edges", 0),
                ("Random edges", 1),
                ("Complete graph", 2)]
TxtFT = (("Text files", "*.txt"),
         ("All files", "*.*"))
ImgFT = ((".ppm", "*.ppm"),
         (".gif", "*.gif"),
         (".pgm", "*.pgm"))
Algorithms = [("Dijkstra's algorithm", "D"),
              ("Floyd's algorithm", "F")]
ColourOptions = [(root.RootBg),                                                                    # Blue
                 ("#F9E4c8"),                                                                      # Blueberry muffin
                 ("#C8E9E4"),                                                                      # Green
                 ("#FFFFe9"),                                                                      # Yellow
                 ("#F9C8E4")]                                                                      # Pink
Widgets = [(-160, -176, -144),
           (18, 9, 3),
           (36, 18, 6),
           (-36, -18, -6),
           (-80, -40, -8),
           (-80, -96, -64),
           (-126, -70, -14),
           (-200, -144, 3),
           (-144, -144, -36)]
ArrowShape = (25, 25, 12)
Lbl1Font = "Calibri 16 bold"
Lbl2Font = "Calibri 15"
Lbl3Font = "Calirbi 10"
Lbl4Font = EntFont = "Calibri 14 bold"
ArrowFont = "Calibri 18"
BtnFont = "Calibri 13"
SettingsTitleFont = "Calibri 15 bold underline"
SettingsFont = "Calibri 13"
LbxFont = "Calibri 13"
Lbl4Font = "Calibri 14 bold"
SpaceFont = "Calirbi 11 bold"
NodeR = 16
Lbl1W = 6
Lbl2W = 12
EntW = 5
BtnW = 16
BtnH = 2
SettingsBtnW = 10
SettingsLblW = 26
RdbtnW = 3
CnvW = root.Width * 7 // 8
CnvH = root.Height * 3 // 4 - 40
SettingsCnvW = 216
SettingsCnvH = 100
# Create colours
ChangeColour(root.RootBg)
root.LineAf = root.ArrowBg
root.NodeBd = root.Fg
root.NodeAf = root.LineAf
root.IconBg = root.Fg
SpaceTxt = "- - - - - - - - - - - - - - - -"
# -------------------------------------------------------------------------------------------------
# Main canvas
cnv = Canvas(root, width=CnvW, height=CnvH, bg=root.CnvBg)
cnv.grid(row=2, column=0, padx=10, rowspan=10, columnspan=10, sticky="N")
# -----------------------------------------------
LeftBtn = Button(root, text="<<<", width=3, height=5, bg=root.ArrowBg,
                 fg=root.Fg, activebackground=root.ArrowBg, font=ArrowFont,
                 state=DISABLED, command=LeftPage)
LeftBtn.grid(row=0, column=0, rowspan=2, padx=10, pady=40, sticky="NW")
RightBtn = Button(root, text=">>>", width=3, height=5, bg=root.ArrowBg,
                  fg=root.Fg, activebackground=root.ArrowBg, font=ArrowFont,
                  state=DISABLED, command=RightPage)
RightBtn.grid(row=0, column=9, rowspan=2, padx=10, pady=40, sticky="NE")
# -----------------------------------------------
Filename = cnv.create_text(5, 5, text="File: ", fill=root.Fg, anchor=NW)                           # Display file path
AlgLbl = cnv.create_text(5, 25, text="Current algorithm: Dijkstra's", fill=root.Fg, anchor=NW)     # Display algorithm
# -----------------------------------------------
# Side buttons
SideFrame = Frame(root, bg=root.RootBg)
SideFrame.grid(row=2, column=10, sticky="NW")
SideList = []
# -----------------------------------------------
AddNodeBtn = Button(SideFrame, text="Add node", bg=root.BtnBg, fg=root.Fg,
                    width=BtnW, height=BtnH, font=BtnFont, activebackground=root.BtnBg,
                    activeforeground=root.Fg, command=AddNode)
SideList.append(AddNodeBtn)
# -----------------------------------------------
AddLinkBtn = Button(SideFrame, text="Add link", bg=root.BtnBg, fg=root.Fg,
                    width=BtnW, height=BtnH, font=BtnFont, activebackground=root.BtnBg,
                    activeforeground=root.Fg, command=AddLink)
SideList.append(AddLinkBtn)
# -----------------------------------------------
AddLinkLbl = Label(SideFrame, text="Link: ", bg=root.RootBg, fg=root.Fg, font=Lbl2Font)
SideList.append(AddLinkLbl)
DirBtn = Button(SideFrame, text=DirOptions[0], bg=root.BtnBg, fg=root.Fg,
                font=BtnFont, width=5, activebackground=root.BtnBg,
                activeforeground=root.Fg, command=ChangeDir)
SideList.append(DirBtn)
# -----------------------------------------------
Space = Label(SideFrame, text=SpaceTxt, font=SpaceFont, bg=root.RootBg, fg=root.Fg)
SideList.append(Space)
# -----------------------------------------------
SelBtn = Button(SideFrame, text="Select item", bg=root.BtnBg, fg=root.Fg,
                width=BtnW, height=BtnH, font=BtnFont, activebackground=root.BtnBg,
                activeforeground=root.Fg, command=Select)
SideList.append(SelBtn)
# -----------------------------------------------
DelSelBtn = Button(SideFrame, text="Delete selected", bg=root.BtnBg, fg=root.Fg,
                   width=BtnW, height=BtnH, font=BtnFont, activebackground=root.BtnBg,
                   activeforeground=root.Fg, command=DelSel)
SideList.append(DelSelBtn)
root.bind("<Delete>", DelSelKey)
# -----------------------------------------------
DelAllBtn = Button(SideFrame, text="Delete all", bg=root.BtnBg, fg=root.Fg, width=BtnW,
                   height=BtnH, font=BtnFont, activebackground=root.BtnBg,
                   activeforeground=root.Fg, command=lambda: DelAll(False, True))
SideList.append(DelAllBtn)
# -----------------------------------------------
Space2 = Label(SideFrame, text=SpaceTxt, font=SpaceFont, bg=root.RootBg, fg=root.Fg)
SideList.append(Space2)
# -----------------------------------------------
StartNodeLbl = Label(SideFrame, text="Starting node:", width=Lbl2W, bg=root.RootBg,
                     fg=root.Fg, font=Lbl3Font)
StartNodeEnt = Entry(SideFrame, width=EntW, bg=root.EntBg, fg=root.Fg, font=EntFont)
SideList.append(StartNodeEnt)

TargetNodeLbl = Label(SideFrame, text="Target node:", width=Lbl2W, bg=root.RootBg,
                      fg=root.Fg, font=Lbl3Font)
TargetNodeEnt = Entry(SideFrame, width=EntW, bg=root.EntBg, fg=root.Fg, font=EntFont)
SideList.append(TargetNodeEnt)
# -----------------------------------------------
SubmitBtn = Button(SideFrame, text="Error check", bg=root.BtnBg, fg=root.Fg, width=BtnW,
                   height=BtnH, font=BtnFont, activebackground=root.BtnBg,
                   activeforeground=root.Fg, command=Submit)
SideList.append(SubmitBtn)
# -----------------------------------------------
ShortestBtn = Button(SideFrame, text="Compute\nshortest path", bg=root.BtnBg, fg=root.Fg,
                     width=BtnW, height=BtnH, font=BtnFont, activebackground=root.BtnBg,
                     activeforeground=root.Fg, command=Shortest, state=DISABLED)
SideList.append(ShortestBtn)
# -----------------------------------------------
SideBtn()                                                                                          # Grid method to lay out the side buttons
# -------------------------------------------------------------------------------------------------
# Settings canvas
SettingsCnv = Canvas(root, width=SettingsCnvW, height=SettingsCnvH,
                     bg=root.RootBg, highlightthickness=0)                                         # Corner canvas for settings
SettingsCnv.grid(row=0, column=10, sticky="NE")
x = 116
root.SettingsArea = SettingsCnv.create_polygon(x, 0, x+SettingsCnvH, 0, x+SettingsCnvH,
                                               SettingsCnvH, fill=root.IconBg)                     # Settings triangle
SettingsCnv.tag_bind(root.SettingsArea, "<Button-1>", SettingsWindow)
SettingsIcon()                                                                                     # Settings icon
# -------------------------------------------------------------------------------------------------
root.mainloop()
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------















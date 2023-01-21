DirOptions = ["==", "=>"]
def CheckInvalidLoop(NodeList): # Check any disconnected parts of graph
    for Value in NodeList:
        if not (isinstance(Value[1], str) or Value[1] == -1):
            return False
    return True

def CheckAllStr(NodeList): # NodeList permanent
    for i in NodeList:
        if not isinstance(i[1], str):
           return False
    return True

def NodeValue(NodeList, Target): # Get value of given node
    for Node in NodeList:
        if Target == Node[0]:
            return Node[1]
#----------------------------------------------------------------------------------------------
def ChangeNodeValues(NodeList, NextNode, Value):
    for Node in NodeList:
        if Node[0] == NextNode: # Search node
            if Node[1] == -1: # No previous value
                Node[1] = Value
            elif isinstance(Node[1], str):
                pass
            elif Value < Node[1]:
                Node[1] = Value

def MakePermanent(NodeList):
    smallest = -1
    for Value in NodeList:
        if Value[1] != -1 and isinstance(Value[1], float): # -1 for no temp value
            if smallest == -1:
                smallest = Value[1]
            else:
                if Value[1] < smallest:
                    smallest = Value[1]
    found = False
    index = -1
    while not found and index < len(NodeList) - 1: # Make smallest permanent
        index += 1
        if smallest == NodeList[index][1] and smallest != -1:
            NodeList[index][1] = str(smallest)
            found = True
    return NodeList[index][0] #return the node thats going to be used

def EditLinks(NodeList, LinkList, CurrentNode, CNValue, NextNode):
    for Link in LinkList: # Search for links connected to the current node
        found = False
        if Link[1] == CurrentNode and Link[3] != DirOptions[1]:
            NextNode = Link[0]
            found = True
        elif Link[0] == CurrentNode:
            NextNode = Link[1]
            found = True
        if found:
            Value = Link[2] + float(CNValue)
            ChangeNodeValues(NodeList, NextNode, Value)

def LabelGraph(NodeList, LinkList, StartNode, TargetNode):
    CurrentNode = StartNode
    NextNode = ''
    for Node in NodeList: # Manually change starting node to 0
        if Node[0] == StartNode:
            Node[1] = 0.0
    MakePermanent(NodeList)
    while not CheckAllStr(NodeList):
        Value = NodeValue(NodeList, CurrentNode)
        EditLinks(NodeList, LinkList, CurrentNode, Value, NextNode)
        if not CheckAllStr(NodeList): # Check closed loops
            if CheckInvalidLoop(NodeList):
                if isinstance(NodeValue(NodeList, TargetNode), str): return True
                return False
        CurrentNode = MakePermanent(NodeList)
    return True

def DPath(NodeList, LinkList, StartNode, TargetNode):
    Loop = LabelGraph(NodeList, LinkList, StartNode, TargetNode)
    if not Loop:
        return 'Not found', 'N/A'
    Path = [TargetNode]
    NextNode = TargetNode
    Value = float(NodeValue(NodeList, NextNode))
    #print(LinkList, NodeList, Path)
    Min = Value # Value of target node
    while NextNode != StartNode:
        index = 0
        found = False
        while not found and index < len(LinkList):
            Link = LinkList[index]
            for i in range(2):
                if Link[i] == NextNode and not found and Link[1-i] not in Path:
                    x = round(float(NodeValue(NodeList, Link[1-i])), 1) # Target node value
                    if round(Value - x, 1) == Link[2]:
                        Value = x
                        NextNode = Link[1-i]
                        found = True
                        Path.append(NextNode)
            index += 1
    Txt = ""
    for Node in Path:
        Txt = Node + " -> " + Txt
    return Txt[:-4], Min








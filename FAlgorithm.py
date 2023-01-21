def PrintMatrices(DistMtrx, RouteMtrx):
    for a in range(len(DistMtrx)):
        print(DistMtrx[a])
    print('')
    for a in range(len(RouteMtrx)):
        print(RouteMtrx[a])

DirOptions = ["==", "=>"]

def Algorithm(DistMtrx, RouteMtrx):
    ind = 0
    while ind < len(DistMtrx):
        row = 0
        while row < len(DistMtrx):
            if row == ind and row + 1 < len(DistMtrx):
                row += 1
            column = 0
            while column < len(DistMtrx):
                if column == ind and column + 1 < len(DistMtrx):
                    column += 1
                value = DistMtrx[row][column]
                if -1 not in (DistMtrx[ind][column], DistMtrx[row][ind]):
                    s = DistMtrx[ind][column] + DistMtrx[row][ind]
                    if value == -1 or value > s:
                        DistMtrx[row][column] = s
                        RouteMtrx[row][column] = RouteMtrx[row][ind]
                column += 1
            row += 1
        ind += 1
    return DistMtrx, RouteMtrx

def FPath(NumOfNodes, LinkList, StartNode, TargetNode):
    DistMtrx = [[-1 for a in range(NumOfNodes)] for b in range(NumOfNodes)]
    RouteMtrx = [[a for a in range(1, NumOfNodes+1)] for b in range(NumOfNodes)]
    for Link in LinkList:
        ind1, ind2 = ord(Link[0]) - 65, ord(Link[1]) - 65
        Value = Link[2]
        if Link[3] != DirOptions[1]: DistMtrx[ind2][ind1] = Value
        DistMtrx[ind1][ind2] = Value
    DistMtrx, RouteMtrx = Algorithm(DistMtrx, RouteMtrx)
    StartInd = ord(StartNode) - 65
    TargetInd = ord(TargetNode) - 65
    Shortest = DistMtrx[StartInd][TargetInd]
    Node = RouteMtrx[StartInd][TargetInd] - 1
    Path = chr(StartInd+65) + ' -> '
    while Node != TargetInd:
        Path += chr(Node+65) + ' -> '
        Node = RouteMtrx[Node][TargetInd] - 1
    Path += chr(Node+65)
    if Shortest == -1:
        return "Not found", "N/A"
    #PrintMatrices(DistMtrx, RouteMtrx)
    return Path, Shortest









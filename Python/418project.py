import random
from re import T
from xml.etree.ElementTree import tostring

class vertex:
    def __init__(self,name,xcoord,ycoord,incedge):
        self.name = name
        self.x = xcoord
        self.y = ycoord
        self.incedge = incedge
    def strng(self,char):
        return self.name
    def __str__(self):
        return self.name + " (" + self.x + ", " + self.y + ") " + self.incedge
class face:
    def __init__(self,name,outcomp,inncomp):
        self.name = name
        self.outcomp = outcomp
        self.inncomp = inncomp
class halfedge:
    def __init__(self,name,origin,twin,incface,next,prev):
        self.name = name
        self.origin = origin
        self.twin = twin
        self.incface = incface
        self.next = next
        self.prev = prev
    def strng(self,char):
        return self.name
    def __str__(self):
        return self.name + " " + self.origin + " " + self.twin + " " + self.incface + " " + self.next + " " + self.prev
class DCEL:
    def __init__(self,vertices,edges,faces):
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
class fulledge:
    def __init__(self,he1,he2,dcel):
        for v in dcel.vertices:
            if he1.origin == v.name:
                he1vert = v
            if he2.origin == v.name:
                he2vert = v
        if he1vert.x < he2vert.x:
            self.leftvert = he1vert
            self.rightvert = he2vert
        elif he1vert.x > he2vert.x:
            self.rightvert = he1vert
            self.leftvert = he2vert
        else:
            if he1vert.y < he2vert.y:
                self.leftvert = he1vert
                self.rightvert = he2vert
            else:
                self.rightvert = he1vert
                self.leftvert = he2vert
        if self.leftvert == he1vert:
            self.tophe = he1
            self.bothe = he2
        else:
            self.tophe = he2
            self.bothe = he1
    def strng(self,char):
        if char == 't':
            return self.tophe.strng(char)
        else:
            return self.bothe.strng(char) 
class trapezoid:
    def __init__(self,name,T,B,R,L):
        self.name = name
        self.top = T
        self.bottom = B
        self.rightp = R
        self.leftp = L
    def strng(self,T,B,R,L):
        str = ""
        if self.top == T:
            str = str + "T\n"
        else:
            str = str + self.top.strng('t') + "\n" 
        if self.bottom == B:
            str = str + "B\n"
        else:
            str = str + self.bottom.strng('b') + "\n"
        if self.leftp == L:
            str = str + "L\n"
        else:
            str = str + self.leftp.strng('l') + "\n"
        if self.rightp == R:
            str = str + "R\n"
        else:
            str = str + self.rightp.strng('r') + "\n"
        return str

class vertnode:
    def __init__(self,vert):
        self.vert = vert
        self.name = vert.name
        self.right = None
        self.left = None
    def setright(self,node):
        self.right = node
    def setleft(self,node):
        self.left = node
    #point will be array with [x,y]
    def totheright(self,point):
        if vert.x < point[0]:
            return True
        else:
            return False
    def totheleft(self,point):
        if vert.x > point[0]:
            return True
        else:
            return False
class trapnode:
    def __init__(self,trap):
        self.trap = trap
        self.name = trap.name
class edgenode:
    def __init__(self,edge):
        self.edge = edge
        self.above = None
        self.below = None
    def setabove(self,node):
        self.above = node
    def setbelow(self,node):
        self.below = node
    def isabove(self,point):
        v1 = [self.edge.leftvert.x - self.edge.rightvert.x,self.edge.leftvert.y - self.edge.rightvert.y]
        v2 = [self.edge.leftvert.x - point[0],self.edge.leftvert.y - point[1]]
        xp = v1[0]*v2[1] - v1[1]*v2[0]
        if xp > 0:
            return True
        else:
            return False
    def isbelow(self,point):
        v1 = [self.edge.leftvert.x - self.edge.rightvert.x,self.edge.leftvert.y - self.edge.rightvert.y]
        v2 = [self.edge.leftvert.x - point[0],self.edge.leftvert.y - point[1]]
        xp = v1[0]*v2[1] - v1[1]*v2[0]
        if xp < 0:
            return True
        else:
            return False
    

def RandomPermutation(A):
    for k in range(len(A)-1,1,-1):
        rndindex = random.randint(0,k)
        temp = A[k]
        A[k] = A[rndindex]
        A[rndindex] = temp
    return A

def GenerateBoundingBox(dcel):
    T = None
    B = None
    R = None
    L = None 
    if len(dcel.vertices) == 0:
        return None
    for v in dcel.vertices:
        if T == None:
            T = v.y
        elif v.y > T:
            T = v.y
        if B == None:
            B = v.y
        elif v.y < B:
            B = v.y
        if R == None:
            R = v.x
        elif v.x > R:
            R = v.x
        if L == None:
            L = v.x
        elif v.x < L:
            L = v.x
    c1 = [T+1,L-1]
    c2 = [B-1,L-1]
    c3 = [B-1,R+1]
    c4 = [T+1,R+1]
    return c1,c2,c3,c4,T+1,B-1,R+1,L-1

def DAGTraversal(dag,p):
    if type(dag) == trapnode:
        #print("AAAAA")
        return dag
    while type(dag) != trapnode:
        if type(dag) == vertnode:
            if dag.totheright(p):
                dag = dag.right
            elif dag.totheleft(p):
                dag = dag.left
            else:
                if dag.vert.y>p[1]:
                    dag = dag.right
                elif dag.vert.y<p[1]:
                    dag = dag.left
                else:
                    return dag
        if type(dag) == edgenode:
            if dag.isabove(p):
                dag = dag.above
            elif dag.isbelow(p):
                dag = dag.below
            else:
                return dag    
    return dag

def DAGTraversalAndReplace(dag,p,tree):
    if type(dag) == trapnode:
        dag = tree
    while type(dag) != trapnode:
        if type(dag) == vertnode:
            if dag.totheright(p):
                if type(dag.right) == trapnode:
                    dag.setright(tree)
                    break
                dag = dag.right
            elif dag.totheleft(p):
                if type(dag.left) == trapnode:
                    dag.setleft(tree)
                    break
                dag = dag.left
            else:
                if dag.vert.y>p[1]:
                    if type(dag.right) == trapnode:
                        dag.setright(tree)
                        break
                    dag = dag.right
                elif dag.vert.y<p[1]:
                    if type(dag.left) == trapnode:
                        dag.setleft(tree)
                        break
                    dag = dag.left
        if type(dag) == edgenode:
            if dag.isabove(p):
                if type(dag.above) == trapnode:
                    dag.setabove(tree)
                    break
                dag = dag.above
            elif dag.isbelow(p):
                if type(dag.below) == trapnode:
                    dag.setbelow(tree)
                    break
                dag = dag.below

def DAGTraversalAndFill(dag,p,node):
    while True:
        if type(dag) == vertnode:
            if dag.totheright(p):
                if dag.right == None:
                    dag.setright(node)
                    break
                dag = dag.right
            elif dag.totheleft(p):
                if dag.left == None:
                    dag.setleft(node)
                    break
                dag = dag.left
        if type(dag) == edgenode:
            if dag.isabove(p):
                if dag.above == None:
                    dag.setabove(node)
                    break
                dag = dag.above
            elif dag.isbelow(p):
                if dag.below == None:
                    dag.setbelow(node)
                    break
                dag = dag.below
            
def FollowSegment(traplist,dag,edge):
    p = edge.leftvert
    q = edge.rightvert
    j = 0
    traps = [DAGTraversal(dag,[p.x,p.y]).trap]
    e = edgenode(edge)
    if type(traps[j].rightp) == vertex:
        rightside = traps[j].rightp.x
    else:
        rightside = traps[j].rightp
    while q.x > rightside:
        if e.isabove([traps[j].rightp.x,traps[j].rightp.y]):
            for t in traplist:
                if t.leftp == traps[j].rightp and t.bottom.tophe.name == traps[j].rightp.incedge:
                    traps.append(t)
                    j = j + 1
                    if type(traps[j].rightp) == vertex:
                        rightside = traps[j].rightp.x
                    else:
                        rightside = traps[j].rightp
                    break
        else:
            for t in traplist:
                if t.leftp == traps[j].rightp:
                    traps.append(t)
                    j = j + 1
                    if type(traps[j].rightp) == vertex:
                        rightside = traps[j].rightp.x
                    else:
                        rightside = traps[j].rightp
                    break
    return traps

def TrapezoidalMap(dcel):
    c1,c2,c3,c4,T,B,R,L = GenerateBoundingBox(dcel)
    trapezoidNum = 0
    trapezoids = []
    t = trapezoid('t'+str(trapezoidNum),T,B,R,L)
    trapezoidNum = trapezoidNum + 1
    trapezoids.append(t)
    edges = []
    for idx, he1 in enumerate(dcel.edges):
        twin = he1.twin
        for indx, he2 in enumerate(dcel.edges):
            if twin == he2.name and indx>idx:
                edges.append(fulledge(he1,he2,dcel))
                break
            elif twin == he2.name and indx<idx:
                break
    edges = RandomPermutation(edges)
    dag = trapnode(t)
    for e in edges:
        affectedtraps = FollowSegment(trapezoids,dag,e)
        if len(affectedtraps) == 1:
            #left trap in case where line is enclosed in trap
            t1 = trapezoid('t'+str(trapezoidNum),affectedtraps[0].top,affectedtraps[0].bottom,e.leftvert,affectedtraps[0].leftp)
            trapezoidNum = trapezoidNum + 1
            trapezoids.append(t1)
            #bottom trap in case where line is enclosed in trap
            t2 = trapezoid('t'+str(trapezoidNum),e,affectedtraps[0].bottom,e.rightvert,e.leftvert)
            trapezoidNum = trapezoidNum + 1
            trapezoids.append(t2)
            #top trap in case where line is enclosed in trap
            t3 = trapezoid('t'+str(trapezoidNum),affectedtraps[0].top,e,e.rightvert,e.leftvert)
            trapezoidNum = trapezoidNum + 1
            trapezoids.append(t3)
            #right trap in case where line is enclosed in trap
            t4 = trapezoid('t'+str(trapezoidNum),affectedtraps[0].top,affectedtraps[0].bottom,affectedtraps[0].rightp,e.rightvert)
            trapezoidNum = trapezoidNum + 1
            trapezoids.append(t4)
            t1node = trapnode(t1)
            t2node = trapnode(t2)
            t3node = trapnode(t3)
            t4node = trapnode(t4)
            leftvnode = vertnode(e.leftvert)
            rightvnode = vertnode(e.rightvert)
            enode = edgenode(e)
            leftvnode.setleft(t1node)
            leftvnode.setright(rightvnode)
            rightvnode.setright(t4node)
            rightvnode.setleft(enode)
            enode.setbelow(t2node)
            enode.setabove(t3node)
            dag = leftvnode
        else:
            # ORDER T B R L
            enode = edgenode(e)
            slope = (e.rightvert.y - e.leftvert.y) / (e.rightvert.x - e.leftvert.x)
            yintercept = e.leftvert.y - (slope * e.leftvert.x)
            for i, af in enumerate(affectedtraps):
                if type(af.rightp) == vertex:
                    rightside = af.rightp.x
                else:
                    rightside = af.rightp
                if type(af.leftp) == vertex:
                    leftside = af.leftp.x
                else:
                    leftside = af.leftp
                if i == 0:
                    t1 = trapezoid('t'+str(trapezoidNum),af.top,af.bottom,e.leftvert,af.leftp)
                    trapezoidNum = trapezoidNum + 1
                    if enode.isabove([af.rightp.x,af.rightp.y]):
                        #trap enclosed by the rightp of the first trapezoid
                        t2 = trapezoid('t'+str(trapezoidNum),af.top,e,af.rightp,e.leftvert)
                        trapezoidNum = trapezoidNum + 1
                        workingtrap = ['t'+str(trapezoidNum),e,af.bottom,e.leftvert,[[rightside-leftside,(slope*(rightside-leftside)) + yintercept-.1]]]
                        trapezoidNum = trapezoidNum + 1
                    else:
                        t2 = trapezoid('t'+str(trapezoidNum),e,af.bottom,af.rightp,e.leftvert)
                        trapezoidNum = trapezoidNum + 1
                        workingtrap = ['t'+str(trapezoidNum),af.top,e,e.leftvert,[[rightside-leftside,(slope*(rightside-leftside)) + yintercept+.1]]]
                        trapezoidNum = trapezoidNum + 1
                    trapezoids.append(t1)
                    trapezoids.append(t2)
                    t1node = trapnode(t1)
                    t2node = trapnode(t2)
                    leftvnode = vertnode(e.leftvert)
                    leftvnode.setleft(t1node)
                    tempenode = enode
                    leftvnode.setright(tempenode)
                    if t2.bottom == e:
                        tempenode.setabove(t2node)
                    else:
                        tempenode.setbelow(t2node)
                    DAGTraversalAndReplace(dag,[e.leftvert.x,e.leftvert.y],leftvnode)
                else:
                    if DAGTraversal(dag,[e.rightvert.x,e.rightvert.y]).trap == af:
                        if workingtrap[1] == e: #working is above
                            t1 = trapezoid(workingtrap[0],workingtrap[1],workingtrap[2],e.rightvert,workingtrap[3])
                            t2 = trapezoid('t'+str(trapezoidNum),e,af.bottom,e.rightvert,af.leftp)
                            trapezoidNum = trapezoidNum + 1
                            t1node = trapnode(t1)
                            t2node = trapnode(t2)
                            for wtp in workingtrap[4]:
                                DAGTraversalAndFill(dag,wtp,t1node)
                        elif workingtrap[2] == e: #working is below
                            t1 = trapezoid('t'+str(trapezoidNum),af.top,e,e.rightvert,af.leftp)
                            t2 = trapezoid(workingtrap[0],workingtrap[1],workingtrap[2],e.rightvert,workingtrap[3])
                            trapezoidNum = trapezoidNum + 1
                            t1node = trapnode(t1)
                            t2node = trapnode(t2)
                            for wtp in workingtrap[4]:
                                DAGTraversalAndFill(dag,wtp,t2node)
                        #t1 is top, t2 is bottom, t3 is right trap
                        t3 = trapezoid('t'+str(trapezoidNum),af.top,af.bottom,af.rightp,e.rightvert)
                        trapezoidNum = trapezoidNum + 1
                        trapezoids.append(t1)
                        trapezoids.append(t2)
                        trapezoids.append(t3)
                        t3node = trapnode(t3)
                        rightvnode = vertnode(e.rightvert)
                        tempenode = enode
                        tempenode.setabove(t1node)
                        tempenode.setbelow(t2node)
                        rightvnode.setright(t3)
                        rightvnode.setleft(tempenode)
                        DAGTraversalAndReplace(dag,[e.rightvert.x,e.rightvert.y],rightvnode)

                    else:
                        tempenode = enode
                        if workingtrap[1] == e: #working is above
                            if enode.isabove([af.rightp.x,af.rightp.y]):
                                t1 = trapezoid(workingtrap[0],workingtrap[1],workingtrap[2],af.rightp,workingtrap[3])
                                trapezoids.append(t1)
                                t1node = trapnode(t1)
                                tempenode.setabove(t1node)
                                DAGTraversalAndReplace(dag,[rightside-leftside,(slope*(rightside-leftside)) + yintercept],tempenode)
                                for wtp in workingtrap[4]:
                                    DAGTraversalAndFill(dag,wtp,t1node)
                                workingtrap = ['t'+str(trapezoidNum),e,af.bottom,af.leftp,[[rightside-leftside,(slope*(rightside-leftside)) + yintercept-.1]]]
                                trapezoidNum = trapezoidNum + 1
                            elif enode.isbelow([af.rightp.x,af.rightp.y]):
                                t1 = trapezoid('t'+str(trapezoidNum),e,af.bottom,af.rightp,af.leftp)
                                trapezoids.append(t1)
                                trapezoidNum = trapezoidNum + 1
                                t1node = trapnode(t1)
                                tempenode.setabove(t1node)
                                DAGTraversalAndReplace(dag,[rightside-leftside,(slope*(rightside-leftside)) + yintercept],tempenode)
                                workingtrap[4] = workingtrap[4] + [rightside-leftside,(slope*(rightside-leftside)) + yintercept+.1]
                        elif workingtrap[2] == e: #working is below
                            if enode.isabove([af.rightp.x,af.rightp.y]):
                                t1 = trapezoid('t'+str(trapezoidNum),af.top,e,af.rightp,af.leftp)
                                trapezoids.append(t1)
                                trapezoidNum = trapezoidNum + 1
                                t1node = trapnode(t1)
                                tempenode.setabove(t1node)
                                DAGTraversalAndReplace(dag,[rightside-leftside,(slope*(rightside-leftside)) + yintercept],tempenode)
                                workingtrap[4] = workingtrap[4] + [rightside-leftside,(slope*(rightside-leftside)) + yintercept-.1]
                            elif enode.isbelow([af.rightp.x,af.rightp.y]):
                                t1 = trapezoid(workingtrap[0],workingtrap[1],workingtrap[2],af.rightp,workingtrap[3])
                                trapezoids.append(t1)
                                t1node = trapnode(t1)
                                tempenode.setabove(t1node)
                                DAGTraversalAndReplace(dag,[rightside-leftside,(slope*(rightside-leftside)) + yintercept],tempenode)
                                for wtp in workingtrap[4]:
                                    DAGTraversalAndFill(dag,wtp,t1node)
                                workingtrap = ['t'+str(trapezoidNum),e,af.bottom,af.leftp,[[rightside-leftside,(slope*(rightside-leftside)) + yintercept+.1]]]
                                trapezoidNum = trapezoidNum + 1
        for af in affectedtraps:
            trapezoids.remove(af)
    return trapezoids, dag, T, B, R, L

if __name__ == "__main__":
    print("Point Location Using Trapezoidal Maps\n\n")
    numtrials = 1
    print("Trial " + str(numtrials) + ":\n")
    fname = input("Name of the input planar subdivision file: ")
    while fname != "x":
        outfile = input("Trapezoidal map constructed in the file ")
        with open(fname) as f:
            lines = f.readlines()
        vertices = []
        faces = []
        edges = []
        for line in lines:
            parts = line.split()
            if line[0] == '\n':
                continue
            elif line[0] == 'v':
                x = parts[1][1:]
                x = x[:-1]
                y = parts[2][:-1]
                vert = vertex(parts[0],float(x),float(y),parts[3])
                vertices.append(vert)
            elif line[0] == 'f':
                fac = face(parts[0],parts[1],parts[2])
                faces.append(fac)
            elif line[0] == 'e':
                edg = halfedge(parts[0],parts[1],parts[2],parts[3],parts[4],parts[5])
                edges.append(edg)
        dcel = DCEL(vertices,edges,faces)
        traps,dag,T,B,R,L = TrapezoidalMap(dcel)
        with open(outfile,'w') as out:
            out.write("****** Trapezoidal Map******\n\n")
            for f in faces:
                count = 0
                trapsonf = ""
                for t in traps:
                    if t.bottom == type(fulledge):
                        if t.bottom.tophe.incface == f.name:
                            trapsonf = trapsonf + t.strng(T,B,R,L) + "\n"
                    elif t.top == type(fulledge):
                        if t.bottom.bothe.incface == f.name:
                            trapsonf = trapsonf + t.strng(T,B,R,L) + "\n"
                    elif t.rightp == type(vertex):
                        for e in edges:
                            if t.rightp.incedge == e.name and e.incface == f.name:
                                trapsonf = trapsonf + t.strng(T,B,R,L) + "\n"
                    elif t.leftp == type(vertex):
                        for e in edges:
                            if t.leftp.incedge == e.name and e.incface == f.name:
                                trapsonf = trapsonf + t.strng(T,B,R,L) + "\n"
                    else:
                        trapsonf = trapsonf + t.strng(T,B,R,L) + "\n"
                    count = count + 1
                out.write("Face " + f.name + " contains "+ str(count) +" trapezoid(s):\n\n")  
                out.write(trapsonf)
        qp = input("Query point: ")
        while qp != 'x':
            xandy = qp.split()
            x = xandy[0][1:]
            x = x[:-1]
            y = xandy[1][:-1]
            point = [float(x),float(y)]
            obj = DAGTraversal(dag,point)
            if type(obj) == trapnode:
                print("Trapezoid containing the point"+ qp +":\n")
                print(obj.trap.strng(T,B,R,L) + "\n")
            elif type(obj) == vertnode:
                print("Vertex of the input subdivision:\n")
                print(obj.vert)
                print("\n")
            elif type(obj) == edgenode:
                print("On an edge of the input subdivision:\n")
                print(obj.edge.tophe)
                print("\n")
            qp = input("Query point: ")
        print("End of all queries in this map.\n\n\n")
        numtrials = numtrials + 1
        print("Trial " + str(numtrials) + ":\n")
        fname = input("Name of the input planar subdivision file: ")
from sage.all import *
from classes.coordinates import TableauColumn
from sage.interfaces.four_ti_2 import four_ti_2 as fti

class FlagVariety:
    '''
    shape is the column shape of first graded component of ring of T-invariants.
    assuming column strictly increasing
    '''
    def __init__(self,shape,n,coordinates):
        def _try_correct_data():
            if n<=0:
                raise ValueError("Invalid n.")

            for i in range(len(shape)-1):
                if shape[i]<shape[i+1] or shape[i]<=0 or shape[i] > n:
                    raise ValueError("invalid shape")
            if shape[-1]<=0 or shape[-1] > n:
                raise ValueError("invalid shape")

            res1 = dict.fromkeys(shape)

            for key in res1.keys():
                res1[key] = []

            for p in coordinates:
                p = TableauColumn(p)
                if len(p) in shape:
                    p.sort_()
                    if p[-1]>n:
                        raise ValueError("one of the entry in column is bigger than n.")
                    try:
                        res1[len(p)].index(p)
                    except ValueError:
                        res1[len(p)].append(p)
                else:
                    raise ValueError("Invalid data")

            for key in res1.keys():
                res1[key].sort(key=list)

            return res1

        def _sage_poset():
            B = self.coordinates
            mat = matrix([[Integer(p1<=p2) for p2 in B] for p1 in B])
            return sage.combinat.posets.posets.FinitePoset(DiGraph(mat).transitive_reduction())

        def _get_shape_r():
            l=[]
            tshape = deepcopy(shape)
            while(tshape != []):
                l.append(len(tshape))
                tshape = [item-1 for item in tshape if item!=1]
            return l

        def set_coordinate_names():
            for i in range(len(self.coordinates)):
                self.coordinates[i].name="p_{"+str(i)+"}"

        self.coordinate_dict = _try_correct_data()
        self.n = n
        #self.d require correct place to put. Here we ment to implement general line bundle but in that case self.d need not be integer. This psrameter is set assuming this class will be used in only t-invariant computation purpose. There this is indeed true that number of boxes in shape are divisible by 1.
        self.d = int(sum(shape)/n)
        self.shape = deepcopy(shape)
        self.shape_row = _get_shape_r()
        self.coordinates = [x for key in sorted(list(self.coordinate_dict),reverse=True) \
                                                    for x in self.coordinate_dict[key]]
        self.bo_poset = _sage_poset()
        set_coordinate_names()


    '''
    shape is column shape of first graded component of ring of T invariants.
    column strictly increasing tableaux. keep function is used to get subvarieties
    by putting some coordinate equal to 0, like schubert variety,
    richardsons variety, chain variety, etc
    '''
    @staticmethod
    def _get_flag_variety(shape,n,keep=(lambda z:True)):
        if n == 0:
            n = sum(shape)
        coords=[]
        coords1=[]
        for key in (dict.fromkeys(shape)).keys():
            coords = coords+[(t.conjugate())[0] for t in SemistandardTableaux([1]*key,max_entry=n)]
        for p in coords:
            if keep(p):
                coords1.append(p)
        return FlagVariety(shape,n,coords1)

    def __eq__(self,other):
        #raise NotImplementedError("== operator is not implemented for flag varieties")
        if not(isinstance(other,FlagVariety)) :
            raise TypeError("Expected instance of FlagVariety.")
        if self.shape != other.shape or self.n != other.n or len(self)!=len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True

    def get_nc_pairs(self):
        '''returns list of noncomparable pairs'''
        res = []
        for i in range(len(self)):
            for j in range(i+1,len(self)):
                if self[i].is_nc(self[j]):
                    res = res + [[self[i],self[j]]]
        return res

    def nc_pair_iterator(self):
        '''Experimental: return iterator for noncomparable pairs'''
        return VarietyNCPairIterator(self)

    def indicator_matrix(self):
        '''
        return matrix indexed by set [1..n] X self.coordinates.
        For p in self.coordinates, column p of matrix is
        indicator vector of coordinate p in set [1..n]
        '''
        return matrix([p.indicator_vector(self.n) for p in self]).transpose()

    def shape_matrix(self):
        '''
        return matrix indexed by [1..l] X self.coordinates,
        where (a_1,...,a_l) are distinct entries in self.shape in strictly decreasing order.
        For i in [1..l] and p in self.coordinates, the entry (i,p) is 1 if len(p) = a_i.
        it is 0 otherwise.
        '''
        l = list(dict.fromkeys(self.shape))
        l.sort(reverse=True)
        m = matrix([[0]*len(self.coordinates)]*len(l))

        for i in range(len(self.coordinates)):
            j = l.index(len(self.coordinates[i]))
            m[j,i]=1
        return m

    def get_augment_indicator_vector(self):
        '''
        Augment indicator vector is v = [-1,..,-1]. n-dimentional.
        '''
        r = int(sum(self.shape)/self.n)
        v = vector([-r]*self.n)
        if sum(self.shape)+sum(v)!=0:
            print("shape cannot be shape of first graded component. cannot compute augment vector.")
            return None
        return v

    def get_augment_shape_vector(self):
        '''
        Augment shape vector is w = (-r_1,...,-r_l) such that self.shape = [a_1^{r_1},...,a_l^{r_l}]
        '''
        l = list(dict.fromkeys(self.shape))
        l.sort(reverse=True)
        w = [0]*len(l)
        for i in range(len(l)):
            w[i]=-1*self.shape.count(l[i])
        return vector(w)

    def get_augmented_indicator_matrix(self):
        '''
        return augmented indicator matrix.
        '''
        v = self.get_augment_indicator_vector()
        m = self.indicator_matrix()
        return m.augment(v)

    def get_augmented_shape_matrix(self):
        '''
        return augmented indicator matrix.
        '''
        w = self.get_augment_shape_vector()
        m = self.shape_matrix()
        return m.augment(w)

    def get_augmented_matrix(self):
        '''
        return augmented matrix.
        '''
        m1 = self.get_augmented_indicator_matrix()
        m2 = self.get_augmented_shape_matrix()
        return block_matrix([[m1],[m2]],subdivide=True)

    def print_poset(self,size=9):
        p = self.bo_poset.plot(element_labels={i:self.coordinates[i] for i in range(len(self))},\
                               element_color="white",element_shape="|", figsize=size,element_size=800)
        return p
    def is_zero(self,p):
        return self.is_point(p)
    def is_point(self,p):
        return self.coordinates == []
    def __bool__(self):
        return not(self.is_zero())
    def __iter__(self):
        return VarietyIterator(self)
    def __getitem__(self,key):
        if key < len(self):
            return self.coordinates[key]
        raise IndexError
    def __setitem__(self,key,value):
        raise AttributeError("cannot write")
    def __len__(self):
        return len(self.coordinates)
    def __str__(self):
        return "Flag Variety on coordinates \n"\
                    +str(block_matrix([[column_matrix(range(1,self.n+1)),self.indicator_matrix()]]))

    def __repr__(self):
        return "Flag Variety on coordinates \n"\
                    +str(block_matrix([[column_matrix(range(1,self.n+1)),self.indicator_matrix()]]))
    def __contains__(self,item):
        return item in self.coordinates

#===============================LATEX START======================
    def latex_m(self,fname=None):
        T = Tableau(self.coordinates)
        T = T.conjugate()
        first = "\\begin{array}[c]{*{"+str(len(T[0]))+"}c}\\cline{1-"+str(len(T[0]))+"}"
        last = '\\end{array}\n'
        latexx = latex(T).splitlines()
        latexx.pop(0)
        latexx.pop()
        latexx[0]=first
        latexx[-1]=last

        latexx = "\n".join(latexx)
        if fname==None:
            return latexx
        latexx = "\\[\n"+latexx+"\n\\]"
        f = open(fname,"w")
        f.write(latexx)
        f.close()
        return

    def latex_matrix(self,aug=False,shape=False,chain=None,fname=None):
        A = None
        if aug:
            A = self.get_augmented_indicator_matrix()
        elif shape:
            A = self.get_augmented_shape_matrix()
        else:
            print("One of aug or shape is required")
            return
        if chain != None:
            C = (self.bo_poset.maximal_chains())[chain]
            A = A.matrix_from_columns(C+[len(self)])

        if fname == None:
            return latex(A)

        latexx = "\\[\n"+latex(A)+"\n\\]"
        f = open(fname,"w")
        f.write(latexx)
        f.close()
        return

    def latex_chain(self,chain,seperator="\\le\n",fname=None):
        T = [self.coordinates[i] for i in chain]
        first = "\\begin{array}[c]{*{"+str(len(T[0]))+"}c}\\cline{1-"+str(len(T[0]))+"}"
        last = '\\end{array}'
        res = ""
        for i in chain:
            res = res+ seperator + self.coordinates[i].latex_m()
        latexx = res
        if fname==None:
            return latexx
        latexx = "\\[\n"+res+"\n\\]"
        f = open(fname,"w")
        f.write(latexx)
        f.close()
        return

class VarietyIterator:
    def __init__(self,variety):
        self.variety = variety
        self._index = 0
    def __next__(self):
        if self._index < len(self.variety):
            self._index = self._index+1
            return self.variety[self._index-1]
        raise StopIteration

class VarietyNCPairIterator:
    def __init__(self,variety):
        self.variety = variety
        self._i = (0,1)
    def __next__(self):
        while self._i[0] < (len(self.variety)-1):

            i,j = self._i[0],self._i[1]

            self._i[1] = self._i[1]+1
            if (self._i[1]) == len(self.variety):
                self._i[0] = self._i[0]+1
                self._i[1] = self._i[0]+1

            if self.variety[i].is_nc(self.variety[j]):
                return [self.variety[i],self.variety[j]]

        raise StopIteration

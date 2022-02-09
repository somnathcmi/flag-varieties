from sage.all import *

class TableauColumn:

    def __init__(self,p,name="p"):
        def check_errors():
            if len(p) == 0:
                raise ValueError("List should be nonempty.")
            for i in range(len(p)):
                if p[i] <= 0:
                    raise ValueError("List should contain positive integers.")

        p = list(p)
        check_errors()
        self.p = p
        self.name = name
    def is_zero(self):
        '''check if two entries of column are equal, then column is zero.'''
        p = list(self)
        p.sort()
        for i in range(1,len(p)):
            if p[i] == p[i-1] :
                return True
        return False

    def __eq__(self,other):
        '''check if two columns are equal upto reordering'''
        if not(isinstance(other,TableauColumn)):
            raise TypeError("Expected instance of TableauColumn class")
        p1 = list(self)
        p2 = list(other)
        p1.sort()
        p2.sort()
        return p1 == p2

    def __le__(self,other):
        '''check self<=other under bruhat order upto reordering columns'''
        if not(isinstance(other,TableauColumn)):
            raise TypeError("Expected instance of PluckCoordinate.")
        p1 = list(self)
        p2 = list(other)
        p1.sort()
        p2.sort()

        l = len(p2)
        if len(p1)>=l:
            for i in range(l) :
                if p1[i]>p2[i] :
                    return False
            return True
        return False
    def __lt__(self,other):
        '''check self<other under bruhat (strict)order upto reordering columns'''
        if self <= other and self != other:
            return True
        return False

    def is_nc(self,other):
        '''check whether columns are comparable or not under bruhat order'''
        if self <= other or other <= self:
            return False
        return True

    def indicator_vector(self,n):
        '''return set indicator vector of self in set {1,...,n}'''
        if n < max(self):
            raise ValueError("Expected n > max(self.p)")
        if self.is_zero():
            raise ValueError("Expected nonzero column.")

        v = [0]*n
        for i in self.p:
            v[i-1] = 1
        return vector(v)

    def sort_(self):
        '''sort the column and return sign of permutation, used to sort self'''
        l = len(self)
        q = list(self)
        coef = 1
        for i in range(l):
            for j in range(l-i-1):
                if q[j] > q[j+1]:
                    q[j],q[j+1] = q[j+1],q[j]
                    coef = -1*coef
        self.p.sort()
        return coef
    def matrix_(self):
        '''column matrix representation of column self'''
        return column_matrix(self)
    def __bool__(self):
        return not(self.is_zero())
    def __iter__(self):
        return TableauColumnIterator(self)
    def __len__(self):
        return len(self.p)
    def __getitem__(self,key):
        if key < len(self):
            return self.p[key]
        raise IndexError
    def __setitem__(self,key,value):
        raise AttributeError("cannot modify column via [] operator.")
    def tex(self):
        return self.name
    def __repr__(self):
        return str(self.p)
    def __str__(self):
        return str(self.p)

    @staticmethod
    def convert_cols_(mat):
        '''convert matrix columns to tableau columns'''
        l = [TableauColumn(x) for x in mat.columns()]
        return l

    def latex_m(self,fname=None):
        T = Tableau([self.p])
        T = T.conjugate()
        first = "\\begin{array}[c]{*{"+str(len(T[0]))+"}c}\\cline{1-"+str(len(T[0]))+"}"
        last = '\\end{array}'
        latexx = latex(T).splitlines()
        latexx.pop(0)
        latexx.pop()
        latexx[0]=first
        latexx[-1]=last

        latexx =  "\n".join(latexx)
        if fname==None:
            return latexx
        latexx = "\\[\n"+latexx+"\n\\]"
        f = open(fname,"w")
        f.write(latexx)
        f.close()
        return

class TableauColumnIterator:

    def __init__(self,column):
        self.column = column
        self._index = 0
    def __next__(self):
        if self._index < len(self.column):
            self._index = self._index+1
            return self.column[self._index-1]
        raise StopIteration


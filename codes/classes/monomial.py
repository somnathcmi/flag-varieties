from sage.all import *
from classes.coordinates import TableauColumn
from classes.variety import FlagVariety

class TableauMonomial:
    @staticmethod
    def _try_correct_data1(variety1,coef1,coords1,vec1):
        cres = []
        vres = len(variety1)*[0]
        if coef1 == 0:
            return (0,cres,vector(vres))
        if (coords1 == None and vec1 == None) or not(isinstance(variety1, FlagVariety)):
            raise ValueError("invalid data")
        elif vec1 == None:
            for p in coords1:
                p = TableauColumn(list(p))
                if p not in variety1 or p.is_zero():
                    return (0,[],vector(vres))
                coef1 = coef1*p.sort_()
                cres.append(p)
            for i in range(len(vres)):
                vres[i] = cres.count(variety1[i])
        else:
            if len(vec1)!= len(variety1):
                raise ValueError("Invalid monomial vector")
            for i in vec1:
                if i < 0:
                    raise ValueError("Invalid monomial vector")
            vres = deepcopy(vec1)
        cres = []
        for i in range(len(vres)):
            cres = cres + [variety1[i]]*Integer(vres[i])
        '''
        shape verification fails for tableau relation so not doing it.
        mat = variety1.shape_matrix()
        shape = mat*vector(vres)
        v = variety1.get_augment_shape_vector()
        d = int(shape[0]/v[0])
        if (shape-d*v) != 0:
            print(shape)
            print(d)
            print(v)
            print(cres)
            raise ValueError("shape do not satisfy criteria")
        '''
        return (coef1,cres,vector(vres))
    def __init__(self,variety,coef=1,coords=None,vec=None,tableau_name="t"):

        (self.coef,self.coords,self.vec) \
                = TableauMonomial._try_correct_data1(variety,coef,coords,vec)
        self.variety = variety
        self.tableau_name=tableau_name

    def tex(self):
        coef = ""
        if abs(self.coef)!=1:
            coef = "+"+str(abs(self.coef)) if self.coef >= 0 else "-"+str(abs(self.coef))
        else:
            coef = "+" if self.coef >= 0 else "-"
        return coef+self.tableau_name


    def __eq__(self,other):
        '''self == other iff self-other = 0'''
        if not(isinstance(other,TableauMonomial)):
            raise TypeError("Expected instance of class PluckMonomial")
        if any([self.coef!=other.coef, self.variety!=other.variety, \
                                        len(self)!=len(other), self.vec!=other.vec]):
            return False
        return True

    def __mul__(self,other):
        if not(isinstance(other,TableauMonomial)):
            raise TypeError("Expected instance of PluckMonomial")
        if self.variety == other.variety:
            return TableauMonomial(self.variety,self.coef*other.coef,vec=(self.vec+other.vec),\
                                   tableau_name=self.tableau_name+other.tableau_name)
        raise ValueError("cannot multiply, variety is not same")

    def __neg__(self):
        return TableauMonomial(self.variety,-self.coef, vec=self.vec,tableau_name=self.tableau_name)

    def get_nc_pair(self):
        '''if monomial is not standatd then return first noncomparable pair'''
        tcols = self.coords
        tl = len(tcols)
        ti = 0
        if tl <= 1:
            return None
        while tcols[ti] <= tcols[ti+1]:
            if ti+2 == tl:
                return None
            ti=ti+1
        return (tcols[ti],tcols[ti+1])

    def indicator_matrix(self):

        l = list(self)
        if self.coef == 0:
            return None
        m = [l[0].indicator_vector(self.variety.n)]
        for i in range(1,len(l)):
            v = l[i].indicator_vector(self.variety.n)
            try:
                m.index(v)
            except:
                m.append(v)
        return matrix(m).transpose()

    def weight(self):
        m = self.variety.indicator_matrix()
        v = self.vec
        return m*v

    def deepcopy(self):
        return TableauMonomial(self.variety,self.coef,vec=self.vec,tableau_name=self.tableau_name)

    def __iter__(self):
        return TableauMonomialIterator(self)

    def __len__(self):
        return len(self.coords)

    def __getitem__(self,key):
        if key >= len(self.coords):
            raise IndexError
        return self.coords[key]
    def __setitem__(self,key,value):
        raise AttributeError("read only")

    def __line_list__(self):
        nn = len(self.coords)
        mm = Tableau([list(p) for p in self.coords]).conjugate()

        coef = " + "+str(abs(self.coef)) if self.coef >= 0 else " - "+str(abs(self.coef))
        spaces = " "*len(str(coef))

        lines = []
        for i in range(len(mm)):
            l = "["+str(" ".join(str(x) for x in list(mm[i])+[" "]*(nn-len(mm[i])) ))+"]"
            lines = lines+([coef+l] if i == int(len(mm)/2) else [spaces+l])
        return lines

    def __repr__(self):
        return str(self)
    def __str__(self):
        return "\n"+"\n".join(x for x in self.__line_list__())
    def __contains__(self,item):
        return item in self.coords
    def __bool__(self):
        return self.coef != 0

#==================================Latex=================================

    def latex_m(self,poly=False,fname=None,mode="a"):
        T = Tableau(self.coords)
        T = T.conjugate()
        coef=""
        if poly:
            cabs = str(abs(self.coef)) if abs(self.coef)!=1 else ""
            coef = "+"+cabs if self.coef>=0 else "-"+cabs
        first = coef + "\\begin{array}[c]{*{"+str(len(T[0]))+"}c}\\cline{1-"+str(len(T[0]))+"}"
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
        f = open(fname,mode)
        f.write(latexx)
        f.close()
        return


class TableauMonomialIterator:

    def __init__(self,monomial):
        self._index = 0
        self.monomial = monomial
    def __next__(self):
        if self._index < len(self.monomial):
            self._index = self._index+1
            return self.monomial[self._index-1]
        raise StopIteration


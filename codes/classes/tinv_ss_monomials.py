from sage.all import *
from sage.interfaces.four_ti_2 import four_ti_2 as fti
from classes.coordinates import TableauColumn
from classes.variety import FlagVariety
from classes.tinv_monomial import TInvariantMonomial

class TInvariantSemistandardMonomials:
    def __init__(self,variety,degree=None,monomials=None,var_name="t"):
        if degree == None and monomials == None:
            raise ValueError
        self.variety = variety
        if monomials != None:
            print("error check on input monomial is not done")
            self.monomials = monomials
            for i in range(len(self.monomials)):
                if self.monomials[i].tableau_name == "t":
                    self.monomials[i].tableau_name = var_name+"_{"+str(i)+"}"
        else:
            row_shape = [degree*x for x in variety.shape_row]
            '''d is such that weight = d*bar{1}. d and degree do not mathc for grassmannian.'''
            d = sum(row_shape)/variety.n
            '''divide all boxes equally in n numbers for equal filling to get weight.'''
            weight = [int(d)]*variety.n
            if sum(row_shape) != sum(weight):
                raise ValueError("possibly t invariant do not exist.")
            Ts = SemistandardTableaux(row_shape,weight)
            monomial_list=[TInvariantMonomial(variety,coef=1,coords=Ts[i].conjugate(),\
                                tableau_name=var_name+"_{"+str(i)+"}") for i in range(len(Ts))]
            self.monomials = [m for m in monomial_list if m.coef!=0]

    def __iter__(self):
        return TInvariantSemistandardMonomialsIterator(self)
    def __len__(self):
        return len(self.monomials)
    def __getitem__(self,key):
        if key >= len(self.monomials):
            raise IndexError
        return self.monomials[key]
    def __repr__(self):
        return str(self)
    def __str__(self):
        return str(self.monomials)
    def __contains__(self,item):
        return item in self.monomials
    def __bool__(self):
        raise NotImplementedError
        return self.monomials != []

    def latex_m(self,var = 't',fname=None):
        s = [h.latex_m() for h in self]
        latexx=""
        sp = '20px'
        for i in range(len(s)):
            latexx = latexx + var+"_{"+str(i)+"}&="+s[i]+"\\hspace{"+sp+"}"
        if fname==None:
            return latexx
        f = open(fname,"w")
        f.write(latexx)
        f.close()
        return

    def latex_m1(self,sublist=None,fname=None):
        latexx = ""
        seperator = ",\\ \n "
        if sublist == None:
            sublist = range(len(self))
        for i in sublist:
            m = self.monomials[i]
            latexx = latexx + seperator + m.latex_m()

        if fname==None:
            return latexx
        latexx = "\\[\n" + latexx + "\n\\]"
        f = open(fname,"w")
        f.write(latexx)
        f.close()
        return


class TInvariantSemistandardMonomialsIterator:

    def __init__(self,monomials):
        self._index = 0
        self.monomials = monomials
    def __next__(self):
        if self._index < len(self.monomials):
            self._index = self._index+1
            return self.monomials[self._index-1]
        raise StopIteration


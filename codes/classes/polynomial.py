from sage.all import *
from classes.coordinates import TableauColumn
from classes.variety import FlagVariety
from classes.monomial import TableauMonomial

class TableauPolynomial:
    def __init__(self,monomials):
        self.terms = []
        for monomial in monomials:
            TableauPolynomial._add_term(self,monomial)
        self._remove_zeros()

    def _remove_zeros(self):
        terms = self.terms
        self.terms = []
        for term in terms:
            if term.coef != 0:
                self.terms.append(term)

    @staticmethod
    def _add_term(poly,term):
        if not(isinstance(term,TableauMonomial)) or not(isinstance(poly,TableauPolynomial)):
            raise ValueError("invalid data")
        if term.coef == 0:
            return poly
        termcopy = term.deepcopy()
        for t in range(len(poly.terms)):
            if poly.terms[t].vec == termcopy.vec:
                #if poly.terms[t].variety == term.variety:
                poly.terms[t].coef = poly.terms[t].coef + termcopy.coef
                return poly
        poly.terms.append(termcopy)
        return poly

    def __eq__(self,other):
        raise NotImplementedError
    def __mul__(self,other):
        if not(isinstance(other,TableauPolynomial)):
            raise ValueError("Expected instance of TableauPolynomial class.")
        res = []
        for m1 in other:
            for m2 in self:
                res.append(m1*m2)
        return TableauPolynomial(res)
    def __add__(self,other):
        if not(isinstance(other,TableauPolynomial)):
            raise ValueError("Expected instance of TableauPolynomial class.")
        res = TableauPolynomial(self.terms)
        for term in other:
            TableauPolynomial._add_term(res,term)
        res._remove_zeros()
        return res
    def __sub__(self,other):
        return self + (-other)
    def __neg__(self):
        ms = []
        for m in self:
            ms.append(-m)
        return TableauPolynomial(ms)

    def get_nc_pair(self):#return one nc pair in polynomial if present else return None
        for i in range(len(self)):
            nc_pair = self[i].get_nc_pair()
            if nc_pair != None:
                return (i,nc_pair)
        return (None,None)

    def __iter__(self):
        return TableauPolynomialIterator(self)
    def __len__(self):
        return len(self.terms)
    def __getitem__(self,key):
        if isinstance(key,slice):
            return self.terms[key]
        if key >= len(self):
            raise IndexError
        return self.terms[key]
    def __setitem__(self,key,value):
        raise AttributeError("read only")
    def tex(self):
        return "".join(x.tex() for x in self)
    def __line_list__(self):
        if self.terms == []:
            return []
        lines = [m.__line_list__() for m in self]
        res = []
        for i in range(len(lines[0])):
            line = ""
            for j in range(len(lines)):
                line = line+lines[j][i]
            res = res + [line]
        return res
    def __str__(self):
        return "\n".join(x for x in self.__line_list__())
    def __repr__(self):
        return str(self)+"\n"
    def __contains__(self,item):
        return item in self.terms
    def __bool__(self):
        return len(self) != 0
#====================================Latex=================================
    def latex_m(self,fname=None,mode="a"):
        latexx = ''
        for term in self.terms:
            latexx = latexx + term.latex_m(poly=True)
        if fname==None:
            return latexx
        latexx = "\\[\n"+latexx+"\n\\]"
        f = open(fname,mode)
        f.write(latexx)
        f.close()
        return

class TableauPolynomialIterator:

    def __init__(self,poly):
        self._index = 0
        self.poly = poly
    def __next__(self):
        if self._index < len(self.poly):
            self._index = self._index+1
            return self.poly[self._index-1]
        raise StopIteration

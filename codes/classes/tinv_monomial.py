from sage.all import *
from sage.interfaces.four_ti_2 import four_ti_2 as fti
from classes.coordinates import TableauColumn
from classes.variety import FlagVariety
from classes.monomial import TableauMonomial

class TInvariantMonomial(TableauMonomial):
    '''
    degree is d if monomial is in d'th graded component of ring of T invariants
    '''
    def __init__(self,variety,coef=1,coords=None,vec=None,monomial=None,tableau_name=None):
        if monomial is not None:
            coef = monomial.coef
            vec = monomial.vec
            coords = monomial.coords
        super().__init__(variety,coef,coords = coords,vec = vec,tableau_name = tableau_name)
        w = super().weight()
        for x in w:
            if x != w[0]:
                raise ValueError("Not invariant monomial")
        if not((w[0]/self.variety.d).is_integer()):
                raise ValueError("number of boxes in first graded component are not multiple of n. so shape cannot be first graded component of ring of invariants.")
        self.degree = int(w[0]/self.variety.d)

    def factor_(self,verbose=False):
        l = list(self)
        if l == []:
            return (self,None)
        v = [1]
        m = [l[0].indicator_vector(self.variety.n)]
        ll = [l[0]]
        for i in range(1,len(l)):
            if l[i] == l[i-1]:
                v[-1] = v[-1]+1
            else:
                v.append(1)
                m.append(l[i].indicator_vector(self.variety.n))
                ll.append(l[i])
        m = matrix(m).transpose()
        m = m.augment(vector([-self.variety.d]*self.variety.n))
        ub = deepcopy(v)
        v.append(self.degree)
        ub.append(floor(self.degree/2))
        v = vector(v)
        ub = vector(ub)
        if verbose:
            print("vector to factor: "%v)
            print("upperbound for factorization algo: " % ub)
        proj = fti.temp_project()
        fti.write_matrix(m,proj+".mat")
        fti.write_matrix(ub,proj+".ub")
        fti.call(command="hilbert",project=proj,verbose=False)
        hb = fti.read_matrix(proj+".hil")
        if hb.nrows() == 0:
            return (self,None)

        h1 = hb[0]
        h2 = list(v - h1)
        if verbose:
            print("first factor: " %h1)
            print("second factor: " %h2)
        h1coords = []
        h2coords = []
        for i in range(len(ll)):
            h1coords = h1coords + [ll[i]]*h1[i]
            h2coords = h2coords + [ll[i]]*h2[i]

        f1 = TableauMonomial(self.variety,self.coef,coords=h1coords)
        f2 = TableauMonomial(self.variety,1,coords=h2coords)
        return (f1,f2)


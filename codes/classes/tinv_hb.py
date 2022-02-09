from sage.all import *
import time
from sage.interfaces.four_ti_2 import four_ti_2 as fti
from classes.coordinates import TableauColumn
from classes.monomial import TableauMonomial
from classes.variety import FlagVariety

class FlagVarietyWithHBOfTInvariants(FlagVariety):

    def __init__(self,shape=None,n=0,coordinates=None,variety=None):
        if variety is not None:
            shape = variety.shape
            n = variety.n
            coordinates = variety.coordinates
        super().__init__(shape,n,coordinates)
        self.hb = None
        self.relations = None
        self.hb_factor_info = None
        self.hb_not_factored = None

    def compute_hb(self,deg=None,save_data=False,keep_chains=False,verbose=True,fname_prefix=None):
        """Compute vector representation of T invariant monomials of asked degree."""
        def expand_chain(hb,C):
            ll = len(self)
            if hb.nrows() == 0 or hb.ncols() == 0:
                return None

            t1 = list(hb)
            l = len(t1[0])
            for j in range(ll):
                if j not in C:
                    t1.insert(j,vector([0]*l))
            t1 = matrix(t1)
            if hb != t1.matrix_from_rows(C+[t1.nrows()-1]):
                print("expand_chain() Error: Cross verification failed.")
            return t1

        def print_chain_data(chain,Ac,hb,hb1):
            if verbose :
                print("Chain:")
                print(matrix([self.coordinates[i] for i in chain]).transpose())
                print("\nWeight Matrix")
                print(Ac)
                print("\nHilbert basis tableau and vector")
                #print(hb1)
                if hb!=None:
                    for j in range(hb.ncols()):
                        print(str(TableauMonomial(self,1,vec=hb.column(j)[:-1]))+","+str(hb1.column(j)))
                else: print("None")
                print("===============================================")
        def save_chain_data(chain_i,chain,Ac,hb,hb1):
            if save_data:
                if fname_prefix!=None:
                    f = open(fname_prefix+"chain_"+f"{i:03}",'w')
                    f.writelines("Chain:\n")
                    f.writelines(str(TableauMonomial(self,1,coords=[self.coordinates[i] for i in chain])))
                    f.writelines("\n\nWeight Matrix\n")
                    f.writelines(str(Ac))
                    f.writelines("\n\nHilbert basis tableau and vector")
                    #f.writelines(str(hb1))
                    if hb!=None:
                        for j in range(hb.ncols()):
                            f.writelines("\n"+str(TableauMonomial(self,1,vec=hb.column(j)[:-1]))+","+str(hb1.column(j)))
                    else: f.writelines("\nNone")
                    f.close()
                #print()

        if self.hb == None:
            chains = self.bo_poset.maximal_chains()
            A = self.get_augmented_matrix()
            HB = []

            for i in range(len(chains)):
                chain = chains[i]
                l = len(chain)
                print(f"{ceil((i/len(chains))*100):03}%\b\b\b\b",end="",flush=True)

                Ac = A.matrix_from_columns(chain)
                Ac = Ac.augment(A.column(-1))

                hb1 = (fti.hilbert(Ac)).transpose()
                #print(str(i)+":"+str(hb.dimensions()))
                hb = expand_chain(hb1,chain)
                print_chain_data(chain,Ac,hb,hb1)
                save_chain_data(i,chain,Ac,hb,hb1)
                if hb != None:
                    for v in hb.columns():
                        try:
                            HB.index(v)
                        except ValueError:
                            HB.append(v)
            self.hb = HB
            print("done hb")

        if deg == None:
            return self.hb
        res = []
        file_open=False
        if save_data:
            if fname_prefix==None:
                save_data = False
            else:
                f = open(fname_prefix+"hb_elem_deg_"+str(deg),'a')
                file_open=True
        for v in self.hb:
            if v[-1] == deg:
                res.append(v)
                if file_open:
                    f.writelines("\n"+str(TableauMonomial(self,1,vec=v[:-1])))
                if verbose:
                    print("\n"+str(TableauMonomial(self,1,vec=v[:-1])))
        if file_open:
            f.close()
        return res

    def hb_monomials(self,deg=None,save_data=False,keep_chains=False,verbose=True,fname_prefix=None):
        """Compute tableau representation of T invariant monomials of asked degree"""
        #begin = time.time()
        hb = self.compute_hb(deg,save_data,keep_chains,verbose,fname_prefix)
        #end = time.time()
        #print(f"Hilbert basis computation time: {end - begin}")
        return [TableauMonomial(self,1,vec=hb[i][:-1],tableau_name="t_{"+str(i)+"}") for i in range(len(hb))]


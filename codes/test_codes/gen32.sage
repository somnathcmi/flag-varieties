

#load("coordinates.py")
#load("variety.py")
#load("monomial.py")
#load("polynomial.py")
#load("plucker_relations.py")
load("classes/tinv_hb.py")
load("classes/straighten.py")
load("classes/tinv_ss_monomials.py")


FV32 = FlagVariety._get_flag_variety([3,2])
FV32HB = FlagVarietyWithHBOfTInvariants(variety=FV32)

T = TInvariantSemistandardMonomials(FV32,1) 
T2 = [(T[i]*T[j],i,j) for i in range(len(T)) for j in range(i,len(T))] 
nc = list(filter((lambda z:True if z[0].get_nc_pair()!=None else False),T2))
Algos = list(map((lambda z:(StraightenAlgo(z[0]),z[1],z[2])),nc))

for S in Algos: S[0].straighten()  
#for S in Algos: S[0].print_steps()  

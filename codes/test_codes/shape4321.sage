load("classes/tinv_hb.py")
load("classes/straighten.py")
load("classes/tinv_ss_monomials.py")

print("creating variety")
FV4321 = FlagVariety._get_flag_variety([4,3,2,1],n=5)
print("creating variety for invariants")
FV4321HB = FlagVarietyWithHBOfTInvariants(variety=FV4321)
print("computing HB")
HB4321 = TInvariantSemistandardMonomials(variety=FV4321,monomials=FV4321HB.hb_monomials(deg=1)) 
print("computinh products of HB")
Algos4321 = [(StraightenAlgo(HB4321[i]*HB4321[j]),i,j) for i in range(len(HB4321)) for j in range(i,len(HB4321))]
print("Straightenning")
for p in Algos4321: 
    print("%s,%s"%(p[1],p[2]))
    p[0].straighten()
print("Done")




#R132 = TInvariantSemistandardMonomials(variety=FV32,degree=1) 
#R232 = TInvariantSemistandardMonomials(variety=FV32,degree=2)
#R1R132 = [R132[i]*R132[j] for i in range(len(R132)) for j in range(i,len(R132))]
#R1R1NS32 = [s for s in R1R132 if s.get_nc_pair()!=None]


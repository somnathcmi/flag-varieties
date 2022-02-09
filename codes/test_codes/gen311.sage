load("classes/tinv_hb.py")
load("classes/straighten.py")
load("classes/tinv_ss_monomials.py")

FV311 = FlagVariety._get_flag_variety([3,1,1],n=5)
FV311HB = FlagVarietyWithHBOfTInvariants(variety=FV311)

HB311 = TInvariantSemistandardMonomials(variety=FV311,monomials=FV311HB.hb_monomials()) 

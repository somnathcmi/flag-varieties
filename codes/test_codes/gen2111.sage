load("classes/tinv_hb.py")
load("classes/straighten.py")
load("classes/tinv_ss_monomials.py")

FV2111 = FlagVariety._get_flag_variety([2,1,1,1],n=5)
FV2111HB = FlagVarietyWithHBOfTInvariants(variety=FV2111)

HB2111 = TInvariantSemistandardMonomials(variety=FV2111,monomials=FV2111HB.hb_monomials()) 

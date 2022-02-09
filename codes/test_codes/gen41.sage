load("classes/tinv_hb.py")
load("classes/straighten.py")
load("classes/tinv_ss_monomials.py")

FV41 = FlagVariety._get_flag_variety([4,1],n=5)
FV41HB = FlagVarietyWithHBOfTInvariants(variety=FV41)

HB41 = TInvariantSemistandardMonomials(variety=FV41,monomials=FV41HB.hb_monomials()) 

load("classes/tinv_hb.py")
load("classes/straighten.py")
load("classes/tinv_ss_monomials.py")

print("Get variety")
G37 = FlagVariety._get_flag_variety([3]*7,n=7)
print("get variety for HB calculations")
G37HB = FlagVarietyWithHBOfTInvariants(variety=G37)
print("calculate HB")
#HB37 = TInvariantSemistandardMonomials(variety=G37,monomials=G37HB.hb_monomials()) 
#HB372 = TInvariantSemistandardMonomials(variety=G37,monomials=G37HB.hb_monomials(deg = 2)) 
#HB373 = TInvariantSemistandardMonomials(variety=G37,monomials=G37HB.hb_monomials(deg = 3)) 

#Start printing data in file.
print("Start generating paper data")

prefix="generated_data/gr37/"

p = G37.print_poset(size=15)
p.save_image(filename=prefix+"bruhat_poset.png")



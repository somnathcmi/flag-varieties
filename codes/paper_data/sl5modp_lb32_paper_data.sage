
import os
import shutil

load("./classes/tinv_hb.py")
load("./classes/straighten.py")
load("./classes/tinv_ss_monomials.py")
load("./classes/apply_relation.py")


cwd = os.getcwd()
prefix = cwd+"/paper_data/generated_data/sl5modp_lb32/"
chains_data = prefix+"chains_data/"
hb_data = prefix+"hb_data/"
#factor_data_deg_3 = prefix+"factor_data/deg_21/"
#factor_data_deg_2 = prefix+"factor_data/deg_14/"


def create_directory_structure():
    try:
        shutil.rmtree(prefix)
    except Exception as e:
        print(f"message from shutil.rmtree: {e}")
    else:
        print(f"message from shutil.rmtree: success")

    try:
        os.makedirs(chains_data)
        os.mkdir(hb_data)
        #os.makedirs(factor_data_deg_3)
        #os.mkdir(factor_data_deg_2)
    except Exception as e:
        print (f"Creation of the directory failed. {e}")
        return False
    else:
        print ("Successfully created the directory structure")
        return True


def save_coordinates(variety,fname=""):
    if fname=="":
        return False

    f = open(fname,"w")
    m = variety.coordinates
    monomial = TableauMonomial(variety,1,coords=m)
    #print(monomial)
    f.writelines(str(monomial))
    f.close()
    return True

#===============================================================================================================
#===============================================================================================================

print("------------------- (SL(5,CC),L([3,2])) data generation started ------------------")

# set to tru if you want to save data  in files.
SAVE = True

if SAVE:
    if not(create_directory_structure()):
        SAVE = False


print("generating sl5modp variety object ")
Sl5ModP_LB32 = FlagVariety._get_flag_variety([3,2],n=5)

#===============================================================================================================
#===============================================================================================================

print("saving bruhat poset image")
p = Sl5ModP_LB32.print_poset(size=15)
p.save_image(filename=prefix+"bruhat_poset.png")

#===============================================================================================================
#===============================================================================================================

print("saving plucker coordinates")
save_coordinates(Sl5ModP_LB32,fname=prefix+"plucker_coordinates")

#===============================================================================================================
#===============================================================================================================

print("generating hb for each chain")
print("1. modifying variety object for hb calculations")
Sl5ModP_LB32_HB = FlagVarietyWithHBOfTInvariants(variety=Sl5ModP_LB32)

print("2. calculating hb")
#G37HB.hb = load(hb_data+"gr37hb.hb_vecs_list")
HBSl5ModP_LB32 = TInvariantSemistandardMonomials(variety=Sl5ModP_LB32,monomials=Sl5ModP_LB32_HB.hb_monomials(verbose = False,save_data=SAVE,fname_prefix=chains_data)) 
print("3. separating hb elements degree wise")
print("3.1. collecting degree 1 elements in hb")
HBSl5ModP_LB32_1 = TInvariantSemistandardMonomials(variety=Sl5ModP_LB32,monomials=Sl5ModP_LB32_HB.hb_monomials(deg = 1,verbose=False,save_data=SAVE,fname_prefix=hb_data)) 
t = HBSl5ModP_LB32_1
print("3.2. collecting degree 2 elements in hb")
HBSl5ModP_LB32_2 = TInvariantSemistandardMonomials(variety=Sl5ModP_LB32,monomials=Sl5ModP_LB32_HB.hb_monomials(deg = 2,verbose=False,save_data=SAVE,fname_prefix=hb_data)) 


#===============================================================================================================
#===============================================================================================================
#straigntenning
print("straightenning x1*x2")
x1 = HBSl5ModP_LB32_2[0]
x2 = HBSl5ModP_LB32_2[1]
SAlgo1 = StraightenAlgo(x1*x2)
SAlgo1.straighten()
#SAlgo1.print_steps()
#verify symbolic rep is correct
f1_monomials = [ t[1]*t[0]*t[3]*t[3], t[1]*t[0]*t[2]*t[3], t[1]*t[0]*t[4]*t[3], t[1]*t[0]*t[0]*t[3], t[1]*t[1]*t[0]*t[3] ]
f1_monomials[1].coef = -1
f1_monomials[2].coef = -1
f1_monomials[4].coef = -1
f1_manual = TableauPolynomial(f1_monomials)

#f1_manual_tex = 
#t_1t_0t_3^2 - t_1t_0t_2t_3 - t_1t_0t_4t_3 + t_1t_0^2t_3 - t_1^2t_0t_3 

print("verification result for f1 (Expected 0)")
print(f1_manual - SAlgo1.poly) # Expect 0 polynomial

print("straightenning t2*t4")
t2 = HBSl5ModP_LB32_1[2]
t4 = HBSl5ModP_LB32_1[4]
SAlgo2 = StraightenAlgo(t2*t4)
SAlgo2.straighten()
#SAlgo2.print_steps()
#verify
f2_monomials = [t[0]*t[3],t[1]*t[3],t[1]*t[2],t[1]*t[4],t[1]*t[0],t[1]*t[1] ]
f2_monomials[2].coef = -1
f2_monomials[3].coef = -1
f2_monomials[5].coef = -1

#f2_manual_tex = 
# -x_2 + t_0t_3 - x_1 + t_1t_3 - t_1t_2 - t_1t_4 + t_1t_0 - t_1^2

print("verification result for f2 (Expected -x_1-x_2)")
print(SAlgo2.poly - TableauPolynomial(f2_monomials)) #Expect -x1-x2 



print("------------------- (SL(5,CC),L([3,2])) data generation finished ------------------")

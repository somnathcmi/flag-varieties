
import os
import shutil

load("./classes/tinv_hb.py")
load("./classes/straighten.py")
load("./classes/tinv_ss_monomials.py")
load("./classes/apply_relation.py")


cwd = os.getcwd()
prefix = cwd+"/paper_data/generated_data/sl5modp_lb311/"
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

print("------------------- (SL(5,CC),L([3,1,1])) data generation started ------------------")

# set to tru if you want to save data  in files.
SAVE = True

if SAVE:
    if not(create_directory_structure()):
        SAVE = False


print("generating sl5modp variety object ")
Sl5ModP_LB311 = FlagVariety._get_flag_variety([3,1,1],n=5)

#===============================================================================================================
#===============================================================================================================

print("saving bruhat poset image")
p = Sl5ModP_LB311.print_poset(size=15)
p.save_image(filename=prefix+"bruhat_poset.png")

#===============================================================================================================
#===============================================================================================================

print("saving plucker coordinates")
save_coordinates(Sl5ModP_LB311,fname=prefix+"plucker_coordinates")

#===============================================================================================================
#===============================================================================================================

print("generating hb for each chain")
print("1. modifying variety object for hb calculations")
Sl5ModP_LB311_HB = FlagVarietyWithHBOfTInvariants(variety=Sl5ModP_LB311)

print("2. calculating hb")
#G37HB.hb = load(hb_data+"gr37hb.hb_vecs_list")
HBSl5ModP_LB311 = TInvariantSemistandardMonomials(variety=Sl5ModP_LB311,monomials=Sl5ModP_LB311_HB.hb_monomials(verbose = False,save_data=SAVE,fname_prefix=chains_data)) 
print("3. separating hb elements degree wise")
print("3.1. collecting degree 1 elements in hb")
HBSl5ModP_LB311_1 = TInvariantSemistandardMonomials(variety=Sl5ModP_LB311,monomials=Sl5ModP_LB311_HB.hb_monomials(deg = 1,verbose=False,save_data=SAVE,fname_prefix=hb_data)) 


print("------------------- (SL(5,CC),L([3,1,1])) data generation finished ------------------")
#===============================================================================================================
#===============================================================================================================

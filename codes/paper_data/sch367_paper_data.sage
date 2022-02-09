
import os
import shutil

load("./classes/tinv_hb.py")
load("./classes/straighten.py")
load("./classes/tinv_ss_monomials.py")
load("./classes/apply_relation.py")


cwd = os.getcwd()
prefix = cwd+"/paper_data/generated_data/sch367/"
chains_data = prefix+"chains_data/"
hb_data = prefix+"hb_data/"
#factor_data_deg_3 = prefix+"factor_data/deg_21/"
factor_data_deg_2 = prefix+"factor_data/deg_14/"


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
        os.makedirs(factor_data_deg_2)
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

print("------------------- X([3,6,7]) data generation started ------------------")

# set to tru if you want to save data  in files.
SAVE = True

if SAVE:
    if not(create_directory_structure()):
        SAVE = False


print("generating schubert variety [3,6,7] object ")
SCH367 = FlagVariety._get_flag_variety([3]*7,n=7,keep=(lambda z:TableauColumn(z) <= TableauColumn([3,6,7])))

#===============================================================================================================
#===============================================================================================================

print("saving schubert variety [3,6,7] bruhat poset image")
p = SCH367.print_poset(size=15)
p.save_image(filename=prefix+"bruhat_poset.png")

#===============================================================================================================
#===============================================================================================================

print("saveing plucker coordinates")
save_coordinates(SCH367,fname=prefix+"plucker_coordinates")

#===============================================================================================================
#===============================================================================================================

print("generating hb for each chain")
print("1. modifying variety object for hb calculations")
SCH367HB = FlagVarietyWithHBOfTInvariants(variety=SCH367)

print("2. calculating hb")
HBSCH367 = TInvariantSemistandardMonomials(variety=SCH367,monomials=SCH367HB.hb_monomials(verbose = False,save_data=SAVE,fname_prefix=chains_data)) 
print("3. separating hb elements degree wise")
print("3.1. collecting degree 1 elements in hb")
HBSCH367_1 = TInvariantSemistandardMonomials(variety=SCH367,monomials=SCH367HB.hb_monomials(deg = 1,verbose=False,save_data=SAVE,fname_prefix=hb_data)) 
print("3.2. collecting degree 2 elements in hb")
HBSCH367_2 = TInvariantSemistandardMonomials(variety=SCH367,monomials=SCH367HB.hb_monomials(deg = 2,verbose=False,save_data=SAVE,fname_prefix=hb_data)) 


print("------------------- X([3,6,7]) data generation finished ------------------")
#===============================================================================================================
#===============================================================================================================

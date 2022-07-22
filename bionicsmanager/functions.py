import json
import codecs
from os.path import exists
from os import remove
from tkinter import PhotoImage
from pathlib import Path
dir_root = Path(__file__).resolve().parent

# // Low level (for python standards lol) functions
def f_write(dir, dta):
    with codecs.open(dir, 'w', 'utf-8') as f_out: 
        f_out.write(json.dumps(dta, indent=4, separators=(",", ":")))

def f_read(dir):
    with codecs.open(dir, 'r', 'utf-8') as f_in:
        return json.loads(f_in.read())

def f_find(dir):
    return exists(dir)

def f_remove(dir):
    """-1: FileNotFoundError
 0: succesfully removed file
"""
    if not f_find(dir): return -1
    remove(dir)
    return 0

# // Helper functions
def h_parse_dir(stv):
    nme = stv.get().strip() + ".json"
    dir = dir_root / "instances" / nme
    return dir, nme

def h_tk_ss(state=str, disable=list):
    for widget in disable:
        widget["state"] = state.lower()

def h_icon_loader(name):
    return PhotoImage(file=dir_root / "icons" / name)

def h_percentage_fixer(decimal=float, n=2):
    'turns a decimal percentage into a normal percentage rounded to n (default 2) decimals. also removes cases like: "10.0"'
    percent = decimal*100

    if str(percent)[-2] == '.' and str(percent)[-1] == '0':
        percent = int(percent) #removes cases like: '10.0%' // this bug is still in python 3.10.4
    else: percent = round(percent, n)

    return percent

def h_calc_prog(dir):
    """return total, done, progress"""
    dta = f_read(dir)
    total = dta["info"]["total"]
    done = 0

    for cat in dta["bionics"]:
        for bnc in dta["bionics"][cat]:
            coeff = 1
            if bnc in dta["info"]["double"]:
                coeff = 2
            tot_bnc = dta["info"]["amount"]*coeff
            done += tot_bnc - dta["bionics"][cat][bnc]
    
    return total, done, h_percentage_fixer(done/total)

# // Goal specific functions
def c_create(dir, amount=int):
    """-1: instance with same name exists
 0: succesfully created new instance
"""
    if f_find(dir): return -1
    dta = f_read(dir_root / "cfg.json")
    dta["info"]["amount"] = amount
    dta["info"]["double"] = []

    total = 0
    for cat in dta["bionics"]:
        for bnc in dta["bionics"][cat]:
            coeff = 1
            if dta["bionics"][cat][bnc] == 2:
                dta["info"]["double"].append(bnc)
                coeff = 2
            dta["bionics"][cat][bnc] = dta["bionics"][cat][bnc]*amount
            tot_bnc = dta["info"]["amount"]*coeff
            total += tot_bnc
    dta["info"]["total"] = total

    f_write(dir, dta)
    return 0

def c_change(dir, bnc=str, amount=int):
    """-1: could not find bnc
 0: succesfully changed amount of bnc"""
    dta = f_read(dir)

    for cat in dta["bionics"]:
        if bnc in dta["bionics"][cat]:
            dta["bionics"][cat][bnc] = amount
            f_write(dir, dta)
            return 0
    return -1

#dir = dir_root / "TEST.json"
#c_create(dir, 12)
#dta = f_read(dir)
#for entry in dta["bionics"]["internal organs"]:
#    c_change(dir, entry, 0)
#print(h_update_progress(dir, 3,3))

#if __name__ == "__main__":
#    from time import sleep
#    dir_cfg = dir_root / "instances" / "TEST.json"
#    def test(result, expected):
#        if result == expected: return True
#        quit()
#    test(c_create(dir_cfg, 12), 0)
#    test(c_create(dir_cfg, 12), -1)
#    test(c_change(dir_cfg, "onerbatic disney", 38), -1)
#    test(c_change(dir_cfg, "energetic kidney", 5), 0)
#    test(c_change(dir_cfg, "energetic kidney", 0), 1)
#    test(c_change(dir_cfg, "energetic kidney", 0), 2)
#    test(c_change(dir_cfg, "energetic kidney", 5), 0)
#    test(f_remove(dir_cfg), 0)
#    test(f_remove(dir_cfg), -1)
#    print('Done')
import cmath
import math
import re
import pandas
import json

ACID_FILENAME = "acids.json"
BASE_FILENAME = "bases.json"

def quadratic_formula(a: float, b: float, c: float):
    determinate = (b**2) - 4*a*c

    sol1 = (-b + cmath.sqrt(determinate)) / (2*a)
    sol2 = (-b - cmath.sqrt(determinate)) / (2*a)
    return (sol1, sol2)

def find_hydrogen_ion_concentration(M, Ka):
    """
    X^2 + Ka*X - Ka*M = 0
    a = 1
    b = Ka
    c = -Ka*M
    """
    assert(Ka > 0)
    assert(M > 0)

    sol1, sol2 = quadratic_formula(1, Ka, -Ka*M)
    if sol1.imag == 0.0 and sol2.imag == 0.0:
        return max(sol1.real, sol2.real)
    elif sol1.imag == 0.0 and not sol2.imag == 0.0:
        return sol1.real
    elif not sol1.imag == 0.0 and sol2.imag == 0.0:
        return sol2.real
    else:
        return None
    
def find_ph(hydrogen_concentration):
    return -math.log10(hydrogen_concentration)

def scientific(num_str: str):
    # Remove whitespace
    while " " in num_str:
        idx = num_str.find(" ")
        num_str = num_str[0:idx] + num_str[idx+1:]

    sci_regex = re.compile(r"([0-9.]*)(\*10\^|\*?e\^)?([0-9.-]*)?")
    mo = sci_regex.match(num_str)

    if not mo:
        return None
    if mo.group(1) and not mo.group(3):
        return float(mo.group(1))

    coeff, mag = float(mo.group(1)), float(mo.group(3))
    return coeff * (10 ** mag)


def load_acids():
    with open(ACID_FILENAME) as f:
        data = json.load(f)
    return data

def load_bases():
    
    with open(BASE_FILENAME) as f:
        data = json.load(f)
    return data


def update_acid(formula, Ka):
    acids = load_acids()
    acids[formula] = Ka
    with open(ACID_FILENAME, 'w') as f:
        json.dump(acids, f)

def update_base(formula, Kb):
    bases = load_bases()
    bases[formula] = Kb
    with open(BASE_FILENAME, 'w') as f:
        json.dump(bases, f)



def main():
    ab = input("Acid or base?: ")
    if ab == "acid":
        acids = load_acids()

        formula = input("Enter formula: ")
        correct = False
        if formula in acids.keys():
            Ka = acids[formula]
            inp = input(f"Ka of {formula}: {Ka}. Correct? (y/n) ")
            if inp == "y":
                correct = True

        if not correct:
            Ka = input("Enter Ka: ")

        
        Ka_num = scientific(Ka)
        if not Ka_num:
            print("Invalid input")
            return
        M = (input("Enter M: "))
        M_num = scientific(M)
        if not M_num:
            print("Invalid input")
            return
        h_conc = find_hydrogen_ion_concentration(M_num, Ka_num)
        pH = find_ph(h_conc)
        print(f"pH: {pH}")

        update_acid(formula, Ka)
    elif ab == "base":
        bases = load_acids()

        formula = input("Enter formula: ")
        correct = False
        if formula in bases.keys():
            Kb = bases[formula]
            inp = input(f"Kb of {formula}: {Kb} Correct? (y/n) ")
            if inp == "y":
                correct = True

        if not correct:
            Kb = input("Enter Kb: ")

        
        Kb_num = scientific(Kb)
        if not Kb_num:
            print("Invalid input")
            return
        M = (input("Enter M: "))
        M_num = scientific(M)
        if not M_num:
            print("Invalid input")
            return
        h_conc = find_hydrogen_ion_concentration(M_num, Kb_num)
        pH = find_ph(h_conc)
        print(f"pH: {14-pH}")

        update_base(formula, Kb)
    else:
        print("Invalid input")
            
main()
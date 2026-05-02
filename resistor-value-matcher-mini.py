#  resistor set, "E24", "E96", "CUSTOM"
RESISTOR_SET = "CUSTOM"  
# ==================== target resistors ====================
targets = [
    144700,
    72300,
    36200,
    18100,
    9050,
    4520,
    2260,
    1130,
    565,
    10.001
]

def get_e24_resistors():

    E24_base = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
    values = [round(r * 10**e, 2) for e in range(-1, 7) for r in E24_base]
    return sorted(set(v for v in values if 0.1 <= v <= 10_000_000))

def get_e96_resistors():

    E96_base = [1.00,1.02,1.05,1.07,1.10,1.13,1.15,1.18,1.21,1.24,1.27,1.30,
                1.33,1.37,1.40,1.43,1.47,1.50,1.54,1.58,1.62,1.65,1.69,1.74,
                1.78,1.82,1.87,1.91,1.96,2.00,2.05,2.10,2.15,2.21,2.26,2.32,
                2.37,2.43,2.49,2.55,2.61,2.67,2.74,2.80,2.87,2.94,3.01,3.09,
                3.16,3.24,3.32,3.40,3.48,3.57,3.65,3.74,3.83,3.92,4.02,4.12,
                4.22,4.32,4.42,4.53,4.64,4.75,4.87,4.99,5.11,5.23,5.36,5.49,
                5.62,5.76,5.90,6.04,6.19,6.34,6.49,6.65,6.81,6.98,7.15,7.32,
                7.50,7.68,7.87,8.06,8.25,8.45,8.66,8.87,9.09,9.31,9.53,9.76]
    values = [round(v * 10**e, 3) for v in E96_base for e in range(-1, 7)]
    return [r for r in values if 0.1 <= r <= 10_000_000]

def get_custom_resistors():

    return [
        1, 10, 22, 47, 100, 150, 220, 470, 1000, 1200, 1800, 2000, 2200, 2400, 2700, 3300, 3900, 4700, 5600,
        6800, 8200, 9100, 10000, 15000, 20000, 22000, 27000, 33000, 39000,
        47000, 100000, 200000, 220000, 330000, 470000, 510000, 1000000
    ]

if RESISTOR_SET == "E24":
    standard_resistors = get_e24_resistors()

elif RESISTOR_SET == "E96":
    standard_resistors = get_e96_resistors()

else:
    standard_resistors = get_custom_resistors()


print(f"Selected: {RESISTOR_SET}")

def series(r1, r2):
    return r1 + r2


def parallel(r1, r2):
    return (r1 * r2) / (r1 + r2)


def find_best(target, resistors):
    best = None
    best_error = float('inf')
    best_type = ""
    best_pair = ()
    
    # single risistor
    for r in resistors:
        err_single = abs(r - target) / target
        if err_single < best_error:
            best_error = err_single
            best = r
            best_type = "single"
            best_pair = (r,)
    
    # series and parallel
    for i, r1 in enumerate(resistors):
        for r2 in resistors:
            # series
            s_val = series(r1, r2)
            err_s = abs(s_val - target) / target
            if err_s < best_error:
                best_error = err_s
                best = s_val
                best_type = "+"
                best_pair = (r1, r2)
            
            # parallel
            p_val = parallel(r1, r2)
            err_p = abs(p_val - target) / target
            if err_p < best_error:
                best_error = err_p
                best = p_val
                best_type = "//"
                best_pair = (r1, r2)
    
    return best, best_error, best_type, best_pair


# get 
if __name__ == "__main__":
    for i, target in enumerate(targets, start=1):
        best_val, error, typ, pair = find_best(target, standard_resistors)
    
        if typ == "single":
            print(f"No. {i} : target:{target} Ohm ")
            print(f"Best: {pair[0]} Ohm = {best_val:.3f} Ohm Single, Err= {error*100:.2f}%")
        else:
            print(f"No. {i} : target:{target} Ohm ")
            if typ == "+":
                print(f"Best: {pair[0]} + {pair[1]} = {best_val:.3f} Ohm, Err= {error*100:.2f}%")
            else:
                print(f"Best: {pair[0]} // {pair[1]} = {best_val:.3f} Ohm, Err= {error*100:.2f}%")
        print()

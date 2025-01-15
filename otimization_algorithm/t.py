import re 

filenames = ["sim_v166_h100_gam-6_p_0.77_D2_1.13_Ts_635.39", "sim_v166_h100_gam6_p_0.77_D2_1.13_Ts_635.39"]

for filename in filenames:
    gam_match = re.search(r"_gam(-?\d+)_", filename)
    h_match = re.search(r"h(\d+)", filename)
    # Extrair os valores com segurança e formato adequado
    gam = gam_match.group(1) if gam_match else None
    h = "h{}".format(h_match.group(1)) if h_match else None

    print(gam)
    print(h)
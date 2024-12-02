import re

# Formatear número en decenas de miles
def formatear_numero(numero, r=2):
    patron = r"(?<=\d)(?=(\d{3})+$)"
    g = numero.split(".")
    n = re.sub(patron, ",", g[0])
    num_formated = ".".join((n, "00"))
    return num_formated
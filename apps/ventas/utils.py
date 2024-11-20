import re

# Formatear número en decenas de miles
def formatear_numero(numero):
    patron = r"(?<=\d)(?=(\d{3})+$)"
    g = numero.split(".")
    n = re.sub(patron, ".", g[0])
    num_formated = ",".join((n, g[1]))
    return num_formated
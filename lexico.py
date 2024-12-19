def automata(cadena):
    estado = 0
    for carater in cadena:
        if estado == 0:
            if carater == 'm':
                estado = 1
            elif carater == 'h':
                estado = 2
            else:
                return False
        elif estado == 1:
            if carater == 'h':
                estado = 3
            elif carater == 'a':
                estado = 2
            else:
                return False
        elif estado == 2:
            if carater == 'm':
                estado = 1
            else:
                return False
        elif estado == 3:
            if carater == 'a':
                estado = 3
        else: 
            return False
    return estado in [2, 3]
ejemplos = ["mh", "mhaaaa", "h", "hma", "hmha", "hhhh"]

resultados = [cadena for cadena in ejemplos if automata(cadena)]

print("aceptadas:", resultados)
def automata(cadena):
    estado = 0
    for caracter in cadena:
        if estado == 0:
            if caracter == 'm':
                estado = 1
            elif caracter == 'h':
                estado = 2
            else:
                return False
        elif estado == 1:     
            if caracter =='a':
                estado = 3
            elif caracter == 'a':
                estado = 2
            else:
                return False
        elif estado == 2:
            if caracter == 'm':
                estado = 1
    return estado == 3

cadenas = ["mha", "mhaaa", "mhbbb"]
resultados = [cadena for cadena in cadenas if automata(cadena)]
print("Cadenas aceptadas", resultados)
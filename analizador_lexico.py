import re

# Definimos las expresiones regulares para los diferentes tipos de tokens
TOKEN_REGEX = [
    (r'\s+', None),  # Espacios en blanco (ignorarlos)
    (r'\{', 'LBRACE'),  # Llave izquierda
    (r'\}', 'RBRACE'),  # Llave derecha
    (r':', 'COLON'),  # Dos puntos
    (r',', 'COMMA'),  # Coma
    (r'"(\\.|[^"\\])*"', 'STRING'),  # Cadenas de texto
    (r'\d+(\.\d+)?', 'NUMBER'),  # Números (enteros y decimales)
    (r'true|false', 'BOOLEAN'),  # Booleanos
    (r'null', 'NULL'),  # Null
]

# Compilamos las expresiones regulares en un patrón
token_pattern = re.compile('|'.join(f'(?P<{name}>{pattern})' for pattern, name in TOKEN_REGEX if name))

def tokenize_with_nesting(json_string):
    tokens = {}  # Resultado final con anidaciones
    stack = [tokens]  # Pila para manejar contextos anidados
    current_key = None  # Clave actual en procesamiento

    for match in token_pattern.finditer(json_string):
        kind = match.lastgroup  # Tipo de token
        value = match.group()   # Valor del token

        if kind == 'STRING':
            if current_key is None:
                current_key = value.strip('"')  # Guardar como clave
            else:
                stack[-1][current_key] = value.strip('"')  # Asignar valor a la clave actual
                current_key = None  # Reiniciar clave
        elif kind == 'NUMBER':
            stack[-1][current_key] = float(value)  # Asignar número como valor
            current_key = None
        elif kind == 'BOOLEAN':
            stack[-1][current_key] = value == 'true'  # Asignar booleano como valor
            current_key = None
        elif kind == 'NULL':
            stack[-1][current_key] = None  # Asignar null como valor
            current_key = None
        elif kind == 'LBRACE':
            # Crear un nuevo contexto (diccionario anidado)
            new_context = {}
            if current_key is not None:
                stack[-1][current_key] = new_context  # Asignar el nuevo diccionario a la clave actual
                current_key = None
            stack.append(new_context)  # Añadir el nuevo contexto a la pila
        elif kind == 'RBRACE':
            stack.pop()  # Salir del contexto actual
        elif kind == 'COLON':
            continue  # Ignorar los dos puntos
        elif kind == 'COMMA':
            continue  # Ignorar las comas

    return tokens

# JSON de ejemplo con anidaciones
json_texto = '''
{
  "nombre": "Juan",
  "edad": 30,
  "direccion": {
    "calle": "Calle Falsa",
    "ciudad": "Springfield"
  },
  "activo": true
}
'''

# Analizar el JSON
resultado = tokenize_with_nesting(json_texto)
print(resultado)

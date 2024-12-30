import re
import json

# Definir los patrones para cada tipo de token
token_specification = [
    ('NUMBER',    r'\d+'),            # Números
    ('STRING',    r'"[^"]*"'),        # Cadenas de texto entre comillas
    ('LBRACE',    r'{'),              # Llave de apertura {
    ('RBRACE',    r'}'),              # Llave de cierre }
    ('LBRACKET',  r'\['),             # Corchete de apertura [
    ('RBRACKET',  r'\]'),             # Corchete de cierre ]
    ('COLON',     r':'),              # Dos puntos :
    ('COMMA',     r','),              # Coma ,
    ('ID',        r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identificadores (clave)
    ('SKIP',      r'[ \t\n\r]+'),     # Espacios en blanco
    ('MISMATCH',  r'.'),              # Cualquier otro carácter inesperado
]

# Compilar los patrones en una expresión regular
tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
get_token = re.compile(tok_regex).match

def lex(characters):
    position = 0
    tokens = []  # Lista para guardar los tokens

    while position < len(characters):
        match = get_token(characters[position:])
        if match:
            type_ = match.lastgroup
            value = match.group(type_)
            if type_ == 'SKIP':
                # Ignorar los espacios en blanco y saltos de línea
                pass
            elif type_ == 'MISMATCH':
                # Si encontramos un carácter inesperado, lanzar un error
                raise RuntimeError(f'Unexpected character: {value}')
            else:
                tokens.append((type_, value))  # Guardar token en la lista
            position += len(value)
        else:
            raise RuntimeError(f'Unexpected character at position {position}')
    
    return tokens  # Devolver la lista de tokens

# Ejemplo de uso
json_data = '''
{
  "id": "1",
  "nombre": "Juan",
  "direccion": {
    "calle": "Main St",
    "ciudad": "Madrid",
    "pais": "España"
  }
}
'''

# Ejecutar el analizador léxico y obtener los tokens
tokens = lex(json_data)

# Imprimir los tokens guardados
for token in tokens:
    print(token)

# Guardar los tokens en un archivo JSON
with open('tokens.json', 'w') as f:
    json.dump(tokens, f, indent=4)

print("Tokens guardados en 'tokens.json'")

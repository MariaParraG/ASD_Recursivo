"""
Análisis Sintáctico Descendente - ASD
Algoritmos: PRIMEROS, SIGUIENTES y PREDICCIÓN
Ejercicios 1 y 2 de la presentación

Convenciones:
  - Los no terminales son letras mayúsculas: S, A, B, C, D
  - Los terminales son en minúsculas: uno, dos, tres, cuatro, cinco, seis
  - 'ε' representa la cadena vacía (epsilon)
  - '$' representa el fin de entrada (usado en SIGUIENTES)
"""

EPSILON = 'ε'
END = '$'


# ─────────────────────────────────────────────
#  Utilidades generales
# ─────────────────────────────────────────────

def es_terminal(simbolo, no_terminales):
    return simbolo not in no_terminales and simbolo != EPSILON


def calcular_primeros(gramatica, no_terminales):
    """
    Calcula el conjunto PRIMEROS para cada no terminal.
    
    gramatica: dict  { 'A': [['B', 'C', 'D'], ['A', 'tres'], [ε]], ... }
    """
    primeros = {nt: set() for nt in no_terminales}

    def primeros_de_secuencia(secuencia):
        """PRIMEROS de una secuencia de símbolos."""
        resultado = set()
        for simbolo in secuencia:
            if simbolo == EPSILON:
                resultado.add(EPSILON)
                break
            if es_terminal(simbolo, no_terminales):
                resultado.add(simbolo)
                break
            # es no terminal
            p = primeros[simbolo]
            resultado |= (p - {EPSILON})
            if EPSILON not in p:
                break
        else:
            resultado.add(EPSILON)
        return resultado

    # Punto fijo
    cambio = True
    while cambio:
        cambio = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                nuevos = primeros_de_secuencia(prod)
                antes = len(primeros[nt])
                primeros[nt] |= nuevos
                if len(primeros[nt]) > antes:
                    cambio = True

    return primeros


def calcular_siguientes(gramatica, no_terminales, axioma, primeros):
    """
    Calcula el conjunto SIGUIENTES para cada no terminal.
    """
    siguientes = {nt: set() for nt in no_terminales}
    siguientes[axioma].add(END)

    def primeros_de_secuencia(secuencia):
        resultado = set()
        for simbolo in secuencia:
            if simbolo == EPSILON:
                resultado.add(EPSILON)
                break
            if es_terminal(simbolo, no_terminales):
                resultado.add(simbolo)
                break
            p = primeros[simbolo]
            resultado |= (p - {EPSILON})
            if EPSILON not in p:
                break
        else:
            resultado.add(EPSILON)
        return resultado

    cambio = True
    while cambio:
        cambio = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                for i, simbolo in enumerate(prod):
                    if simbolo not in no_terminales:
                        continue
                    beta = prod[i + 1:]
                    # PRIMEROS del resto de la producción
                    p_beta = primeros_de_secuencia(beta) if beta else {EPSILON}
                    antes = len(siguientes[simbolo])
                    # Añadir PRIMEROS(β) − {ε}
                    siguientes[simbolo] |= (p_beta - {EPSILON})
                    # Si ε ∈ PRIMEROS(β), añadir SIGUIENTES(cabeza)
                    if EPSILON in p_beta:
                        siguientes[simbolo] |= siguientes[nt]
                    if len(siguientes[simbolo]) > antes:
                        cambio = True

    return siguientes


def calcular_prediccion(gramatica, no_terminales, primeros, siguientes):
    """
    Calcula el conjunto PREDICCIÓN para cada producción.
    
    Retorna dict: { (NT, índice_producción): set }
    """
    prediccion = {}

    def primeros_de_secuencia(secuencia):
        resultado = set()
        for simbolo in secuencia:
            if simbolo == EPSILON:
                resultado.add(EPSILON)
                break
            if es_terminal(simbolo, no_terminales):
                resultado.add(simbolo)
                break
            p = primeros[simbolo]
            resultado |= (p - {EPSILON})
            if EPSILON not in p:
                break
        else:
            resultado.add(EPSILON)
        return resultado

    for nt, producciones in gramatica.items():
        for idx, prod in enumerate(producciones):
            p = primeros_de_secuencia(prod)
            pred = p - {EPSILON}
            if EPSILON in p:
                pred |= siguientes[nt]
            prediccion[(nt, idx)] = pred

    return prediccion


def imprimir_resultados(nombre, gramatica, no_terminales, axioma):
    print("=" * 60)
    print(f"  {nombre}")
    print("=" * 60)

    # Gramática
    print("\nGramática:")
    for nt, prods in gramatica.items():
        for prod in prods:
            rhs = ' '.join(prod)
            print(f"  {nt} → {rhs}")

    primeros   = calcular_primeros(gramatica, no_terminales)
    siguientes = calcular_siguientes(gramatica, no_terminales, axioma, primeros)
    prediccion = calcular_prediccion(gramatica, no_terminales, primeros, siguientes)

    # PRIMEROS
    print("\nConjuntos PRIMEROS:")
    for nt in no_terminales:
        p = sorted(primeros[nt], key=lambda x: (x == EPSILON, x))
        print(f"  PRIMEROS({nt}) = {{ {', '.join(p)} }}")

    # SIGUIENTES
    print("\nConjuntos SIGUIENTES:")
    for nt in no_terminales:
        s = sorted(siguientes[nt], key=lambda x: (x == END, x))
        print(f"  SIGUIENTES({nt}) = {{ {', '.join(s)} }}")

    # PREDICCIÓN
    print("\nConjuntos PREDICCIÓN:")
    for nt, prods in gramatica.items():
        for idx, prod in enumerate(prods):
            rhs = ' '.join(prod)
            pred = sorted(prediccion[(nt, idx)], key=lambda x: (x == END, x))
            print(f"  PREDICCIÓN({nt} → {rhs}) = {{ {', '.join(pred)} }}")

    print()


# ─────────────────────────────────────────────
#  EJERCICIO 1
# ─────────────────────────────────────────────
#  S → A uno B C
#  S → S dos
#  A → B C D
#  A → A tres
#  A → ε
#  B → D cuatro C tres
#  B → ε
#  C → cinco D B
#  C → ε
#  D → seis
#  D → ε

gramatica1 = {
    'S': [['A', 'uno', 'B', 'C'],
          ['S', 'dos']],
    'A': [['B', 'C', 'D'],
          ['A', 'tres'],
          [EPSILON]],
    'B': [['D', 'cuatro', 'C', 'tres'],
          [EPSILON]],
    'C': [['cinco', 'D', 'B'],
          [EPSILON]],
    'D': [['seis'],
          [EPSILON]],
}

no_terminales1 = ['S', 'A', 'B', 'C', 'D']

imprimir_resultados("EJERCICIO 1", gramatica1, no_terminales1, 'S')


# ─────────────────────────────────────────────
#  EJERCICIO 2
# ─────────────────────────────────────────────
#  S → A B uno
#  A → dos B
#  A → ε
#  B → C D
#  B → tres
#  B → ε
#  C → cuatro A B
#  C → cinco
#  D → seis
#  D → ε

gramatica2 = {
    'S': [['A', 'B', 'uno']],
    'A': [['dos', 'B'],
          [EPSILON]],
    'B': [['C', 'D'],
          ['tres'],
          [EPSILON]],
    'C': [['cuatro', 'A', 'B'],
          ['cinco']],
    'D': [['seis'],
          [EPSILON]],
}

no_terminales2 = ['S', 'A', 'B', 'C', 'D']

imprimir_resultados("EJERCICIO 2", gramatica2, no_terminales2, 'S')

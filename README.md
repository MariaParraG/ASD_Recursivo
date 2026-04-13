# Análisis Sintáctico Descendente (ASD)
### Conjuntos de PRIMEROS, SIGUIENTES y PREDICCIÓN

**Asignatura:** Lenguajes de Programación — Procesadores de Lenguaje  
**Universidad:** Sergio Arboleda  
**Tema:** Análisis Sintáctico Descendente Predictivo

---

## Descripción

Este proyecto implementa en Python los tres algoritmos fundamentales del Análisis Sintáctico Descendente Predictivo:

- **PRIMEROS (FIRST):** conjunto de terminales con los que puede comenzar una cadena derivada desde un no terminal.
- **SIGUIENTES (FOLLOW):** conjunto de terminales que pueden aparecer inmediatamente después de un no terminal en alguna forma sentencial.
- **PREDICCIÓN (PREDICT):** conjunto de tokens que permiten al parser elegir qué producción aplicar para un no terminal dado.

Los algoritmos se aplican sobre las gramáticas de los **Ejercicios 1 y 2** de la presentación 6 del curso.

---

## Requisitos

- Python 3.6 o superior
- No requiere librerías externas

---

## Uso

```bash
python conjuntos_gramatica.py
```

La salida muestra, para cada ejercicio: la gramática, los conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN de todos los no terminales y producciones.

---

## Estructura del código

```
conjuntos_gramatica.py
│
├── es_terminal(simbolo, no_terminales)
│     Determina si un símbolo es terminal.
│
├── calcular_primeros(gramatica, no_terminales)
│     Calcula PRIMEROS para todos los no terminales
│     mediante iteración de punto fijo.
│
├── calcular_siguientes(gramatica, no_terminales, axioma, primeros)
│     Calcula SIGUIENTES para todos los no terminales
│     mediante iteración de punto fijo.
│     Inicializa SIGUIENTES(axioma) = { $ }.
│
├── calcular_prediccion(gramatica, no_terminales, primeros, siguientes)
│     Calcula PREDICCIÓN para cada producción:
│       PRED(A → α) = PRIMEROS(α) − {ε}
│                   ∪ SIGUIENTES(A)  si ε ∈ PRIMEROS(α)
│
└── imprimir_resultados(nombre, gramatica, no_terminales, axioma)
      Orquesta los tres cálculos e imprime los resultados.
```

### Convenciones internas

| Símbolo | Representación en código |
|---------|--------------------------|
| ε (cadena vacía) | `'ε'` |
| $ (fin de entrada) | `'$'` |
| No terminales | Letras mayúsculas: `S`, `A`, `B`, `C`, `D` |
| Terminales | Palabras en minúsculas: `uno`, `dos`, `tres`, `cuatro`, `cinco`, `seis` |

### Formato de la gramática

Cada gramática es un `dict` de Python donde la clave es el no terminal y el valor es una lista de producciones; cada producción es a su vez una lista de símbolos:

```python
gramatica = {
    'S': [['A', 'uno', 'B', 'C'],   # S → A uno B C
          ['S', 'dos']],             # S → S dos
    'A': [['B', 'C', 'D'],          # A → B C D
          [EPSILON]],                # A → ε
    ...
}
```

---

## Gramáticas de los ejercicios

### Ejercicio 1

| Producción |
|------------|
| S → A **uno** B C |
| S → S **dos** |
| A → B C D |
| A → A **tres** |
| A → ε |
| B → D **cuatro** C **tres** |
| B → ε |
| C → **cinco** D B |
| C → ε |
| D → **seis** |
| D → ε |

### Ejercicio 2

| Producción |
|------------|
| S → A B **uno** |
| A → **dos** B |
| A → ε |
| B → C D |
| B → **tres** |
| B → ε |
| C → **cuatro** A B |
| C → **cinco** |
| D → **seis** |
| D → ε |

---

## Resultados

### Ejercicio 1

**PRIMEROS**

| No terminal | PRIMEROS |
|-------------|----------|
| S | { cinco, cuatro, seis, tres, uno } |
| A | { cinco, cuatro, seis, tres, ε } |
| B | { cuatro, seis, ε } |
| C | { cinco, ε } |
| D | { seis, ε } |

**SIGUIENTES**

| No terminal | SIGUIENTES |
|-------------|------------|
| S | { dos, $ } |
| A | { tres, uno } |
| B | { cinco, dos, seis, tres, uno, $ } |
| C | { dos, seis, tres, uno, $ } |
| D | { cuatro, dos, seis, tres, uno, $ } |

**PREDICCIÓN**

| Producción | PREDICCIÓN |
|------------|------------|
| S → A uno B C | { cinco, cuatro, seis, tres, uno } |
| S → S dos | { cinco, cuatro, seis, tres, uno } |
| A → B C D | { cinco, cuatro, seis, tres, uno } |
| A → A tres | { cinco, cuatro, seis, tres } |
| A → ε | { tres, uno } |
| B → D cuatro C tres | { cuatro, seis } |
| B → ε | { cinco, dos, seis, tres, uno, $ } |
| C → cinco D B | { cinco } |
| C → ε | { dos, seis, tres, uno, $ } |
| D → seis | { seis } |
| D → ε | { cuatro, dos, seis, tres, uno, $ } |

---

### Ejercicio 2

**PRIMEROS**

| No terminal | PRIMEROS |
|-------------|----------|
| S | { cinco, cuatro, dos, tres, uno } |
| A | { dos, ε } |
| B | { cinco, cuatro, tres, ε } |
| C | { cinco, cuatro } |
| D | { seis, ε } |

**SIGUIENTES**

| No terminal | SIGUIENTES |
|-------------|------------|
| S | { $ } |
| A | { cinco, cuatro, seis, tres, uno } |
| B | { cinco, cuatro, seis, tres, uno } |
| C | { cinco, cuatro, seis, tres, uno } |
| D | { cinco, cuatro, seis, tres, uno } |

**PREDICCIÓN**

| Producción | PREDICCIÓN |
|------------|------------|
| S → A B uno | { cinco, cuatro, dos, tres, uno } |
| A → dos B | { dos } |
| A → ε | { cinco, cuatro, seis, tres, uno } |
| B → C D | { cinco, cuatro } |
| B → tres | { tres } |
| B → ε | { cinco, cuatro, seis, tres, uno } |
| C → cuatro A B | { cuatro } |
| C → cinco | { cinco } |
| D → seis | { seis } |
| D → ε | { cinco, cuatro, seis, tres, uno } |

---

## Algoritmos implementados

### PRIMEROS — Punto fijo

```
Para cada no terminal NT:
  PRIMEROS(NT) = ∅

Repetir hasta que no haya cambios:
  Para cada producción NT → X1 X2 ... Xk:
    Para cada Xi en la producción:
      Si Xi es terminal: agregar Xi a PRIMEROS(NT); parar
      Si Xi es ε:        agregar ε a PRIMEROS(NT); parar
      Si Xi es NT':      agregar PRIMEROS(NT') − {ε} a PRIMEROS(NT)
                         Si ε ∉ PRIMEROS(NT'): parar
    Si todos los Xi pueden derivar ε: agregar ε a PRIMEROS(NT)
```

### SIGUIENTES — Punto fijo

```
SIGUIENTES(axioma) = { $ }
Para el resto: SIGUIENTES(NT) = ∅

Repetir hasta que no haya cambios:
  Para cada producción A → α NT β:
    Agregar PRIMEROS(β) − {ε} a SIGUIENTES(NT)
    Si ε ∈ PRIMEROS(β): agregar SIGUIENTES(A) a SIGUIENTES(NT)
    Si β = ε:           agregar SIGUIENTES(A) a SIGUIENTES(NT)
```

### PREDICCIÓN

```
Para cada producción A → α:
  PREDICCIÓN(A → α) = PRIMEROS(α) − {ε}
  Si ε ∈ PRIMEROS(α):
    PREDICCIÓN(A → α) = PREDICCIÓN(A → α) ∪ SIGUIENTES(A)
```

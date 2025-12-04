import time
from copy import deepcopy
from collections import deque

def mostrar_tablero(tablero): #solo muestra el tablero
    for fila in tablero:
        print("".join(fila))
    print()

#-------- ENCUENTRA TODOS LOS AUTOS (letras)--------------------
def encontrar_autos(tablero):
    # Creamos un conjunto vacío para guardar las letras de autos (sin repetidos)
    autos = set()
    # Recorremos cada fila del tablero
    for fila in tablero:
        # Recorremos cada celda dentro de la fila
        for c in fila:
            # Si la celda NO es vacío ni muro...
            if c not in ['.', ' ', '#']:
                # ...entonces es un auto, lo agregamos al conjunto
                autos.add(c)
    # Retornamos el conjunto con todas las letras encontradas
    return autos

#------ ENCUENTRAS LAS POSICIONES DE LOS AUTOS (letras) ------------------
def encontrar_posicion_auto(tablero, letra):
    posiciones = [] #guardamos las posiciones de un auto especifico, o sea letra

    # enumerate -> recorre la lista y devuelve (índice, elemento) siempre en ese orden
    for i, fila in enumerate(tablero): #recorremos cada fila del tablero, obtenemos su
                                       #indice con i
        for j, c in enumerate(fila): #recorremos cada celda de la fila y obtenemos su indice, j
            if c == letra: #si en la celda esta la letra
                posiciones.append((i, j)) #guardamos la posicion
    return posiciones

def orientacion_auto(coords):
    #si el auto tiene solo una celda, caso particular, no tiene orientación
    if len(coords) <= 1:
        return None
    #tomamos la fila de la primera parte del auto encontrada
    fila_inicial = coords[0][0]
    #revisamos si todas las otras partes están en la misma fila
    for f, c in coords:
        if f != fila_inicial:
        #esta version, cree nicole, es mejor que la usada en def mover_auto
            #si encontramos alguna celda con fila diferente, es vertical
            return "V"
    return "H" #si las celdas comparten filas, son horizontales

#con esta funcion moveremos un auto paso a paso
# asi validamos constantemente los movimientos
#ademas creo que tiene una mejor presentacion en el print
def mover_un_paso(tablero, letra, direccion):
    filas = len(tablero)
    columnas = len(tablero[0])

    coords = encontrar_posicion_auto(tablero, letra)
    #obtenemos las coordenadas del auto
    if not coords:
        return False, None

    coords = sorted(coords)

    # dr, dc -> indica el cambio de la posición del auto acorde a la dirección
    # dr -> filas
    # dc -> columnas

    dr, dc = {                  # esto se refleja en la línea 79
        'L': (0, -1),   # la fila no se mueves, la columna disminuye en 1
        'R': (0,  1),   # la fila no se mueves, la columna aumenta en 1
        'U': (-1, 0),   # la fila disminuye en 1, la columna no se mueve
        'D': (1,  0)    # la fila aumenta en 1, la columna no se mueve
    }[direccion] # cuando dirección tenga un valor (L, R, U o D), dr y dc tomarán la clave equivalente a ese valor.
                 # EJM:     dirección = L ->    (dr, dc) = (0, -1)

    nuevas = []
    for f, c in coords:
        nf, nc = f + dr, c + dc
        #o sea esto es
        #nueva fila (nf) es igual a fila + el cambio de direccion que implicaria cada movimiento, lo mismo aplica para nc
        nuevas.append((nf, nc))

    #la condición de victoria del juego
    # es cuando auto X sale por la derecha del tablero
    # tmb se puede decir que es cuando su posicion se excede de
    # los indices de la matriz por columnas
    for nf, nc in nuevas:
        if letra == 'X' and direccion == 'R' and nc >= columnas:
            nuevo = deepcopy(tablero)   # deepcopy crea una copia completa e independiente de tablero
            # borramos X actual
            for f, c in coords:
                nuevo[f][c] = '.'
            # dibujamos la parte de X que sigue dentro (por estética)
            for f2, c2 in nuevas:
                if 0 <= f2 < filas and 0 <= c2 < columnas:
                    nuevo[f2][c2] = 'X'
            return 'Ganaste', nuevo

    #aca validamos colisiones límites
    for nf, nc in nuevas:
        if nf < 0 or nf >= filas or nc < 0 or nc >= columnas:
            return False, None
        celda = tablero[nf][nc]
        if celda not in ['.', ' ', letra]:
            return False, None
        #al retornar false,none le indicamos que es un movimiento invalido
        #casi igual que en def mover_auto

    #aplicamos el movimiento sobre una copia pq
    #es conveniente tener el tablero original intacto para
    #testear todos los movimientos posibles desde ese punto
    #si no usamos copias pueden haber errores de malos movimientos
    #autos desaparecidos e incluso loops infinitos
    nuevo = deepcopy(tablero)
    for f, c in coords:
        nuevo[f][c] = '.'
    for nf, nc in nuevas:
        if 0 <= nf < filas and 0 <= nc < columnas:
            nuevo[nf][nc] = letra
    return True, nuevo #True indica que la operación fue exitosa

#generamos estado (situacion actual del tablero, como foto congelada del momento actual del juego) y búsqueda por niveles
# esto es algo tipo algoritmo BFS (lo que es busqueda en amplitud)
# el cual busca o recorre estructuras de datos para encontrar
#caminos de solucion cortos entre dos nodos de un grafo
#esto lo hace en terminos de numeros de aristas, (ver imagen x wasap)
#   Grafo -> un mapa de puntos conectados con líneas
#   nodo -> cada punto de ese mapa
#   arista -> es la conexión que une dos nodos

def clave_estado(tablero):
    # convierte el tablero en una clave única e inmutable
    # Para poder guardar el estado en un set/dict
    return tuple("".join(fila) for fila in tablero)
    #esto basicamente lo genera en una tupla de strings (cada string es una fila del tablero):
#    tablero = [                                     Cadenas
#        ['.', 'X', '.'],               Primera fila: ".X."                     TUPLA (agrupa todas las cadenas)
#        ['A', 'A', '.'],       ->      Segunda fila: "AA."       ->    (".X.", "AA.", "...")
#        ['.', '.', '.']                Tercera fila: "..."
#    ]

    # para que sea almacenable en diccionarios (las listas no pueden ser claves porque son mutables)
    #nos sirve para:
        #visitados.add(clave_estado(tablero)) en def buscar ruta

#esta funcion crea todos los movs posibles desde un tablero
def generar_sucesores(tablero):
    sucesores = []
    #recorremos todos los autos
    #detectamos su posicion, H o V
    #generamos movimientos validos
    #devolvemos que auto se movio, direccion, tablero resultante
    #y si el movimiento gana el juego
    for letra in sorted(encontrar_autos(tablero)):
        coords = encontrar_posicion_auto(tablero, letra)
        ori = orientacion_auto(coords)
        if letra == 'X':
            direcciones = ['R', 'L', 'U', 'D']   # X se mueve libremente
        else:
            # resto de autos solo según orientación
            direcciones = ['L', 'R'] if ori == 'H' else ['U', 'D']
        for d in direcciones:
            res, nuevo = mover_un_paso(tablero, letra, d)
            #aca intentamos mover el auto en cada direccion valida
            if not res:
                continue #si el movimiento es invalido, seguimos
            gano = (res == 'Ganaste')
            sucesores.append((letra, d, nuevo, gano))
    return sucesores

def reconstruir_ruta(padres, clave_final):
    #btw se le llama padre pq ese es el tablero original
    #cada posibilidad de resolucion es como un hijo
        #es como si el algoritmo BFS encontrase la ruta ganadora
        #empieza desde ese resultado final y va hacia atras
        #hace preguntas tipo: Quien es mi padre? Que movimiento me trajo aqui?
        #luego sige con el padre: y el padre de mi padre? y el padre de ese?
            # 'padres' es un diccionario que guarda el tablero anterior en base a su clave:
            #  clave_estado -- (estado_anterior, (letra_movida, direccion))
            # clave_final -> es la clave del estado actual
    info = padres[clave_final]

    if info is None:
    # Si info es None significa que este es el estado inicial,
    # es decir, no tiene un padre del cual venir.
    # Aquí empezamos la reconstrucción.
        return []
    clave_anterior, movimiento = info
    #'info' contiene una tupla: (clave_del_padre, movimiento_realizado)
    # movimiento_realizado es (letra, direccion)
    ruta = reconstruir_ruta(padres, clave_anterior)
    #reconstruimos ruta desde el inicio hasta el tablero padre
    #aca aplicamos recursividad
    ruta.append(movimiento)
    return ruta #devuelve la ruta completa hasta ese punto

# max_estados -> es para tener un límite máximo y no siga infinitamente
def buscar_ruta(tablero, max_estados=200000):
    inicio = tablero
    clave_ini = clave_estado(inicio)

    # Diccionario que recuerda: estado → (padre, movimiento)
    padres = {clave_ini: None} # guarda el estado anterior, iniciando en None porque no ha iniciado
    visitados = {clave_ini}    # Estados ya vistos para evitar loops (ciclos repetitivos)
    # Cola propia del algoritmo BFS
    cola = deque([inicio]) #cola es el primero que entra es el primero que sale, tipo PEPS
    #el deque es una funcion que permite agregar y quitar elementos rápidamente
    # cola -> estructura de datos llamada deque en el que el primer estado que entra es el primero que sale para ser procesado, y
    # los nuevos estados se agregan al final para ser procesados después

    # Procesamos hasta agotar la cola o superar el límite
    while cola and len(visitados) <= max_estados:
        actual = cola.popleft() # popleft saca y devuelve el primer elemento de cola
        clave_act = clave_estado(actual)

        # Probamos todos los movimientos posibles desde este estado
        for letra, d, nuevo, gano in generar_sucesores(actual):
            # Si esta jugada gana, reconstruimos la solución
            if gano:
                ruta = reconstruir_ruta(padres, clave_act)
                ruta.append((letra, d))
                return ruta
            # Generamos la clave del tablero nuevo
            clave_nuevo = clave_estado(nuevo)
            # Si nunca hemos estado
            if clave_nuevo not in visitados:
                visitados.add(clave_nuevo)  # lo recordamos
                padres[clave_nuevo] = (clave_act, (letra, d))
                cola.append(nuevo)  # y lo agregamos para seguir explorando

    # Si no se encontró solución
    return None


def texto_dir(d): #esto es nada mas para el print explicativo
    return {
        'L': 'izquierda',
        'R': 'derecha',
        'U': 'arriba',
        'D': 'abajo'
    }[d]


#ESTE ES EL MAIN
def resolver_automaticamente(tablero, tamaniodex=None, delay=2):
    print("-----Resolucion automatica-----")
    print("Tablero inicial:\n")
    mostrar_tablero(tablero)
    time.sleep(delay)   # delay -> indica cuantos segundos debe esperar para continuar

    ruta = buscar_ruta(tablero)

    if ruta is None:
        print("No existe manera de que el auto 'X' salga del tablero.")
        print("Puede que el nivel no tenga solución.\n")
        return "Sin solucion", 0

    print(f"Esta partida se puede ganar en {len(ruta)} movimientos.")
    print("Este es el paso a paso:\n")
    time.sleep(delay)

    # Copia del tablero para ir actualizando visualmente
    tablero_actual = deepcopy(tablero)
    paso = 1

    # Recorremos cada movimiento de la ruta
    for letra, d in ruta:
        print(f"Paso {paso}:")

        # Comentarios explicativos según el auto movido
        if letra == 'X':
            if d == 'R':
                print("---El auto 'X' avanza un paso hacia la derecha.")
            elif d == 'L':
                print("---El auto 'X' se mueve un paso a la izquierda para reacomodarse.")
            elif d == 'U':
                print("---El auto 'X' sube una casilla buscando una mejor posición.")
            else:
                print("---El auto 'X' baja una casilla para posicionarse mejor.")
        else:
            print(f"Movemos el auto '{letra}' hacia la {texto_dir(d)} para ir despejando el camino.")

        # Aplicamos el movimiento real
        res, nuevo = mover_un_paso(tablero_actual, letra, d)
        tablero_actual = nuevo

        # Mostramos el tablero luego de ese movimiento
        mostrar_tablero(tablero_actual)
        time.sleep(delay)

        # Si la jugada ganó, terminamos
        if res == 'Ganaste':
            print("El auto 'X' ha salido del tablero. Nivel resuelto.\n")
            return "Ganaste", len(ruta)

        paso += 1

    print("La secuencia terminó sin que 'X' salga del tablero (esto no debería pasar).")

    return "Sin solucion", 0

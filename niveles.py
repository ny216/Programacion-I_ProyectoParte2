import random #importamos la libreria random para resultados aleatorios (posiciones de autos) 
from historial import guardar #importamos la funcion guardar para almacenar los resultados del jugador 

def nivelitos(usuario, nivel):
    #funcion con dos argumentos (usuario, nivel) obtenidos previamente al momento de elegir en el menu la opcion 1 
    #detalles es un diccionario con claves 1,2,3 que son los niveles de juego y los valores los detalles por nivel
    #configuracion o detalles generales de cada nivel
    detalles = {
        1: {
            "filas": 8,
            "columnas": 8,
            "tamaniodex": 2,            #el auto x ocupa 2 celdas
            "tamaniohorizontal": 2,     #autos horizontales ocupan 2
            "tamaniovertical": 2,       #autos verticales ocupan 2
            "autosextra": ["A", "B", "C", "D"]},
        2: {
            "filas": 10,
            "columnas": 10,
            "tamaniodex": 2,
            "tamaniohorizontal": 2,
            "tamaniovertical": 2,
            "autosextra": ["A", "B", "C", "D", "E", "F"]},
        3: {
            "filas": 12,
            "columnas": 12,
            "tamaniodex": 3,            #en este nivel x ocupa 3 celdas
            "tamaniohorizontal": 3,     #autos horizontales ocupan 3 celdas
            "tamaniovertical": 2,
            "autosextra": ["A", "B", "C", "D", "E", "F", "G", "H"]
        }}

    cfg = detalles[nivel] #cfg espera la clave de nivel para cargar los valores a configurar 
    filas = cfg["filas"] #obtiene el valor de la clave filas
    columnas = cfg["columnas"] #obtiene el valor de la clave columnas
    tamaniodex = cfg["tamaniodex"] #obtiene el valor de la clave tamniox
    tamaniohorizontal = cfg["tamaniohorizontal"] #obtiene el valor de la clave tamaniohorizontal
    tamaniovertical = cfg["tamaniovertical"] #obtiene el valor de la clave tamniovertical 
    autosextra = cfg["autosextra"] #obtiene el valor de la clave autosextra 

    #imprimimos el mensaje de bienvenida segun el nivel 
    print(f"\nBienvenido al nivel {nivel}")
    print("Recuerda: El objetivo es sacar el auto 'X' por la derecha.")
    print("          El auto X se mueve libremente, el resto de autos")
    print("          se mueve de acuerdo a su posición\n")

    #esto crea el tabla con puntos para distinguir los espacios libres
    #version lambda de un for aninado que recorre e imprime "." en todas las filas y columnas  
    tablero = [["." for columna in range(columnas)] for fila in range(filas)]

    #esto pone los bordes o muros al tablero, siendo representados con #
    for f in range(filas):
        for c in range(columnas):
            if f == 0 or f == filas - 1 or c == 0 or c == columnas - 1:
                tablero[i][j] = "#"

    # auto X -------------------------------------------------------------------------------------------------------------------
    #tiene una posicon inicial aleatoria diferente a la fila inferior (fila-1) y a la fila superior (0)
    fauto = random.randint(1, filas - 2)  #esto define una fila aleatoria evitando bordes
                                             #de la 1 a la 6
    #tiene una posicon inicial aleatoria diferente a la columna izquierda (0) y a 
    #la columna derecha dependiendo del tamanio del auto X (columnas-1)
    cauto = random.randint(1, columnas - (tamaniodex + 1))  # igual, pero se le resta el espacio que ocupa x y uno mas del muro
    #imprimimos cada letra que contiene el tamanio del auto X (2 o 3) 
    for letrita in range(tamaniodex): #ahora lo ponemos asi pq es variable
                                      #a veces ocupa 2 o 3 espacios
        tablero[fauto][cauto + letrita] = "X"

    # esto crea la salida aleatoriamente en el lado derecho --------------------------------------------------------------------
    #validamos la posicion correcta del espacio de la salida del tabero (siempre lado derecho)
    while True:
        #es una posicion aleatoria diferente al borde superior(0) e inferior(-1) 
        fsalida = random.randint(1, filas - 2)  # escoge una fila aleatoria, evitando
                                                   # borde inferior y superior
                                                   # "-2" es pq el indice mayor siempre es uno menos
        if fsalida != fauto:  #la fila de salida y la fila inicial del auto X deben ser diferentes 
            #se imprime un espacio vacio en la columna derecha siendo esta la salida
            tablero[fsalida][-1] = " "    # "-1" -> pq la salida siempre se ubica en la última columna    
            break

    #autos extra ------------------------------------------------------------------------------------------------------
    #recorremos la lista de autos extras 
    for auto in autosextra: 
        colocado = False #esto indica que aun no se ha colocado el auto, cambia al final del bucle
        intentos = 0 #contador de intentos para evitar un bucle infinito 
        while not colocado and intentos < 100: #el max de intetos evita el bucle infinito
            orientacion = random.choice(["horizontal", "vertical"])
            fila = random.randint(1, filas - 2) #el menos 2 evita que toquemos los muros
            col = random.randint(1, columnas - 2)
            intentos += 1 #sumamos un intento al intetar colocar el auto

            #validamos si las posiciones aletorias estan desocupadas 
            if orientacion == "horizontal": #en caso sea horizontal
                #si la posicion columna + tamaniohorizontal -1 es menor que el borde, el espacio esta libre
                if col+ tamaniohorizontal - 1 <= columnas - 2:
                #col es la columna de donde partimos, le sumamos el tamanio del auto
                #columnas - 2 es la ultima columna que no es muro
                #esta condicion se resume a que la ultima partecita del auto debe estar
                #antes del indice del muro
                #si no se cumple, vuelve a escoger al azar
                    espaciolibre = True #aca supones que si hay espacio
                                        # osea que no hay otro auto, los muros lo revisamos
                                        #con la condicion anterior
                    for celda in range(tamaniohorizontal): #recorremos cada celda
                                                           #que ocuparia el auto
                        if tablero[fila][col + celda] != ".": #si es diferente al punto, no esta vacio
                            espaciolibre = False
                            break #esto sale del for para repetir el bucle
                                  #hasta que colocado sea TRUE
                    if espaciolibre: #si sigue siendo TRUE
                        for celda in range(tamaniohorizontal):
                            tablero[fila][col + celda] = auto #colocamos el auto en el tablero
                    colocado = True #el TRUE hara que al negarlo ya no entre al bucle
                    #pasamos al siguiente auto

            else: #en cambio, si el auto es vertical, mismo proceso pero en fila
                if fila + tamaniovertical - 1 <= filas - 2:
                    espaciolibre = True
                    #recorremos los valores de 0 a tamaniovertical(tamanio del auto) 
                    for k in range(tamaniovertical):
                        if tablero[fila + k][col] != ".":
                            espaciolibre = False
                            break
                    if espaciolibre:
                        for k in range(tamaniovertical):
                            tablero[fila + k][col] = auto
                        colocado = True
    #se imprime el tablero con los autos y la salida en consola 
    mostrar_tablero(tablero)

    #invocamos a la funcion resolver_manualmente con todos sus argumentos 
    return resolver_manualmente(tablero,tamaniodex, usuario, nivel, autosextra)

#esta funcion guarda la cantidad de movimientos por usuario y nivel, y la condicion de ganado o abandonado  
def resolver_manualmente (tablero, tamaniodex, usuario, nivel, autosextra):

    #configuraciones iniciales 
    modo = "Manual"
    movimientos = 0
    #se ejecutara siempre que el usuario no escriba la palabra "fin"
    while True:
        #el usuario selecciona el auto que quiere mover 
        seleccion = input("\nSeleccione un auto (letra) o escriba 'fin' para salir: ").strip().upper()

        #condiciona a que el jugador termine el juego si escribe la palabra "fin" 
        if seleccion == "FIN": #si el jugador desea salir
        # guardamos la info en la funcion guardar para el historial
            print("Abandonaste la partida.")
            guardar(usuario, nivel, "Abandono", movimientos, modo)
            return "Abandono" #este resultado se manda a menu
        #pq te hace salir del juego pero lo del menu es un bucle que no termina
        #al menos de que le pongas la opcion 3

        #si la opcion es mas de una letra, le vuelve a pedir al usuario su input 
        if len(seleccion) != 1:
            print()
            print("Por favor ingrese solo 1 letra")
            mostrar_tablero(tablero)
            continue
            
        #si la opcion no es una letra valida, le vuelve a pedir al usuario su input 
        if not seleccion.isalpha():
            print("\nPor favor, ingrese una letra válida.")
            mostrar_tablero(tablero)
            continue
            
        #si la letra no se encuetra en el tablero, le vuelve a pedir al usuario su input
        if seleccion not in autosextra and seleccion != 'X':
            print()
            print("Letra no existente.")
            mostrar_tablero(tablero)
            continue
            
        #imprimimos las opciones de movimeinto que tiene el auto  
        direccion = input("Mover (U/D/L/R): ").strip().upper() #el strip es por si el usuario
                                                               # comete error de poner espacios adicionales
        # u es UP, d es DOWN, l es LEFT y r es RIGHT
        #mientras que el usuario no ingrese un movimiento valido, le volvera a pedir su input 
        while direccion not in ["U", "D", "L", "R"]:
        #valida la direccion ingrsada
            direccion = input("Mover (U/D/L/R): ").strip().upper()

        # mov es como cuantas espacios se moverá el auto seleccionado
        mov = input("Movimientos: ")

        # Mientras el valor no sea un número o sea <= 0, sigue pidiendo
        while not mov.isdigit() or int(mov) <= 0:
            print("Por favor ingresa un número válido (mayor que 0).")
            mov = input("Movimientos: ")

        mov = int(mov)

        #llama a la funcion mover_auto para que se realice el movimiento
        resultado = mover_auto(tablero, seleccion, direccion, mov, tamaniodex)

        #si X logra salir del tablero, el usuario gana
        if resultado == "Ganaste": #en caso el usuario gan
            movimientos += mov #sumamos los movimientos de la jugada ganaddora
            mostrar_tablero(tablero)
            print("\n¡Felicidades! Lograste sacar el auto principal")
            guardar(usuario, nivel, "Gano", movimientos, modo)
            return "Ganaste"

        elif not resultado: #en caso el movimiento fue invalido
            print("Movimiento no válido")
            mostrar_tablero(tablero)

        else: #en caso el movimiento sea valido pero aun no gane
            movimientos = movimientos + mov #suma movimientos realizados siempre y cuando sean validos
            mostrar_tablero(tablero)

#funcion que imprime el tablero en consola 
def mostrar_tablero(tablero):
    for fila in tablero:
        print("".join(fila))
    print()
    
#funcion que permite y guarda los movimientos de los autos
def mover_auto(tablero, letra, direccion, mov, tamaniodex):
    filas = len(tablero) 
    columnas = len(tablero[0])

    #recorremos toda la matriz hasta encontrar las celdas donde
    #esten las letras del auto que se desea mover
    coordenadas = []
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] == letra:
                coordenadas.append((i, j)) #dos pares de coordenadas pq son dos letras
    #si el largi de las coordenadas es 0 es pq no hay un auto 
    if len(coordenadas) == 0:
        return False

    #con el sort ordenamos las coordenadas para buscarlas 
    coordenadas.sort()
    #determinamos la orientación (horizontal o vertical)
    horizontal = True #asumimos que esta en horizontal
    base = coordenadas[0][0] #esta es la primera fila encontrada
    #recorremos las filas y columnas de las coordenadas 
    for (f, c) in coordenadas:
        if f != base: #si en algun momento la fila es diferente
                      #a la primera fila que vimos
            horizontal = False #no es horizontal
            break
    #esto valida las restricciones de movimiento segun orientación
    if letra != "X":
        if horizontal and direccion not in ["L", "R"]:
            return False
        if not horizontal and direccion not in ["U", "D"]:
            return False

  #hace el proceso por cada movimiento que quiera hacer
    #el mov es el valor del argumento que se adquiere del usuario 
    for mover in range(mov):
        #copiamos las coordenadas
        coordenadas_actuales = [] #no podemos poner coordenadas_actuales = coordenadas
                                  # porque no seria crear una copia y afectaria a coordenadas
        #recorremos las posiciones de las coordenadas y las guardamos en las coordenadas actuales 
        for (f, c) in coordenadas:
            coordenadas_actuales.append((f, c))

        nuevas = [] #aqui se guarda la nueva posicion del auto tras moverse un solo paso
        for (f, c) in coordenadas: #recorre cada parte o letra del auto
            if direccion == "L": #si te quieres mover a la izq
                nuevas.append((f, c - 1)) #es como disminuir una columna
            elif direccion == "R": #si quieres ir a la derecha
                nuevas.append((f, c + 1)) #es como aumentar una columna
            #misma logica con arriba y abajo pero modificando columnas
            elif direccion == "U":
                nuevas.append((f - 1, c))
            elif direccion == "D":
                nuevas.append((f + 1, c))

        #revisamos las celdas nuevas que ocuparia el auto
        for (nuevafila, nuevacolumna) in nuevas:
            #este es el caso particular de ganar
            #consideramos salida por derecha, unicamente para
            #si la columna nueva es mayor o igual al ancho del tablero significa
            #que el auto esta saliendo del tablero
            if direccion == "R" and nuevacolumna >= columnas:
                if letra == "X":
                    print("¡Ganaste!")
                    return "Ganaste"
                else:
                    return False #en caso no sea asi, aun no gano 

            #si la nueva posicion se sobrepasa del tama;o del tablero, el movimiento es invalido
            if nuevafila < 0 or nuevafila >= filas or nuevacolumna < 0 or nuevacolumna >= columnas:
                return False

            libres = [" ", "."]

            #si la nuevaposicion del auto no esta vacia
            if tablero[nuevafila][nuevacolumna] not in libres:
                # pero si es parte del mismo auto, esta permitido, xq hay momentos donde se pone sobre uno
                #x ejemplo:  (l = libre)
                # movimiento: 1    lxx  -> xxl
                #los dos x del medio tecnicamente o visualmente, no se movieron
                #pero en el codigo si hay un cambio
                encontrado = False #iniciamos asumiendo que no hay coincidencia
                for (f_ant, c_ant) in coordenadas_actuales: #recorremos las posiciones que ocupaba
                                                            #el auto antes de moverse un paso
                    if nuevafila == f_ant and nuevacolumna == c_ant: #si una posicion coincide con la nueva celda o posicion
                                                                    #entonces si es el mismo auto
                        encontrado = True
                        break
                if not encontrado:
                    return False

        #si paso todas las validaciones anteriores, movemos el auto un paso
        coordenadas = []
        for (nuevafila, nuevacolumna) in nuevas:
            coordenadas.append((nuevafila, nuevacolumna))

    #borramos las posiciones antiguas
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] == letra:
                tablero[i][j] = "."

    #colocamos el auto en su nueva posición
    for (f, c) in coordenadas:
        tablero[f][c] = letra


    return True


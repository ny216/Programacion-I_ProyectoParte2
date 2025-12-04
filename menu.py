import time
from historial import mostrarh, verificarusuarioexiste, mostrar_estadisticas
from niveles import nivelitos

def mostrar_menu():
    #muestra en pantalla el menu principal con cinco opciones
    print()
    print("===== DESATASCA EL AUTO - MENU PRINCIPAL =====")
    print("1 . Iniciar nuevo juego")
    print("2 . Resolver automáticmente")
    print("3 . Ver historial de juegos")
    print("4 . Ver estadisticas")
    print("5 . Salir")
    print("==============================================")
    print()

while True:
    #el usuario elige una opcion del menu y se valida esta opcion
    mostrar_menu() #muestra los prints anteriores
    #usamos .strip para eliminar espacios del input (inicio y final)
    opcion = input("Ingrese una opción [1 - 5]: ").strip()
    print()
    #si el input no es un numero entre el 1 y 5, el programa vuelve a solicitar un # valido
    while not opcion.isdigit() or int(opcion) not in [1, 2, 3, 4, 5]:
        opcion = input("Opción no válida. Ingrese una opción [1 - 5]: ").strip()
        print()
    #una vez obtenido un valor valido, se convierte en entreo (int)
    opcion = int(opcion)


    # salir del programa o juego----------------------------------------------------------------
    if opcion == 5:
        oraci = "Saliendo del programa..."
        for x in oraci:
            time.sleep(0.2)
            #evita el salto de línea automático de print
            print(x,end="")
        #tiempo de espera antes de cerrar
        time.sleep(1)
        break  # en este caso ya no es exit, xq ahora estamos usando un bucle
        # es suficiente con romperlo

    # juego automático-------------------------------------------------------------------------
    elif opcion == 2:
        print("Escribe o pega el tablero como alguna de las dos opciones.")
        print('Recuerda que deben tener la misma longitud de filas y columnas')
        print("Cuando termines, escribe una línea solo con FIN\n")
        print("1)   Como lista de listas de Python")
        print("     Ejemplo:")
        print('             [["#", ".", "A"],["#", "X", "X"]]\n')
        print("2)   Como texto normal:\n")
        print("     Ejemplo:")
        print("             ######## ")
        print("             #......# ")
        print("             #.XX...# ")
        print("             #....... ")
        print("        Sucesivamente...\n")
        print("Tablero (múltiples líneas permitidas):")

        # ejemplo para que prueben (quitale los # de la izquierda):

        #[
        #    ["#", "#", "#", "#", "#", "#", "#", "#"],
        #    ["#", ".", ".", ".", ".", ".", ".", "#"],
        #    ["#", ".", ".", ".", ".", ".", " ", " "],
        #    ["#", ".", "X", "X", ".", ".", ".", "#"],
        #    ["#", ".", ".", ".", ".", ".", ".", "#"],
        #    ["#", ".", "D", ".", ".", ".", ".", "#"],
        #    ["#", ".", "D", ".", "A", "A", ".", "#"],
        #    ["#", "#", "#", "#", "#", "#", "#", "#"]
        #    ]

        while True:
            lineas = []
            while True:
                linea = input()
                if linea.strip().upper() == "FIN":
                    break
                #la consola registra cada ENTER como una nueva "línea"
                lineas.append(linea)
            #elementos de la lista convertirlo a cad
            texto = "\n".join(lineas)

            tablero = None

            #convertir lo que el usuario escribió en una lista de listas real
            try:
                # eval -> convierte las cadenas en estructuras de python
                # texto es una cadena, eval la interpreta como el codigo real, o sea, lo lee como lista de listas
                posible_tablero = eval(texto)

                # isninstace -> verifica si el objeto es lo que dice ser, ejemplo: si tablero es una lista o f una lista
                # all -> devuelve True si todos los elementos son True, en este caso, si cada fila es una lista, devuelve True
                         # esto te asegura que tengas una lista de listas
                if isinstance(posible_tablero, list) and all(isinstance(f, list) for f in posible_tablero):
                    valido = True
                    #recorrer en sublista
                    for fila in posible_tablero:
                        #recorrer en elemento
                        for c in fila:
                            if not (c == "#" or c == "." or c == " " or c.isalpha()):
                                valido = False
                                break

                        if not valido:
                            break
                    if valido:
                        tablero = posible_tablero
                    else:
                        #se lanza un excepción intencional
                        raise Exception() # llamamos a except

            #cuando no puede ser convertido a una matriz con eval()
            #cuando se ve forzado a saltar a esta etapa (valido = false)
            # ---> cuando algo falla en el try
            except Exception: # para la opción 2 (texto)

                tablero = [] #se guardará la matriz correcta
                formato_texto_del_tablero_valido = True #se asume, inicialmente, que el texto tiene un buen formato

                #recorrer cada línea que el usuario ingresó
                #cada fila --> str
                for fila in lineas: #lineas definida en (69)
                    # en caso fila termine con salto de línea
                    if fila.endswith("\n"):
                        #eliminar de la fila el salto de línea
                        fila = fila[: -1]

                    # si hay lineas vacías debe ser inválido

                    if fila.strip() == "":
                        formato_texto_del_tablero_valido = False
                        break

                    fila_final = [] #almacenar los caracteres válidos de la fila actual

                    #recorrer cada caracter
                    for c in fila:
                        #debe cumplir con este formar
                        if not (c == "#" or c == "." or c == " " or c.isalpha()):
                            formato_texto_del_tablero_valido = False
                            break
                        #si es válido se agrega a fila_final
                        fila_final.append(c)
                    #se detectó un caracter inválido y no se procesan más filas
                    if not formato_texto_del_tablero_valido:
                        break

                    ##si la fila terminó sin problemas, se añade fila_final como fila a tablero
                    tablero.append(fila_final)

                #validamos que filas y columnas tengan la misma longitud
                #obligatorio porque sino se podría tener un tablero irregular
                #el tablero no está vacío y el formato es válido
                if tablero and formato_texto_del_tablero_valido:
                    #medir la longitud de la primera fila
                    columna = len(tablero[0])
                    #comprobar que todas las filas cuenten con la misma longitud
                    if not all(len(fila) == columna for fila in tablero):
                        formato_texto_del_tablero_valido = False

                #si ha habido errores al pasar la matriz --> La vuelve a solicitar
                if not formato_texto_del_tablero_valido or not tablero:
                    print('\n Formato inválido. Debe ser: ')
                    print("1)   Como lista de listas de Python")
                    print("     Ejemplo:")
                    print('             [["#", ".", "A"],["#", "X", "X"]]\n')
                    print("2)   Como texto normal:\n")
                    print("     Ejemplo:")
                    print("             ######## ")
                    print("             #......# ")
                    print("             #.XX...# ")
                    print("             #....... ")
                    print("        Sucesivamente...\n")
                    print("Intente nuevamente.\n")
                    #se reinicia el bucle subprincipal --> While true
                    continue
            break
        #el usuario ingresara el tamaño del vehiculo X
        tamaniodex = int(input("Tamaño del auto X (2 o 3): "))
        while not tamaniodex in [2, 3]:
            #validara que el tamaño sea entre 2 y tres 
            tamaniodex = int(input("Tamaño del auto X (2 o 3): "))

        # para saber qué nivel es al momento de guardarlo en el historial
        filas = len(tablero)
        if filas > 0: # en caso tablero no tenga filas
            columnas = len(tablero[0])
        else:
            columnas = 0
        #el nivel 1 es un tablero de 8x8
        if filas == 8 and columnas == 8:
            nivel_detectado = 1
        #el nivel 2 es un tablero de 10x10
        elif filas == 10 and columnas == 10:
            nivel_detectado = 2
        #el nivel 3 es un tablero de 12x12
        elif filas == 12 and columnas == 12:
            nivel_detectado = 3
        #si no es ninguno de los anteriores, se considera "otro"
        else:
            nivel_detectado = "Otro"

        from nivelautomatico import resolver_automaticamente
        from historial import guardar
        resultado, movimientos = resolver_automaticamente(tablero, tamaniodex)

        guardar("Computadora", nivel_detectado, resultado, movimientos, "Automatico")
        print("\nResultado:", resultado, f"Movimientos: {movimientos}")
        time.sleep(2)

    # muestra historial-------------------------------------------------------------------------
    elif opcion == 3:
        print()
        mostrarh()
        print("\nVolviendo al menú...\n")
        time.sleep(1)
        #automáticamente continúa el ciclo del menu
        
    #ver estadisticas---------------------------------------
    elif opcion == 4:
        #ver_estadisticas()
        mostrar_estadisticas()
        print("\nVolviendo al menú...\n")
        time.sleep(1)

    # Juego manual ---------------------------------------------------------------------
    elif opcion == 1:
        # solicita el nombre del usuario
        print()
        print("Como máximo su nombre puede ser de 12 letras")
        usuario = input("Ingrese su nombre: ").strip()

        #cambié la longitud a 12 para la palabra computadora :) en la versión automática
        while len(usuario) > 12 or len(usuario) == 0:
            if len(usuario) == 0:
                print("Por favor, ingrese un nombre")
            else:
                print("Por favor, un máximo de 12 letras")
            usuario = input("Ingrese su nombre: ").strip()
        print()
        print("\nIniciando juego ... \n")

        if not verificarusuarioexiste(usuario):
            #si el usuario es nuevo, tiene que empezar desde el nivel 1
            niveli= 1
            #avanza automáticamente por los 3 niveles
            while niveli <= 3:
                print(f"\nCargando nivel {niveli}...")
                time.sleep(1)
                #es un import dinamico de acuerdo al nivel actual

                resultado = nivelitos(usuario, niveli)
                #cada vez que gana, pasa automáticamente al siguiente nivel
                if resultado == "Ganaste":
                    niveli += 1
                #si no gane, se sale del bucle
                else:
                    break

            print("\nRegresando al menú principal...\n")
            time.sleep(1)
            #automáticamente continúa el ciclo del menu

        # si el usuario existe en el historial--------------------------------------------------------
        elif verificarusuarioexiste(usuario):
            #si el usuario es verdadero, le dara nuevamnete la bienvenida 
            print()
            print(f"Hola de nuevo, {usuario}!")
            #le pregunta que nivel quiere jugar (solo los que ya paso)
            nivel = input("Ingrese el nivel que desea jugar: ").strip()
            #debe validar el nivel ingresado 
            while not nivel.isdigit() or int(nivel) not in [1, 2, 3]:
                nivel = input("Nivel inválido. Elige 1, 2 o 3: ").strip()
            #convierte el nivel (string) en un entero (int)
            nivelus = int(nivel) #nivel actual es igual al nivel ingresado

            while nivelus <= 3:
                #mientras el nivel sea valido, se ejecutara el nivel seleccionado 
                resultado = nivelitos(usuario, nivelus)
                #si gana, sube automaticamente de nivel hasta pasar los 3 
                if resultado == "Ganaste":
                    nivelus += 1
                #si no gana, se queda en el mismo nivel y sale del bucle 
                else:
                    break

            print("\nRegresando al menú principal...\n")
            time.sleep(1)
            #automáticamente continúa el ciclo del menu





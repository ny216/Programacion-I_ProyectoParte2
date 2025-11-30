# datetime es un modulo para trabajar con fechas y horas, abarca ambos
import datetime

#deberia tambien crear un archivo para que guarde la info y sea mas facil de mostrar dps

def guardar(usuario, nivel, resultado, movimientos, modo):
    # datetime.datetime.noe : obtiene la fecha y hora actual
        # el 1er datetime es para llamar al modulo, dicho modulo tiene muchas cosas relacionadas a fechas y horas
        # el 2do datetime es para llamar la clase (plantilla) dentro de ese modulo que represente un objeto con fecha y hora
    # strftime : string format time ; convierte el objetivo fecha y hora en una cadena de texto
    # %.... : codigos especiales que tiene la cantidad fija de digitos predifinia.
        # %Y: año con 4 dígitos (predefinido la cantidad de digitos)
        # %m: mes con 2 digitos (predefinido la cantidad de digitos)
        # ....

    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{usuario}, {nivel}, {resultado}, {movimientos}, {fecha_hora}, {modo}\n"
    # with open (... ) as archivo -> abre archivos
    # "a" -> agrega nueva info al final del archivo
    with open ("historial.csv", "a") as archivo:
        # linea se agrega después de la info que ya estaba en el archivo, sin eliminar nada previo
        archivo.write(linea)


def mostrarh():
    try:  #usamos try para que en caso se presente algún error, el código no se pare
        with open("historial.csv.", "r") as archivo: # historia.txt(abre el archivo) y "r" lo lee

            # lee el contenido del archivo y cada linea se guarda en la cadena "lineas"
            lineas = archivo.readlines()

            # readlines() -> internamente divide el código por saltos de línea, en done cada parte separada se guarda
            # como un elemento independiente en una lista

            #verificar si existe un contenido(historial)
        if not lineas: #si no hay lineas
            print("No hay partidas registradas")# si no hay historial te imprime que no hay
            return

            # si ponemos: return "No hay partidas registradas", tendríamos que llamar a la función después

        historial = [] #Crea una lista vacía que se usará para guardar los datos de las partidas de forma organizadaa
        for linea in lineas: #inicia un bucle que recorre cada linea que se  leyo el archivo
            partes = [p.strip() for p in linea.strip().split(",")]  # .strip :elimina espacios enblanco y saltos de linea al principio
            # .split: Divide la línea en partes más pequeñas (una lista de strings) utilizando la coma (,) como separador. Esto significa que cada dato en tu archivo debe estar separado por una coma.
            # p.strip: elimina espacios en blanco adicionales  que puedan haber quedado en alguna parte
            if len(partes) == 6: #asegurar que solo procesa 5 lineas "nombre,nivel rsultado movimiento,fecha y hora"
                historial.append({ #si la linea es valida crea un diccionario
                    "nombre": partes[0],
                    "nivel": partes[1],
                    "resultado": partes[2],
                    "movimientos": partes[3],
                    "fecha_hora": partes[4],
                    "modo": partes[5]
                })

        #esto para mostrarlo en pantalla
        imprimir_historial(historial)

    except FileNotFoundError:
        print("No hay historial guardado aún")

def verificarusuarioexiste(nombre):
    try:
        # with open (... ) as archivo -> abre archivo
        # "r" -> se pone modo lectura
        with open("historial.csv", "r") as archivo:
            for linea in archivo:

                # encuentra el usuario
                # linea.startswith -> verifica que empieze exactamente con el nombre y una coma
                if linea.startswith(nombre + ","):
                    return True
        # no encuentra al usuario
        # en caso ninguna lina del archico empieza con ese nombre y coma
        return False
    except FileNotFoundError:
        return False

def imprimir_historial(historial):

    print("%s" % ("=====  HISTORIAL DE JUEGOS  =====".center(60)))
    print()
    print("| %s | %s |  %s |%s |%s | %s |" % ("Nombre".center(11), "Fecha y hora".center(19), "Nivel".center(5), "Resul.".center(7), "Mov.".center(5), "Modo".center(10)))
    print("|%s| %s" % (" ___________ ".center(12), "___________________ | ______ | ______ | ____ | __________ |"))

    # Imprime cada fila del historial
    for juego in historial:
        # juegos es un diccionario por la forma en que se construye, las claves serían: nombre, nivel, resultado
        # historial -> línea 47
        # ajustamos los anchos y nombres para que coincidan con la imagen

        nombre = f"{juego['nombre']:^12}"            # 10 espacios, alineado a la izquierda
        fecha_hora = f"{juego['fecha_hora']:<19}"   # 19 espacios, alineado a la izquierda
        nivel = f"{juego['nivel']:^6}"              # 5 espacios, centrado

        # accede al valor de la clave "resultado" del diccionario juego
        # en la línea 18, se especifica que el orden de cada lína que se guarda en archivo, ahí se ha establecido el lugar de la variable resutaldo
        resultado = juego['resultado']

        # evalua si el texto de "resultado" en minusculas empieza con las letras "gan"
        if resultado.lower().startswith("gan"):
            resultado = "Gano"

        else:
            resultado = "Aband."

        resultado = f"{resultado:<6}"
        movimientos = f"{juego['movimientos']:^4}"
        modo = f"{juego['modo']:^10}"

        print(f"| {nombre}| {fecha_hora} | {nivel} | {resultado} | {movimientos} | {modo} |")


def mostrar_estadisticas():
    try:
        with open("historial.csv", "r") as archivo:
            lineas = archivo.readlines()

        if not lineas:
            print("No hay partidas registradas para mostrar estadísticas.")
            return

        total_partidas = 0
        victorias = 0
        movimientos_totales = 0
        victorias_por_usuario = {}      #CONTADORES DE DATOS

        niveles_cantidad = {}   #DICCIONARIO DE DATOS

        for linea in lineas:
            partes = [p.strip() for p in linea.split(",")]

            if len(partes) < 6: # en caso haya error (no se guardó algún dato)
                continue    # continuamos con el código
            nombre, nivel, resultado, movimientos, fecha, modo = partes
            total_partidas = total_partidas + 1 # estamos contando las líneas correctas, sin errores

            try:
                movimientos = int(movimientos)          #ITERACION DE DATOS
            except ValueError:
                movimientos = 0 # en caso movimientos no sea un numero, solamente por si aca
                # mejor prevenir que lamentar, uno nunca sabe

            movimientos_totales += movimientos

            # contar victorias
            if resultado.lower().startswith("gan"):
                victorias += 1
                if nombre not in victorias_por_usuario:
                    victorias_por_usuario[nombre] = 0
                victorias_por_usuario[nombre] += 1

            # contar partidas por nivel
            # is digit verifica si el nivel es digito
            if nivel.isdigit() or nivel == "Duda":
                if nivel not in niveles_cantidad:
                    niveles_cantidad[nivel] = 0
                niveles_cantidad[nivel] += 1

        porcentaje_victorias = round((victorias / total_partidas) * 100,2 )

        # para que no salga error al divider entre 0
        if total_partidas > 0:
            promedio_movimientos = round(movimientos_totales / total_partidas, 2)
        elif total_partidas == 0:
            promedio_movimientos = 0


        # detectar el jugador con más victorias
        jugador_top = "N/A"
        mayor_numero_de_victorias = 0

        for jugador, victorias in victorias_por_usuario.items():
            if victorias > mayor_numero_de_victorias:
                mayor_numero_de_victorias = victorias
                jugador_top = jugador

        # mostrar estadísticas
        print("----------------------------------------------------------")
        print("%s" % ("===== ESTADÍSTICAS GENERALES =====".center(58)))
        print()
        print("Total de partidas jugadas:", f"{total_partidas:>15}")
        print("Total de victorias:", f"{victorias:>21}")
        print("Porcentaje de victorias:", f"{porcentaje_victorias:>20}%")
        print(f"Promedio de movimientos por partida:", f"{promedio_movimientos:>7}")
        print(f"Jugador con más victorias:", f"{jugador_top:>16} ({mayor_numero_de_victorias:} victorias)\n")

        print("Partidas por nivel:")
        
        #sorted --> crea un nueva lista de tuplas 
        #se ordena por el valor inicial de cada tupla --> viene a ser la clave del diccionario
        #al venir de un archivo todo es leido como str
        #comparación por su valor ASCII
        for niv, cant in sorted(niveles_cantidad.items()):
            print(f"{"Nivel":>9}", f"{niv}: {cant} partidas")
        print()
        print("----------------------------------------------------------")

    except FileNotFoundError:
        print("No hay historial guardado aún.")



import os
import csv
import psycopg2


# Conectar a la base de datos
def conectar_db():
    try:
        conn = psycopg2.connect(
        host="cc3201.dcc.uchile.cl",
        database="cc3201",
        user="cc3201",
        password="brawl",
        port="5519",
        options="-c statement_timeout=60000"  # 60 segundos de tiempo de espera
        )
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Insertar en la tabla Mes
def insertar_mes(conn, meses):
    try:
        cursor = conn.cursor()
        for mes in meses:
            query = "INSERT INTO ProyectBrawlStars.Mes (nombre_mes, anio) VALUES (%s, %s)"
            cursor.execute(query, (mes, 2023))
        conn.commit()
        print("Tabla Mes poblada exitosamente.")
    except Exception as e:
        print("Error al insertar en la tabla Mes:", e)
        conn.rollback()
    finally:
        cursor.close()

# Insertar en la tabla Pais
def insertar_pais(conn, paises):
    try:
        cursor = conn.cursor()
        for pais in paises:
            query = "INSERT INTO ProyectBrawlStars.Pais (nombre_pais) VALUES (%s)"
            cursor.execute(query, (pais,))
        conn.commit()
        print("Tabla Pais poblada exitosamente.")
    except Exception as e:
        print("Error al insertar en la tabla Pais:", e)
        conn.rollback()
    finally:
        cursor.close()

# Insertar en la tabla Brawler
def insertar_brawler(conn, brawlers):
    try:
        cursor = conn.cursor()
        for brawler in brawlers:
            query = """
            INSERT INTO ProyectBrawlStars.Brawler (nombre_brawler) 
            VALUES (%s)
            ON CONFLICT (nombre_brawler) DO NOTHING
            """
            cursor.execute(query, (brawler,))
        conn.commit()
        print("Tabla Brawler poblada exitosamente.")
    except Exception as e:
        print("Error al insertar en la tabla Brawler:", e)
        conn.rollback()
    finally:
        cursor.close()

# Insertar en la tabla Club
def insertar_clubes(conn, ruta_directorio, paises):
    try:
        cursor = conn.cursor()
        archivos = [archivo for archivo in os.listdir(ruta_directorio) if archivo.endswith(".csv")]

        for indice, archivo in enumerate(archivos): 
            ruta_archivo = os.path.join(ruta_directorio, archivo)

            with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
                lector_csv = csv.reader(csvfile)
                next(lector_csv)  

                for fila in lector_csv:
                    tag_club = fila[1]
                    nombre_club = fila[2]
                    nombre_pais = paises[indice]

                    query = """
                    INSERT INTO ProyectBrawlStars.Club (tag_club, nombre_club, nombre_pais)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (tag_club) DO NOTHING
                    """
                    cursor.execute(query, (tag_club, nombre_club, nombre_pais))

        conn.commit()
        print(f"Tabla Club poblada exitosamente desde la ruta: {ruta_directorio}")
    except Exception as e:
        print(f"Error al insertar en la tabla Club desde la ruta {ruta_directorio}:", e)
        conn.rollback()
    finally:
        cursor.close()

# Insertar en la tabla Jugador
def insertar_jugadores(conn, ruta_directorio, paises):
    try:
        cursor = conn.cursor()
        archivos = [archivo for archivo in os.listdir(ruta_directorio) if archivo.endswith(".csv")]

        for indice, archivo in enumerate(archivos): 
            ruta_archivo = os.path.join(ruta_directorio, archivo)

            with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
                lector_csv = csv.reader(csvfile)
                next(lector_csv)  

                for fila in lector_csv:
                    tag_jugador = fila[1]
                    nombre_jugador = fila[2]
                    color_nombre = fila[3]
                    icono = fila[4]
                    nombre_pais = paises[indice]

                    # Inserta el jugador en la tabla y omite si el tag ya existe
                    query = """
                    INSERT INTO ProyectBrawlStars.Jugador (tag_jugador, nombre_jugador, color_nombre, icono, nombre_pais)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (tag_jugador) DO UPDATE SET 
                        nombre_jugador = EXCLUDED.nombre_jugador,
                        color_nombre = EXCLUDED.color_nombre,
                        icono = EXCLUDED.icono,
                        nombre_pais = EXCLUDED.nombre_pais
                    """
                    cursor.execute(query, (tag_jugador, nombre_jugador, color_nombre, icono, nombre_pais))

        conn.commit()
        print(f"Tabla Jugador poblada exitosamente desde la ruta: {ruta_directorio}")
    except Exception as e:
        print(f"Error al insertar en la tabla Jugador desde la ruta {ruta_directorio}:", e)
        conn.rollback()
    finally:
        cursor.close()
    
#Insertar en la tabla JuegaCon

def insertar_juega_con(conn, ruta_carpeta, nombre_mes, brawlers):
    try:
        cursor = conn.cursor()
        archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".csv")]
        i = 0 

        for archivo_csv in archivos:
            ruta_archivo = os.path.join(ruta_carpeta, archivo_csv)

            # Leer el archivo CSV
            with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) 

                for fila in reader:
                    tag_jugador = fila[1]
                    trofeos = int(fila[5])
                    puesto = int(fila[6])
                    nombre_brawler = brawlers[i]  

                    # Insertar los datos en la tabla JuegaCon
                    query = """
                        INSERT INTO ProyectBrawlStars.JuegaCon (tag_jugador, nombre_brawler, nombre_mes, trofeos, puesto)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                        """
                    cursor.execute(query, (tag_jugador, nombre_brawler, nombre_mes, trofeos, puesto))
            i += 1

        # Confirmar los cambios en la base de datos
        conn.commit()
        print(f"Datos insertados correctamente en la tabla JuegaCon desde {ruta_carpeta}.")
    except Exception as e:
        print(f"Error al cargar los datos en la tabla JuegaCon desde {ruta_carpeta} donde:", e)
        conn.rollback()
    finally:
        cursor.close()

#Insertar Ranking_Club_Pais
def insertar_Ranking_Club_País(conn, ruta_carpeta, nombre_mes, paises):
    try:
        cursor = conn.cursor()
        archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".csv")]
        i = 0 

        for archivo_csv in archivos:
            ruta_archivo = os.path.join(ruta_carpeta, archivo_csv)

            # Leer el archivo CSV
            with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) 

                for fila in reader:
                    tag_club = fila[1]
                    trofeos = int(fila[4])
                    puesto = int(fila[5])
                    nombre_pais = paises[i]  

                    # Insertar los datos en la tabla JuegaCon
                    query = """
                        INSERT INTO ProyectBrawlStars.Ranking_Club_Pais (tag_club, nombre_pais, nombre_mes, trofeos, puesto)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                        """
                    cursor.execute(query, (tag_club, nombre_pais, nombre_mes, trofeos, puesto))
            i += 1

        # Confirmar los cambios en la base de datos
        conn.commit()
        print(f"Datos insertados correctamente en la tabla Ranking_Club_País desde {ruta_carpeta}.")
    except Exception as e:
        print(f"Error al cargar los datos en la tabla Ranking_Club_País desde {ruta_carpeta} donde:", e, )
        conn.rollback()
    finally:
        cursor.close()


#Insertar Evolucion_Club
def insertar_Evolucion_Club(conn, ruta_carpeta, nombre_mes):
    try:
        cursor = conn.cursor()
        archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".csv")]


        for archivo_csv in archivos:
            ruta_archivo = os.path.join(ruta_carpeta, archivo_csv)

            # Leer el archivo CSV
            with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) 

                for fila in reader:
                    tag_club = fila[1]
                    trofeos_totales = int(fila[4])
                    miembros = int(fila[6])
 

                    # Insertar los datos en la tabla JuegaCon
                    query = """
                        INSERT INTO ProyectBrawlStars.Evolucion_Club (tag_club, nombre_mes, trofeos_totales, miembros)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                        """
                    cursor.execute(query, (tag_club, nombre_mes, trofeos_totales, miembros))


        # Confirmar los cambios en la base de datos
        conn.commit()
        print(f"Datos insertados correctamente en la tabla Evolucion_Club desde {ruta_carpeta}.")
    except Exception as e:
        print(f"Error al cargar los datos en la tabla Evolucion_Club desde {ruta_carpeta} donde:", e)
        conn.rollback()
    finally:
        cursor.close()
 

 #Insertar Ranking_Jugador_Pais
def insertar_Ranking_Jugador_Pais(conn, ruta_carpeta, nombre_mes, paises):
    try:
        cursor = conn.cursor()
        archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".csv")]
        i = 0

        for archivo_csv in archivos:
            ruta_archivo = os.path.join(ruta_carpeta, archivo_csv)

            # Leer el archivo CSV
            with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) 

                for fila in reader:
                    tag_jugador = fila[1]
                    trofeos_totales = int(fila[5])
                    puesto = int(fila[6])
                    nombre_pais = paises[i]
 

                    # Insertar los datos en la tabla JuegaCon
                    query = """
                        INSERT INTO ProyectBrawlStars.Ranking_Jugador_Pais (tag_jugador, nombre_pais, nombre_mes, trofeos_totales, puesto)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                        """
                    cursor.execute(query, (tag_jugador, nombre_pais, nombre_mes, trofeos_totales, puesto))
            i+=1

        # Confirmar los cambios en la base de datos
        conn.commit()
        print(f"Datos insertados correctamente en la tabla Ranking_Jugador_Pais desde {ruta_carpeta}.")
    except Exception as e:
        print(f"Error al cargar los datos en la tabla Ranking_Jugador_Pais desde {ruta_carpeta} donde:", e)
        conn.rollback()
    finally:
        cursor.close()

 #Insertar Trofeos_Pais_200_Player
def insertar_Trofeos_Pais_200_Player(conn, ruta_carpeta, nombre_mes, paises):
    try:
        cursor = conn.cursor()
        archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".csv")]
        i = 0

        for archivo_csv in archivos:
            ruta_archivo = os.path.join(ruta_carpeta, archivo_csv)
            trofeos_totales = 0
            # Leer el archivo CSV
            with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) 


                for fila in reader:
                    trofeos_totales += int(fila[5])
                
                nombre_pais = paises[i]
                # Insertar los datos en la tabla Trofeos_Pais_200_Player
                query = """
                    INSERT INTO ProyectBrawlStars.Trofeos_Pais_200_Player (nombre_pais, nombre_mes, trofeos_totales)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """
                cursor.execute(query, (nombre_pais, nombre_mes, trofeos_totales))
            i+=1

        # Confirmar los cambios en la base de datos
        conn.commit()
        print(f"Datos insertados correctamente en la tabla Trofeos_Pais_200_Player desde {ruta_carpeta}.")
    except Exception as e:
        print(f"Error al cargar los datos en la tabla Trofeos_Pais_200_Player desde {ruta_carpeta} donde:", e)
        conn.rollback()
    finally:
        cursor.close()

 #Insertar Trofeos_Pais_200_Club
def insertar_Trofeos_Pais_200_Club(conn, ruta_carpeta, nombre_mes, paises):
    try:
        cursor = conn.cursor()
        archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".csv")]
        i = 0

        for archivo_csv in archivos:
            ruta_archivo = os.path.join(ruta_carpeta, archivo_csv)
            trofeos_totales = 0
            integrantes_totales = 0
            # Leer el archivo CSV
            with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) 


                for fila in reader:
                    trofeos_totales += int(fila[4])
                    integrantes_totales += int(fila[6])
                
                nombre_pais = paises[i]
                # Insertar los datos en la tabla Trofeos_Pais_200_Player
                query = """
                    INSERT INTO ProyectBrawlStars.Trofeos_Pais_200_Club (nombre_pais, nombre_mes, trofeos_totales, integrantes_totales)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """
                cursor.execute(query, (nombre_pais, nombre_mes, trofeos_totales, integrantes_totales))
            i+=1

        # Confirmar los cambios en la base de datos
        conn.commit()
        print(f"Datos insertados correctamente en la tabla Trofeos_Pais_200_Club desde {ruta_carpeta}.")
    except Exception as e:
        print(f"Error al cargar los datos en la tabla Trofeos_Pais_200_Club desde {ruta_carpeta} donde:", e)
        conn.rollback()
    finally:
        cursor.close()

#Insertar Trofeos_200_Brawler
def insertar_Trofeos_200_Brawler(conn, ruta_carpeta, nombre_mes, brawlers):
    try:
        cursor = conn.cursor()
        archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".csv")]
        i = 0

        for archivo_csv in archivos:
            ruta_archivo = os.path.join(ruta_carpeta, archivo_csv)
            trofeos_totales = 0
            # Leer el archivo CSV
            with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) 


                for fila in reader:
                    trofeos_totales += int(fila[5])
                
                nombre_brawler = brawlers[i]
                # Insertar los datos en la tabla Trofeos_Pais_200_Player
                query = """
                    INSERT INTO ProyectBrawlStars.Trofeos_200_Brawler (nombre_brawler, nombre_mes, trofeos_totales)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """
                cursor.execute(query, (nombre_brawler, nombre_mes, trofeos_totales))
            i+=1

        # Confirmar los cambios en la base de datos
        conn.commit()
        print(f"Datos insertados correctamente en la tabla Trofeos_200_Brawler desde {ruta_carpeta}.")
    except Exception as e:
        print(f"Error al cargar los datos en la tabla Trofeos_200_Brawler desde {ruta_carpeta} donde:", e)
        conn.rollback()
    finally:
        cursor.close()


# Generamos un main que use todas las funciones anteriores jeje
def main():
    conn = conectar_db()
    if conn:
        meses = ["August", "February", "March", "November", "October", "September"]
        paises = ["Afghanistan", "Åland_Islands","Albania", "Algeria", "American_Samoa", "Andorra", "Angola", "Anguilla", "Antarctica", "Antigua_and_Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia,_Plurinational_State", "Bonaire,_Sint_Eustatius_and_Saba", "Bosnia_and_Herzegovina", "Botswana", "Bouvet", "Brazil", "British_Indian_Ocean_Territory", "Brunei", "Bulgaria", "Burkina_Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape_Verde", "Cayman_Islands", "Central_African_Republic", "Chad", "Chile", "China", "Christmas_Island", "Coco_(Keeling)_Islands", "Colombia", "Comoros", "Congo,_the_Democratic_Republic_of_the", "Congo", "Cook_Islands", "Costa_Rica", "Côte_dlvoire", "Croatia", "Cuba", "Curaçao", "Cyprus", "Czech_Republic", "Denmark", "Djibouti", "Dominica", "Dominican_Republic", "Ecuador", "Egypt", "El_Salvador", "Equatorial_Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland_Islands_(Malvinas)", "Faroe_Islands", "Fiji", "Finland", "France", "French_Guiana", "French_Polynesia", "French_Southern_Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard_Island_and_McDonald_Islands", "Holy_See_(Vatican_City_State)", "Honduras", "Hong_Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran,_Islamic_Republic", "Iraq", "Ireland", "Isle_of_Man", "Israel", "Italy", "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea,_Democratic_Peoples_Republic", "Korea,_Republic", "Kuwait", "Kyrgyzstan", "Lao_Peoples_Democratic_Republic", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macao", "Macedonia,_the_former_Yugoslav_Republic", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall_Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia,_Federated_States", "Moldova,_Republic", "Monaco", "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New_Caledonia", "New_Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk_Island", "Northern_Mariana", "Norway", "Oman", "Pakistan", "Palau", "Palestine,_State", "Panama", "Papua_New_Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto_Rico", "Qatar", "Réunion", "Romania", "Russia_Federation", "Rwanda", "Saint_Barthélemy", "Saint_Helena,_Ascension_and_Tristan_da_Cunha", "Saint_Kitts_and_Nevis", "Saint_Lucia", "Saint_Martin_(French_part)", "Saint_Pierre_and_Miquelon", "Saint_Vincent_and_the_Grenadines", "Samoa", "San_Marino", "Sao_Tome_and_Principe", "Saudi_Arabia", "Senegal", "Serbia", "Seychelles", "Sierra_Leone", "Singapore", "Sint_Maarten_(Dutch_part)", "Slovakia", "Slovenia", "Solomon_Islands", "Somalia", "South_Africa", "South_Sudan", "Spain", "Sri_Lanka", "Sudan", "Suriname", "Svalbard_and_Jan_Mayen", "Swaziland", "Sweden", "Switzerland", "Syrian_Arab_Republic", "Taiwan,_Province_of_China", "Tajikistan", "Tanzania,_United_Republic_of", "Thailand", "Timor-Leste", "Togo", "Tokelau", "Tonga", "Trinidad_and_Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks_and_Caicos_Islands", "Tuvalu", "Uganda", "Ukraine", "United_Arab_Emirates", "United_Kingdom", "United_States", "United_States_Minor_Outlying_Islands", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela,_Bolivarian_Republic_of", "Viet_Nam", "Virgin_Islands,_British", "Virgin_Islands,_U.S.", "Wallis_and_Futuna", "Western_Sahara", "Yemen", "Zambia", "Zimbabwe"]
        brawlersMarchFeb = ["8-BIT", "AMBER", "ASH", "BARLEY", "BEA", "BELLE", "BIBI", "BO", "BONNIE", "BROCK", "BULL", "BUSTER", "BUZZ", "BYRON", "CARL", "CHESTER", "COLLETTE", "COLT", "CROW", "DARRYL", "DYNAMIKE", "EDGAR", "EL PRIMO", "EMZ", "EVE", "FANG", "FRANK", "GALE", "GENE", "GRAY", "GRIFF", "GROM", "GUS", "JACKY", "JANET", "JESSIE", "LEON", "LOLA", "LOU", "MANDY", "MAX", "MEG", "MORTIS", "MR. P", "NANI", "NITA", "OTIS", "PAM", "PENNY", "PIPER", "POCO", "R-T", "RICO", "ROSA", "RUFFS", "SAM", "SANDY", "SHELLY", "SPIKE", "SPROUT", "SQUEAK", "STU", "SURGE", "TARA", "TICK", "WILLOW"]
        brawlersAugust = ["8-BIT", "AMBER", "ASH", "BARLEY", "BEA", "BELLE", "BIBI", "BO", "BONNIE", "BROCK", "BULL", "BUSTER", "BUZZ", "BYRON", "CARL", "CHESTER", "COLLETTE", "COLT", "CORDELIUS", "CROW", "DARRYL", "DOUG", "DYNAMIKE", "EDGAR", "EL PRIMO", "EMZ", "EVE", "FANG", "FRANK", "GALE", "GENE", "GRAY", "GRIFF", "GROM", "GUS", "HANK", "JACKY", "JANET", "JESSIE", "LEON", "LOLA", "LOU", "MAISIE", "MANDY", "MAX", "MEG", "MORTIS", "MR. P", "NANI", "NITA", "OTIS", "PAM", "PENNY", "PIPER", "POCO", "R-T", "RICO", "ROSA", "RUFFS", "SAM", "SANDY", "SHELLY", "SPIKE", "SPROUT", "SQUEAK", "STU", "SURGE", "TARA", "TICK", "WILLOW"]
        brawlers = ["8-BIT", "AMBER", "ASH", "BARLEY", "BEA", "BELLE", "BIBI", "BO", "BONNIE", "BROCK", "BULL", "BUSTER", "BUZZ", "BYRON", "CARL", "CHARLIE", "CHESTER", "CHUCK", "COLLETTE", "COLT", "CORDELIUS", "CROW", "DARRYL", "DOUG", "DYNAMIKE", "EDGAR", "EL PRIMO", "EMZ", "EVE", "FANG", "FRANK", "GALE", "GENE", "GRAY", "GRIFF", "GROM", "GUS", "HANK", "JACKY", "JANET", "JESSIE", "LEON", "LOLA", "LOU", "MAISIE", "MANDY", "MAX", "MEG", "MORTIS", "MR. P", "NANI", "NITA", "OTIS", "PAM", "PEARL", "PENNY", "PIPER", "POCO", "R-T", "RICO", "ROSA", "RUFFS", "SAM", "SANDY", "SHELLY", "SPIKE", "SPROUT", "SQUEAK", "STU", "SURGE", "TARA", "TICK", "WILLOW"]


        #insertar_mes(conn, meses)
        #insertar_pais(conn, paises)
        #insertar_brawler(conn, brawlers)

        #for mes in meses:
            #insertar_clubes(conn, f'database/mensuales/month data - {mes} 2023/country_club_rankings', paises)
        #for mes in meses:
            #ruta1 = f"database/mensuales/month data - {mes} 2023/country_player_rankings"
            #insertar_jugadores(conn, ruta1, paises)
            #ruta2 = f"database/mensuales/month data - {mes} 2023/brawler_ranking"
            #insertar_jugadores(conn, ruta2, paises)

        #insertar_juega_con(conn, f'database/mensuales/month data - February 2023/brawler_ranking', "February", brawlersMarchFeb)
        #insertar_juega_con(conn, f'database/mensuales/month data - March 2023/brawler_ranking', "March", brawlersMarchFeb)
        #insertar_juega_con(conn, f'database/mensuales/month data - August 2023/brawler_ranking', "August", brawlersAugust)
        #insertar_juega_con(conn, f'database/mensuales/month data - November 2023/brawler_ranking', "November", brawlers)
        #insertar_juega_con(conn, f'database/mensuales/month data - October 2023/brawler_ranking', "October", brawlers)
        #insertar_juega_con(conn, f'database/mensuales/month data - September 2023/brawler_ranking', "September", brawlers)
        
        #for mes in meses:
            #insertar_Ranking_Club_País(conn, f'database/mensuales/month data - {mes} 2023/country_club_rankings', mes, paises)
            #insertar_Evolucion_Club(conn, f'database/mensuales/month data - {mes} 2023/country_club_rankings', mes)
            #insertar_Ranking_Jugador_Pais(conn, f"database/mensuales/month data - {mes} 2023/country_player_rankings", mes, paises)
            #insertar_Trofeos_Pais_200_Player(conn, f"database/mensuales/month data - {mes} 2023/country_player_rankings", mes, paises)
            #insertar_Trofeos_Pais_200_Club(conn, f'database/mensuales/month data - {mes} 2023/country_club_rankings', mes, paises)


        insertar_Trofeos_200_Brawler(conn, f'database/mensuales/month data - February 2023/brawler_ranking', "February", brawlersMarchFeb)
        insertar_Trofeos_200_Brawler(conn, f'database/mensuales/month data - March 2023/brawler_ranking', "March", brawlersMarchFeb)
        insertar_Trofeos_200_Brawler(conn, f'database/mensuales/month data - August 2023/brawler_ranking', "August", brawlersAugust)
        insertar_Trofeos_200_Brawler(conn, f'database/mensuales/month data - November 2023/brawler_ranking', "November", brawlers)
        insertar_Trofeos_200_Brawler(conn, f'database/mensuales/month data - October 2023/brawler_ranking', "October", brawlers)
        insertar_Trofeos_200_Brawler(conn, f'database/mensuales/month data - September 2023/brawler_ranking', "September", brawlers)
        conn.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()

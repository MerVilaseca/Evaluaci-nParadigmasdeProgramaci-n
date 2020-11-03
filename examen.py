
# librerias propias
import os 

# librerias especiales
import pandas as pd

RESUME_FILE = './src/resumen_legajo.csv'
VACACIONES_TOMADAS_FILE = './src/vaciones_tomadas.csv'

COLUMNS_RESUMEN_LEGAJO = ['Legajo','Apellido','Nombre','Total Vacaciones']


def load_csv(file_path):
    """
    Carga de archivo csv
    """
    print(f"Buscando archivo {RESUME_FILE.split('/')[-1]}....")

    if os.path.isfile(RESUME_FILE) == False:
        print('archivo no existe, se procederá a crear uno...')
        return pd.DataFrame(columns=COLUMNS_RESUMEN_LEGAJO)
    return pd.read_csv(file_path,sep=';')


def sobreescribiendo_df(df):
    """
    Creando nuevo dataframe
    """
    print('ingrese los nuevos datos')

    df_new = pd.DataFrame()
    while True:
        dicx = {}
        
        dicx['Legajo'] = input('ingrese el cod legajo')
        dicx['Apellido'] = input('ingrese el nombre')
        dicx['Nombre'] = input('ingrese el apellido')
        dicx['Total Vacaciones'] = input('ingrese el total vacaciones')
        
        df_new.append(dicx, columns=COLUMNS_RESUMEN_LEGAJO)

        op = input('Desea seguir ingresando nuevos datos? y|n')
        if 'n' == op.lower():
            break
    
    df.to_csv('./src/resumen_legajo_backup.csv', index=False, sep=';')
    # nuevo
    df_new.to_csv(RESUME_FILE, sep=';', index=False)

def modificar_df(df_resumen, codigo_legado):
    """
    Modificar archivo legado
    """
    print('ingrese el código de legado que desea modificar')
    if codigo_legado not in df_resumen['Legajo'].unique():
        print(f'codigo legajo ingresado no existe, {codigo_legado}')
        return

    df = df_resumen[df_resumen['Legajo'] == codigo_legado]

    df['Apellido'] = input('Apellido: ')
    df['Nombre'] = input('Nombre: ')
    df['Total Vacaciones'] = int(input('Total Vacaciones: '))

    df.to_csv(RESUME_FILE, index=False, sep=';')


def vaciones_restantes(df_resumen, df_detalle, codigo_legado):
    """
    Determina la cantidad de vacaciones restantes según el código de legajo
    """
    if codigo_legado not in df_resumen['Legajo'].unique():
        print(f'codigo legajo ingresado no existe, {codigo_legado}')
        return
    
    df_union = df_resumen.merge(df_detalle,how='right',left_on='Legajo',right_on='Legajo')
    df_legajo = df_union[df_union['Legajo']== codigo_legado ]


    nombre_completo = list(df_legajo['Nombre'])[0] + ' ' + list(df_legajo['Apellido'])[0]
    total_vacaciones = list(df_legajo['Total Vacaciones'])[0]
    vacaciones_tomadas = df_legajo['Fecha'].count()

    print(f'Legajo {codigo_legado}: {nombre_completo} , le restan {total_vacaciones - vacaciones_tomadas} de vacaciones')

# programa principal
def main():
    """
    Programa principal
    """

    print("Bienvenido al menú interactivo")
    while(True):
        print("""\n\n
        ¿Qué queres hacer? Escribe una opción
        1) Cargar datos tabla Resumen Legajo
        2) Mostrar días disponibles de vaciones por empleado
        3) Salir""")
        opcion = input()
        if opcion == '1':
            # Mostrando archivo en pantalla
            df = load_csv(RESUME_FILE)
            print(df)

            print("""\n
                ¿Qué acción desea realizar? Escribe una opción
                1) Sobreescribir archivo
                2) Modificar archivo 
                3) Retornar al menú principal""")
            opcion_submenu = input()
            # submenu opciones
            if opcion_submenu == '1':
                sobreescribiendo_df(df)

            elif opcion_submenu == '2':
                codigo_legado = int(input('Ingrese el código de Legajo ...\n'))
                
                # procesando
                modificar_df(df, codigo_legado)

            elif opcion_submenu == '3':
                continue
            else:
                print("Comando desconocido, vuelve a intentarlo")
        
        elif opcion == '2':
            codigo_legado = int(input('Ingrese el código de Legajo ...\n'))
            
            df_resumen = load_csv(RESUME_FILE)
            df_detalle = load_csv(VACACIONES_TOMADAS_FILE)

            # procesando solicitud
            vaciones_restantes(df_resumen, df_detalle, codigo_legado)

        elif opcion =='3':
            print("¡Hasta luego! Ha sido un placer ayudarte")
            break
        else:
            print("Comando desconocido, vuelve a intentarlo")

# Ejecucion programa principal
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)


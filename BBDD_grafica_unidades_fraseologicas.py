#   se supone que esto debe ejecutarse en Windows
import os
import json
"""import boto3
from botocore.exceptions import ClientError"""
#from boto3.dynamodb import Table
#  ARN del rol   DynamoDBRole_full_ADMIN   : arn:aws:iam::590183836735:role/DynamoDBRole_full_ADMIN
#instalamos de nuevo Python, por ejemplo Python 3.10      por si acaso, con winget por ejemplo, un gestor de paquetes ya integrado en Windows
print("\n\t\t Comprobando que Python 3.10 está instalado.....")
os.system('winget install "Python.Python.3.10"')
#print("\n\t\t Comprobando que librerías boto3 y AWS están instaladas.....")

#instalamos por si no lo estuviera, AWS y boto3
"""os.system("pip install AWS")            #   Instala y configura AWS CLI con tus credenciales de AWS, aunque las credenciales irán aparte
os.system("pip install boto3")          #   Instala Boto3, el SDK de Python para AWS, con el comando pip install boto3

# Establece la región de DynamoDB
region = "us-east-1"

# Crea una sesión en la región deseada
session = boto3.Session(region_name=region)

# Crea un cliente de STS
sts_client = session.client('sts')"""


#boto3.set_stream_logger('botocore', level='DEBUG')

# Asume el rol y obtén las credenciales temporales
"""assumed_role = sts_client.assume_role(
    RoleArn="arn:aws:iam::xxxxxxxxxxxxxxxxxx:role/xxxxxxxxxxxxxxxx",
    RoleSessionName="AssumeRoleSession1"
)"""
"""assumed_role = sts_client.assume_role(
    RoleArn="arn:aws:iam::xxxxxxxxxx:user/xxxxxxxxxxxxxxx",
    RoleSessionName="AssumeRoleSession1"
)"""
"""#credentials = assumed_role['Credentials']
credentials = {}

# Crea un cliente de DynamoDB usando las credenciales temporales
clave = input("Introduce clave de acceso:\t")
clave_sec = input("Introduce clave de acceso secreta:\t")
credentials['AccessKeyId'] = clave
credentials['SecretAccessKey'] = clave_sec
dynamodb = boto3.resource(      'dynamodb', 
                                aws_access_key_id=credentials['AccessKeyId'],
                                aws_secret_access_key=credentials['SecretAccessKey'],
                                #aws_session_token=credentials['SessionToken'],
                                region_name=region,
                                endpoint_url='https://dynamodb.us-east-1.amazonaws.com')"""

#aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
#aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
#aws_session_token=assumed_role['Credentials']['SessionToken'],

# Nombre de la tabla de DynamoDB
nombre_tabla = "unidades_fraseologicas"


# Inicializamos el diccionario vacío
db = {}
#db_aws = {}


# Abre el archivo existente y lee el diccionario, para que el diccionario se meta en memoria, y luego se le añada en memoria las adiciones, y luego se meta el diccionario nuevo con adicciones ( o sin ellas, igual solo hubo consultas)

#                           ES IMPERATIVO cambiar a la carpeta Descargas, más bien Downloads, para poder usar archivos sin recibir errores por permisos de usuario
#                           más concretamente con el error  [Errno 9] Bad file descriptor    
# Obtén el directorio actual
ruta = os.getcwd()

# Encuentra la posición del directorio 'Users' en la ruta
pos = ruta.index('Users')

# Trunca la ruta hasta 'Users/(usuario)/'
user_dir = ruta[:pos] + ruta[pos:ruta.index('\\', pos+6)+1]
print("user_dir:\t"+str(user_dir))


# Añade 'Downloads' a la ruta
downloads_dir = os.path.join(user_dir, 'Downloads')

# Cambia al directorio de descargas
os.chdir(downloads_dir)


filename = "unidades_fraseologicas.txt"  # Asegúrate de reemplazar esto con el nombre de tu archivo si has puesto otro nombre de archivo, al principio del código lo mismo

with open(filename, 'r', encoding='utf-8') as f:
    db = json.load(f)
    
try:
    f.close()
except:
    pass


def listar_db():
    os.system("cls")
    print("\n\t\t\tRecuerda que si un valor de una pareja clave-valor está entre corchetes ' [valor] ' es porque contiene una lista de varios valores ")
    print("\n\n")
    for v,k in db.items():
        if type(k) == list:
            db[v] = tuple(db[v])
            k = tuple(k)
        #print(str(type(k))+"\t"+str(type(db[v])))    #esto fue para comprobar que realmente cambió el tipo de lista a tupla
        print("clave: "+v+"\tvalor: "+str(k)+"\n")

while True:
    print("\n1. Añadir\n2. Buscar en claves\n3. Buscar en valores\n4. Buscar en ambos\n5. Borrar pareja clave-valor\n6. Borrar valor de una clave\n7. Borrar un string de una tupla\n8. Salir del programa\n9. Ver la BBDD completa\n\n\tRecuerda que introducir algo que no sea número te retendrá aquí")
    opcion = None
    while opcion not in list(range(1,10)):     
        try:
            opcion = int(input("Elige una opción (1-9): "))
        except ValueError:
            print("Por favor, introduce un número válido entre 1 y 8.")
            opcion = None
    opcion = int(opcion)
    if opcion == 1:
        clave = input("Introduce la clave: ").lower()
        valor = input("Introduce el valor: ").lower()
        if clave in db.keys():  # comprueba si esa clave introducida ya existe
            if type(db[clave]) is tuple and valor not in db[clave]:
                db[clave] = list(db[clave])
                db[clave].append(valor)
                db[clave] = tuple(db[clave])
            elif clave in db.keys() and (db[clave] is None or db[clave] == ''):  # comprueba si esa clave introducida ya existe y no tiene valor
                db[clave] = valor  # cambia el valor a lo que contenga la variable 'valor', pero sin estar haciendo el if anterior, que convierte al final en tupla añadiendo el valor del usuario, pero el primer elemento str queda en blanco
            elif type(db[clave]) is str and db[clave] != valor:
                db[clave] = [db[clave], valor]  # cambia el valor a una lista que contiene el valor existente y 'valor'
            if db[clave] == [""] or db[clave] == (""):  # esto por si acaso no hay nada en valor
                    db[clave] = valor
                    db[clave] = tuple(db[clave])
        elif db.get(clave) == valor:
                os.system("cls")
                print("\n\n\t Lo siento, pero ya existe una pareja clave-valor que coinciden exactamente con los que acabas de introducir")
        else:
                # Comprueba si el valor ya existe en el diccionario, tanto en uno de los string de una tupla como si está en algún valor string. Pero se hace después de haber comprobado en otro "if" que la clave no existe ya
            comprobador = False
            for k, v in db.items():
                if isinstance(v, tuple):
                # Si el valor es una tupla, comprueba si el valor está en la tupla
                    if valor in v:
                        print(f'La clave {k} tiene un valor que coincide: {v}')
                        comprobador = True
                else:
                # Si el valor no es una tupla, comprueba si el valor coincide
                    if v == valor:
                        print(f'La clave {k} tiene un valor que coincide: {v}')
                        comprobador = True
            if comprobador == False:
                db[clave] = valor
                print("pareja clave-valor añadida correctamente")
        
    elif opcion in [2, 3, 4]:
        palabra = input("Introduce la palabra a buscar: ").lower()
        for clave, valor in db.items():
            if opcion in [2, 4] and palabra in clave:
                print(f"Clave: {clave}\t,\t Valor: {valor}")
            else:
                print("\n\t\t Clave no encontrada")
            if opcion in [3, 4] and palabra in str(valor):
                print(f"Clave: {clave}\t,\t Valor: {valor}")
            else:
                print("\n\t\t Valor no encontrado")
    elif opcion == 5:
        clave = input("Introduce la clave de la pareja a borrar, debe coincidir exactamente: ").lower()
        if clave in db.keys():
            del db[clave]
        else:
            print("La clave no existe.")
    elif opcion == 6:
        clave = input("Introduce la clave del valor a borrar: ").lower()
        if clave in db.keys():
            db[clave] = ""
            print("valor de clave "+clave+" borrado, valor es tipo "+str(type(db[clave])))
        else:
            print("El valor no existe.")
    elif opcion == 7:
        clave = input("Introduce la clave de la pareja: ").lower()
        string = input("Introduce el string a borrar: ").lower()
        if clave in db and type(db[clave]) is tuple and string in db[clave]:
            db[clave] = list(db[clave])
            db[clave].remove(string)
            db[clave] = tuple(db[clave])
        else:
            print("La clave no existe o el string no está en la tupla.")
    elif opcion == 8:
        os.system("cls")
        print("\t\t\t\tSaliendo del programa...")
        break
    elif opcion == 9:
        os.system("pause")
        os.system("cls")
        opc = input("¿Prefieres ver la Base de Datos compacta o en lista por cada línea? Introduce:\tcompacta / lista\t: ")
        while opc not in ("compacta","lista") or type(opc) != str:
            opc = None
            os.system("cls")
            opc = input("¿Prefieres ver la Base de Datos compacta o en lista por cada línea?\n\t\t\tIntroduce:\tcompacta / lista\t: ")
#        print("type opc =  "+str(type(opc)))
        if opc == "compacta":
            print("\n\n\t\t\tContenido de la Base de Datos completa:\t"+str(db))
        elif opc == "lista":
            listar_db()


ruta = os.getcwd()
ruta_completa = os.path.join(ruta, filename)

# Compara los diccionarios y sincroniza los datos para que lo que no hay en 'db' pero sí en 'db_aws', esté en ambos
"""def aws_hacia_db():
    for clave in db_aws.keys():
        if clave not in db:
            db[clave] = db_aws[clave]
        elif db[clave] != db_aws[clave]:
            db[clave] = db_aws[clave]

# Compara los diccionarios y sincroniza los datos para que lo que no hay en 'db_aws' pero sí en 'db', esté en ambos
def db_hacia_aws():
    for clave in db.keys():
        if clave not in db_aws:
            db_aws[clave] = db[clave]
        elif db_aws[clave] != db[clave]:
            db_aws[clave] = db[clave]"""

#sync = input("""\n\n\t\tAhora tiene que elegir entre:\n\t1. \tSincronizar los datos leídos de la tabla sincronizada en AWS, hacia la tabla en local
#                    \n\t2. \tSincronizar los datos en local que no están en la nube y subirlos a la nube\n\t3. \tSincronizar ambos con lo que no tiene del otro\n\t4. Ignorar y seguir""")
"""while sync not in list(range(1,5)):     
        try:
            sync = int(input("Elige una opción (1-4): "))
        except ValueError:
            print("Por favor, introduce un número válido entre 1 y 4.")
            sync = None
sync = int(sync)
if sync == 1:
    aws_hacia_db()
    print("\n\t\t\t\tSincronización de AWS a los archivos locales correcta")
elif sync == 2:
    db_hacia_aws()
    print("\n\t\t\t\tSincronización de archivos locales a AWS correcta")
elif sync == 3:
    aws_hacia_db()
    db_hacia_aws()
    print("\n\t\t\t\tSincronización bidireccional entre local y AWS correcta")
elif sync == 4:
    pass
else:
    sync = None
    print("\n\n\tHa ocurrido un error, la entrada de usuario para elegir sincronización tiene un valor no permitido\n\t\t\tRevisar 0x000000059619583c")"""
#sync = None
os.system("pause"), os.system("cls")  # pausa y borrar lo impreso hasta el momento en consola para limpiar



'''#                                   ahora preguntar al usuario si quiere borrar de AWS lo que no esté en local
sync = input("\n\n\t\t\t¿Desea borrar en local todas las entradas de la tabla sincronizada en AWS que NO estén en local?\n\t\tY / N:\t")
while sync not in ('Y', 'N'):
    sync = input("\nY / N:\t")

if sync == 'Y':
# Compara las claves de db y db_aws en orden inverso para detectar claves que ya no existen en 'db_aws' , y borrarlas también de 'db'
    for clave in reversed(list(db.keys())):
        if clave not in db_aws:
            del db[clave]
elif sync == 'N':
    pass
else:
    sync = None
    os.system("pause")
    print("\n\n\tHa ocurrido un error, la entrada de usuario para elegir sincronización tiene un valor no permitido\n\t\t\tRevisar 0x000000059619583c")'''



"""table = dynamodb.Table(nombre_tabla)

# Actualiza la tabla de DynamoDB con los datos de db_aws
for clave, valor in db_aws.items():
    # Crea un objeto de actualización de elementos
    actualizacion = {
        'Key': {'clave': clave},
        'UpdateExpression': 'SET valor = :v',
        'ExpressionAttributeValues': {
            ':v': valor
        },
        'ReturnValues': 'UPDATED_NEW'
    }

# Establece los valores de clave y valor para la actualización
#actualizacion['ExpressionAttributeValues'][':k'] = clave

    # Intenta actualizar el elemento existente
    try:
        table.update_item(**actualizacion)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            # La clave no existe, crea un nuevo elemento
            # La clave no existe, crea un nuevo elemento
            table.put_item(Item={'clave': clave, 'valor': valor})
        else:
            raise e"""

#       ahora a sobreescribir en local con 'db'
try:
    with open(ruta_completa, 'w+', encoding='utf-8') as ff:  # es necesario sobreescribir, pues hemos leído el archivo, metido en la variable db como diccionario, le añadimos si el usuario lo hizo, y lo escribimos sobreeescribiendo todo lo anterior. Si no se añadieron cosas, seguirá igual, pero sino con más cosas
        #print("\t\tAbierto adecuadamente")
        if os.path.exists(ruta_completa):
            json.dump(db, ff, ensure_ascii=False)
    
except Exception as e:
    print(f"Ocurrió un error: {e}")
pregunta = None
#                       Ahora preguntamos al usuario hasta que introduzca "Y" o "N" para saber si quiere ver toda la BBDD
while pregunta == None or pregunta not in ("Y", "N"):
    pregunta = input("¿Quieres ver la BBDD en local entera? Introduce: Y / N: \t")

if pregunta == "Y":
    with open(ruta_completa,'r', encoding='utf-8') as f:
        """print(f"\n\t\tcontenido de  {filename} ")
        cont = f.read()
        print("\n\n\t\tcontenido:\t"+str(cont))
        f.close()
        del cont"""
        listar_db()
        """print("keys:\t "+str(db.keys()))         
        print("\tvalues:\t "+str(db.values()))
        del db"""                               # esto fue para probar a ver todas las claves y valores por separado
        os.system("pause")
        os.system("cls")
        "del os, pregunta"
        print("\t\t\t\t\t\t\tMuchas gracias, ¡Hasta pronto!")
else:
    os.system("cls")
    del os, pregunta, db
    print("\n\n")
    print("\t\t\t\t\t\t\tMuchas gracias, ¡Hasta pronto!")


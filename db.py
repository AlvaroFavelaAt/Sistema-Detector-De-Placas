import pyodbc

def conectar():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=SistemaPlacas;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None


def guardar_datos(nombre, telefono, direccion, placa, marca, modelo, año):
    try:
        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO Propietarios (nombre, telefono, direccion)
            OUTPUT INSERTED.id_propietario
            VALUES (?, ?, ?)
        """, (nombre, telefono, direccion))

        id_propietario = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO Vehiculos (placa, marca, modelo, año, id_propietario)
            VALUES (?, ?, ?, ?, ?)
        """, (placa, marca, modelo, año, id_propietario))

        conexion.commit()
        conexion.close()

        print("✅ Datos guardados correctamente")

    except Exception as e:
        print("❌ Error al guardar:", e)


def consultar_por_placa(placa):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT 
                V.placa, V.marca, V.modelo, V.año,
                P.nombre, P.telefono, P.direccion
            FROM Vehiculos V
            INNER JOIN Propietarios P
            ON V.id_propietario = P.id_propietario
            WHERE V.placa = ?
        """, (placa,))

        resultado = cursor.fetchone()
        conexion.close()
        return resultado

    except Exception as e:
        print("❌ Error al consultar:", e)
        return None

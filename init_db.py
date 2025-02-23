import sqlite3

DATABASE = 'keys.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Creamos la tabla de claves de activacion si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activation_keys (
            key TEXT PRIMARY KEY,
            used INTEGER DEFAULT 0
        )
    ''')
    # Inserta algunas claves de ejemplo (esto lo puedes personalizar o cargar desde otro origen)
    keys = [('clave123', 0), ('clave456', 0), ('clave789', 0)]
    for k, used in keys:
        try:
            cursor.execute('INSERT INTO activation_keys (key, used) VALUES (?, ?)', (k, used))
        except sqlite3.IntegrityError:
            # Si la clave ya existe, se ignora
            pass
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada.")

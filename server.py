from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'keys.db'

def obtener_conexion():
    return sqlite3.connect(DATABASE)

@app.route('/api/validar', methods=['GET'])
def validar_clave():
    clave = request.args.get('clave', '').strip()
    if not clave:
        return jsonify({'status': 'error', 'message': 'Falta la clave'}), 400

    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT used FROM activation_keys WHERE key=?', (clave,))
    resultado = cursor.fetchone()

    if resultado is None:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Clave inválida'}), 400
    elif resultado[0] == 1:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Clave ya utilizada'}), 400
    else:
        # Marca la clave como usada
        cursor.execute('UPDATE activation_keys SET used=1 WHERE key=?', (clave,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'OK', 'message': 'Activación exitosa'}), 200

if __name__ == '__main__':
    # En producción se recomienda usar un servidor WSGI y HTTPS
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def conectar_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="livros",
            user="teste_livros",  # Usando o usuário com permissões
            password="minha_senha_segura"  # Usando a senha do usuário
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@app.route('/', methods=['GET'])
def pagina_inicial():
    print('Página inicial do Sistema de Biblioteca')
    return 'Bem vindo ao Sistema de Biblioteca!'

@app.route('/livros', methods=['GET'])
def listar_livros():
    conn = conectar_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM livros")
        livros = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{'id': livro[0], 'titulo': livro[1], 'autor': livro[2]} for livro in livros])
    else:
        return jsonify({'error': 'Não foi possível conectar ao banco de dados'}), 500

@app.route('/livros/<int:id>', methods=["GET"])
def obter_livro(id):
    conn = conectar_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM livros WHERE id = %s", (id,))
        livro = cur.fetchone()
        cur.close()
        conn.close()
        if livro:
            return jsonify({'id': livro[0], 'titulo': livro[1], 'autor': livro[2]})
        else:
            return jsonify({'error': 'Livro não encontrado'}), 404
    else:
        return jsonify({'error': 'Não foi possível conectar ao banco de dados'}),500

@app.route('/livros', methods=['POST'])
def adicionar_livro():
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    if not titulo or not autor:
        return jsonify({'error': 'Título e autor são obrigatórios'}), 400
    conn = conectar_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO livros (titulo, autor) VALUES (%s, %s)", (titulo, autor))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Livro adicionado com sucesso'}), 201
        except psycopg2.Error as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({'error': f'Erro ao adicionar livro: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Não foi possível conectar ao banco de dados'}), 500

@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    if not titulo or not autor:
        return jsonify({'error': 'Título e autor são obrigatórios'}), 400
    conn = conectar_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE livros SET titulo = %s, autor = %s WHERE id = %s", (titulo, autor, id))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Livro atualizado com sucesso'}), 200
        except psycopg2.Error as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({'error': f'Erro ao atualizar livro: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Não foi possível conectar ao banco de dados'}), 500

@app.route('/livros/<int:id>', methods=['DELETE'])
def remover_livro(id):
    conn = conectar_db()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM livros WHERE id = %s", (id,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Livro removido com sucesso'}), 200
        except psycopg2.Error as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({'error': f'Erro ao remover livro: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Não foi possível conectar ao banco de dados'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
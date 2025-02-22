import psycopg2

def conectar_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="livros",
            user="teste_livros",
            password="minha_senha_segura"
        )
        print("Conexão com o banco de dados PostgreSQL estabelecida com sucesso!")
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados PostgreSQL: {e}")
        return None

# Testando
conn = conectar_db()
if conn:
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros")
        resultados = cursor.fetchall()
        print(resultados)
    except psycopg2.Error as e:
        print(f"Erro ao executar a consulta: {e}")
    finally:
        cursor.close()
        conn.close()
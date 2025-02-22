from flask import Flask, jsonify, request

app = Flask(__name__)

livros = [
	{
        'id': 1,
        'título': 'O Senhor dos Anéis - A Sociedade do Anel',
        'autor': 'J.R.R Tolkien'
    },
    {
        'id': 2,
        'título': 'Harry Potter e a Pedra Filosofal',
        'autor': 'J.K Howling'
    },
    {
        'id': 3,
        'título': 'Hábitos Atômicos',
        'autor': 'James Clear'
    },
]

@app.route('/', methods=['GET'])
def pagina_inicial():
	return 'Bem Vindo ao Sistema de Biblioteca!'


app.run(debug=True, host='0.0.0.0', port=5000)
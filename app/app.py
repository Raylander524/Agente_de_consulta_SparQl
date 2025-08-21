from flask import Flask, render_template, request, redirect, url_for
from service import chamar_modelo

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        texto = request.form.get('texto_input', '')
        resultado = chamar_modelo(texto)
        return redirect(url_for('mostrar_resultado', resultado=resultado))
    
    return render_template('index.html')

@app.route('/resultado')
def mostrar_resultado():
    resultado = request.args.get('resultado', '')
    return render_template('resultado.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
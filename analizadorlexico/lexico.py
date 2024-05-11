from flask import Flask, request, render_template, flash
import lexer
import logging

app = Flask(__name__)
app.secret_key = 'claveAleatoria'
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    codigoArchivo = ""
    file_name = ""

    if request.method == 'POST':
        logging.debug("Received POST request")

        if 'file' in request.files and request.files['file']:
            file = request.files['file']
            file_name = file.filename
            codigoArchivo = file.read().decode('utf-8')
            logging.debug(f"Code from file: {codigoArchivo}")
            flash(f'Archivo "{file_name}" Se ha subido correctamente.')
        elif 'codigoArchivo' in request.form and request.form['codigoArchivo']:
            codigoArchivo = request.form['codigoArchivo']
            logging.debug(f"Code from textarea: {codigoArchivo}")

        if 'analizar' in request.form:
            lexer.lexer.input(codigoArchivo)

            line_number = 1
            while True:
                tok = lexer.lexer.token()
                if not tok:
                    break

                if tok.type in lexer.reserved.values():
                    token_type = f"<Reservada {tok.type.title()}>"
                elif tok.type == 'LPAREN':
                    token_type = "<Paréntesis de apertura>"
                elif tok.type == 'RPAREN':
                    token_type = "<Paréntesis de cierre>"
                else:
                    token_type = tok.type

                tokens.append((f"Línea {line_number}", token_type, tok.value))
                logging.debug(f"Token: {tok}")

                line_number += 1

    return render_template('index.html', codigoArchivo=codigoArchivo, tokens=tokens, file_name=file_name)


if __name__ == '__main__':
    app.run(debug=True, port=5000)


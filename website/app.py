from crypt import methods
from flask import Flask, render_template, request, g

from model_utils import Preprocessor, initialize_model, predict, get_names, preprocess_code

def create_app():
    app = Flask(__name__)

    print('I am starting')

    # Run on start
    return app 

print('Initializing preprocessor')
preprocess = Preprocessor()
print('Initializing model')
m = initialize_model()
print('Done initializing model')

app = create_app()

@app.route('/', methods=['POST', 'GET'])
def index():
    cols = ["quicksort", "mergesort", "selectionsort", "insertionsort", 
        "bubblesort", "linearsearch", "binarysearch", "linkedlist", "hashmap"]
    probs = [(col, "") for col in cols]
    data = {'code': None, 'lang': None, 'results': [], 'probabilities': probs, 'error_msg': None}
    #app.logger.debug(f'REQUEST METHOD: [{request.method}]')

    if request.method == 'POST':
        code = request.form['code']
        lang = request.form['lang']

        data['code'] = code 
        data['lang'] = lang

        X = preprocess_code(code, lang)
        X = preprocess(X)

        probabilities = predict(m, X)
        results = get_names(probabilities)

        

        probabilities = list(zip(cols, map(lambda x: '{:.3f}%'.format(round(x * 100, 3)), probabilities.tolist())))
        app.logger.debug(probabilities)

        #probabilities = dict(zip(cols, probabilities))
        #app.logger.debug(f'Probabilities: [{probabilities}]')
        data['results'] = results 
        data['probabilities'] = probabilities #dict(zip(cols, probabilities))

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
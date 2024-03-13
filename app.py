from flask import Flask, render_template, jsonify, request
import autobrand

app = Flask(__name__)

# Initialize scrapper
scrapper = autobrand.Scrapper()
scrapper.login()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/<item_id>')
def search_item(item_id):

    # Store the data of the searched item in result
    result = scrapper.search_item(item_id)

    data = {
        'denumire': result['Name'],
        'pret': result['Price'],
        'disponibilitate': result['Availability'],
        'producator': result['Producer']
    }

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

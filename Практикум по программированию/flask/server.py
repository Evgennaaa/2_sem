from flask import Flask, jsonify, abort

app = Flask(__name__)

users = [
    {
        'login': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol'
    },
    {
        'login': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web'
    }
]

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@app.route('/user/<int:user_id>', methods=['GET'])
def get_task(user_id):
    user = list(filter(lambda t: t['login'] == user_id, users))
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

if __name__ == '__main__':
    app.run(debug=True)
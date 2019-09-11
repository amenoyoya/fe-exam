from flask import Flask, jsonify, session, request
import yaml, hashlib, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex() # セッション暗号化

# load application configures
with open('./config.yml') as f:
    configures = yaml.load(f)

# GET /api/ => APIサーバー設定を返す
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'endpoints': configures['endpoints']
    })

# POST /api/$auth => ログイン状態を返す
@app.route(configures['endpoints']['auth'], methods=['POST'])
def auth():
    if 'auth_token' not in session:
        return jsonify({
            'auth': False, 'message': 'not authenticated yet'
        })
    if secrets.compare_digest(session['auth_token'], request.json.get('auth_token')):
        return jsonify({
            'auth': True, 'username': session.get('username')
        })
    return jsonify({
        'auth': False, 'message': 'authentication timed out'
    })

# POST /api/$auth_session => セッションからログイン状態を返す
@app.route(configures['endpoints']['auth_session'], methods=['POST'])
def auth_session():
    if 'auth_token' not in session:
        return jsonify({
            'token': 'err', 'username': '', 'message': 'not authenticated yet'
        }), 401
    return jsonify({
        'token': session['auth_token'], 'username': session.get('username')
    })

# POST /api/$login => ユーザーログイン処理を実行
@app.route(configures['endpoints']['login'], methods=['POST'])
def login():
    if 'username' not in request.json or 'password' not in request.json:
        return jsonify({
            'login': False, 'message': 'invalid parameters'
        })
    # ユーザー名の一致するメンバーのパスワードを抽出
    passwords = [x['password'] for x in configures['auth']['members'] if x['name'] == request.json['username']]
    # パスワードの一致あり
    if len(passwords) > 0 and hashlib.sha256(request.json['password'].encode('utf-8')).hexdigest() == passwords[0]:
        token = secrets.token_hex() # トークン発行
        session['auth_token'] = token # セッションにトークン保存
        session['username'] = request.json['username']
        return jsonify({
            'login': True, 'token': token, 'username': request.json['username']
        })
    # パスワードの一致なし
    return jsonify({
        'login': False, 'message': 'username or password is wrong'
    })

# POST /api/$logout => セッションからログイン状態を削除
@app.route(configures['endpoints']['logout'], methods=['POST'])
def logout():
    if 'auth_token' in session:
        del session['auth_token']
    if 'username' in session:
        del session['username']
    return jsonify({
        'token': 'null', 'username': ''
    })

if __name__ == '__main__':
    # run server
    app.run(debug=True)

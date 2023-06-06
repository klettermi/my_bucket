from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
url = 'mongodb+srv://sparta:test@cluster0.5ikuzog.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url, tlsCAFile=ca)

db = client.dbsparta
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1
    doc = {
        'num':count,  #버킷 등록 시, db에서 특정 버킷을 찾기 위해 'num' 이라는 고유 값 부여
        'bucket' :bucket_receive,
        'done' : 0   #'done' key값을 추가 해 각 버킷의 완료 상태 구분(0 = 미완료, 1 = 완료)
    }
    db.buckets.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})
    
@app.route("/bucket/done", methods = ["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.buckets.update_one({'num': int(num_receive)}, {'$set':{'done':1}})
    return jsonify({'mgs': '버킷 완료!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.buckets.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.n0imoeb.mongodb.net/cluster0?retryWrites=true&w=majority', tlsCAFile=ca )
db = client.test


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/review", methods=["POST"])
def review_post():
    review_receive = request.form['review_give']

    review_list = list(db.review.find({},{'_id':False}))

    count = len(review_list) + 1

    doc = {
        'num':count,
        'review':review_receive,
        'done':0
    }

    db.review.insert_one(doc)


    return jsonify({'msg': '리뷰 감사합니다 😍'})


@app.route("/review/done", methods=["POST"])
def review_done():
    num_receive = request.form['num_give']
    db.review.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    return jsonify({'msg': '✏️ 수정완료'})








@app.route("/review/cancel", methods=["POST"])
def review_cancel():
    num_receive = request.form['num_give']
    db.review.update_one({'num': int(num_receive)},{'$set':{'done':0}})
    return jsonify({'msg': '☠️ 삭제완료'})

# @app.route("/review/cancel", methods=["POST"])
# def review_cancel():
#     num_receive = request.form['num_give']
#     db.review.update_one({'num': int(num_receive)},{'$set':{'done':0}})
#     return jsonify({'msg': ''})


@app.route("/review", methods=["GET"])
def review_get():
    review_list = list(db.review.find({},{'_id':False}))

    return jsonify({'reviews': review_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
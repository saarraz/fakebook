import json
import time
import datetime
from io import StringIO
import sys
import os
from flask import Flask, Response, send_from_directory, abort, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import model
from manager import Manager

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'images'
configure_uploads(app, photos)
manager = Manager('asda')


def return_json(func):
    def wrapper(*args, **kwargs):
        resp = json.dumps(func(*args, **kwargs))
        print(resp, file=sys.stderr)
        return Response(resp, mimetype='application/json')
    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/login/<access_token>', methods=['POST'])
@return_json
def login(access_token):
    global manager
    manager = Manager(access_token)
    return {'user_id': model.User.main_user().id}


@app.route('/users/<user_id>', methods=['GET'])
@return_json
def user(user_id):
    return model.User.from_id(int(user_id)).to_json()


@app.route('/pages/<page_id>', methods=['GET'])
@return_json
def page(page_id):
    return model.Page.from_id(int(page_id)).to_json()


@app.route('/feed/from/<from_time>', methods=['GET'])
@return_json
def feed(from_time):
    try:
        from_time = datetime.datetime.fromtimestamp(int(from_time))
    except OSError:
        # Invalid argument
        from_time = datetime.datetime(year=1970, month=1, day=1)
    return {
        'posts': sorted([post.to_json() for post in model.Post.all() if post.time > from_time],
                        key=lambda post: post['time'])[::-1],
        'time': time.mktime(datetime.datetime.now().timetuple())
    }


@app.route('/notifications/from/<from_time>', methods=['GET'])
@return_json
def notifications(from_time):
    try:
        from_time = datetime.datetime.fromtimestamp(int(from_time))
    except OSError:
        # Invalid argument
        from_time = datetime.datetime(year=1970, month=1, day=1)
    return {
        'notificatons': sorted([notification.to_json() for notification in model.notifications
                                if notification.time() > from_time],
                               key=lambda notification: notification['time']),
        'time': time.mktime(datetime.datetime.now().timetuple())
    }


@app.route('/notifications/<id>/read', methods=['POST'])
@return_json
def mark_notification_as_read(id):
    notification = model.Notification.from_id(int(id))
    notification.read = True


@app.route('/images/<image_id>', methods=['GET'])
def image(image_id):
    img = model.Image.from_id(int(image_id))
    return send_from_directory(os.path.dirname(img.path), os.path.basename(img.path))


@app.route('/images', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        abort(404)
        return
    filename = photos.save(request.files['image'])
    image = manager.on_upload_image(filename)
    return {'id': image}


@app.route('/posts/<post_id>/comment', methods=['POST'])
def comment_on_post(post_id):
    return comment_on_reactable(model.Post.from_id(post_id))


@app.route('/comments/<comment_id>/reply', methods=['POST'])
def reply_to_comment(comment_id):
    return comment_on_reactable(model.Comment.from_id(comment_id))


@app.route('/posts', methods=['POST'])
@return_json
def add_post():
    post = manager.on_user_post(request.form['text'],
                                model.Image.from_id(int(request.form['image'])) if 'image' in request.form else None)
    return {'id': post.id}


@app.route('/posts/<post_id>/react', methods=['DELETE', 'POST'])
def react_to_post(post_id):
    post = model.Post.from_id(int(post_id))
    return react_to_reactable(post)


@app.route('/comments/<comment_id>/react', methods=['DELETE', 'POST'])
def react_to_comment(comment_id):
    comment = model.Comment.from_id(int(comment_id))
    return react_to_reactable(comment)


def react_to_reactable(target: model.Reactable):
    if request.method == 'DELETE':
        manager.on_remove_reaction(target)
    else:  # POST
        type = int(request.form['type'])
        manager.on_react(target, type)


def comment_on_reactable(target: model.Reactable):
    manager.on_comment(target)


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)

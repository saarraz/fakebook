class Points(object):
    LIKE = 0
    SAD = 1
    LOVE = 2
    HATE = 3
    FUCK_YOU = 4
    SHIT = 5

    def __init__(self):
        self.p = {}

    def add(self, user, type):
        self.p[user] = type

    def remove(self, user):
        del self.p[user]

class User(object):
    def __init__(self, user_name, img):
		self.name = user_name
		self.img = img
		
class Comment(object):
    def __init__(self, _text, _user):
        self.text = _text
        self.points = Points()
        self.user = _user

    def vote(self, user, type):
        self.points.add(user, type)

    def remove_vote(self, user, type):
        self.points.remove(user, type)


class Post(object):
    def __init__(self, _text, _img, _name, _caption):
        if _text == None:
            self.img = _img
        else:
            self.text = _text
        self.caption = _caption
        self.name = _name
        self.point = Points(0)
        self.comments = []

    def comment(self, _text):
        self.comments.append(Comment(_text, self.name))

"""_________       should add some votes here any time ;)       ________"""


class feed(object):
    def __init__(self, _type):
        self.type = _type
        self.posts = []

    def post(self, _text, _img, _name, _caption):
        self.posts.append(Post(_text, _img, _name, _caption))
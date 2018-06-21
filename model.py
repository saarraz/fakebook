import abc
import random
import time
from typing import Optional, List, Union
import os
from PIL import Image as PILImage
import datetime

next_id = 0

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')


class Node(object):
    __metaclass__ = abc.ABCMeta

    classes = []

    @staticmethod
    def generate_id():
        global next_id
        next_id += 1
        return next_id

    @staticmethod
    def new_node_class(new_class):
        Node.classes.append(new_class)
        new_class._all = {}

    @classmethod
    def all(cls):
        if not hasattr(cls, '_all'):
            return []
        return cls._all.values()

    @classmethod
    def from_id(cls, id: int):
        if cls == Node:
            for clazz in cls.classes:
                if id in clazz.all():
                    return clazz.all()[id]
        else:
            if hasattr(cls, '_all'):
                return cls._all[id]
        raise KeyError('No such object')

    def __init__(self):
        if self.__class__ not in self.classes:
            self.new_node_class(self.__class__)
        self.id = self.generate_id()
        self.__class__._all[self.id] = self

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @abc.abstractmethod
    def to_json(self):
        raise NotImplementedError


class Reaction(object):
    LIKE = 0
    SAD = 1
    LOVE = 2
    HAHA = 3
    FUCK_YOU = 4
    SHIT = 5
    THROW_UP = 6
    TYPES = [LIKE, SAD, LOVE, HAHA, FUCK_YOU, SHIT, THROW_UP]

    def __init__(self, user, target, type, time):
        self.user = user
        self.target = target
        self.type = type
        self.time = time

    def to_json(self):
        return {
            'type': self.type,
            'time': time.mktime(self.time.timetuple()),
            'user': self.user.id
        }


class User(Node):
    NORMAL = 0
    UPSET_BIRTHDAY = 1

    GENDER_MALE = 0
    GENDER_FEMALE = 1

    def __init__(self, full_name, profile_picture, gender):
        super(User, self).__init__()
        self.gender = gender
        self.full_name = full_name
        self.profile_picture = profile_picture
        self.birthday = None
        self.mode = self.NORMAL

    def to_json(self):
        return {'id': self.id, 'full_name': self.full_name, 'profile_picture': self.profile_picture.id,
                'gender': self.gender}

    _main_user = None

    @classmethod
    def main_user(cls):
        assert cls._main_user is not None, 'Main user not set'
        return cls._main_user

    @classmethod
    def set_main_user(cls, user):
        cls._main_user = user


class Image(Node):
    def __init__(self, path):
        super(Image, self).__init__()
        self.path = path

    @classmethod
    def from_file(cls, path):
        return Image(path)


class Page(Node):
    def __init__(self, name: str, profile_picture: Image):
        super(Page, self).__init__()
        self.name = name
        self.profile_picture = profile_picture

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'profile_picture': self.profile_picture.id
        }

class Reactable(Node):
    def __init__(self):
        super(Reactable, self).__init__()
        self.reactions = {}
        self.comments = []

    @abc.abstractmethod
    def target_string(self):
        raise NotImplementedError


class Post(Reactable):
    def __init__(self, _time: datetime.datetime, _text: str, _img: Optional[Image], poster: Union[User, Page]):
        super(Post, self).__init__()
        self.image = _img
        self.text = _text
        self.time = _time
        self.poster = poster
        self.views = None

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.poster.id if isinstance(self.poster, User) else None,
            'page_id': self.poster.id if isinstance(self.poster, Page) else None,
            'time': time.mktime(self.time.timetuple()),
            'text': self.text,
            'image': self.image.id if self.image is not None else None,
            'reactions': [reaction.to_json() for reaction in self.reactions.values()],
            'comments': [comment.to_json() for comment in self.comments],
            'views': self.views
        }

    def target_string(self):
        return '{whose} {post}'.format(whose='your' if self.poster == User.main_user()
                                                          else '${}$\'s'.format(self.poster.full_name),
                                       post='post' if self.image is None else 'photo')


class Comment(Reactable):
    def __init__(self, _text, _user, _parent : Reactable):
        super(Comment, self).__init__()
        self.text = _text
        self.user = _user
        self.target = _parent

    def vote(self, user, type):
        self.reactions.add(user, type)

    def remove_vote(self, user, type):
        self.reactions.remove(user, type)

    def to_json(self):
        return {
            'text': self.text,
            'reactions': self.reactions,
            'user': self.user.id,
            'replies': [reply.to_json() for reply in self.comments]
        }

    def target_string(self):
        return '{whose} {comment} on {target}'.format(whose='your' if self.user == User.main_user()
                                                          else '${}$\'s'.format(self.user.full_name),
                                                      comment='comment' if isinstance(self.target, Post) else 'reply',
                                                      target=self.target.target_string())


class Notification(Node):

    def __init__(self, time : datetime.datetime):
        super(Notification, self).__init__()
        self.read = False
        self._time = time

    def time(self):
        return self._time

    def kind(self):
        return self.__class__.KIND

    @abc.abstractmethod
    def format(self):
        raise NotImplementedError

    @abc.abstractmethod
    def image(self):
        raise NotImplementedError

    def to_json(self):
        return {
            'id': self.id,
            'time': time.mktime(self.time().timetuple()),
            'kind': self.__class__.KIND,
            'text': self.format(),
            'image': self.image().id,
            'read': self.read
        }


def users_string(users):
    if len(users) == 1:
        return '${}$'.format(users[0])
    elif len(users) == 2:
        return '${}$ and ${}$'.format(users[0], users[1])
    else:
        return '${}$ and {} others'.format(users[0], len(users) - 1)


class BirthdayNotification(Notification):
    KIND = 0

    ACTION_CALLS = [
        'Try to ignore this elegantly.',
        'Say happy birthday then continue ignoring {them}.',
        'Copy your birthday wishes from last year.',
        'Just so you know, {they} didn\'t wish you anything on your birthday.'
    ]

    def __init__(self, users: List[User], date: datetime.datetime):
        super(BirthdayNotification, self).__init__(date)
        self.date = date
        self.users = users
        self.action_call = random.choice(self.ACTION_CALLS)

    def format_action_call(self):
        return self.action_call.format(them='them' if len(self.users) > 1
                                            else {User.GENDER_FEMALE: 'her',
                                                  User.GENDER_MALE: 'him'}[self.users[0].gender],
                                       they='they' if len(self.users) > 1
                                       else {User.GENDER_FEMALE: 'she',
                                             User.GENDER_MALE: 'he'}[self.users[0].gender])

    def format(self):
        if len(self.users) == 1:
            return 'It\'s ${}$\'s birthday today. {}'.format(self.users[0].full_name, self.format_action_call())
        elif len(self.users) == 2:
            return '${}$ and ${}$ have birthdays today. {}'.format(self.users[0].full_name, self.users[1].full_name,
                                                                   self.format_action_call())
        else:
            return '${}$ and {} others have birthdays today. {}'.format(self.users[0], len(self.users) - 1,
                                                                        self.format_action_call())

    def image(self):
        return self.users[0].profile_picture


class PostNotification(Notification):

    KIND = 1

    def __init__(self, post : Post):
        super(PostNotification, self).__init__(post.time)
        self.post = post

    def format(self):
        if self.post.image is not None:
            return '${user}$ uploaded a photo.'.format(user=self.post.poster.full_name,
                                                       their='his' if self.post.poster else 'her')
        return '${user}$ updated {their} status.'.format(user=self.post.poster.full_name,
                                                         their={User.GENDER_MALE: 'his', User.GENDER_FEMALE: 'her'}
                                                                   [self.post.poster.gender])

    def image(self):
        return self.post.poster.profile_picture


Activity = Union[Comment, Reaction]


class ActivityNotification(Notification):

    def __init__(self, activities: List[Union[Activity]]):
        super(ActivityNotification, self).__init__(None)
        assert len(set(activity.target for activity in activities)) == 1
        assert len(set(type(activity) for activity in activities)) == 1
        self.activities = activities

    def kind(self):
        if isinstance(self.activities[0], Reaction):
            return 2
        else:
            return 3

    @property
    def target(self):
        return self.activities[0].target

    def users(self):
        return set()

    def time(self):
        return max(activity.time for activity in self.activities)

    def format(self):
        users = set(activity.user for activity in self.activities)
        if isinstance(self.activities[0], Reaction):
            if all(reaction.type == Reaction.LIKE for reaction in self.activities):
                what = 'liked'
            else:
                what = 'reacted to'
        else:
            assert isinstance(self.activities[0], Comment)
            if isinstance(self.target, Comment):
                what = 'replied to'
            else:
                what = 'commented on'

        return '{users} {what} {target}'.format(users=users_string(users), what=what,
                                                target=self.target.target_string())

    def image(self):
        return self.activities[0].user.profile_picture


random_people = []
friends = []
user_feed = []
notifications = []
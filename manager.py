import threading
from typing import Optional

import datetime
import model
import os
import time
import random

import random_name
from bots.fake_news.english.bot import EnglishFakeNewsBot
from bots.random_post.bot import RandomUserPostBot


class Manager(object):
    BIRTHDAY_INTERVAL = datetime.timedelta(hours=1)

    def __init__(self, access_token):
        self.access_token = access_token
        self._last_birthday_determination_time = None
        self._bots = [
            EnglishFakeNewsBot(),
            RandomUserPostBot()
        ]
        self.__generate_initial_content()

    def __generate_initial_content(self):
        print('Generating content')
        main_user_photo = model.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saar.jpg'))
        main_user = model.User('Saar Raz', main_user_photo, model.User.GENDER_MALE)
        friend = model.User('Matan Raviv', main_user_photo, model.User.GENDER_MALE)
        model.friends.append(friend)
        friend = model.User('Uria Shaul-Mandel', main_user_photo, model.User.GENDER_MALE)
        model.friends.append(friend)
        friend = model.User('Dvir Mordechai-Navot', main_user_photo, model.User.GENDER_MALE)
        friend.birthday = datetime.datetime.today()
        model.friends.append(friend)
        for i in range(2000):
            gender = random.choice([model.User.GENDER_FEMALE, model.User.GENDER_MALE])
            model.random_people.append(model.User(random_name.generate_name(gender == model.User.GENDER_MALE),
                                                  random_name.generate_pic(gender == model.User.GENDER_MALE), gender))
        model.User.set_main_user(main_user)
        for i in range(15):
            self.post(
                random.choice(self._bots)
                    .generate(
                        random.choice(model.friends),
                        datetime.datetime.now()
                        - datetime.timedelta(seconds=random.random() * datetime.timedelta(days=1).total_seconds())
                    )
            )
        threading.Thread(target=self.periodically).start()

    def periodically(self):
        while True:
            self.__determine_birthdays()
            self.__send_birthday_notifications()
            time.sleep(5)

    def __determine_birthdays(self):
        if self._last_birthday_determination_time is None \
           or datetime.datetime.now() - self._last_birthday_determination_time > self.BIRTHDAY_INTERVAL:
            for birthday_boy in random.sample(model.friends, random.randint(1, min(3, len(model.friends)))):
                birthday_boy.birthday = datetime.datetime.today()

    def __send_birthday_notifications(self):
        today = datetime.datetime.today()
        for user in model.friends:
            if user.birthday == today:
                continue
            try:
                notification_from_today = next(notification for notification in model.BirthdayNotification.all()
                                               if notification.date == datetime.datetime.today())

                if user not in notification_from_today.users:
                    notification_from_today.users.append(user)
                    notification_from_today.read = False
            except StopIteration:
                model.notifications.append(model.BirthdayNotification([user], datetime.datetime.today()))

    def on_upload_image(self, path: str) -> model.Image:
        return model.Image(path)

    def on_user_post(self, text: str, image: Optional[model.Image]) -> model.Post:
        post = model.Post(datetime.datetime.now(), text, image, model.User.main_user())
        model.user_feed.append(post)
        return post

    def on_remove_reaction(self, target: model.Reactable):
        del target.reactions[model.User.main_user()]

    def on_react(self, target: model.Reactable, type: int):
        if type not in model.Reaction.TYPES:
            raise ValueError('Unrecognized reaction type {}'.format(type))
        target.reactions[model.User] = target

    def on_comment(self, target: model.Reactable, text: str):
        cmnt = model.Comment(text, model.User.main_user(), target)
        target.comments.append(cmnt)
        self.notify_activity(cmnt)
        for friend in model.friends:
            self.react(friend, cmnt, model.Reaction.FUCK_YOU)

    def post(self, post):
        model.user_feed.append(post)
        if isinstance(post.poster, model.Page):
            post.views = random.randint(1000, 100000)
            reaction_count = int(random.random() * 0.3 * post.views)
            for i in range(reaction_count):
                person = random.choice(model.random_people)
                post.reactions[person] = model.Reaction(person, post, random.choice(model.Reaction.TYPES)
                                                        if random.random() > 0.7 else model.Reaction.LIKE,
                                                        datetime.datetime.now()
                                                        + (datetime.datetime.now() - post.time) * (i / reaction_count))
        if isinstance(post.poster, model.User) and post.poster in model.friends:
            model.notifications.append(model.PostNotification(post))

    def react(self, who: model.User, what: model.Reactable, how: int, when: Optional[datetime.datetime]=None):
        reaction = model.Reaction(who, what, how, when if when is not None else datetime.datetime.now())
        what.reactions[who] = reaction
        self.notify_activity(reaction)

    def notify_activity(self, activity: model.Activity) -> model.ActivityNotification:
        for notification in model.Notification.all():
            if notification.target == activity.target and type(notification.activities[0]) == type(activity) \
               and activity.time - notification.time() < datetime.timedelta(days=1):
                notification.read = False
                notification.activities.append(activity)
                return notification
        notification = model.ActivityNotification([activity])
        model.notifications.append(notification)
        return notification

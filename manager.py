import threading
from typing import Optional

import datetime
import model
import os


class Manager(object):
    def __init__(self, access_token):
        self.access_token = access_token
        main_user_photo = model.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saar.jpg'))
        main_user = model.User('Saar Raz', main_user_photo, model.User.GENDER_MALE)
        friend = model.User('A Friend', main_user_photo, model.User.GENDER_MALE)
        friend.birthday = datetime.datetime.today()
        model.friends.append(friend)
        model.User.set_main_user(main_user)
        self.on_user_post('Test post - this is my profile picture', main_user_photo)
        threading.Thread(target=self.periodically).start()

    def periodically(self):
        self.__send_birthday_notifications()

    def __send_birthday_notifications(self):
        today = datetime.datetime.today()
        for user in model.friends:
            print(user.full_name)
            if user.birthday == today:
                continue
            try:
                notification_from_today = next(notification for notification in model.BirthdayNotification.all()
                                               if notification.date == datetime.datetime.today())
                if user not in notification_from_today.users:
                    notification_from_today.users = user
                    notification_from_today.read = False
            except StopIteration:
                print('Notifying birthday')
                model.notifications.append(model.BirthdayNotification([user], datetime.datetime.today()))

    def on_upload_image(self, path: str) -> model.Image:
        return model.Image(path)

    def on_user_post(self, text: str, image: Optional[model.Image]) -> model.Post:
        post = model.Post(datetime.datetime.now(), text, image, model.User.main_user())
        model.user_feed.append(post)
        model.notifications.append(model.PostNotification(post))
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

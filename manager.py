from typing import Optional, Union

import datetime
import models
import os


class Manager(object):
    def __init__(self, access_token):
        self.access_token = access_token
        main_user_photo = models.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saar.jpg'))
        main_user = models.User('Saar Raz', main_user_photo, models.User.GENDER_MALE)
        friend = models.User('A Friend', main_user_photo, models.User.GENDER_MALE)
        models.friends.append(friend)
        models.User.set_main_user(main_user)
        self.on_user_post('Test post - this is my profile picture', main_user_photo)

    def periodically(self):
        for user in models.friends:
            if user.has_birthday and not any(notification.user for notification in models.BirthdayNotification.all()):


    def on_upload_image(self, path: str) -> models.Image:
        return models.Image(path)

    def on_user_post(self, text: str, image: Optional[models.Image]) -> models.Post:
        post = models.Post(datetime.datetime.now(), text, image, models.User.main_user())
        models.user_feed.append(post)
        models.PostNotification(post)
        return post

    def on_remove_reaction(self, target: models.Reactable):
        del target.reactions[models.User.main_user()]

    def on_react(self, target: models.Reactable, type: int):
        if type not in models.Reaction.TYPES:
            raise ValueError('Unrecognized reaction type {}'.format(type))
        target.reactions[models.User] = target

    def on_comment(self, target: models.Reactable, text: str):
        cmnt = models.Comment(text, models.User.main_user(), target)
        target.comments.append(cmnt)
        self.notify_activity(cmnt)
        for friend in models.friends:
            self.react(friend, cmnt, models.Reaction.FUCK_YOU)

    def react(self, who: models.User, what: models.Reactable, how: int, when: Optional[datetime.datetime]=None):
        reaction = models.Reaction(who, what, how, when if when is not None else datetime.datetime.now())
        what.reactions[who] = reaction
        self.notify_activity(reaction)

    def notify_activity(self, activity: models.Activity) -> models.ActivityNotification:
        for notification in models.Notification.all():
            if notification.target == activity.target and type(notification.activities[0]) == type(activity) \
               and activity.time - notification.time() < datetime.timedelta(days=1):
                notification.read = False
                notification.activities.append(activity)
                return notification
        return models.ActivityNotification([activity])

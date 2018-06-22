import threading
from typing import Optional

import datetime
import model
import os
import time
import random
# import privacypolicy

import random_name
import topic.detect
from bots.fake_news.english.bot import EnglishFakeNewsBot
from bots.fake_news.hebrew.main import HebrewFakeNewsBot
from bots.random_post.bot import RandomUserPostBot


class Manager(object):
    BIRTHDAY_INTERVAL = datetime.timedelta(hours=1)
    BIRTHDAY_UPSET_INTERVAL = datetime.timedelta(minutes=5)

    def __init__(self, access_token):
        self.access_token = access_token
        self._last_birthday_determination_time = None
        self._bots = [
            EnglishFakeNewsBot(),
            RandomUserPostBot(),
            HebrewFakeNewsBot()
        ]
        self.batman = model.User('Batman', model.Image(os.path.join(model.IMAGE_DIR, 'profile', 'batman.jpg')),
                                 model.User.GENDER_MALE)
        self.__generate_initial_content()

    def __generate_initial_content(self):
        print('Generating content')
        main_user_photo = model.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saar.jpg'))
        main_user = model.User('Saar Raz', main_user_photo, model.User.GENDER_MALE)
        main_user_photo = model.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saar.jpg'))
        photo0 = model.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'matan.jpg'))
        friend = model.User('Matan Raviv', photo0, model.User.GENDER_MALE)
        model.friends.append(friend)
        photo1 = model.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uria.jpg'))
        friend = model.User('Uria Shaul-Mandel', photo1, model.User.GENDER_MALE)
        model.friends.append(friend)
        photo2 = model.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dvir.jpg'))
        friend = model.User('Dvir Mordechai-Navot', photo2, model.User.GENDER_MALE)
        model.friends.append(friend)
        photo2 = model.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'angela.jpg'))
        friend = model.User('Angela Merkel', photo2, model.User.GENDER_MALE)
        friend.birthday = datetime.datetime.today()
        model.friends.append(friend)
        photo2 = model.Image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bar.jpg'))
        friend = model.User('Bar Rafaeli', photo2, model.User.GENDER_MALE)
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
            self.__upset_birthday_boys()
            time.sleep(5)

    def __upset_birthday_boys(self):
        try:
            birthday_notification = next(n for n in model.BirthdayNotification.all()
                                         if n.date == datetime.datetime.today())
            if datetime.datetime.now() - birthday_notification.time > self.BIRTHDAY_UPSET_INTERVAL:
                for birthday_boy in birthday_notification.users:
                    try:
                        post = next(p for p in model.Post.all() if p.timeline == birthday_boy
                                    and p.poster == model.User.main_user())
                    except StopIteration:
                        # User did not wish us a happy birthday! be angry at him
                        if birthday_boy.birthday_upsetness == 0:
                            birthday_boy.birthday_upsetness = 1
        except StopIteration:
            pass

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
                    notification_from_today.time = datetime.datetime.now()
                    notification_from_today.read = False
            except StopIteration:
                model.notifications.append(model.BirthdayNotification([user], datetime.datetime.now()))

    def on_upload_image(self, path: str) -> model.Image:
        return model.Image(path)

    def on_user_post(self, text: str, image: Optional[model.Image]) -> model.Post:
        post = model.Post(datetime.datetime.now(), text, image, model.User.main_user(), None)
        model.user_feed.append(post)
        if True:
            upset_birthday_boys = model.friends#[u for u in model.User.all()
                                  # if 0 < u.birthday_upsetness < model.User.MAX_BIRTHDAY_UPSETNESS]
            if upset_birthday_boys:
                def send_angry_replies():
                    try:
                        post_topic = topic.detect.get_topic(post.text)
                    except ValueError:
                        return
                    time.sleep(random.randint(5, 10))
                    first_commenter = upset_birthday_boys[0]
                    first_comment_text = random.choice([
                        'יש לך זמן לכתוב על {topic}, אבל להגיד מזל טוב לא נכנס בלו"ז. נחמד לראות את סדר העדיפויות'.format(topic=post_topic),
                        'אני מבי{} שמאוד חשוב לך {topic}, יותר ממני אפילו (מה התאריך היום?)'.format('ן' if first_commenter.gender == model.User.GENDER_MALE else 'נה', topic=post_topic),
                        'יש לך זמן לכתוב על {topic}, אבל להגיד מזל טוב לא נכנס בלו"ז. חבר חרא'.format(topic=post_topic),
                        'יש לך זמן לחפור על {topic}, אבל להגיד מזל טוב לא נכנס בלו"ז. אין בעיה.'.format(topic=post_topic)
                    ])
                    self.react(first_commenter, post, random.choice(model.Reaction.NEGATIVE_TYPES))
                    first_comment = self.comment(first_commenter, post, first_comment_text)
                    if len(upset_birthday_boys) > 1:
                        time.sleep(random.randint(10, 30))
                        second_commenter = random.choice(upset_birthday_boys[1:])
                        self.react(second_commenter, post, random.choice(model.Reaction.NEGATIVE_TYPES))
                        self.react(second_commenter, first_comment, model.Reaction.LIKE)
                        second_comment_text = random.choice([
                            'גם לי {him} לא כתב{} כלום... '.format('' if second_commenter.gender == model.User.GENDER_MALE else 'ה', him='הוא' if second_commenter.gender == model.User.GENDER_MALE else 'היא'),
                            'אנחנו באותה סירה. אפס אכפתיות',
                            'גם אני אותו דבר, חרא חבר באמת'
                        ])
                        self.comment(second_commenter, first_comment, second_comment_text)

                threading.Thread(target=send_angry_replies).start()
        if True:
            def girlify(word):
                return word + word[-1] * random.randint(1, 10)
            # Image post
            def reply_positively_to_image():
                liking_friends = random.sample(model.friends, min(len(model.friends), random.randint(10, 80)))
                for friend in liking_friends:
                    time.sleep(random.randint(1, 2))
                    self.react(friend, post, random.choice([model.Reaction.LIKE, model.Reaction.LOVE]))
                    if random.random() < 0.5:
                        target_is_male = model.User.main_user().is_male()
                        self.comment(friend, post, (
                            girlify(random.choice([
                                'מהמם' if target_is_male else 'מהממת',
                                'מושלם' if target_is_male else 'מושלמת',
                                ('הורס' if target_is_male else 'הורסת')
                                + ('את הבריאות' if random.random() < .5 else ''),
                                ('חתיך' if target_is_male else '')
                                + ('את הבריאות' if random.random() < .5 else ''),
                                'יפה שלי',
                                ('לא' if random.random() < .5 else '') + 'אני מתה',
                                ('לא' if random.random() < .5 else '') + 'אין דברים כאל' + random.choice(['ה', 'ו']),
                                girlify('לפרופיל')
                            ]))
                            if not friend.is_male()
                            else random.choice(
                                [
                                    'תמונה יפה ' + (random.choice(['חיים', 'מאמי']) if not target_is_male else random.choice(['גבר','אחי'])) + ' שלי',
                                    'לא רע',
                                    'נדירה'
                                ] +
                                (['אחלה אופי'] if not target_is_male else [
                                    'אח יקר',
                                    'אחי'
                                    + ''.join('י' if random.random() < .9 else 'ע' for i in range(random.randint(1, 10))),
                                ])
                            )
                        ))
            def reply_negatively_to_image():
                liking_friends = random.sample(model.friends, min(len(model.friends), random.randint(10, 150)))
                for friend in liking_friends:
                    time.sleep(random.randint(1, 2))
                    self.react(friend, post, random.choice([model.Reaction.THROW_UP, model.Reaction.HAHA]))
                    if random.random() < 0.5:
                        target_is_male = model.User.main_user().is_male()
                        self.comment(friend, post, (
                            random.choice([
                                'ח' * random.randint(10, 20) + random.choice(['', ' פיגוע ' + random.choice(['מוצלח', 'טוב'])]),
                                'חחחחחחח מה קרה' + random.choice(['', '?']),
                                random.choice(['', 'לפחות ']) + 'יש לך אופי ' + random.choice(['סביר', 'סבבה', 'טוב']),
                                'הכל בסדר' + random.choice(['', '?']),
                                random.choice(['', 'בוא ל' if target_is_male else 'בואי ל']) + 'פרטי' + random.choice(['', girlify(' דחוף'), 'עכשיו']),
                                'מה זה מה קרה לך לפנים' + random.choice(['?', ''])
                            ])
                        ))
            threading.Thread(target=random.choice([reply_positively_to_image, reply_negatively_to_image])).start()
        return post

    def on_remove_reaction(self, target: model.Reactable):
        del target.reactions[model.User.main_user()]

    def on_react(self, target: model.Reactable, type: int):
        if type not in model.Reaction.TYPES:
            raise ValueError('Unrecognized reaction type {}'.format(type))
        target.reactions[model.User.main_user()] = model.Reaction(model.User.main_user(), target, type,
                                                                  datetime.datetime.now())

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
        if post.image is None:
            upset_birthday_boys = [u for u in model.User.all()
                                   if 0 < u.birthday_upsetness < model.User.MAX_BIRTHDAY_UPSETNESS]
            if upset_birthday_boys:
                def send_angry_replies():
                    try:
                        post_topic = topic.detect.get_topic(post.text)
                    except ValueError:
                        return
                    time.sleep(random.randint(5, 10))
                    first_commenter = upset_birthday_boys[0]
                    first_comment_text = random.choice([
                        'יש לך זמן לכתוב על {topic}, אבל להגיד מזל טוב לא נכנס בלו"ז. נחמד לראות את סדר העדיפויות'.format(topic=post_topic),
                        'אני מבי{} שמאוד חשוב לך {topic}, יותר ממני אפילו (מה התאריך היום?)'.format('ן' if first_commenter.gender == model.User.GENDER_MALE else 'נה', topic=post_topic),
                        'יש לך זמן לכתוב על {topic}, אבל להגיד מזל טוב לא נכנס בלו"ז. חבר חרא'.format(topic=post_topic),
                        'יש לך זמן לחפור על {topic}, אבל להגיד מזל טוב לא נכנס בלו"ז. אין בעיה.'.format(topic=post_topic)
                    ])
                    self.react(first_commenter, post, random.choice(model.Reaction.NEGATIVE_TYPES))
                    first_comment = self.comment(first_commenter, post, first_comment_text)
                    if len(upset_birthday_boys) > 1:
                        time.sleep(random.randint(10, 30))
                        second_commenter = random.choice(upset_birthday_boys[1:])
                        self.react(second_commenter, post, random.choice(model.Reaction.NEGATIVE_TYPES))
                        self.react(second_commenter, first_comment, model.Reaction.LIKE)
                        first_comment.reactions.append(model.Reaction(second_commenter, first_comment,
                                                                      model.Reaction.LIKE, datetime.datetime.now()))
                        second_comment_text = random.choice([
                            'גם לי {him} לא כתב{} כלום... '.format('' if second_commenter.gender == model.User.GENDER_MALE else 'ה', him='הוא' if second_commenter.gender == model.User.GENDER_MALE else 'היא'),
                            'אנחנו באותה סירה. אפס אכפתיות',
                            'גם אני אותו דבר, חרא חבר באמת'
                        ])
                        self.comment(second_commenter, first_comment, second_comment_text)

                threading.Thread(target=send_angry_replies).start()
        else:
            def girlify(word):
                return word + word[-1] * random.randint(1, 10)
            # Image post
            def reply_positively_to_image():
                liking_friends = random.sample(model.random_people, min(len(model.random_people), random.randint(10, 80)))
                for friend in liking_friends:
                    time.sleep(random.randint(1, 10))
                    self.react(friend, post, random.choice([model.Reaction.LIKE, model.Reaction.LOVE]))
                    if random.random() < 0.1:
                        target_is_male = model.User.main_user().is_male()
                        self.comment(friend, post, (
                            girlify(random.choice([
                                'מהמם' if target_is_male else 'מהממת',
                                'מושלם' if target_is_male else 'מושלמת',
                                ('הורס' if target_is_male else 'הורסת')
                                + ('את הבריאות' if random.random() < .5 else ''),
                                ('חתיך' if target_is_male else '')
                                + ('את הבריאות' if random.random() < .5 else ''),
                                'יפה שלי',
                                ('לא' if random.random() < .5 else '') + 'אני מתה',
                                ('לא' if random.random() < .5 else '') + 'אין דברים כאל' + random.choice(['ה', 'ו']),
                                girlify('לפרופיל')
                            ]))
                            if not friend.is_male()
                            else random.choice(
                                [
                                    'תמונה יפה ' + (random.choice(['חיים', 'מאמי']) if not target_is_male else random.choice(['גבר','אחי'])) + ' שלי',
                                    'לא רע',
                                    'נדירה'
                                ] +
                                (['אחלה אופי'] if not target_is_male else [
                                    'אח יקר',
                                    'אחי'
                                    + ''.join('י' if random.random() < .9 else 'ע' for i in range(random.randint(1, 10))),
                                ])
                            )
                        ))
            def reply_negatively_to_image():
                liking_friends = random.sample(model.random_people, min(len(model.random_people),random.randint(10, 150)))
                for friend in liking_friends:
                    time.sleep(random.randint(1, 10))
                    self.react(friend, post, random.choice([model.Reaction.THROW_UP, model.Reaction.HAHA]))
                    if random.random() < 0.1:
                        target_is_male = model.User.main_user().is_male()
                        self.comment(friend, post, (
                            random.choice([
                                'ח' * random.randint(10, 20) + random.choice(['', ' פיגוע ' + random.choice(['מוצלח', 'טוב'])]),
                                'חחחחחחח מה קרה' + random.choice(['', '?']),
                                random.choice(['', 'לפחות ']) + 'יש לך אופי ' + random.choice(['סביר', 'סבבה', 'טוב']),
                                'הכל בסדר' + random.choice(['', '?']),
                                random.choice(['', 'בוא ל' if target_is_male else 'בואי ל']) + 'פרטי' + random.choice(['', girlify(' דחוף'), 'עכשיו']),
                                'מה זה מה קרה לך לפנים' + random.choice(['?', ''])
                            ])
                        ))
            threading.Thread(target=random.choice([reply_positively_to_image, reply_negatively_to_image])).start()
        if isinstance(post.poster, model.User) and post.poster in model.friends:
            model.notifications.append(model.PostNotification(post))

    def react(self, who: model.User, what: model.Reactable, how: int, when: Optional[datetime.datetime]=None):
        reaction = model.Reaction(who, what, how, when if when is not None else datetime.datetime.now())
        what.reactions[who] = reaction
        self.notify_activity(reaction)
        return reaction

    def comment(self, who: model.User, what: model.Reactable, text: str):
        comment = model.Comment(text, who, what)
        what.comments.append(comment)
        self.notify_activity(comment)
        return comment

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

#    def we_have_updated_our_privacy_policy(self):
#        str = privacypolicy.get_privacy_policy("3")
#        print(str)

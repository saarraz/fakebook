import os
import model
import random
from bots.post_bot import PostBot

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')


class EnglishFakeNewsBot(PostBot):

    NAME = [
        'Donald Trump',
        'Cristiano Ronaldo',
        'Drake',
        'LeBron James',
        'Lionel Messi',
        'Justin Bieber',
        'Gordon Ramsay',
        'Dwayne Johnson',
        'Vin Diesel',
        'Jackie Chan',
        'Clvin Harris',
        'Stephen Curry',
        'Robert Downey Jr',
        'Taylor Swift',
        'Bruno Mars',
        'Tom Cruise',
        'Jennifer Lopez',
        'Novak Djokovic',
        'Neymar',
        'Ed Sheeran',
        'Usain Bolt',
        'Conor McGregor',
        'Katy Perry',
        'Britney Spears',
        'Kim Jong-un'
    ]

    INTRODUCTION = [
        'BREAKING NEWS',
        'SCANDAL',
        'LATEST NEWS',
        'TRUMP',
        'AMAZING',
        'SHOCKING',
        'WATCH',
        ''
    ]

    VERB = [
        'convicted',
        'found',
        'accused',
        'banned',
        'exposed',
        'approved',
        'been told',
        'accepted'
    ]

    END = [
        'by a dog',
        'by a police officer',
        'by a bodygurd',
        'for 100, 000, 000 USD in an auction',
        'by a whole kindergurden',
        'for new job as a cleaner'
    ]

    def __init__(self):
        self.sources = [
            model.Page('The New York Times', model.Image.from_file(os.path.join(IMAGE_DIR, 'new_york_times.png'))),
            model.Page('BBC News', model.Image.from_file(os.path.join(IMAGE_DIR, 'bbc.png'))),
            model.Page('CNN', model.Image.from_file(os.path.join(IMAGE_DIR, 'cnn.png'))),
            model.Page('Fox News', model.Image.from_file(os.path.join(IMAGE_DIR, 'fox_news.png')))
        ]

    def generate(self, user, when):
        return model.Post(when, '{}: {} {} {}'.format(random.choice(self.INTRODUCTION), random.choice(self.NAME),
                                                      random.choice(self.VERB), random.choice(self.END)), None,
                          random.choice(self.sources), None)

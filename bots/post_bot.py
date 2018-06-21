import abc


class PostBot(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate(self, user, date):
        raise NotImplementedError()

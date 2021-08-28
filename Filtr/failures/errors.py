''' Filtr Errors '''

class NoPathError(Exception):
    ''' is Raised when a path is not provided when there should be one '''

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return ' {0} '.format(self.message)
        else:
            return 'A path has not been provided'


class DataLimitError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return ' {0} '.format(self.message)
        else:
            return 'The Data limit cannot be lower than 25'

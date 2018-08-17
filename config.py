''' config.py- configuration file'''


class Default():
    '''parent config file'''
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'very secret'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = 'access'


class Development(Default):
    '''Configurations for development'''
    DEBUG = True
    TESTING = True


class Test(Default):
    '''the class is used to run tests'''
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'this-really-needs-to-be-changed'


class Production(Default):
    '''production configarations'''
    TESTING = False


CONFIG = {
    'development': Development,
    'testing': Test,
    'production': Production,
    'default': Default
}

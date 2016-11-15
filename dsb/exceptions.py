class InvalidLogin(Exception):
    '''
    Raised for invalid login credentials

    Probably also for wrong formatted api-responses
    '''
    pass


class InvalidPlan(Exception):
    '''
    Raised for invalid plans

    Currently only if there's no title given
    '''
    pass

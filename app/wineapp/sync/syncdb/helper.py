import datetime

VERBOSE = True
LOGGING = False

def log(message):
    try:
        message = str(message)
        if VERBOSE:
            print(datetime.datetime.now().strftime('[%H:%M:%S] ') + message)
        if LOGGING:
            pass
    except Exception as e:
        print e
        print message

import config

class DebugTools:
    def output(content):
        if config.DEBUG:
            print(content)
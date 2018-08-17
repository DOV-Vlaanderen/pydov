class AbstractHook(object):
    def __init__(self, name):
        self.name = name

    def xml_downloaded(self, url):
        pass


class VerboseHook(AbstractHook):
    def __init__(self):
        AbstractHook.__init__(self, "VerboseHook")

    def xml_downloaded(self, url):
        print("Downloaded XML from %s" % url)

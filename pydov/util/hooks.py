import sys


class AbstractHook(object):
    def __init__(self, name):
        self.name = name

    def wfs_search(self, typename):
        pass

    def wfs_result(self, number_of_results):
        pass

    def xml_requested(self, url):
        pass

    def xml_cache_hit(self, url):
        pass

    def xml_cache_miss(self, url):
        pass

    def xml_downloaded(self, url):
        pass


class SimpleStatusHook(AbstractHook):
    def __init__(self):
        super(SimpleStatusHook, self).__init__('SimpleStatusHook')
        self.result_count = 0
        self.prog_counter = 0

    def _write_progress(self, char):
        if self.prog_counter == 0:
            sys.stdout.write('[%03i/%03i] ' % (self.prog_counter,
                                               self.result_count))
            sys.stdout.flush()
        elif self.prog_counter % 50 == 0:
            sys.stdout.write('\n[%03i/%03i] ' % (self.prog_counter,
                                                 self.result_count))
            sys.stdout.flush()

        sys.stdout.write(char)
        sys.stdout.flush()
        self.prog_counter += 1

        if self.prog_counter == self.result_count:
            sys.stdout.write('\n')
            sys.stdout.flush()

    def wfs_search(self, typename):
        self.result_count = 0
        self.prog_counter = 0

    def wfs_result(self, number_of_results):
        self.result_count = number_of_results

    def xml_cache_hit(self, url):
        self._write_progress('c')

    def xml_downloaded(self, url):
        self._write_progress('.')

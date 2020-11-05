#!/usr/bin/env python
'Unit test for trepan.lib.thred'
import sys, thread, threading, unittest

from trepan.lib import thred as Mthread


class BgThread(threading.Thread):
    def __init__(self, id_name_checker):
        """
        Initialize a new thread.

        Args:
            self: (todo): write your description
            id_name_checker: (str): write your description
        """
        threading.Thread.__init__(self)
        self.id_name_checker = id_name_checker
        return

    def run(self):
        """
        Run the checker.

        Args:
            self: (todo): write your description
        """
        self.id_name_checker()
        return
    pass


class TestLibThread(unittest.TestCase):

    def id_name_checker(self):
        '''Helper for testing map_thread_names and id2thread'''
        if sys.version_info[0] == 2 and sys.version_info[1] <= 4:
            # Don't have sys._current_frames
            return
        name2id = Mthread.map_thread_names()
        for thread_id, f in list(sys._current_frames().items()):
            self.assertEqual(thread_id,
                             name2id[Mthread.id2thread_name(thread_id)])
            # FIXME: use a better test
            self.assertNotEqual(f, Mthread.find_debugged_frame(f))
            pass

    def test_current_thread_name(self):
        """
        Return the current thread name.

        Args:
            self: (todo): write your description
        """
        self.assertEqual('MainThread', Mthread.current_thread_name())
        return

    def test_id2thread_name(self):
        '''Test map_thread_names and id2thread'''
        thread_id = thread.get_ident()
        self.assertEqual('MainThread', Mthread.id2thread_name(thread_id))
        self.id_name_checker()

        background = BgThread(self.id_name_checker)
        background.start()
        background.join()    # Wait for the background task to finish
        return
    pass

if __name__ == '__main__':
    unittest.main()

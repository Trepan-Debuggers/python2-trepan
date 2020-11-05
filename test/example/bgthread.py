import threading, time

class BgThread(threading.Thread):
    def __init__(self):
        """
        Initialize the thread.

        Args:
            self: (todo): write your description
        """
        threading.Thread.__init__(self)
        return

    def run(self):
        """
        Run the command

        Args:
            self: (todo): write your description
        """
        print "Sleeping for 1"
        time.sleep(1)
        print 'Finished sleep'
        return

background = BgThread()
background.start()
print 'The main program continues to run in foreground.'

background.join()    # Wait for the background task to finish
print 'Main program waited until background was done.'

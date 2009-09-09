# -*- coding: utf-8 -*-
"""A base class for a debugger interface."""

NotImplementedMessage = "This method must be overriden in a subclass"

class DebuggerInterface():
    """
A debugger interface handles the communication or interaction with between
the program and the outside portion which could be
    - a user, 
    - a front-end that talks to a user, or
    - another interface in another process or computer
    """

    def __init__(self, inp=None, out=None):
        self.input  = inp or sys.stdin
        self.output = out or sys.stdout
        self.interactive = False 
        return

    def close(self):
        """ Closes all input and/or output """
        raise NotImplementedError, NotImplementedMessage
        return

    def confirm(self, prompt, default):
        """ Called when a dangerous action is about to be done to make sure
        it's okay. `prompt' is printed; user response is returned."""
        raise NotImplementedError, NotImplementedMessage

    def errmsg(self, str, prefix="*** "):
        """Common routine for reporting debugger error messages.
           """
        raise NotImplementedError, NotImplementedMessage

    def finalize(self, last_wishes=None):
        raise NotImplementedError, NotImplementedMessage

    def msg(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        if hasattr(self.output, 'writeline'):
            self.output.writeline(msg)
        elif hasattr(self.output, 'writelines'):
            self.output.writelines(msg + "\n")
            pass
        return

    def msg_nocr(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will not have a newline added to it
        """
        self.output.write(msg)
        return

    def read_command(self, prompt):
        raise NotImplementedError, NotImplementedMessage

    def readline(self, prompt, add_to_history=True):
        raise NotImplementedError, NotImplementedMessage
    
    pass

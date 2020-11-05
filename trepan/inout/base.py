# -*- coding: utf-8 -*-
#   Copyright (C) 2009, 2014-2015 Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""classes to support communication to and from the debugger.  This
communcation might be to/from another process or another computer.
And reading may be from a debugger command script.

For example, we'd like to support Sockets, and serial lines and file
reading, as well a readline-type input. Encryption and Authentication
methods might decorate some of the communication channels.

Some ideas originiated as part of Matt Fleming's 2006 Google Summer of
Code project.
"""

NotImplementedMessage = "This method must be overriden in a subclass"


# FIXME: In 2.6 we can really use an Absctract Class (ABC). But for now,
# we want 2.5.x compatibility.
class DebuggerInputBase(object):
    """ This is an abstract class that specifies debugger input. """

    def __init__(self, inp=None, opts=None):
        """
        Initialize a new input.

        Args:
            self: (todo): write your description
            inp: (int): write your description
            opts: (todo): write your description
        """
        self.input   = None
        self.closed = None
        return

    def close(self):
        """
        Close the connection.

        Args:
            self: (todo): write your description
        """
        self.closed = True
        if self.input:
            self.input.close()
            pass
        return

    def use_history(self):
        """
        Return true if history : attrpc.

        Args:
            self: (todo): write your description
        """
        return False

    def open(self, inp, opts=None):
        """Use this to set where to read from. """
        raise NotImplementedError(NotImplementedMessage)

    def readline(self, use_raw=None):
        """Read a line of input. EOFError will be raised on EOF.

        Note that we don't support prompting first. Instead, arrange
        to call DebuggerOutput.write() first with the prompt. If
        `use_raw' is set raw_input() will be used in that is supported
        by the specific input input. If this option is left None as is
        normally expected the value from the class initialization is
        used.
        """
        raise NotImplementedError(NotImplementedMessage)

    pass


# FIXME: In 2.6 we can really use an Abstract Class (ABC). But for now,
# we want 2.5.x compatibility.
class DebuggerOutputBase(object):
    """ This is an abstract class that specifies debugger output. """

    def __init__(self, out=None, opts=None):
        """
        Initialize an output.

        Args:
            self: (todo): write your description
            out: (str): write your description
            opts: (todo): write your description
        """
        self.output = None
        return

    def close(self):
        """
        Closes the connection.

        Args:
            self: (todo): write your description
        """
        if self.output:
            self.output.close()
            pass
        return

    def flush(self):
        """
        Flush the given message.

        Args:
            self: (todo): write your description
        """
        raise NotImplementedError(NotImplementedMessage)

    def write(self, output):
        """Use this to set where to write to. output can be a
        file object or a string. This code raises IOError on error.
        """
        raise NotImplementedError(NotImplementedMessage)

    def writeline(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        self.write("%s\n" % msg)
        return
    pass


class DebuggerInOutBase(object):
    """ This is an abstract class that specifies debugger input output when
    handled by the same channel, e.g. a socket or tty.
    """

    def __init__(self, inout=None, opts=None):
        """
        Initialize the object.

        Args:
            self: (todo): write your description
            inout: (int): write your description
            opts: (todo): write your description
        """
        self.inout = None
        return

    def close(self):
        """
        Closes the connection.

        Args:
            self: (todo): write your description
        """
        if self.inout:
            self.inout.close()
            pass
        return

    def flush(self):
        """
        Flush the given message.

        Args:
            self: (todo): write your description
        """
        raise NotImplementedError(NotImplementedMessage)

    def open(self, inp, opts=None):
        """Use this to set where to read from. """
        raise NotImplementedError(NotImplementedMessage)

    def readline(self, use_raw=None):
        """Read a line of input. EOFError will be raised on EOF.

        Note that we don't support prompting first. Instead, arrange
        to call DebuggerOutput.write() first with the prompt. If
        `use_raw' is set raw_input() will be used in that is supported
        by the specific input input. If this option is left None as is
        normally expected the value from the class initialization is
        used.
        """
        raise NotImplementedError(NotImplementedMessage)

    def write(self, output):
        """Use this to set where to write to. output can be a
        file object or a string. This code raises IOError on error.
        """
        raise NotImplementedError(NotImplementedMessage)

    def writeline(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        self.write("%s\n" % msg)
        return
    pass


# Demo
if __name__=='__main__':
    class MyInput(DebuggerInputBase):
        def open(self, inp, opts=None):
            """
            Open a file using the specified options.

            Args:
                self: (todo): write your description
                inp: (str): write your description
                opts: (todo): write your description
            """
            print("open(%s) called" % inp)
            pass
        pass

    class MyOutput(DebuggerOutputBase):
        def writeline(self, s):
            """
            Write string s to the output.

            Args:
                self: (todo): write your description
                s: (int): write your description
            """
            print "writeline:", s
            pass
        pass
    inp = MyInput()
    inp.open('foo')
    inp.close()
    out = MyOutput()
    out.writeline('foo')
    try:
        out.write('foo')
    except NotImplementedError:
        print 'Ooops. Forgot to implement write()'
        pass

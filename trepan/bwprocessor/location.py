# -*- coding: utf-8 -*-
''' Location routines'''

import pyficache, linecache, tempfile

from trepan.lib import stack as Mstack


def format_location(proc_obj):
    """Show where we are. GUI's and front-end interfaces often
    use this to update displays. So it is helpful to make sure
    we give at least some place that's located in a file.
    """
    i_stack = proc_obj.curindex
    if i_stack is None or proc_obj.stack is None:
        return False
    location = {}
    core_obj = proc_obj.core
    dbgr_obj = proc_obj.debugger

    # Evaluation routines like "exec" don't show useful location
    # info. In these cases, we will use the position before that in
    # the stack.  Hence the looping below which in practices loops
    # once and sometimes twice.
    while i_stack >= 0:
        frame_lineno = proc_obj.stack[i_stack]
        i_stack -= 1
        frame, lineno = frame_lineno

        filename = Mstack.frame2file(core_obj, frame)

        location['filename'] = filename
        location['fn_name']  = frame.f_code.co_name
        location['lineno']   = lineno

        if '<string>' == filename and dbgr_obj.eval_string:
            filename = pyficache.unmap_file(filename)
            if '<string>' == filename:
                fd = tempfile.NamedTemporaryFile(suffix='.py',
                                                 prefix='eval_string',
                                                 delete=False)
                fd.write(dbgr_obj.eval_string)
                fd.close()
                pyficache.remap_file(fd.name, '<string>')
                filename = fd.name
                pass
            pass

        opts = {
            'reload_on_change' : proc_obj.settings('reload'),
            'output'           : 'plain'
            }
        line = pyficache.getline(filename, lineno, opts)
        if not line:
            line = linecache.getline(filename, lineno,
                                     proc_obj.curframe.f_globals)
            pass

        if line and len(line.strip()) != 0:
            location['text'] = line
            pass
        if '<string>' != filename: break
        pass

    return location

def print_location(proc_obj, event=None):
    """
    Print the location of the event.

    Args:
        proc_obj: (todo): write your description
        event: (todo): write your description
    """
    response = proc_obj.response
    response['name'] = 'status'
    response['location'] = format_location(proc_obj)
    if event:
        response['event'] = event
        if event in ['return', 'exception']:
            val = proc_obj._saferepr(proc_obj.event_arg)
            event['arg'] = val
            pass
        pass
    proc_obj.intf[-1].msg(response)
    return


# Demo it
if __name__=='__main__':
    class MockDebugger:
        def __init__(self):
            """
            Initialize the module

            Args:
                self: (todo): write your description
            """
            self.eval_string = None
        pass

    class MockProcessor:
        def __init__(self, core_obj):
            """
            Initialize the core object.

            Args:
                self: (todo): write your description
                core_obj: (todo): write your description
            """
            self.curindex = 0
            self.stack = []
            self.core = core_obj
            self.debugger = MockDebugger()
            self.opts = {'highlight': 'plain', 'reload': False}
            pass

        def settings(self, key):
            """
            Get the settings for a key.

            Args:
                self: (todo): write your description
                key: (str): write your description
            """
            return self.opts[key]
        pass

    class MockCore:
        """
        Returns the filename for a file.

        Args:
            self: (todo): write your description
            fn: (str): write your description
        """
        def filename(self, fn): return fn

        """
        Determine whether the frame filename.

        Args:
            self: (todo): write your description
            frame: (todo): write your description
        """
        def canonic_filename(self, frame): return frame.f_code.co_filename
        pass

    core = MockCore()
    cmdproc = MockProcessor(core)

    import sys
    cmdproc.curframe = cmdproc.frame = sys._getframe()
    cmdproc.stack.append((sys._getframe(), 10))

    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(format_location(cmdproc))

    def test(cmdproc, pp):
        """
        Run test.

        Args:
            cmdproc: (int): write your description
            pp: (int): write your description
        """
        cmdproc.stack[0:0] = [(sys._getframe(1), 1)]
        pp.pprint(format_location(cmdproc))
        pass
    eval('test(cmdproc, pp)')
    cmdproc.debugger.eval_string = 'Fooled you!'
    eval('test(cmdproc, pp)')
    pass

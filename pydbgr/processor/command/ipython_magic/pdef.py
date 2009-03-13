# from IPython.genutils import arg_split
def ipy_pdef(obj, args):
    """The debugger interface to magic_pdef"""
    # argv = arg_split(args)
    debugger = obj.user_ns['ipshell'].debugger
    proc = debugger.core.processor
    namespaces = [('Locals', proc.curframe.f_locals),
                  ('Globals', proc.curframe.f_globals)]
    __IPYTHON__.magic_pdef("pdef %s" % args, namespaces)
    return

import IPython
if __name__ == '__main__':
    ipshell = IPython.Shell.IPShellEmbed()
    pass

ip = IPython.ipapi.get()
ip.expose_magic('pdef', ipy_pdef)

import IPython
# from IPython.genutils import arg_split
def ipy_pdoc(obj, args):
    """The debugger interface to magic_pdoc"""
    # argv = arg_split(args)
    debugger = obj.user_ns['ipshell'].debugger
    proc = debugger.core.processor
    namespaces = [('Locals', proc.curframe.f_locals),
                  ('Globals', proc.curframe.f_globals)]
    __IPYTHON__.magic_pdoc("pdoc %s" % args, namespaces=namespaces)
    return

if __name__ == '__main__':
    ipshell = IPython.Shell.IPShellEmbed()
    pass

ip = IPython.ipapi.get()
ip.expose_magic('pdoc', ipy_pdoc)

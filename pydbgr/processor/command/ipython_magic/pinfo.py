import IPython
# from IPython.genutils import arg_split
def ipy_pinfo(obj, args):
    """The debugger equivalant of ?obj"""
    # argv = arg_split(args)
    debugger = obj.user_ns['ipshell'].debugger
    proc = debugger.core.processor
    namespaces = [('Locals', proc.curframe.f_locals),
                  ('Globals', proc.curframe.f_globals)]
    __IPYTHON__.magic_pinfo("pinfo %s" % args, namespaces)
    return

if __name__ == '__main__':
    ipshell = IPython.Shell.IPShellEmbed()
    pass

ip = IPython.ipapi.get()
ip.expose_magic('pinfo', ipy_pinfo)

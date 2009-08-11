# -*- coding: utf-8 -*-
#   Copyright (C) 2009 Rocky Bernstein
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
try:
    import IPython

    import os, sys

    # Our local modules
    from import_relative import import_relative, get_srcdir

    import_relative('lib', '...', 'pydbgr')
    Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
    Mmisc      = import_relative('misc', '...', 'pydbgr')

    from IPython.genutils import arg_split

    class IPythonCommand(Mbase_cmd.DebuggerCommand):
        """ipython [-d] [ipython-arg1 ipython-arg2 ...]

Run IPython as a command subshell. You need to have ipython installed
for this command to work. If no IPython options are given, the
following options are passed: 
   -noconfirm_exit -prompt_in1 'Pydbgr In [\#]: '

If -d is passed you can access debugger state via local variable "debugger".
Debugger commands like are installed as IPython magic commands, e.g.
%list, %up, %where.
"""
        aliases       = ('ipy',)
        category      = 'support'
        min_args      = 0
        max_args      = None
        name          = os.path.basename(__file__).split('.')[0]
        need_stack    = False
        short_help    = 'Run IPython as a command subshell'

        def run(self, args):

            debug = False
            if len(args) > 1:
                if args[1] == '-d':
                    debug = True
                    argv  = args[2:]
                else:
                    argv  = args[1:]
            else:
                argv = ['-noconfirm_exit','-prompt_in1', 'Pydbgr In [\\#]: ']
                pass

            if self.proc.curframe and self.proc.curframe.f_locals:
                user_ns = self.proc.curframe.f_locals
            else:
                user_ns = {}
                pass

            # IPython does it's own history thing.
            # Make sure it doesn't damage ours.
            have_line_edit = self.debugger.intf[-1].input.line_edit
            if have_line_edit:
                try:
                    self.proc.write_history_file()
                except IOError:
                    pass
                pass

            if debug: user_ns['debugger'] = self.debugger
            global ipshell
            ipshell = IPython.Shell.IPShellEmbed(argv=argv, user_ns=user_ns)
            user_ns['ipshell'] = ipshell

            # Give ipython and the user a way to get access to the debugger
            setattr(ipshell, 'debugger', self.debugger)

            if hasattr(ipshell.IP, "magic_pydbgr"):
                # We get an infinite loop when doing recursive edits
                self.msg("removing magic %pydbgr")
                delattr(ipshell.ip, "magic_pydbgr")
                pass

            # add IPython "magic" commands for all debugger comamnds and
            # aliases.  No doubt, this probably could be done in a
            # better way without "exec".  (Someone just needs to suggest
            # a way...)
            ip = IPython.ipapi.get()
            magic_fn_template="""
def ipy_%s(self, args):
   argv = arg_split(args)
   proc = ipshell.debugger.core.processor
   cmd = proc.name2cmd['%s']
   leave = cmd.run(['%s'] + argv)
   if leave: self.shell.exit()
   return
"""
            expose_magic_template = 'ip.expose_magic("%s", ipy_%s)'
            for cmd_instance in self.proc.cmd_instances:
                name = cmd_instance.name
                exec magic_fn_template % ((name,) * 3)
                for alias in cmd_instance.aliases:
                    exec expose_magic_template % (alias, name)
                pass

# We don't have any of these yet. When we do we can uncomment...
#             # Add more IPython magic commands using files in the
#             # ipython_magic subdirectory.  This also gives us a way to
#             # overwrite the default magics created above.
#             srcdir = get_srcdir()
#             sys.path.insert(0, srcdir)
#             Mcommand = import_relative('ipython_magic')
#             for mod_name in Mcommand.__modules__:
#                 import_name = "ipython_magic." + mod_name
#                 command_mod = getattr(__import__(import_name), mod_name)
#                 fn = getattr(command_mod, 'ipy_%s' % mod_name)
#                 ip.expose_magic(mod_name, fn)
#                 pass
#             sys.path.remove(srcdir)
        
            # And just when you thought we've forgotten about running
            # the shell...
            ipshell()

#             # Restore our history if we can do so.
#             if have_line_edit and self.histfile is not None:
#                 try:
#                     self.readline.read_history_file(self.histfile)
#                 except IOError:
#                     pass
#                 return False
            return self.continue_running
        pass
    pass
except ImportError:
    pass

if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = IPythonCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    if len(sys.argv) > 1:
        print "Type IPython commands; exit() or EOF (Ctrl-D) quits."
        if sys.argv[1] == '-d':
            argv  = sys.argv[1:]
        else:
            argv  = sys.argv[2:]
            pass
        print command.run(['ipython'] + argv)
        pass
    pass

from import_relative import *
# Our local modules

Mbase_subcmd  = import_relative('base_subcmd', os.path.pardir)

class ShowDbgPydbgr(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """Show debugging the debugger"""
    min_abbrev = 4 # Min 'show pydb"
    pass

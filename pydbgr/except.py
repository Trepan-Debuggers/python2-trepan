class DebuggerQuit(Exception):
    """Exception to signal graceful debugger termination"""

class DebuggerRestart(Exception):
    """Exception to signal a (soft) program restart"""


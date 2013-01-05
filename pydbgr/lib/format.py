from pygments.formatters.terminal import TERMINAL_COLORS
from pygments.console import ansiformat
from pygments.token import *

def format_token(ttype, token, colorscheme=TERMINAL_COLORS, highlight='light' ):
    if 'plain' == highlight: return token
    darkbg = 'light' == highlight

    color = colorscheme.get(ttype)
    if color:
        color = color[darkbg]
        return ansiformat(color, token)
        pass
    return token

Arrow      = Name.Variable
Compare    = Name.Exception
Const      = String
Filename   = Comment.Preproc
Function   = Name.Function
Label      = Operator.Word
LineNumber = Number
Offset     = Operator
Opcode     = Name.Function
Return     = Operator.Word
Var        = Keyword

# Should come last since "Name" is used above
Name       = Comment.Preproc

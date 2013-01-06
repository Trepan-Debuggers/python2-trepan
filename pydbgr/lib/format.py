# -*- coding: utf-8 -*-
#   Copyright (C) 2013 Rocky Bernstein <rocky@gnu.org>
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
'''Pygments-related terminal formatting'''

from pygments                     import highlight, lex
from pygments.console             import ansiformat
from pygments.filter              import Filter
from pygments.formatters          import TerminalFormatter
from pygments.formatters.terminal import TERMINAL_COLORS
from pygments.lexers              import RstLexer
from pygments.token               import *

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

color_scheme = TERMINAL_COLORS.copy()
color_scheme[Generic.Strong] = ('*black*', '*white*')
color_scheme[Name.Variable]  = ('_black_', '_white_')
color_scheme[Generic.Emph]   = TERMINAL_COLORS[Comment.Preproc]

# Should come last since "Name" is used above
Name = Comment.Preproc

class RstFilter(Filter):

    def __init__(self, **options):
        Filter.__init__(self, **options)
        pass

    def filter(self, lexer, stream):
        for ttype, value in stream:
            if ttype is Token.Name.Variable:
                value = value[1:-1]
                pass
            if ttype is Token.Generic.Emph:
                type
                value = value[1:-1]
                pass            
            elif ttype is Token.Generic.Strong:
                value = value[2:-2]
                pass
            yield ttype, value
            pass
        return
    pass

rst_lex = RstLexer()
rst_filt = RstFilter()
rst_lex.add_filter(rst_filt)
tf = TerminalFormatter(colorscheme=color_scheme)

def rst_text(text):
    return highlight(text, rst_lex, tf)

if __name__ == '__main__':
    string = '`A` very *emphasis* **strong** `code`'
    print highlight(string, rst_lex, tf)
    for t in lex(string, rst_lex):
        print t
        pass
    pass

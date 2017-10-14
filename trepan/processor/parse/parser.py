#  Copyright (c) 2017 Rocky Bernstein
"""
Parsing for a trepan2/trepan3k debugger
"breakpoint' or "list" command arguments

This is a debugger location along with:
 - an optional condition parsing for breakpoints commands
 - a range or count for "list" commands
"""

from __future__ import print_function

import sys
from spark_parser.ast import AST

from trepan.processor.parse.scanner import LocationScanner

from spark_parser import GenericASTBuilder

DEFAULT_DEBUG = {'rules': False, 'transition': False, 'reduce': False,
                 # 'errorstack': 'full',
                 'dups': False, 'local_print': False}

class LocationError(Exception):
    def __init__(self, text, text_cursor):
        self.text = text
        self.text_cursor = text_cursor

    def __str__(self):
        return self.text + "\n" + self.text_cursor

class LocationParser(GenericASTBuilder):
    """Location parsing as used in trepan2 and trepan3k
    for list and breakpoint commands
    Note: function parse() comes from GenericASTBuilder
    """

    def __init__(self, start_nt, text, debug=None):
        super(LocationParser, self).__init__(AST, start_nt, debug=DEFAULT_DEBUG)
        self.debug = debug
        self.text  = text

    def error(self, tokens, index):
        token = tokens[index]
        if self.debug.get('local_print', False):
            print(self.text)
            print(' ' * (token.offset + len(str(token.value))) + '^')
            print("Syntax error at or near token '%s'" % token.value)
            if 'context' in self.debug and self.debug['context']:
                super(LocationParser, self).error(tokens, index)
        raise LocationError(self.text,
                         ' ' * (token.offset + len(str(token.value))) + '^')

    def nonterminal(self, nt, args):
        has_len = hasattr(args, '__len__')

        collect = ('tokens',)
        if nt in collect:
            #
            #  Collect iterated thingies together.
            #
            rv = args[0]
            for arg in args[1:]:
                rv.append(arg)

        if (has_len and len(args) == 1 and
            hasattr(args[0], '__len__') and len(args[0]) == 1):
            # Remove singleton derivations
            rv = GenericASTBuilder.nonterminal(self, nt, args[0])
            del args[0] # save memory
        else:
            rv = GenericASTBuilder.nonterminal(self, nt, args)
        return rv

    def p_bp_location(self, args):
        '''
        bp_start    ::= opt_space location_if opt_space
        '''

    def p_list_range(self, args):
        '''
        ## START HERE
        range_start  ::= opt_space range
        range ::= location
        range ::= location opt_space COMMA opt_space NUMBER
        range ::= COMMA opt_space location
        range ::= location opt_space COMMA
        range ::= opt_space DIRECTION
        '''

    ##########################################################
    # Expression grammar rules. Grammar rule functions
    # start with the name p_ and are collected automatically
    ##########################################################
    def p_location(self, args):
        '''
        opt_space   ::= SPACE?

        location_if ::= location
        location_if ::= location SPACE IF tokens

        # Note no space is allowed between FILENAME and NUMBER
        location    ::= FILENAME COLON NUMBER
        location    ::= FUNCNAME

        # In the below, the second FILENAME is really the word
        # "line". We ferret this out in a reduction rule though.
        location    ::= FILENAME SPACE FILENAME SPACE NUMBER

        # If just a number is given, the the filename is implied
        location    ::=  NUMBER
        location    ::=  METHOD

        # For tokens we accept anything. Were really just
        # going to use the underlying string from the part
        # after "if".  So below we all of the possible tokens

        tokens      ::= token+
        token       ::= FILENAME
        token       ::= FUNCNAME
        token       ::= COLON
        token       ::= NUMBER
        token       ::= COMMA
        token       ::= DIRECTION
        token       ::= SPACE
        '''

    def add_custom_rules(self, tokens, orig_customize):
        self.check_reduce['location'] = 'tokens'

    def reduce_is_invalid(self, rule, ast, tokens, first, last):
        if rule == ('location', ('FILENAME', 'SPACE', 'FILENAME', 'SPACE', 'NUMBER')):
            # In this rule the 2nd filename should be 'line'. if not, the rule
            # is invalid
            return tokens[first+2].value != 'line'
        return False


def parse_location(start_symbol, text, out=sys.stdout,
                      show_tokens=False, parser_debug=DEFAULT_DEBUG):
    assert isinstance(text, str)
    tokens = LocationScanner().tokenize(text)
    if show_tokens:
        for t in tokens:
            print(t)

    # For heavy grammar debugging
    # parser_debug = {'rules': True, 'transition': True, 'reduce': True,
    #                 'errorstack': True, 'dups': True}
    # parser_debug = {'rules': False, 'transition': False, 'reduce': True,
    #                 'errorstack': True, 'dups': False}

    parser = LocationParser(start_symbol, text, parser_debug)
    parser.check_grammar(frozenset(('bp_start', 'range_start')))
    parser.add_custom_rules(tokens, {})
    return parser.parse(tokens)

def parse_bp_location(*args, **kwargs):
    return parse_location('bp_start', *args, **kwargs)

def parse_range(*args, **kwargs):
    return parse_location('range_start', *args, **kwargs)

# if __name__ == '__main__':
#     lines = """
#     /tmp/foo.py:12
#     '''/tmp/foo.py:12''' line 14
#     /tmp/foo.py line 12
#     '''/tmp/foo.py line 12''' line 25
#     12
#     ../foo.py:5
#     gcd()
#     foo.py line 5 if x > 1
#     """.splitlines()
#     for line in lines:
#         if not line.strip():
#             continue
#         print("=" * 30)
#         print(line)
#         print("+" * 30)
#         ast = parse_bp_location(line, show_tokens=True)
#         print(ast)

#     bad_lines = """
#     /tmp/foo.py
#     '''/tmp/foo.py'''
#     /tmp/foo.py 12
#     /tmp/foo.py line
#     gcd()
#     foo.py if x > 1
#     """.splitlines()
#     for line in bad_lines:
#         if not line.strip():
#             continue
#         print("=" * 30)
#         print(line)
#         print("+" * 30)
#         try:
#             ast = parse_bp_location(line, show_tokens=True)
#         except:
#             continue
#         print(ast)

#     lines = """
#     1
#     2,
#     ,3
#     4,10
#     """.splitlines()
#     for line in lines:
#         if not line.strip():
#             continue
#         print("=" * 30)
#         print(line)
#         print("+" * 30)
#         ast = parse_range(line, show_tokens=True)
#         print(ast)

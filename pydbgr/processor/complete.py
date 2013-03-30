# Completion part of CommandProcessor
import re

def complete_token(complete_ary, prefix):
    return sorted([cmd for cmd in
                   complete_ary if cmd.startswith(prefix)]) + [None]

# Find the next token in str string from start_pos, we return
# the token and the next blank position after the token or
# str.size if this is the last token. Tokens are delimited by
# white space.
def next_token(str, start_pos):
    look_at = str[start_pos:-1]
    match = re.search('\S', look_at)
    if match:
        pos = match.pos
    else:
        pos = 0
        pass
    next_nonblank_pos = start_pos + pos
    next_match = re.search('\s', str[next_nonblank_pos:-1])
    if next_match:
        next_blank_pos = next_nonblank_pos + next_match.pos
    else:
        next_blank_pos = len(str)
        pass
    return [next_blank_pos, str[next_nonblank_pos:next_blank_pos-1]]

def complete_token_with_next(complete_hash, prefix, cmd_prefix=''):
    result = []
    for cmd_name, cmd_obj in complete_hash:
        if cmd_name.startwith(cmd_prefix + prefix):
            result.append([cmd_name[len(cmd_prefix):-1], cmd_obj])
            pass
        pass
    pass
    return sorted(result, cmp=lambda a, b: cmp(a[0].lower(), b[0].lower()))

def completer(self, str, state, last_token=''):
    next_blank_pos, token = next_token(str, 0)
    if len(token) == 0 and not 0 == len(last_token):
        return ['', None]
    matches = complete_token(self.commands.keys() +
                             self.aliases.keys() +
                             self.macros.keys(), token)
    return matches + [None]

if __name__=='__main__':
    print(complete_token(['ba', 'aa', 'ab'], 'a'))
    print(complete_token(['cond', 'condition', 'continue'], 'cond'))
    print(next_token('ab cd ef', 0))
    print(next_token('ab cd ef', 2))
    pass

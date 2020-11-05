class Token:
    """
    Class representing a token.
    kind: the kind of token, e.g. filename, number, other
    value: specific instance value, e.g. "/tmp/foo.c", or 5
    offset: byte offset from start of parse string
    """
    def __init__(self, kind, value=None, offset=None):
        """
        Initialize this message.

        Args:
            self: (todo): write your description
            kind: (int): write your description
            value: (todo): write your description
            offset: (int): write your description
        """
        self.offset = offset
        self.kind = kind
        self.value = value

    def __eq__(self, o):
        """ '==', but it's okay if offset is different"""
        if isinstance(o, Token):
            # Both are tokens: compare kind and value
            # It's okay if offsets are different
            return (self.kind == o.kind)
        else:
            return self.kind == o

    def __repr__(self):
        """
        Return a repr representation of this class.

        Args:
            self: (todo): write your description
        """
        return str(self.kind)

    def __repr1__(self, indent, sib_num=''):
        """
        Return a human - readable string representation of this object.

        Args:
            self: (todo): write your description
            indent: (int): write your description
            sib_num: (int): write your description
        """
        return self.format(line_prefix=indent, sib_num=sib_num)

    def __str__(self):
        """
        Return a formatted string with the format.

        Args:
            self: (todo): write your description
        """
        return self.format(line_prefix='')

    def format(self, line_prefix='', sib_num=None):
        """
        Format the formatted line.

        Args:
            self: (todo): write your description
            line_prefix: (str): write your description
            sib_num: (int): write your description
        """
        if sib_num:
            sib_num = "%d." % sib_num
        else:
            sib_num = ''
        prefix = ('%s%s' % (line_prefix, sib_num))
        offset_opname = '%5s %-10s' % (self.offset, self.kind)
        if not self.value:
            return "%s%s" % (prefix, offset_opname)
        return "%s%s %s" % (prefix, offset_opname,  self.value)

    def __hash__(self):
        """
        Returns the hash of this node.

        Args:
            self: (todo): write your description
        """
        return hash(self.kind)

    def __getitem__(self, i):
        """
        Return the item from the given index.

        Args:
            self: (todo): write your description
            i: (todo): write your description
        """
        raise IndexError

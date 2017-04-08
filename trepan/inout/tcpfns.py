# -*- coding: utf-8 -*-
#   Copyright (C) 2009-2014, 2017 Rocky Bernstein <rocky@gnu.org>
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
"""Subsidiary routines used to "pack" and "unpack" TCP messages. """

TCP_MAX_PACKET = 8192  # Largest size for a recv
LOG_MAX_MSG    = 8     # int(log(TCP_MAX_PACKET)) # big packet


def pack_msg(msg):
    fmt = '%%0%dd' % LOG_MAX_MSG  # A funny way of writing: '%08d'
    return ( fmt % len(msg)) + msg


def unpack_msg(buf):
    length  = int(buf[0:LOG_MAX_MSG])
    data = buf[LOG_MAX_MSG:LOG_MAX_MSG+length]
    buf = buf[LOG_MAX_MSG+length:]
    return buf, data

def unpack_msg_segment(buf):
    if len(buf) == 0:
        # Fake a quit
        return '', 'q', 1
    length  = int(buf[0:LOG_MAX_MSG])
    data    = buf[LOG_MAX_MSG:LOG_MAX_MSG+length]
    buf     = buf[LOG_MAX_MSG+length:]
    return buf, data, length

# Demo
if __name__=='__main__':
    msg = "Hi there!"
    assert unpack_msg(pack_msg(msg))[1] == msg
    pass

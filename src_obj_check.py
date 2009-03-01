import marshal
def source_obj_check(source_filename, obj_filename):
    source_dump = marshal.dumps(compile(open(source_filename).read(), 
                                        source_filename, 'exec'))
    open('/tmp/f1', 'w').write(source_dump)
    obj_dump = open(obj_filename).read()[8:]
    open('/tmp/f2', 'w').write(obj_dump)
    return source_dump == obj_dump

print source_obj_check('/src/external-vcs/pydbgr-svn/__pkginfo__.py', '__pkginfo__.pyc')



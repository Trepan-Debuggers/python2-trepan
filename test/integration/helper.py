import difflib, os, sys, time
from import_relative import get_srcdir

def run_debugger(testname, python_file, dbgr_opts='', args='',
                 outfile=None):
    srcdir    = get_srcdir()
    datadir   = os.path.join(srcdir, '..', 'data')
    progdir   = os.path.join(srcdir, '..', 'example')  
    dbgrdir   = os.path.join(srcdir, '..', '..', 'pydbgr')
    dbgr_short= "cli.py"
    dbgr_path = os.path.join(dbgrdir, dbgr_short)

    rightfile = os.path.join(datadir, "%s.right" % testname)

    os.environ['PYTHONPATH']=os.pathsep.join(sys.path)
    cmdfile     = os.path.join(datadir, "%s.cmd"   % testname)
    outfile     = os.path.join(srcdir, "%s.out" % testname)
    programfile = os.path.join(progdir, python_file)
    outfile_opt = '--output=%s ' % outfile

    if os.path.exists(outfile): os.unlink(outfile)

    cmd = "%s --command %s %s %s %s %s" % \
          (dbgr_path, cmdfile, outfile_opt, dbgr_opts, programfile, args)

    print cmd
    os.system(cmd)
    fromfile  = rightfile
    fromdate  = time.ctime(os.stat(fromfile).st_mtime)
    fromlines = open(fromfile, 'U').readlines()
    tofile    = outfile
    todate    = time.ctime(os.stat(tofile).st_mtime)
    tolines   = open(tofile, 'U').readlines()
    diff = list(difflib.unified_diff(fromlines, tolines, fromfile,
                                     tofile, fromdate, todate))
    if len(diff) == 0:
        os.unlink(outfile)
        pass
    for line in diff:
        print line,
        pass
    return len(diff) == 0
    



def enquote_executable(executable):
    if ' ' in executable:
        # make sure we quote only the executable in case of env
        # for example /usr/bin/env "/dir with spaces/bin/jython"
        # instead of "/usr/bin/env /dir with spaces/bin/jython"
        # otherwise whole
        if executable.startswith('/usr/bin/env '):
            env, _executable = executable.split(' ', 1)
            if ' ' in _executable and not _executable.startswith('"'):
                executable = '%s "%s"' % (env, _executable)
        else:
            if not executable.startswith('"'):
                executable = '"%s"' % executable
    return executable
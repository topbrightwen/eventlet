# https://github.com/eventlet/eventlet/issues/38
# get_hub on windows broken by kqueue
from __future__ import print_function

# no standard tests in this file, ignore
__test__ = False


def main():
    # Simulate absence of kqueue even on platforms that support it.
    import select
    try:
        del select.kqueue
    except AttributeError:
        pass

    from eventlet.support.six.moves import builtins

    original_import = builtins.__import__
    state = [False]

    def fail_import(name, *args, **kwargs):
        if 'epoll' in name:
            raise ImportError('disabled for test')
        if 'kqueue' in name:
            state[0] = True
        return original_import(name, *args, **kwargs)

    builtins.__import__ = fail_import

    import eventlet.hubs
    eventlet.hubs.get_default_hub()
    assert state[0], 'did not try to import kqueue'
    print('pass')


if __name__ == '__main__':
    main()

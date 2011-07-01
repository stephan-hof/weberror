import sys
import os
from weberror.reporter import *
from weberror import collector

def setup_file(fn, content=None):
    fn = os.path.join(os.path.dirname(__file__), 'reporter_output', fn)
    if os.path.exists(fn):
        os.unlink(fn)
    if content is not None:
        f = open(fn, 'wb')
        f.write(content)
        f.close()
    return fn
    
def test_logger():
    fn = setup_file('test_logger.log')
    rep = LogReporter(
        filename=fn,
        show_hidden_frames=False)
    try:
        int('a')
    except:
        exc_data = collector.collect_exception(*sys.exc_info())
    else:
        assert 0
    rep.report(exc_data)
    content = open(fn).read()
    assert len(content.splitlines()) == 4
    assert 'ValueError' in content
    assert 'int' in content
    assert 'test_reporter.py' in content
    assert 'test_logger' in content
    
    try:
        1 / 0
    except:
        exc_data = collector.collect_exception(*sys.exc_info())
    else:
        assert 0
    rep.report(exc_data)
    content = open(fn).read()
    print content
    assert len(content.splitlines()) == 8
    assert 'ZeroDivisionError' in content

def test_file():
    fn = setup_file('test_file.log')
    f = open(fn, 'w')
    rep = FileReporter(
        file=f,
        show_hidden_frames=False)

    try:
        int('a')
    except:
        exc_data = collector.collect_exception(*sys.exc_info())
    else:
        assert 0
    rep.report(exc_data)
    f.flush()
    content = open(fn).read()
    assert len(content.splitlines()) == 4
    assert 'ValueError' in content
    assert 'int' in content
    assert 'test_reporter.py' in content
    assert 'test_file' in content

    try:
        1 / 0
    except:
        exc_data = collector.collect_exception(*sys.exc_info())
    else:
        assert 0
    rep.report(exc_data)
    f.flush()
    content = open(fn).read()
    print content
    assert len(content.splitlines()) == 8
    assert 'ZeroDivisionError' in content

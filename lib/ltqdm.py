from time import sleep

import contextlib
import sys

from tqdm import tqdm


class DummyTqdmFile(object):
    """Dummy file-like that will write to tqdm"""
    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        # Avoid print() second call (useless \n)
        if len(x.rstrip()) > 0:
            tqdm.write(x, file=self.file)


@contextlib.contextmanager
def stdout_redirect_to_tqdm():
    save_stdout = sys.stdout
    try:
        sys.stdout = DummyTqdmFile(sys.stdout)
        yield save_stdout
    # Relay exceptions
    except Exception as exc:
        raise exc
    # Always restore sys.stdout if necessary
    finally:
        sys.stdout = save_stdout

# # Redirect stdout to tqdm.write() (don't forget the `as save_stdout`)
with stdout_redirect_to_tqdm() as save_stdout:
    # tqdm call need to specify sys.stdout, not sys.stderr (default)
    # and dynamic_ncols=True to autodetect console width
    for _ in tqdm(range(3), file=save_stdout, dynamic_ncols=True):
        sleep(0.5)


import logging
import tempfile
import base64
import os
from pathlib import Path
from src.zxbc import main


def test_zxbasic():
    log = logging.getLogger()
    log.debug('Testing zxbasic')

    # Write ZX Basic to file.
    tmp = tempfile.NamedTemporaryFile()
    bas_filename = f'{tmp.name}.bas'
    log.debug(f'Basic filename: {bas_filename}')
    with open(bas_filename, 'w') as f:
        f.write('10 PRINT "Hello"')

    # Compile the tape file from basic source.
    main(['-taB', bas_filename])

    # Read and base64 encode the binary tape file.
    tap_filename = f'{Path(bas_filename).stem}.tap'
    log.debug(f'Tape filename: {tap_filename}')
    with open(tap_filename, 'rb') as f:
        encoded = base64.b64encode(f.read())
        log.debug(f'Encoded: {encoded}')

    os.remove(bas_filename)
    os.remove(tap_filename)

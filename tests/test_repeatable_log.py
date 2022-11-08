import json
import re
import shutil
import time
import zipfile
import pytest
import tempfile
import os
import pydov

from pydov.search.boring import BoringSearch
from pydov.util.errors import LogReplayError
from pydov.util.hooks import Hooks, RepeatableLogRecorder, RepeatableLogReplayer
from tests.abstract import ServiceCheck


@pytest.fixture()
def temp_directory():
    """PyTest fixture providing a temporary directory that does not exist on
    disk.

    Yields
    ------
    str
        Path to temporary directory that does not exist on disk yet.
    """
    temp_dir = os.path.join(tempfile.gettempdir(), 'pydov-test-repeatable-log')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

    yield temp_dir

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture()
def log_recorder(temp_directory):
    """PyTest fixture providing an instance of the RepeatableLogRecorder hook,
    using a temporary directory to store the archive.

    Parameters
    ----------
    temp_directory : pytest.fixture
        Fixture providing a temporary directory.

    Yields
    ------
    RepeatableLogRecorder
        RepeatableLogRecorder hook instance.
    """
    orig_hooks = Hooks(pydov.hooks)
    recorder = RepeatableLogRecorder(temp_directory)
    pydov.hooks = Hooks((recorder,))

    yield recorder

    pydov.hooks = orig_hooks


@pytest.fixture()
def log_archive(log_recorder):
    """PyTest fixture installing the log recorder and executing a Boring search
    to record the session in an archive.

    Yields the resulting archive as ZipFile with read possibilities, for
    inspection.

    Parameters
    ----------
    log_recorder : pytest.fixture
        Fixture providing an instance of a RepeatableLogRecorder.

    Yields
    ------
    zipfile.ZipFile
        Resulting archive open in read mode.
    """
    bs = BoringSearch()
    bs.search(max_features=1)

    log_recorder._pydov_exit()

    with zipfile.ZipFile(log_recorder.log_archive, 'r') as z:
        yield z


class TestRepeatableLogRecorder(object):
    """Class grouping tests for the RepeatableLogRecorder."""

    def test_create_log_directory(self, temp_directory):
        """Test whether to log directory is created if it does not exist yet.

        Parameters
        ----------
        temp_directory : str
            Fixture providing a temporary directory.
        """
        assert not os.path.exists(temp_directory)
        RepeatableLogRecorder(temp_directory)
        assert os.path.exists(temp_directory)

    def test_create_log_archive(self, temp_directory):
        """Test whether the log archive is recorded and the filename matches the expectations.

        Parameters
        ----------
        temp_directory : str
            Fixture providing a temporary directory.
        """
        RepeatableLogRecorder(temp_directory)
        assert len(os.listdir(temp_directory)) >= 1

        log_file = os.listdir(temp_directory)[0]
        assert re.match(
            r'^pydov-archive-[0-9]{8}T[0-9]{6}-([0-9a-z]){6}.zip', log_file)

    def test_pydov_code(self, log_recorder):
        """Test whether the pydov code is recorded in the archive.

        Parameters
        ----------
        log_recorder : RepeatableLogRecorder
            Fixture providing an instance of a RepeatableLogRecorder.
        """
        log_recorder._pydov_exit()

        with zipfile.ZipFile(log_recorder.log_archive, 'r') as z:
            assert 'pydov/__init__.py' in [f.filename for f in z.filelist]

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_contents(self, log_archive):
        """Test whether the contents of the archive match the recorded session.

        Parameters
        ----------
        log_archive : zipfile.ZipFile
            Fixture providing the recorded session as archive in read mode.
        """
        assert 'metadata.json' in [f.filename for f in log_archive.filelist]

        metadata = json.loads(log_archive.read('metadata.json'))

        for lib in ['pydov', 'owslib', 'pandas', 'numpy', 'requests',
                    'fiona', 'geopandas']:
            assert lib in metadata['versions']

        for t in ['start', 'end']:
            assert t in metadata['timings']
            assert re.match(r'[0-9]{8}T[0-9]{6}', metadata['timings'][t])

        assert 'run_time_secs' in metadata['timings']

        # metadata
        assert len([f.filename for f in log_archive.filelist
                    if f.filename.startswith('meta/')]) == 2

        # wfs getfeature
        assert len([f.filename for f in log_archive.filelist
                    if f.filename.startswith('wfs/')]) == 1

        # DOV xml
        assert len([f.filename for f in log_archive.filelist
                    if f.filename.startswith('xml/')]) == 1


class TestRepeatableLogReplayer(object):
    """Class grouping tests for the RepeatableLogReplayer."""
    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_replay(self, log_recorder):
        """Test whether a recorded session can be replayed using the archive.

        Parameters
        ----------
        log_recorder : RepeatableLogRecorder
            Fixture providing an instance of a RepeatableLogRecorder.
        """
        bs = BoringSearch()
        bs.search(max_features=1)
        log_recorder._pydov_exit()

        zip_contents = dict()

        with zipfile.ZipFile(log_recorder.log_archive, 'r') as z:
            for f in [f.filename for f in z.filelist]:
                zip_contents[f] = z.read(f)

        with zipfile.ZipFile(
                log_recorder.log_archive, 'w',
                compression=zipfile.ZIP_DEFLATED) as z:

            for f in zip_contents:
                if f.startswith('wfs/'):
                    z.writestr(f, zip_contents[f].decode('utf-8').replace(
                        'gemeente>Wortegem-Petegem<',
                        'gemeente>Wortelgem<').encode('utf-8')
                    )
                else:
                    z.writestr(f, zip_contents[f])

        pydov.hooks = Hooks((RepeatableLogReplayer(log_recorder.log_archive),))

        bs = BoringSearch()
        df = bs.search(max_features=1)
        assert df.iloc[0].gemeente == 'Wortelgem'

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_replay_other_fails(self, log_recorder):
        """Test whether an error is raised when a session is modified and
        cannot be replayed using the saved archive.

        Parameters
        ----------
        log_recorder : RepeatableLogRecorder
            Fixture providing an instance of a RepeatableLogRecorder.
        """
        bs = BoringSearch()
        bs.search(max_features=1)
        log_recorder._pydov_exit()

        pydov.hooks = Hooks((RepeatableLogReplayer(log_recorder.log_archive),))

        with pytest.raises(LogReplayError):
            bs = BoringSearch()
            bs.search(max_features=2)

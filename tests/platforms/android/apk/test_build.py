import subprocess
from pathlib import Path
from unittest import mock

import pytest
from requests import exceptions as requests_exceptions

from briefcase.exceptions import BriefcaseCommandError
from briefcase.platforms.android.apk import ApkRunCommand


@pytest.fixture
def build_command(tmp_path, first_app_config):
    command = ApkRunCommand(
        base_path=tmp_path,
        apps={'first': first_app_config}
    )
    command.host_os = 'Linux'
    command.host_arch = 'wonky'

    command.os = mock.MagicMock()
    command.os.environ = {}
    command.subprocess = mock.MagicMock()
    return command


def test_sdk_url(build_command):
    assert (build_command.sdk_url == (
        'https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip')
    )

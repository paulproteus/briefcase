import subprocess
from pathlib import Path
from unittest import mock

import pytest
from requests import exceptions as requests_exceptions

from briefcase.exceptions import BriefcaseCommandError
from briefcase.platforms.android.apk import ApkBuildCommand


@pytest.fixture
def build_command(tmp_path, first_app_config):
    command = ApkBuildCommand(
        base_path=tmp_path,
        apps={'first': first_app_config}
    )
    command.sdk_path = tmp_path / 'sdk_path'
    command.host_os = 'Linux'
    command.os = mock.MagicMock()
    command.os.environ = {}
    command.sys = mock.MagicMock()
    command.sys.version_info.major = 3
    command.sys.version_info.minor = 7
    command.requests = mock.MagicMock()
    command.subprocess = mock.MagicMock()
    return command


def test_sdk_url(build_command):
    assert (build_command.sdk_url == (
        'https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip')
    )


def test_permit_python_37(build_command):
    build_command.verify_python_version()


@pytest.mark.parametrize("major,minor", [(3, 5), (3, 6), (3, 8)])
def test_require_python_37(build_command, major, minor):
    build_command.sys.version_info.major = major
    build_command.sys.version_info.minor = minor
    with pytest.raises(BriefcaseCommandError):
        build_command.verify_python_version()


def test_verify_sdk_succeeds_immediately_when_tools_exist(build_command):
    build_command.sdk_path.mkdir()
    build_command.verify_tools()
    assert something

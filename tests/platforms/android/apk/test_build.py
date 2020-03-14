import subprocess
from io import StringIO
from pathlib import Path
from unittest import mock
from zipfile import ZipFile

import pytest
from requests import exceptions as requests_exceptions

from briefcase.exceptions import BriefcaseCommandError
from briefcase.platforms.android.apk import ApkBuildCommand


def create_sentinel_zipfile(path: Path):
    out = StringIO()
    with ZipFile(out, 'w') as zipfile:
        zipfile.writestr('sentinel.txt', '')
    return out


@pytest.fixture
def build_command(tmp_path, first_app_config):
    command = ApkBuildCommand(
        base_path=tmp_path,
        apps={'first': first_app_config}
    )
    command.tmp_path = tmp_path
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
    assert build_command.sdk_url(build_command.host_os) == (
        'https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip')


def test_permit_python_37(build_command):
    build_command.verify_python_version()


@pytest.mark.parametrize("major,minor", [(3, 5), (3, 6), (3, 8)])
def test_require_python_37(build_command, major, minor):
    build_command.sys.version_info.major = major
    build_command.sys.version_info.minor = minor
    with pytest.raises(BriefcaseCommandError):
        build_command.verify_python_version()


def test_verify_tools_succeeds_immediately_when_tools_exist(build_command):
    tools_bin = build_command.sdk_path / "tools" / "bin"
    tools_bin.mkdir(parents=True, mode=0o755)
    (tools_bin / "sdkmanager").touch(mode=0o755)
    licenses = build_command.sdk_path / "licenses"
    licenses.mkdir(parents=True, mode=0o755)
    (licenses / "android-sdk-license").touch()

    # Expect verify_tools() to raise no exceptions, and expect no requests
    # or subprocesses.
    build_command.verify_tools()
    build_command.requests.get.assert_not_called()
    build_command.subprocess.run.assert_not_called()
    build_command.subprocess.check_output.assert_not_called()


def test_verify_tools_downloads_sdk(build_command):
    sdk_zip_path = (build_command.tmp_path / "sdk.zip").resolve()
    create_sentinel_zipfile(sdk_zip_path)
    response = mock.MagicMock()
    response.status_code = 404
    build_command.requests.get.return_value = 
    build_command.sdk_url = lambda *args: 'file://' + str(sdk_zip_path)
    # TODO: Add parameterization for mode 644 and/or absent sdkmanager.
    # Expect verify_tools() to raise no exceptions, and expect no requests
    # or subprocesses.
    build_command.verify_tools()
    build_command.requests.get.assert_not_called()
    build_command.subprocess.run.assert_not_called()
    build_command.subprocess.check_output.assert_not_called()

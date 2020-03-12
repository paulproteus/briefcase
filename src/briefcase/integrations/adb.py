import subprocess
import os

from briefcase.exceptions import BriefcaseCommandError


def install_apk(sdk_path, device, apk_path, sub=subprocess):
    """
    Install an APK file on an Android device.

    :param sdk_path: The path of the Android SDK to use.
    :param device: The name of the device in a format usable by `adb -s`.
    :param apk_path: The path of the Android APK file to install.

    Returns `None` on success; raises an exception on failure.
    """
    try:
        output = sub.check_output([str(sdk_path / 'platform-tools' / 'adb'), '-s', device, 'install', str(apk_path)])
    except subprocess.CalledProcessError as e:
        output_lines = e.output.decode('ascii', 'replace').split('\n')
        if any((line.startswith('error: device ') and line.endswith("'not found") for line in output_lines)):
            raise BriefcaseCommandError("""\
Android device called {device} not found. If you created the
`robotfriend` emulator," you can start it by running this command.

$ {emulator} -avd robotfriend &

Once it is running, find the device name in the first column of the
output of the following command.

$ {adb} devices -l
""".format(
        device=device,
        adb=sdk_path / "platform-tools" / "adb",
        emulator=sdk_path / "emulator" / "emulator"))
        raise BriefcaseCommandError(
            "Unable to launch app. Received this output from `adb`\n" +
            e.output.decode('ascii', 'replace'))

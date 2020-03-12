import subprocess
import os

from briefcase.exceptions import BriefcaseCommandError


def install_apk(sdk_path, device_name, apk_path, sub=subprocess):
    """
    Install an APK file on an Android device.

    :param sdk_path: The path of the Android SDK to use.
    :param device_name: The name of the device in a format usable by `adb -s`.
    :param apk_path: The path of the Android APK file to install.

    Returns `None` on success; raises an exception on failure.
    """
    try:
        output = sub.check_output([str(sdk_path / 'platform-tools' / 'adb'), '-s', device_name, str(apk_path)])
    except subprocess.CalledProcessError as e:
        output_lines = e.output.split('\n')
        if any((line.startswith('error: device ') and line.endswith("'not found"):
            raise BriefcaseCommandError("""\
Android device called {device_name} not found. If you created the
`robotfriend` emulator," you can start it by running this command.

$ {emulator} -avd robotfriend &

Once it is running, find the device name in the first column of the
output of the following command.

$ {adb} devices -l
""".format(
        device_name=device_name,
        adb=sdk_path / "platform-tools" / "adb",
        emulator=sdk_path / "emulator" / "emulator"))
        raise BriefcaseCommandError(
            "Unable to launch app. Received this output from `adb`\n" +
            e.output)

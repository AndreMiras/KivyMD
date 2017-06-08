from buildozer import Buildozer, urlretrieve
from buildozer.targets.android import TargetAndroid
import os
from optparse import OptionParser

# Designed to be used on Gitlab CI
# This file ensures that Build Tools 19.1 is installed
# This file will also install an android api version if an android api is passed in with "--api"
# 19.1 is used because it is the only build tool version I can get to work properly (minimum required by p4a also)

parser = OptionParser()
parser.add_option("--api", dest="api",
                  help="Android API to install", default=None)

(options, args) = parser.parse_args()


class FixedTargetAndroid(TargetAndroid):
    @property
    def android_ndk_version(self):
        return "10e"


class NoOutputBuildozer(Buildozer):
    def set_target(self, target):
        '''Set the target to use (one of buildozer.targets, such as "android")
        '''
        self.targetname = target
        m = __import__('buildozer.targets.{0}'.format(target),
                       fromlist=['buildozer'])
        self.target = m.get_target(self)

    def download(self, url, filename, cwd=None):
        def report_hook(index, blksize, size):
            pass
        url = url + filename
        if cwd:
            filename = os.path.join(cwd, filename)
        if self.file_exists(filename):
            os.unlink(filename)

        self.debug('Downloading {0}'.format(url))
        urlretrieve(url, filename, report_hook)
        return filename


buildozer = NoOutputBuildozer(target='android')
buildozer.log_level = 0

# Ensure directories exist
buildozer.mkdir(buildozer.global_buildozer_dir)
buildozer.mkdir(buildozer.global_cache_dir)
buildozer.mkdir(os.path.join(buildozer.global_platform_dir, buildozer.targetname, 'platform'))

target = FixedTargetAndroid(buildozer)
target._install_android_sdk()
target._install_android_ndk()
target._install_apache_ant()


def run_expect(cmd):
    from pexpect import EOF
    java_tool_options = os.environ.get('JAVA_TOOL_OPTIONS', '')
    child = target.buildozer.cmd_expect(cmd, cwd=target.buildozer.global_platform_dir,
                                        timeout=None,
                                        env={
                                            'JAVA_TOOL_OPTIONS': java_tool_options + ' -Dfile.encoding=UTF-8'
                                        })
    while True:
        index = child.expect([EOF, u'[y/n]: '])
        if index == 0:
            break
        child.sendline('y')

plat_dir = buildozer.global_platform_dir

if not options.api:
    for i in range(2):
        run_expect(plat_dir + "/android-sdk-20/tools/android update sdk -u -a -t platform-tools,tools")
        run_expect(plat_dir + "/android-sdk-20/tools/android update sdk -u -a -t build-tools-19.1.0")
else:
    run_expect(plat_dir + "/android-sdk-20/tools/android update sdk -u -a -t android-{}".format(options.api))

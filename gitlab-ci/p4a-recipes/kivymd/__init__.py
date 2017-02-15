from os import environ

import sh
from pythonforandroid.logger import shprint, info_main, info
from pythonforandroid.toolchain import PythonRecipe
from pythonforandroid.util import ensure_dir


class KivyMDRecipe(PythonRecipe):
    # This recipe installs KivyMD into the android dist from source
    depends = ['kivy']
    site_packages_name = 'kivymd'
    call_hostpython_via_targetpython = False

    def should_build(self, arch):
        return True

    def unpack(self, arch):
        info_main('Unpacking {} for {}'.format(self.name, arch))

        build_dir = self.get_build_container_dir(arch)

        user_dir = environ.get('P4A_{}_DIR'.format(self.name.lower()))
        if user_dir is not None:
            info("Installing KivyMD development versoion (from source)")
            self.clean_build()
            shprint(sh.rm, '-rf', build_dir)
            shprint(sh.mkdir, '-p', build_dir)
            shprint(sh.rmdir, build_dir)
            ensure_dir(build_dir)
            ensure_dir(build_dir + "/kivymd")
            shprint(sh.cp, user_dir + '/setup.py', self.get_build_dir(arch) + "/setup.py")
            shprint(sh.cp, '-a', user_dir + "/kivymd", self.get_build_dir(arch) + "/kivymd")
            return


recipe = KivyMDRecipe()

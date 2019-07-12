# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

class LuaConan(ConanFile):
    name = "lua"
    version = "5.3.5"
    description = "Keep it short"
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("conan", "lua", "scripting")
    url = "https://github.com/DEGoodmanWilson/conan-lua"
    homepage = "https://www.lua.org/"
    author = "Don Goodman-Wilson <don@goodman-wilson.com>"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://www.lua.org/ftp/{0}-{1}.tar.gz".format(self.name, self.version)
        tools.get(source_url, sha1="112eb10ff04d1b4c9898e121d6bdf54a81482447")
        extracted_dir = self.name + "-" + self.version

        #Rename to "source_folder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            # Set platform to one of aix bsd c89 freebsd generic linux macosx mingw posix solaris
            # TODO for now we only support linux, windows, and mac. In the future we 
            target = "generic"
            if self.settings.os == 'Windows':
                target = "windows"
                # TODO mingw
            elif self.settings.os == 'Linux':
                target = "linux"
            elif self.settings.os == 'Macos':
                target = "macosx"

            env_build.make(target=target)


    def package(self):
        source_folder = os.path.join(self._source_subfolder, "src")
        self.copy("lua.h", dst="include", src=source_folder)
        self.copy("lua", dst="bin", src=source_folder)
        self.copy("luac", dst="bin", src=source_folder)
        self.copy(pattern="*.dll", dst="bin", src=source_folder, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=source_folder, keep_path=False)
        self.copy(pattern="*.a", dst="lib", src=source_folder, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=source_folder, keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=source_folder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

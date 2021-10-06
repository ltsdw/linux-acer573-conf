#! /bin/python

from typing import List

class PKGBUILD:

    def __init__(self, _major: float, _minor: int, _pkgrel: int) -> None:
        self._major: float = _major
        self._minor: int = _minor
        self._pkgrel: int = _pkgrel
        self.pkgver: str = f'{self._major}.{self._minor}'
        self.linux_url: str
        self.sign_url: str
        self.patch_url: str
        self.source: str
        self.sha256sums: str = ''

    def goToPkgbuildPath(self) -> None:
        from sys import argv
        from os.path import join, abspath, exists
        from os import chdir, getcwd


        def removeBinFromPath(argv0: str) -> str:
            directories = argv0.split('/')[:-1]
            pkgbuild_path = '/'

            for directory in directories:
                pkgbuild_path = join(pkgbuild_path, directory)

            return pkgbuild_path

        argv0: str = argv[0]

        if (argv0[0] == '/'):
            chdir(abspath(join(removeBinFromPath(argv0), '..')))
        else:
            chdir(getcwd())

        if not exists('PKGBUILD'):
            chdir('..')
            if not exists('PKGBUILD'):
                exit('No PKGBUILD found!')

    def returnSource(self, directories: List[str]) -> str:
        from os import walk

        source: str = '''        "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-${_major}.tar.xz"
        "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-${_major}.tar.sign"
        "https://cdn.kernel.org/pub/linux/kernel/v5.x/patch-${pkgver}.xz"\n'''

        for directory in directories:
            for (_, _, files) in walk(directory):
                for file in files:
                    source += f'        "{file}"\n'

        return source

    def returnSha256(self, pwd: str, directories: List[str], list_of_filenames: List[str]) -> str:
        from hashlib import sha256
        from os import walk, chdir

        sha256sums: str = ''
        for filename in list_of_filenames:
            with open(filename, 'rb') as f_linux:
                _bytes: bytes = f_linux.read()
                sha256sum: str = sha256(_bytes).hexdigest()
                sha256sums += f'            "{sha256sum}"\n'

        for directory in directories:
            chdir(pwd + '/' + directory)
            directory: str = pwd + '/' + directory
            for (_, _, filenames) in walk(directory):
                for filename in filenames:
                    if 'config-custom-sdw' in filename:
                        sha256sums += f'            "SKIP"\n'
                    else:
                        with open(filename, 'rb') as f_linux:
                            _bytes: bytes = f_linux.read()
                            sha256sum: str = sha256(_bytes).hexdigest()
                            sha256sums += f'            "{sha256sum}"\n'
        chdir(pwd)

        return sha256sums

    def download(self) -> None:
        from requests import get, Response
        from os.path import exists
        from os import getcwd

        linux: str = f'linux-{self._major}.tar.xz'
        sign: str = f'linux-{self._major}.tar.sign'
        patch: str = f'patch-{self.pkgver}.xz'

        self.linux_url: str = f'https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-{self._major}.tar.xz'
        self.sign_url: str = f'https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-{self._major}.tar.sign'
        self.patch_url: str = f'https://cdn.kernel.org/pub/linux/kernel/v5.x/patch-{self.pkgver}.xz'

        if not exists(linux):
            print(f'Downloading {linux}')
            linux_file: Response = get(self.linux_url, allow_redirects=True)
            open(linux, 'wb').write(linux_file.content)

        if not exists(sign):
            print(f'Downloading {sign}')
            sign_file: Response = get(self.sign_url, allow_redirects=True)
            open(sign, 'wb').write(sign_file.content)
 
        if not exists(patch):
            print(f'Downloading {patch}')
            patch_file: Response = get(self.patch_url, allow_redirects=True)
            open(patch, 'wb').write(patch_file.content)
            
        self.sha256sums = self.returnSha256(getcwd(), ['patches', 'cpu_scheduler', 'config'],
                                            [linux, sign, patch])

    def updatePackageBuild(self) -> None:
        is_open: bool = False
        self.source = self.returnSource(['patches', 'cpu_scheduler', 'config'])

        with open('PKGBUILD', 'r') as pkgbuild:
            tmp: List[str] = pkgbuild.readlines()

        with open('PKGBUILD', 'w') as pkgbuild:
            for line in tmp:
                if '_major=' in line:
                    pkgbuild.write(f'_major={self._major}\n')
                elif '_minor=' in line:
                    pkgbuild.write(f'_minor={self._minor}\n')
                elif 'pkgrel=' in line:
                    pkgbuild.write(f'pkgrel={self._pkgrel}\n')
                elif 'source=(' in line:
                    is_open = True
                    pkgbuild.write(line)
                    pkgbuild.write(self.source)
                elif 'sha256sums=(' in line:
                    is_open = True
                    pkgbuild.write(line)
                    pkgbuild.write(self.sha256sums)
                elif '        )' in line or '       )' in line:
                    is_open = False
                    pkgbuild.write(line)
                elif not is_open:
                    pkgbuild.write(line)


def main() -> None:
    re_pkgbuild = PKGBUILD(5.14, 9, 1)
    re_pkgbuild.goToPkgbuildPath()
    re_pkgbuild.download()
    re_pkgbuild.updatePackageBuild()


if __name__ == '__main__':
    main()


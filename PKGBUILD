_where="$PWD"

cp "$_where"/config/config-custom-sdw "$_where"
cp "$_where"/cpu_scheduler/prjc_v5.8-r0.patch "$_where"
cp "$_where"/patches/* "$_where"

### BUILD OPTIONS
# Set these variables to ANYTHING that is not null to enable them

# Tweak kernel options prior to a build via nconfig
_makenconfig=y

_major=5.8
_minor=7
_srcname=linux-${_major}
pkgbase=linux-ltsdw
pkgver=${_major}.${_minor}
pkgrel=1
arch=('x86_64')
license=('GPL2')
makedepends=('bc' 'cpio' 'git' 'inetutils' 'kmod' 'libelf' 'xmlto')
options=('!strip')

source=(
        "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-${_major}.tar.xz"
        "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-${_major}.tar.sign"
        "https://cdn.kernel.org/pub/linux/kernel/v5.x/patch-${pkgver}.xz"
        "0001-enable_additional_cpu_optimizations_for_gcc_v9.1+_kernel_v5.8+.patch"
        "config-custom-sdw"
        "prjc_v5.8-r0.patch"
        "0001-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch"
        "0002-Initialize-ata-before-graphics.patch"
        "0002-intel_idle-tweak-cpuidle-cstates.patch"
        "0002-locking-rwsem-spin-faster.patch"
        "0002-pci-pme-wakeups.patch"
        "0007-v5.8-fsync.patch"
        "0008-kconfig-add-500Hz-timer-interrupt-kernel-config-opti.patch"
        "0009-01-x86-ptrace-Prevent-ptrace-from-clearing-the-FS-GS-se.patch"
        "0009-02-x86-cpu-Add-unsafe_fsgsbase-to-enable-CR4.FSGSBASE.patch"
        "0009-03-x86-fsgsbase-64-Add-intrinsics-for-FSGSBASE-instruct.patch"
        "0009-04-x86-fsgsbase-64-Enable-FSGSBASE-instructions-in-help.patch"
        "0009-05-x86-process-64-Make-save_fsgs_for_kvm-ready-for-FSGS.patch"
        "0009-06-x86-process-64-Use-FSBSBASE-in-switch_to-if-availabl.patch"
        "0009-07-x86-process-64-Use-FSGSBASE-instructions-on-thread-c.patch"
        "0009-08-x86-speculation-swapgs-Check-FSGSBASE-in-enabling-SW.patch"
        "0009-09-x86-entry-64-Switch-CR3-before-SWAPGS-in-paranoid-en.patch"
        "0009-10-x86-entry-64-Introduce-the-FIND_PERCPU_BASE-macro.patch"
        "0009-11-x86-entry-64-Handle-FSGSBASE-enabled-paranoid-entry-.patch"
        "0009-12-x86-cpu-Enable-FSGSBASE-on-64bit-by-default-and-add-.patch"
        "0009-13-x86-elf-Enumerate-kernel-FSGSBASE-capability-in-AT_H.patch"
        "0009-14-Documentation-x86-64-Add-documentation-for-GS-FS-add.patch"
        "0009-15-selftests-x86-fsgsbase-Test-GS-selector-on-ptracer-i.patch"
        "0009-16-selftests-x86-fsgsbase-Test-ptracer-induced-GS-base-.patch"
        "0009-17-selftests-x86-fsgsbase-Fix-a-comment-in-the-ptrace_w.patch"
        "0009-18-selftests-x86-fsgsbase-Add-a-missing-memory-constrai.patch"
        "0009-19-x86-ptrace-Fix-32-bit-PTRACE_SETREGS-vs-fsbase-and-g.patch"
        "0009-20-selftests-x86-Add-a-syscall_arg_fault_64-test-for-ne.patch"
        "0009-21-x86-fsgsbase-Fix-Xen-PV-support.patch"
       )

sha256sums=(
            'e7f75186aa0642114af8f19d99559937300ca27acaf7451b36d4f9b0f85cf1f5'
            'SKIP'
            'd394c98a7031fe2c88009082ccfdd8ec588dfbcf83a8d7969d016c4881e7028d'
            '7dd5fa929a4c6b9cfcdbc7c0a4a9e6d02dbe0dc55e1704856c016515d5e42189'
            'fcebb7e01669fc4a5c7d98f6468dd68de1e70dde3fb1728a16bc7f48a3476274'
            'aa02d8dc476093eec104020bca4e47b0684381f3aa7d3caeb50c6b195c19a02f'
            'f6383abef027fd9a430fd33415355e0df492cdc3c90e9938bf2d98f4f63b32e6'
            '3e1903d2f323a1c6ddaab1126ee22920cd8321e025a0fb3dfb16f7dea2d83551'
            '8399e8cb5a34e0f702bde2c90b8db888774abb590c41bce4e7b5466bcf455d65'
            '43cd10b3e9933981514da9619a87b338478f40e81954b56d7bd1000a8a041049'
            '6be86f5dd9d8f2d66d33713b7b98c2021c78e0fa57d345e4bfbfd0d9541bb9a2'
            'cd225e86d72eaf6c31ef3d7b20df397f4cc44ddd04389850691292cdf292b204'
            'b6095af58f7c09588b81e2cbf72ac97c89226d7fd6eb2f35dcaa2fd075a1ed95'
            '28176dba00f48cc463d8f7774e716692c6f9b09d2c9f74b7089ed054f53064a7'
            'b67efcb736d71946d9a6b2b30b66ea2ab5e1614f1021bfddac4785f0785ca44f'
            'add1f2eaf3ec2569de3ad0523169eabf4eca430f2f61bbb15f5d49412b0c88eb'
            'a94b3692d48003d5bc692bf3d3bac4d66bd0f6658bdbc0b6dfe4e923b9526821'
            'a848547a315bfb2ac0f54f91acb2503a5cb72ebacf453c777ec71c4e8c3d12e6'
            'bfef3650e5a7243e0ce291a0ee9b4871c79a40b877c4d522df6a976f5240e8eb'
            '609d858a58db5665c01b9b23156df3419732a84926b6eeaf9ecdb9b337791393'
            'd1dbb6e493edbc97fb65ee2e26421a93112883acd9b87e770123a8eb91ca2878'
            'b59f666fca3aa257124b777088240eb6315a0b3646f6b7c14290c649fffb6e75'
            '6332b72167e0549b7aab01590b14e7d20bbe939feb717da99ad5c1784fa4482e'
            '1c372c9f5ff6865cffb36f9c19e72d8d6e3b58c39979627975ad6f4679ee62dd'
            'abdb59437dc405694765ccc191ad86367d935cb297bf910049ae45b0a6757afd'
            '6d99ab483776b0498bc73e15389a8eeac80d15a3d05a0485219297a95b41d791'
            '4906042f6f1f37f849c03d5d0762ffe1acf8bf60b8b344b4f8f5beeeafada297'
            '766da6a48152ddbc496f6633fc45108ce02b33bc61149a18b63a0e85f5dbf304'
            '361dbfd94e815d194541ed8cef23d57f9d190c453f8eb5d39fb905ef68774a8f'
            '5295f0f23d45181c050e530ecaec3efa50a0dc1480c720cacc86f62f2b544e5c'
            '69ad72ddcf3c512b4ab22f495bcebff988aa98919ce5f460b281d191668aa1d3'
            '016b5df77f0404485a8024559a463f89b6123404b4b33f3d2992c634ddfa0225'
            'f42e7c5d0f4db5036bdf5dc84ffd56b6a3daca8f2b0f48ba024cc8b5774ef76a'
            '1cf2e43fc049e7b6902115fc702671e817a6f8c1f524e999ac9b64fdc593ccc4'
            )

export KBUILD_BUILD_HOST=archlinux
export KBUILD_BUILD_USER=$pkgbase
export KBUILD_BUILD_TIMESTAMP="$(date -Ru${SOURCE_DATE_EPOCH:+d @$SOURCE_DATE_EPOCH})"

prepare() {
    cd ${_srcname}

    ### Setting version
        msg2 "Setting version..."
        scripts/setlocalversion --save-scmversion
        echo "-$pkgrel" > localversion.10-pkgrel
        echo "${pkgbase#linux}" > localversion.20-pkgname

    ### Add upstream patches
        msg2 "Add upstream patches"
        patch -Np1 -i $srcdir/patch-${pkgver}

    ### Add some patches
        for i in $srcdir/*.patch; do
	        echo -e "\033[0;31m Applying patch ${i}... \033[0m"
	        patch -Np1 -i "${i}"
        done

    ### Setting config
        msg2 "Setting config..."
        cp -Tf $srcdir/config-custom-sdw ./.config
        make olddefconfig

    ### Prepared version
        make -s kernelrelease > version
        msg2 "Prepared %s version %s" "$pkgbase" "$(<version)"

    ### Running make nconfig

        [[ -z "$_makenconfig" ]] || make nconfig

    ### Save configuration for later reuse
        cat ./.config > ../../config/config-custom-d
}

build() {
    cd ${_srcname}
    make bzImage modules
}

_package() {
    pkgdesc="The $pkgdesc kernel and modules"
    depends=('coreutils' 'kmod' 'initramfs')
    optdepends=('crda: to set the correct wireless channels of your country'
                'linux-firmware: firmware images needed for some devices'
                'modprobed-db: Keeps track of EVERY kernel module that has ever been probed - useful for those of us who make localmodconfig')

    cd $_srcname

    local kernver="$(<version)"
    local modulesdir="$pkgdir/usr/lib/modules/$kernver"

    msg2 "Installing boot image..."
    # systemd expects to find the kernel here to allow hibernation
    # https://github.com/systemd/systemd/commit/edda44605f06a41fb86b7ab8128dcf99161d2344
    install -Dm644 "$(make -s image_name)" "$modulesdir/vmlinuz"

    # Used by mkinitcpio to name the kernel
    echo "$pkgbase" | install -Dm644 /dev/stdin "$modulesdir/pkgbase"

    msg2 "Installing modules..."
    make INSTALL_MOD_PATH="$pkgdir/usr" modules_install

    # remove build and source links
    rm "$modulesdir"/{source,build}

    msg2 "Fixing permissions..."
    chmod -Rc u=rwX,go=rX "$pkgdir"
}

_package-headers() {
    pkgdesc="Headers and scripts for building modules for the $pkgdesc kernel"

    cd ${_srcname}
    local builddir="$pkgdir/usr/lib/modules/$(<version)/build"

    msg2 "Installing build files..."
    install -Dt "$builddir" -m644 .config Makefile Module.symvers System.map \
        localversion.* version vmlinux
    install -Dt "$builddir/kernel" -m644 kernel/Makefile
    install -Dt "$builddir/arch/x86" -m644 arch/x86/Makefile
    cp -t "$builddir" -a scripts

    # add objtool for external module building and enabled VALIDATION_STACK option
    install -Dt "$builddir/tools/objtool" tools/objtool/objtool

    # add xfs and shmem for aufs building
    mkdir -p "$builddir"/{fs/xfs,mm}

    msg2 "Installing headers..."
    cp -t "$builddir" -a include
    cp -t "$builddir/arch/x86" -a arch/x86/include
    install -Dt "$builddir/arch/x86/kernel" -m644 arch/x86/kernel/asm-offsets.s

    install -Dt "$builddir/drivers/md" -m644 drivers/md/*.h
    install -Dt "$builddir/net/mac80211" -m644 net/mac80211/*.h

    # http://bugs.archlinux.org/task/13146
    install -Dt "$builddir/drivers/media/i2c" -m644 drivers/media/i2c/msp3400-driver.h

    # http://bugs.archlinux.org/task/20402
    install -Dt "$builddir/drivers/media/usb/dvb-usb" -m644 drivers/media/usb/dvb-usb/*.h
    install -Dt "$builddir/drivers/media/dvb-frontends" -m644 drivers/media/dvb-frontends/*.h
    install -Dt "$builddir/drivers/media/tuners" -m644 drivers/media/tuners/*.h

    msg2 "Installing KConfig files..."
    find . -name 'Kconfig*' -exec install -Dm644 {} "$builddir/{}" \;

    msg2 "Removing unneeded architectures..."
    local arch
    for arch in "$builddir"/arch/*/; do
        [[ $arch = */x86/ ]] && continue
        echo "Removing $(basename "$arch")"
        rm -r "$arch"
    done

    msg2 "Removing documentation..."
    rm -r "$builddir/Documentation"

    msg2 "Removing broken symlinks..."
    find -L "$builddir" -type l -printf 'Removing %P\n' -delete

    msg2 "Removing loose objects..."
    find "$builddir" -type f -name '*.o' -printf 'Removing %P\n' -delete

    msg2 "Stripping build tools..."
    local file
    while read -rd '' file; do
        case "$(file -bi "$file")" in
            application/x-sharedlib\;*)      # Libraries (.so)
                strip -v $STRIP_SHARED "$file" ;;
            application/x-archive\;*)        # Libraries (.a)
                strip -v $STRIP_STATIC "$file" ;;
            application/x-executable\;*)     # Binaries
                strip -v $STRIP_BINARIES "$file" ;;
            application/x-pie-executable\;*) # Relocatable binaries
                strip -v $STRIP_SHARED "$file" ;;
        esac
    done < <(find "$builddir" -type f -perm -u+x ! -name vmlinux -print0)

    msg2 "Adding symlink..."
    mkdir -p "$pkgdir/usr/src"
    ln -sr "$builddir" "$pkgdir/usr/src/$pkgbase"

    msg2 "Fixing permissions..."
    chmod -Rc u=rwX,go=rX "$pkgdir"
}

pkgname=("$pkgbase" "$pkgbase-headers")
for _p in "${pkgname[@]}"; do
  eval "package_$_p() {
    $(declare -f "_package${_p#$pkgbase}")
    _package${_p#$pkgbase}
  }"
done

validpgpkeys=(
  'ABAF11C65A2970B130ABE3C479BE3E4300411886'  # Linus Torvalds
  '647F28654894E3BD457199BE38DBBDC86092693E'  # Greg Kroah-Hartman
)


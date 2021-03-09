_where="$PWD"

cp "$_where"/config/config-custom-sdw "$_where"
cp "$_where"/cpu_scheduler/prjc_v5.11-r2.patch "$_where"
cp "$_where"/patches/* "$_where"

### BUILD OPTIONS
# Set these variables to ANYTHING that is not null to enable them

_major=5.11
_minor=4
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
        "0000-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch"
        "0000-enable_additional_cpu_optimizations_for_gcc_v11.0+_kernel_v5.8+.patch"
        "0001-initialize-ata-before-graphics.patch"
        "0001-intel_idle-tweak-cpuidle-cstates.patch"
        "0001-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch"
        "0001-locking-rwsem-spin-faster.patch"
        "0001-pci-pme-wakeups.patch"
        "0002-v5.11-futex2_interface.patch"
        "0003-kconfig-add-500Hz-timer-interrupt-kernel-config-opti.patch"
        "prjc_v5.11-r2.patch"
        "config-custom-sdw"
       )

sha256sums=(
            "04f07b54f0d40adfab02ee6cbd2a942c96728d87c1ef9e120d0cb9ba3fe067b4"
            "SKIP"
            "d509c3900cf02a8d9f1692ffcc9d4a27d2b515ad50c0a231d5d00a125e9bd7a8" 
            "f6383abef027fd9a430fd33415355e0df492cdc3c90e9938bf2d98f4f63b32e6"
            "9b0c200b0dadfcfb1b3c42acd0c007e1d582a86abc6b04f3096e0535c8784ab6"
            "1ba1dc14899c5227ee561f57efb23ea8c72e433128a5cbe0cd7a53993d295889"
            "8399e8cb5a34e0f702bde2c90b8db888774abb590c41bce4e7b5466bcf455d65"
            "2f4c91470f43af834d63917a94546372b2d982f4a79f2cea167cea9b43260128"
            "43cd10b3e9933981514da9619a87b338478f40e81954b56d7bd1000a8a041049"
            "a4e64d65b512fd89fb4d8c66ca8436e55f477987a2ae944cec253d8b3b82e2ba"
            "073e7b8ab48aa9abdb5cedb5c729a2f624275ebdbe1769476231c9e712145496"
            "222fb05515b0efb13c21ab5c8096904f4c8e67c148cc28203dad547a351d797e"
            "e394d4b7721f55837a8364c8311cb06cb5a59484de8aa8731e38d1aff2b7014e"
            "b02155d9d15abfa9d5887585f602feabf81f38fc8dcaf7bcc09655192c39e6b7"
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
        make nconfig

    ### Save configuration for later reuse
        cat .config > ../../config/config-custom-sdw
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

    # remove copied patches
    rm -rf $_where/*.patch
    rm -rf $_where/config-custom-sdw

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


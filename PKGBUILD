_where="$PWD"

cp "$_where/config/config-custom-sdw" $_where
cp "$_where/cpu_scheduler/"* $_where
cp "$_where/patches/"* $_where

### BUILD OPTIONS
# Set these variables to ANYTHING that is not null to enable them

_major=5.16
_minor=14
_srcname=linux-${_major}
pkgbase=linux-ltsdw-lto
pkgver=${_major}.${_minor}
pkgrel=1
arch=('x86_64')
license=('GPL2')
makedepends=('bc' 'cpio' 'git' 'inetutils' 'kmod' 'libelf' 'xmlto' 'clang' 'llvm')
options=('!strip')

source=(
        "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-${_major}.tar.xz"
        "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-${_major}.tar.sign"
        "https://cdn.kernel.org/pub/linux/kernel/v5.x/patch-${pkgver}.xz"
        "0001-pci-pme-wakeups.patch"
        "0001-do-accept-in-LIFO-order-for-cache-efficiency.patch"
        "0003-MGLRU_5.16.patch"
        "0001-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch"
        "0001-intel_idle-tweak-cpuidle-cstates.patch"
        "0001-initialize-ata-before-graphics.patch"
        "0001-give-rdrand-some-credit.patch"
        "0001-increase-the-ext4-default-commit-age.patch"
        "0001-smpboot-reuse-timer-calibration.patch"
        "0001-locking-rwsem-spin-faster.patch"
        "0001-enable-stateless-firmware-loading.patch"
        "0002-v5.16-fsync1_via_futex_waitv.patch"
        "0001-kconfig-add-500Hz-timer-interrupt-kernel-conf.patch"
        "0000-default-to-CC_OPTIMIZE_FOR_PERFORMANCE_O3-for-clang.patch"
        "0000-more-uarches-for-kernel-5.15+.patch"
        "0000-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch"
        "prjc_v5.16-r0.patch"
        "config-custom-sdw"
       )

sha256sums=(
            "027d7e8988bb69ac12ee92406c3be1fe13f990b1ca2249e226225cd1573308bb"
            "dddc9fa3ada89431ec11d1df74d18d3b4fb16b975f72867602092c86b63ef227"
            "b937799c9a78417161b3f40a4fae99d6a9ed7fe653a4b84d9908cd11a6ab62ca"
            "72c2d9063d95fdc25125520b16a72d2c361878d7767aeb3e456becfdd2f05f3d"
            "e11a3d3c29496a115b5b140db79ea9c4e1aac5db15c39e5b650e4e4a66d5b903"
            "d814badbb20b900aff35579882aade938ffa028badfce88a8d0d06d19eed0781"
            "f5d29a664e06699b6e2237f0cd34ec4d14e7207155666df7fd237151649243d0"
            "7107c547c55fae3fb5aef86885e6f061ade5991114553227ad7af73d766d0e00"
            "fd211a0ebda270dd8ae8938ef61e69cfec217c2fdaae434cc73e16b6c3022036"
            "abacadd30f8be5d7dba827410b8922eb880480b1f942352e63a066c6562c0551"
            "45e8f4b221e5cb9f6cd80079d74684d76032c2f7f462b102c988a2bcd301eb45"
            "0a7a3dfe2558f1ad9d4767893dffb6386c907e8893963efba4c93111aa783fbc"
            "d5afd337dc6667d6e8256953542db55bb7e9af09654915d07d93d49695c7785c"
            "4ffbdd8ea0ac3a6502722e483625e6c801cd50adf16c02b8a773639d0cd521d9"
            "9df628fd530950e37d31da854cb314d536f33c83935adf5c47e71266a55f7004"
            "dbca7be48e4ce8886ac7c6c655af1a277684f68a7b5a2e22e8ef2d7bd33ed3dc"
            "7bbb41762567e41c1153d83a73a5e524808253aa0be57227e432ff477a88c7d8"
            "380bcf40cc8396e97bd1d7f2577ab2ace51885858d3f155b1fb2dd5469efd00d"
            "f6383abef027fd9a430fd33415355e0df492cdc3c90e9938bf2d98f4f63b32e6"
            "7bd99d10ec9f834de95424d033f940f9531beb3a7b4d9711448f0ed66832c03d"
            "SKIP"
            )

export KBUILD_BUILD_HOST=archlinux
export KBUILD_BUILD_USER=$pkgbase
export KBUILD_BUILD_TIMESTAMP="$(date -Ru${SOURCE_DATE_EPOCH:+d @$SOURCE_DATE_EPOCH})"
export CFLAGS="-march=native -O3 -falign-functions=32 -fno-math-errno -fno-semantic-interposition -fno-trapping-math"

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
        make LLVM=1 LLVM_IAS=1 -j$(nproc) olddefconfig

    ### scripts/config
        ./scripts/config -e LTO_CLANG_THIN

    ### Prepared version
        make LLVM=1 LLVM_IAS=1 -j$(nproc) -s kernelrelease > version
        msg2 "Prepared %s version %s" "$pkgbase" "$(<version)"

    ### Running make nconfig
    make LLVM=1 LLVM_IAS=1 -j$(nproc) nconfig

    ### Save configuration for later reuse
        cat .config > ../../config/config-custom-sdw
}

build() {
    cd ${_srcname}
    make LLVM=1 LLVM_IAS=1 -j$(nproc) bzImage modules
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
    install -Dm644 "$(make LLVM=1 LLVM_IAS=1 -j$(nproc) -s image_name)" "$modulesdir/vmlinuz"

    # Used by mkinitcpio to name the kernel
    echo "$pkgbase" | install -Dm644 /dev/stdin "$modulesdir/pkgbase"

    msg2 "Installing modules..."
    make LLVM=1 LLVM_IAS=1 -j$(nproc) INSTALL_MOD_PATH="$pkgdir/usr" modules_install

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

_where="$PWD"

cp "$_where/config/config-custom-sdw" $_where
cp "$_where/cpu_scheduler/"* $_where
cp "$_where/patches/"* $_where

### BUILD OPTIONS
# Set these variables to ANYTHING that is not null to enable them

_major=5.17
_minor=8
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
        "0004-mm-Support-soft-dirty-flag-reset-for-VA-range.patch"
        "0000-more-uarches-for-kernel-5.17+.patch"
        "0001-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch"
        "0001-intel_idle-tweak-cpuidle-cstates.patch"
        "0001-initialize-ata-before-graphics.patch"
        "0001-give-rdrand-some-credit.patch"
        "0001-increase-the-ext4-default-commit-age.patch"
        "0001-smpboot-reuse-timer-calibration.patch"
        "0001-locking-rwsem-spin-faster.patch"
        "0001-enable-stateless-firmware-loading.patch"
        "0003-MGLRU_5.17.patch"
        "0001-kconfig-add-500Hz-timer-interrupt-kernel-conf.patch"
        "0002-v5.17-fsync1_via_futex_waitv.patch"
        "0000-default-to-CC_OPTIMIZE_FOR_PERFORMANCE_O3-for-clang.patch"
        "0004-mm-Support-soft-dirty-flag-read-with-reset.patch"
        "0000-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch"
        "prjc_v5.17-r1.patch"
        "config-custom-sdw"
       )

sha256sums=(
            "555fef61dddb591a83d62dd04e252792f9af4ba9ef14683f64840e46fa20b1b1"
            "81147b5a3dc08fdd41c0a36b098164f148f070024a4ff6ce6486f93a4637ac70"
            "3dcdb3dd014240fe4eb344a20cd62bef568f33458d391946fdee5a4a8f0ef83f"
            "52ea7832aed7f4eae6da965776fedd83837e00b7b7551e6686d6489633a6a3a8"
            "214e27301bd9e9ab24ae4da5bebe405fa25ca5f77c764e0d1dce92571c53cd5e"
            "1b656ad96004f27e9dc63d7f430b50d5c48510d6d4cd595a81c24b21adb70313"
            "dea86a521603414a8c7bf9cf1f41090d5d6f8035ce31407449e25964befb1e50"
            "260333b57dbe1180eced49ededf1a9b3d2404d597242e5c79f76aa6e7073b54c"
            "c3be452e4bc1473a5535b0d6014c5b9cf35c45bf0c80b31c8620eb9636d5c325"
            "bb0bbd7125540bb97a18922688a6115db38bf7157930d56d7fa5b4534bbaedbc"
            "734d99ad8791f5cc41222ab877070fa4108450e16d5881155af8374c89d154b3"
            "9c931aa68f62012994c188e31c17f5c4d93618a2677864d53f3b43519e3dc419"
            "8eec5dfed7a0e3164294d429dd8023e5b02c4ae6121c53a8619e99135f574dd6"
            "5c75ac423bdf050d19e9446c55d59074a5bf86f8e86641adf63e6b2d48ccfb40"
            "bedbb4cfb8d8906681d9827efaafc872e8a87b44e5f78881329779755a9e0e71"
            "7cd3617c97e67360c2f31e97fa751b83dccf47919f313ce141d2290ccecc4611"
            "dbca7be48e4ce8886ac7c6c655af1a277684f68a7b5a2e22e8ef2d7bd33ed3dc"
            "9df628fd530950e37d31da854cb314d536f33c83935adf5c47e71266a55f7004"
            "7bbb41762567e41c1153d83a73a5e524808253aa0be57227e432ff477a88c7d8"
            "b0319a7dff9c48b2f3e3d3597ee154bf92223149a633a8b7ce4026252db86da6"
            "f6383abef027fd9a430fd33415355e0df492cdc3c90e9938bf2d98f4f63b32e6"
            "16031e6da6c6dbb848189b49ebe118a70dca0bb28fba20e45ff83bde9bb3c986"
            "SKIP"
            )

export KBUILD_BUILD_HOST=archlinux
export KBUILD_BUILD_USER=$pkgbase
export KBUILD_BUILD_TIMESTAMP="$(date -Ru${SOURCE_DATE_EPOCH:+d @$SOURCE_DATE_EPOCH})"
export CFLAGS="-mno-sse -mno-mmx -mno-sse2 -mno-3dnow -mno-avx -mno-avx2 -O0 -O2 -fno-tree-vectorize -march=native -mpopcnt"

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

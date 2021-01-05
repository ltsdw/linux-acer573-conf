_where="$PWD"

cp "$_where"/config/config-custom-sdw "$_where"
cp "$_where"/cpu_scheduler/prjc_v5.10-r2.patch "$_where"
cp "$_where"/patches/* "$_where"

### BUILD OPTIONS
# Set these variables to ANYTHING that is not null to enable them

# Tweak kernel options prior to a build via nconfig
_makenconfig=y

_major=5.10
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
        "0000-enable_additional_cpu_optimizations_for_gcc_v10.1+_kernel_v5.8+.patch"
        "0001-initialize-ata-before-graphics.patch"
        "0001-intel_idle-tweak-cpuidle-cstates.patch"
        "0001-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch"
        "0001-kernel-time-reduce-ntp-wakeups.patch"
        "0001-locking-rwsem-spin-faster.patch"
        "0001-pci-pme-wakeups.patch"
        "0002-v5.10-fsync.patch"
        "0003-kconfig-add-500Hz-timer-interrupt-kernel-config-opti.patch"
        "0004-firmware_rome_error.patch"
        "prjc_v5.10-r2.patch"
        "config-custom-sdw"
       )

sha256sums=(
            "dcdf99e43e98330d925016985bfbc7b83c66d367b714b2de0cbbfcbf83d8ca43"
            "SKIP"
            "0089cea5866978effd79567fdfdffe0ae950747f32a56e5f00b98d38e686f5b1" 
            "f6383abef027fd9a430fd33415355e0df492cdc3c90e9938bf2d98f4f63b32e6"
            "a915eb8cc9ff87a33a17b95ce9b9471f43e0849b9b38e88dc9cdc1f1f08bb8c2"
            "1ba1dc14899c5227ee561f57efb23ea8c72e433128a5cbe0cd7a53993d295889"
            "9fe1ffba6c1b6e6fd72e145a81732a388129dd7a1b9458105a0b03af41c49a2f"
            "2f4c91470f43af834d63917a94546372b2d982f4a79f2cea167cea9b43260128"
            "c3512e1d000952fa189284a69195bc4f7b7ae91cb35bd55c639378ac4f666ca1"
            "43cd10b3e9933981514da9619a87b338478f40e81954b56d7bd1000a8a041049"
            "4c5e1545f586e04f2149ad376d6daf42e43cfab8588c72cd389980a9bfa2e4ee"
            "b302ba6c5bbe8ed19b20207505d513208fae1e678cf4d8e7ac0b154e5fe3f456"
            "222fb05515b0efb13c21ab5c8096904f4c8e67c148cc28203dad547a351d797e"
            "5e804e1f241ce542f3f0e83d274ede6aa4b0539e510fb9376f8106e8732ce69b"
            "e308292fc42840a2366280ea7cf26314e92b931bb11f04ad4830276fc0326ee1"
            "a0c168fd440f6db5273196a0179b93b5fc9a4d1f7b84f21327d7172591e87ace"
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


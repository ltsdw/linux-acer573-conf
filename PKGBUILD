### BUILD OPTIONS
# Set these variables to ANYTHING that is not null to enable them

# Tweak kernel options prior to a build via nconfig
_makenconfig=y

_enable_gcc_more_v=y
# Optionally select a sub architecture by number if building in a clean chroot
# Leaving this entry blank will require user interaction during the build
# which will cause a failure to build if using makechrootpkg. Note that the
# generic (default) option is 26.
#
# Note - the march=native option is unavailable by this method, use the nconfig
# and manually select it.

#  21. Intel Broadwell (MBROADWELL)
#  26. Generic-x86-64 (GENERIC_CPU)

_subarch=

_major=5.0
_minor=6
_srcname=linux-${_major}
pkgbase=linux-shadow
pkgver=${_major}.${_minor}
pkgrel=1
arch=('x86_64')
url='https://github.com/clearlinux-pkgs/linux'
license=('GPL2')
makedepends=('bc' 'git' 'inetutils' 'kmod' 'libelf' 'linux-firmware' 'xmlto')
options=('!strip')
_ucode='20190312'
_gcc_more_v='20180509'
source=(
  "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-${_major}.tar.xz"
  "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-${_major}.tar.sign"
  "https://cdn.kernel.org/pub/linux/kernel/v5.x/patch-${pkgver}.xz"
  "intel-ucode-${_ucode}.tar.gz::https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/archive/microcode-${_ucode}.tar.gz"
  "enable_additional_cpu_optimizations-$_gcc_more_v.tar.gz::https://github.com/graysky2/kernel_gcc_patch/archive/$_gcc_more_v.tar.gz"
  '60-linux.hook'  # pacman hook for depmod
  '90-linux.hook'  # pacman hook for initramfs regeneration
  '99-linux.hook'  # pacman hook for remove initramfs
  'linux.preset'   # standard config files for mkinitcpio ramdisk
)

_kernelname=${pkgbase#linux}
: ${_kernelname:=-shadow}

prepare() {
    cd ${_srcname}

    ### Add upstream patches
        msg2 'Add upstream patches'
        patch -Np1 -i ../patch-${pkgver}

    ### Setting version
        msg2 'Setting version...'
        scripts/setlocalversion --save-scmversion
        echo "-$pkgrel" > localversion.10-pkgrel
        echo "$_kernelname" > localversion.20-pkgname

    ### Add Clearlinux patches
        cp -R ../../clearlinuxBACK ${srcdir}/clearlinuxpatch
        for i in $(grep "^Patch" ${srcdir}/clearlinuxpatch/linux.spec | grep -Ev "^Patch0126" | sed -n "s/.*: //p"); do
        msg2 "Applying patch ${i}..."
        patch -Np1 -i "$srcdir/clearlinuxpatch/${i}"
        done

    ### Setting config
        msg2 'Setting config...'
        cp -Tf ../../ponto\ config/config-custom-2 ./.config

    ### Copying i915 firmware and intel-ucode
        msg2 "Copying i915 firmware and intel-ucode-${_ucode}..."
        cp -a /usr/lib/firmware/i915 firmware/
        cp -a ${srcdir}/Intel-Linux-Processor-Microcode-Data-Files-microcode-${_ucode}/intel-ucode firmware/
        cp ${srcdir}/Intel-Linux-Processor-Microcode-Data-Files-microcode-${_ucode}/intel-ucode-with-caveats/06* firmware/intel-ucode
        rm -f firmware/intel-ucode/0f*

    ### Patch source to unlock additional gcc CPU optimizations
        # https://github.com/graysky2/kernel_gcc_patch
        if [ "${_enable_gcc_more_v}" = "y" ]; then
        msg2 'Enabling additional gcc CPU optimizations...'
        patch -Np1 -i "$srcdir/kernel_gcc_patch-$_gcc_more_v/enable_additional_cpu_optimizations_for_gcc_v8.1+_kernel_v4.13+.patch"
        fi

    ### Get kernel version
        if [ "${_enable_gcc_more_v}" = "y" ] || [ -n "${_subarch}" ]; then
        yes "$_subarch" | make oldconfig
        else
        make prepare
        fi

    ### Prepared version
        make -s kernelrelease > ../version
        msg2 "Prepared %s version %s" "$pkgbase" "$(<../version)"

    ### Running make nconfig

        [[ -z "$_makenconfig" ]] || make nconfig

    ### Save configuration for later reuse

        cp -Tf ./.config "${startdir}/config-${pkgver}-${pkgrel}${_kernelname}"
}

build() {
    cd ${_srcname}

    make bzImage modules
}

_package() {
    pkgdesc='kernel and modules'
    depends=('coreutils' 'linux-firmware' 'kmod' 'mkinitcpio>=0.7')
    optdepends=('crda: to set the correct wireless channels of your country' 'modprobed-db: Keeps track of EVERY kernel module that has ever been probed - useful for those of us who make localmodconfig')
    backup=('etc/mkinitcpio.d/${pkgbase}.preset')
    install=linux.install

    local kernver="$(<version)"
    local modulesdir="$pkgdir/usr/lib/modules/$kernver"

    cd ${_srcname}

    msg2 'Installing boot image...'
    # systemd expects to find the kernel here to allow hibernation
    # https://github.com/systemd/systemd/commit/edda44605f06a41fb86b7ab8128dcf99161d2344
    install -Dm644 "$(make -s image_name)" "$modulesdir/vmlinuz"
    install -Dm644 "$modulesdir/vmlinuz" "$pkgdir/boot/vmlinuz-$pkgbase"

    msg2 'Installing modules...'
    make INSTALL_MOD_PATH="$pkgdir/usr" modules_install

    # a place for external modules,
    # with version file for building modules and running depmod from hook
    local extramodules="extramodules$_kernelname"
    local extradir="$pkgdir/usr/lib/modules/$extramodules"
    install -Dt "$extradir" -m644 ../version
    ln -sr "$extradir" "$modulesdir/extramodules"

    # remove build and source links
    rm "$modulesdir"/{source,build}

    msg2 'Installing hooks...'
    
    # sed expression for following substitutions
    local subst="
      s|%PKGBASE%|$pkgbase|g
      s|%KERNVER%|$kernver|g
      s|%EXTRAMODULES%|$extramodules|g
    "

    # hack to allow specifying an initially nonexisting install file
    sed "$subst" "$startdir/$install" > "$startdir/$install.pkg"
    true && install=$install.pkg

    # fill in mkinitcpio preset and pacman hooks
    sed "$subst" ../linux.preset | install -Dm644 /dev/stdin \
        "$pkgdir/etc/mkinitcpio.d/$pkgbase.preset"
    sed "$subst" ../60-linux.hook | install -Dm644 /dev/stdin \
        "$pkgdir/usr/share/libalpm/hooks/60-${pkgbase}.hook"
    sed "$subst" ../90-linux.hook | install -Dm644 /dev/stdin \
        "$pkgdir/usr/share/libalpm/hooks/90-${pkgbase}.hook"
    sed "$subst" ../99-linux.hook | install -Dm644 /dev/stdin \
        "$pkgdir/usr/share/libalpm/hooks/99-${pkgbase}.hook"

    msg2 'Fixing permissions...'
    chmod -Rc u=rwX,go=rX "$pkgdir"
}

_package-headers() {
    pkgdesc='header files and scripts for building modules for linux-shadow'

    local builddir="$pkgdir/usr/lib/modules/$(<version)/build"

    cd ${_srcname}

    msg2 'Installing build files...'
    install -Dt "$builddir" -m644 Makefile .config Module.symvers System.map vmlinux
    install -Dt "$builddir/kernel" -m644 kernel/Makefile
    install -Dt "$builddir/arch/x86" -m644 arch/x86/Makefile
    cp -t "$builddir" -a scripts

    # add objtool for external module building and enabled VALIDATION_STACK option
    install -Dt "$builddir/tools/objtool" tools/objtool/objtool

    # add xfs and shmem for aufs building
    mkdir -p "$builddir"/{fs/xfs,mm}

    # ???
    mkdir "$builddir/.tmp_versions"

    msg2 'Installing headers...'
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

    msg2 'Installing KConfig files...'
    find . -name "Kconfig*" -exec install -Dm644 {} "$builddir/{}" \;

    msg2 'Removing unneeded architectures...'
    local arch
    for arch in "$builddir"/arch/*/; do
        [[ $arch = */x86/ ]] && continue
        echo "Removing $(basename "$arch")"
        rm -r "$arch"
    done

    msg2 'Removing documentation...'
    rm -r "$builddir/Documentation"

    msg2 'Removing broken symlinks...'
    find -L "$builddir" -type l -printf "Removing %P\n" -delete

    msg2 'Removing loose objects...'
    find "$builddir" -type f -name "*.o" -printf "Removing %P\n" -delete

    msg2 'Stripping build tools...'
    local file
    while read -rd "" file; do
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

    msg2 'Adding symlink...'
    mkdir -p "$pkgdir/usr/src"
    ln -sr "$builddir" "$pkgdir/usr/src/$pkgbase-$pkgver"

    msg2 'Fixing permissions...'
    chmod -Rc u=rwX,go=rX "$pkgdir"
}

pkgname=("$pkgbase" "$pkgbase-headers")
for _p in "${pkgname[@]}"; do
  eval "package_$_p() {
    $(declare -f "_package${_p#$pkgbase}")
    _package${_p#$pkgbase}
  }"
done

sha256sums=('437b141a6499159f5a7282d5eb4b2be055f8e862ccce44d7464e8759c31a2e43'
            'SKIP'
            '188fbac8a0c853d560252f0b37ab98c6707ad8d0840394bef7e269229fefd6d3'
            '2a4438a66ed1a9b82be943d6d19366c006787ba5af302f425674ca6d8c928099'
            '226e30068ea0fecdb22f337391385701996bfbdba37cdcf0f1dbf55f1080542d'
            'ae2e95db94ef7176207c690224169594d49445e04249d2499e9d2fbc117a0b21'
            'c043f3033bb781e2688794a59f6d1f7ed49ef9b13eb77ff9a425df33a244a636'
            'ed9d35cb7d7bd829ff6253353efa5e2d119820fe4f4310aea536671f5e4caa37'
            'ad6344badc91ad0630caacde83f7f9b97276f80d26a20619a87952be65492c65')

validpgpkeys=(
  'ABAF11C65A2970B130ABE3C479BE3E4300411886'  # Linus Torvalds
  '647F28654894E3BD457199BE38DBBDC86092693E'  # Greg Kroah-Hartman
)

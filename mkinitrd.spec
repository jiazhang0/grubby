Summary: Makes an initial ramdisk
Name: mkinitrd
%define version 1.9
Version: %{version}
Release: 3
Copyright: GPL
Group: Utilities/System
Source: mkinitrd-%{version}.tar.gz
ExclusiveArch: i386 sparc sparc64
ExclusiveOs: Linux
Requires: /bin/ash.static losetup e2fsprogs /bin/sh fileutils grep mount gzip tar /sbin/insmod.static
BuildRoot: /var/tmp/%{name}-root

%description
Generic kernels can be built without drivers for any SCSI adapters which
load the SCSI driver as a module. To solve the problem of allowing the
kernel to read the module without being able to address the SCSI adapter,
an initial ramdisk is used. That ramdisk is loaded by the operating system
loader (such as lilo) and is available to the kernel as soon as it is loaded.
That image is resonsible for loading the proper SCSI adapter and allowing
the kernel to mount the root filesystem. This program creates such a ramdisk
image using information found in /etc/conf.modules.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
make BUILDROOT=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(755,root,root) /sbin/mkinitrd
%attr(644,root,root) /usr/man/man8/mkinitrd.8

%changelog
* Mon Jan 11 1999 Matt Wilson <msw@redhat.com>
- Ignore the absence of scsi modules, include them if they are there, but
  don't complain if they are not.
- changed --no-scsi-modules to --omit-scsi-modules (as it should have been)

* Thu Nov  5 1998 Jeff Johnson <jbj@redhat.com>
- import from ultrapenguin 1.1.

* Tue Oct 20 1998 Jakub Jelinek <jj@ultra.linux.cz>
- fix for combined sparc/sparc64 insmod, also pluto module is really
  fc4:soc:pluto and we don't look at deps, so special case it.

* Sat Aug 29 1998 Erik Troan <ewt@redhat.com>
- replaced --needs-scsi-mods (which is now the default) with
  --omit-scsi-mods

* Fri Aug  7 1998 Jeff Johnson <jbj@redhat.com>
- correct obscure regex/shell interaction (hardwires tabs on line 232)

* Mon Jan 12 1998 Erik Troan <ewt@redhat.com>
- added 'make archive' rule to Makefile
- rewrote install procedure for more robust version handling
- be smarter about grabbing options from /etc/conf.modules

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- made it use /bin/ash.static

* Wed Apr 16 1997 Erik Troan <ewt@redhat.com>
- Only use '-s' to install binaries if /usr/bin/strip is present.
- Use an image size of 2500 if binaries can't be stripped (1500 otherwise)
- Don't use "mount -o loop" anymore -- losetup the proper devices manually
- Requires losetup, e2fsprogs

* Wed Mar 12 1997 Michael K. Johnson <johnsonm@redhat.com>
- Fixed a bug in parsing options.
- Changed to use a build tree, then copy the finished tree into the
  image after it is built.
- Added patches derived from ones written by Christian Hechelmann which
  add an option to put the kernel version number at the end of the module
  name and use install -s to strip binaries on the fly.

%define	libauditver	1.4.2-1
%define	libsepolver	2.0.41-3
%define	libsemanagever	2.0.43-4
%define	libselinuxver	2.0.90-3
%define	sepolgenver	1.0.23

Summary: SELinux policy core utilities
Name:	 policycoreutils
Version: 2.0.83
Release: 19.1%{?dist}
License: GPLv2+
Group:	 System Environment/Base
Source:  http://www.nsa.gov/selinux/archives/policycoreutils-%{version}.tgz
Source1: http://www.nsa.gov/selinux/archives/sepolgen-%{sepolgenver}.tgz
URL:	 http://www.selinuxproject.org
Source2: system-config-selinux.png
Source3: system-config-selinux.desktop
Source4: system-config-selinux.pam
Source5: system-config-selinux.console
Source6: selinux-polgengui.desktop
Source7: selinux-polgengui.console
Source8: policycoreutils_man_ru2.tar.bz2
Patch:	 policycoreutils-rhat.patch
Patch1:	 policycoreutils-po.patch
Patch3:	 policycoreutils-gui.patch
Patch4:	 policycoreutils-sepolgen.patch
Patch5:	 policycoreutils-rhel6.patch
Obsoletes: policycoreutils < 2.0.61-2

%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%global pkgpythondir  %{python_sitelib}/%{name}

BuildRequires: pam-devel libcgroup-devel libsepol-static >= %{libsepolver} libsemanage-static >= %{libsemanagever} libselinux-devel >= %{libselinuxver}  libcap-devel audit-libs-devel >=  %{libauditver} gettext
BuildRequires: desktop-file-utils dbus-devel dbus-glib-devel
BuildRequires: python-devel
Requires: /bin/mount /bin/egrep /bin/awk /usr/bin/diff rpm /bin/sed
Requires: libsepol >= %{libsepolver} coreutils checkpolicy  libselinux-utils >=  %{libselinuxver}
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service  /sbin/chkconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

policycoreutils contains the policy core utilities that are required
for basic operation of a SELinux system.  These utilities include
load_policy to load policies, setfiles to label filesystems, newrole
to switch roles, and run_init to run /etc/init.d scripts in the proper
context.

%prep
%setup -q -a 1 
%patch -p1 -b .rhat
%patch1 -p1 -b .rhatpo
%patch3 -p1 -b .gui
%patch4 -p1 -b .sepolgen
%patch5 -p1 -b .rhel6

%build
make LSPP_PRIV=y LIBDIR="%{_libdir}" CFLAGS="%{optflags} -fPIE" LDFLAGS="-pie -Wl,-z,relro" all 
make -C sepolgen-%{sepolgenver} LSPP_PRIV=y LIBDIR="%{_libdir}" CFLAGS="%{optflags} -fPIE" LDFLAGS="-pie -Wl,-z,relro" all 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/var/lib/selinux
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/rc.d/init.d
%{__mkdir} -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
%{__mkdir} -p %{buildroot}%{_datadir}/pixmaps
%{__mkdir} -p %{buildroot}/%{_usr}/share/doc/%{name}-%{version}/
cp COPYING %{buildroot}/%{_usr}/share/doc/%{name}-%{version}/

make LSPP_PRIV=y  DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" install
make -C sepolgen-%{sepolgenver} DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" install

install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/system-config-selinux
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/system-config-selinux
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/selinux-polgengui
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/security/console.apps/system-config-selinux
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/security/console.apps/selinux-polgengui
tar -jxf %{SOURCE8} -C %{buildroot}/
rm -f %{buildroot}/usr/share/man/ru/man8/genhomedircon.8.gz
ln -sf consolehelper %{buildroot}%{_bindir}/system-config-selinux
ln -sf consolehelper %{buildroot}%{_bindir}/selinux-polgengui

desktop-file-install	--vendor fedora \
			--dir ${RPM_BUILD_ROOT}%{_datadir}/applications	\
			--add-category Settings				\
			%{SOURCE3}

desktop-file-install	--vendor fedora \
			--dir ${RPM_BUILD_ROOT}%{_datadir}/applications	\
			%{SOURCE6}
%find_lang %{name}

%package python
Summary: SELinux policy core python utilities
Group:	 System Environment/Base
Requires: policycoreutils = %{version}-%{release} 
Requires: libsemanage-python >= %{libsemanagever} libselinux-python libcgroup
Requires: audit-libs-python >=  %{libauditver} 
Requires: /usr/bin/make
Requires(pre): python >= 2.6
Obsoletes: policycoreutils < 2.0.61-2
Requires: setools-libs-python

%description python
The policycoreutils-python package contains the management tools use to manage an SELinux environment.

%files python
%defattr(-,root,root,-)
%{_sbindir}/semanage
%{_bindir}/audit2allow
%{_bindir}/audit2why
%{_bindir}/chcat
%{_bindir}/sandbox
%{_bindir}/sepolgen-ifgen
%{_bindir}/sepolgen-ifgen-attr-helper
%{python_sitelib}/seobject.py*
%{python_sitelib}/sepolgen
%{python_sitelib}/%{name}*.egg-info
%{pkgpythondir}
%dir  /var/lib/sepolgen
%dir  /var/lib/selinux
/var/lib/sepolgen/perm_map
%{_mandir}/man1/audit2allow.1*
%{_mandir}/ru/man1/audit2allow.1*
%{_mandir}/man1/audit2why.1*
%{_mandir}/man5/sandbox.conf.5*
%{_mandir}/man8/chcat.8*
%{_mandir}/ru/man8/chcat.8*
%{_mandir}/man8/sandbox.8*
%{_mandir}/man8/semanage.8*
%{_mandir}/ru/man8/semanage.8*

%post python
selinuxenabled && [ -f /usr/share/selinux/devel/include/build.conf ] && /usr/bin/sepolgen-ifgen 2>/dev/null 
exit 0

%package sandbox
Summary: SELinux sandbox utilities
Group:	 System Environment/Base
Requires: policycoreutils-python = %{version}-%{release} 
Requires: xorg-x11-server-Xephyr
Requires: matchbox-window-manager
Requires(post): /sbin/chkconfig
BuildRequires: libcap-ng-devel

%description sandbox
The policycoreutils-python package contains the scripts to create graphical sandboxes

%files sandbox
%defattr(-,root,root,-)
%{_datadir}/sandbox/sandboxX.sh

%triggerin python -- selinux-policy
selinuxenabled && [ -f /usr/share/selinux/devel/include/build.conf ] && /usr/bin/sepolgen-ifgen 2>/dev/null
exit 0

%post sandbox
if [ $1 -eq 1 ]; then
   /sbin/chkconfig sandbox --add
fi
%preun sandbox
if [ $1 -eq 0 ]; then
   /sbin/chkconfig sandbox --del
fi

%package newrole
Summary: The newrole application for RBAC/MLS 
Group: System Environment/Base
Requires: policycoreutils = %{version}-%{release} 

%description newrole
RBAC/MLS policy machines require newrole as a way of changing the role 
or level of a logged in user.

%files newrole
%defattr(-,root,root)
%attr(4755,root,root) %{_bindir}/newrole
%{_mandir}/man1/newrole.1.gz

%package gui
Summary: SELinux configuration GUI
Group: System Environment/Base
Requires: policycoreutils-python = %{version}-%{release} 
Requires: gnome-python2-gnome, pygtk2, pygtk2-libglade, gnome-python2-canvas 
Requires: usermode-gtk 
Requires: setools-console
Requires: selinux-policy
Requires: python >= 2.6
BuildRequires: desktop-file-utils

%description gui
system-config-selinux is a utility for managing the SELinux environment

%files gui
%defattr(-,root,root)
%{_bindir}/system-config-selinux
%{_bindir}/selinux-polgengui
%{_bindir}/sepolgen
%{_datadir}/applications/fedora-system-config-selinux.desktop
%{_datadir}/applications/fedora-selinux-polgengui.desktop
%{_datadir}/icons/hicolor/24x24/apps/system-config-selinux.png
%{_datadir}/pixmaps/system-config-selinux.png
%dir %{_datadir}/system-config-selinux
%dir %{_datadir}/system-config-selinux/templates
%{_datadir}/system-config-selinux/system-config-selinux.png
%{_datadir}/system-config-selinux/*.py*
%{_datadir}/system-config-selinux/selinux.tbl
%{_datadir}/system-config-selinux/*.glade
%{_datadir}/system-config-selinux/templates/*.py*
%config(noreplace) %{_sysconfdir}/pam.d/system-config-selinux
%config(noreplace) %{_sysconfdir}/pam.d/selinux-polgengui
%config(noreplace) %{_sysconfdir}/security/console.apps/system-config-selinux
%config(noreplace) %{_sysconfdir}/security/console.apps/selinux-polgengui

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/sbin/restorecon
/sbin/fixfiles
/sbin/setfiles
/sbin/load_policy
%{_sbindir}/seunshare
%{_sbindir}/genhomedircon
%{_sbindir}/load_policy
%{_sbindir}/restorecond
%{_sbindir}/setsebool
%{_sbindir}/semodule
%{_sbindir}/sestatus
%{_sbindir}/run_init
%{_sbindir}/open_init_pty
%{_bindir}/secon
%{_bindir}/semodule_deps
%{_bindir}/semodule_expand
%{_bindir}/semodule_link
%{_bindir}/semodule_package
%{_sysconfdir}/rc.d/init.d/sandbox
%config(noreplace) %{_sysconfdir}/sysconfig/sandbox
%config(noreplace) %{_sysconfdir}/pam.d/newrole
%config(noreplace) %{_sysconfdir}/pam.d/run_init
%config(noreplace) %{_sysconfdir}/sestatus.conf
%attr(755,root,root) /etc/rc.d/init.d/restorecond
%config(noreplace) /etc/selinux/restorecond.conf
%config(noreplace) /etc/selinux/restorecond_user.conf
%{_sysconfdir}/xdg/autostart/restorecond.desktop
%{_datadir}/dbus-1/services/org.selinux.Restorecond.service
# selinux-policy Requires: policycoreutils, so we own this set of directories and our files within them
%{_mandir}/man8/fixfiles.8*
%{_mandir}/ru/man8/fixfiles.8*
%{_mandir}/man8/load_policy.8*
%{_mandir}/ru/man8/load_policy.8*
%{_mandir}/man8/open_init_pty.8*
%{_mandir}/ru/man8/open_init_pty.8*
%{_mandir}/man8/restorecon.8*
%{_mandir}/ru/man8/restorecon.8*
%{_mandir}/man8/restorecond.8*
%{_mandir}/ru/man8/restorecond.8*
%{_mandir}/man8/run_init.8*
%{_mandir}/ru/man8/run_init.8*
%{_mandir}/man8/semodule.8*
%{_mandir}/ru/man8/semodule.8*
%{_mandir}/man8/semodule_deps.8*
%{_mandir}/ru/man8/semodule_deps.8*
%{_mandir}/man8/semodule_expand.8*
%{_mandir}/ru/man8/semodule_expand.8*
%{_mandir}/man8/semodule_link.8*
%{_mandir}/ru/man8/semodule_link.8*
%{_mandir}/man8/semodule_package.8*
%{_mandir}/ru/man8/semodule_package.8*
%{_mandir}/man8/sestatus.8*
%{_mandir}/ru/man8/sestatus.8*
%{_mandir}/man8/setfiles.8*
%{_mandir}/ru/man8/setfiles.8*
%{_mandir}/man8/setsebool.8*
%{_mandir}/ru/man8/setsebool.8*
%{_mandir}/man1/secon.1*
%{_mandir}/ru/man1/secon.1*
%{_mandir}/man8/seunshare.8*
%{_mandir}/man8/genhomedircon.8*
%doc %{_usr}/share/doc/%{name}-%{version}

%preun
if [ $1 -eq 0 ]; then
   /sbin/service restorecond stop > /dev/null 2>&1
   /sbin/chkconfig --del restorecond
fi
exit 0

%post
/sbin/chkconfig --add restorecond
exit 0

%postun
if [ "$1" -ge "1" ]; then 
   [ -x /sbin/service ] && /sbin/service restorecond condrestart  > /dev/null
fi
exit 0

%changelog
* Wed Aug 25 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-19.1
- Fix sandbox -H and -T regression - again
Resolves: #626404

* Mon Aug 23 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-19
- Fix sandbox -H and -T regression
Resolves: #626404
- Fix fcontext translation handling in system-config-selinux

* Fri Aug 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-18
- Fix sandbox error handling

* Fri Aug 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-17
- Apply patch to restorecond from Chris Adams, which will cause restorecond 
- to watch first user that logs in.

* Thu Aug 12 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-16
- Add COPYING file to doc dir
Resolves: #623948

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-15
- Update po and translations
Resolves: #610473

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-14
- More fixes for polgen tools

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-13
- Remove requirement to run selinux-polgen as root

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-12
- Update po and translations
- Fix gui policy generation tools
Resolves: #610473

* Wed Aug 4 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-11
- Update po and translations

* Sat Jul 31 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.83-10
- rebuild against python 2.7

* Wed Jul 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-9
- Update selinux-polgengui to sepolgen policy generation

* Wed Jul 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-8
- Fix invalid free in seunshare and fix man page

* Tue Jul 27 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-7
- Update translations

* Mon Jul 26 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-6
- Fix sandbox man page

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.83-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 20 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-4
- Add translations for menus
- Fixup man page from Russell Coker

* Tue Jun 15 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-3
- Change python scripts to use -s flag
- Update po

* Tue Jun 15 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-1
- Update to upstream
	* Add sandbox support from Dan Walsh with modifications from Steve Lawrence.

* Tue Jun 15 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-31
- Fix sepolgen code generation
Resolve: #603001

* Tue Jun 8 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-30
- Add cgroup support for sandbox 

* Mon Jun 7 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-29
- Allow creation of /var/cache/DOMAIN from sepolgen

* Thu Jun 3 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-28
- Fix sandbox init script 
- Add dbus-launch to sandbox -X
Resolve: #599599

* Thu Jun 3 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-27
- Move genhomedircon.8 to same package as genhomedircon
- Fix sandbox to pass unit test
Resolves: #595796

* Wed Jun 2 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-26
- Fix listing of booleans from audit2allow

* Wed Jun 2 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-25
- Fix audit2allow to output if the current policy has avc
- Update translations
- Fix icon

* Thu May 27 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-24
- Man page fixes
- sandbox fixes
- Move seunshare to base package

* Fri May 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-23
- Fix seunshare translations
- Fix seunshare to work on all arches
- Fix icon for system-config-selinux
Resolves: #595276

* Fri May 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-22
- Fix can_exec definition in sepolgen

* Fri May 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-21
- Add man page for seunshare and genhomedircon
Resolves: #594303
- Fix node management via semanage

* Wed May 19 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-20
- Fixes from upstream for sandbox command
Resolves: #580938

* Thu May 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-18
- Fix sandbox error handling on copyfile
- Fix desktop files

* Tue May 11 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-17
- Fix policy tool to have correct name in menus
- Fix seunshare to handle /tmp being in ~/home
- Fix saving of altered files
- Update translations

* Tue May 4 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-15
- Allow audit2allow to specify alternative policy file for analysis

* Mon May 3 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-14
- Update po
- Fix sepolgen --no_attrs
Resolves: #588280

* Thu Apr 29 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-13
- Make semanage boolean work on disabled machines and during livecd xguest
- Fix homedir and tmpdir handling in sandbox
Resolves: #587263

* Wed Apr 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-11
- Make semanage boolean work on disabled machines 

* Tue Apr 27 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-10
- Make sepolgen-ifgen be quiet

* Wed Apr 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-8
- Make sepolgen report on more interfaces 
- Fix system-config-selinux display of modules

* Thu Apr 15 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-7
- Fix crash when args are empty
Resolves: #582542
- Fix semange to exit on bad options
- Fix semanage dontaudit man page section
Resolves: #582533

* Wed Apr 14 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-6
- Remove debug line from semanage
- Update po

* Tue Apr 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-5
- Fix sandbox comment on HOMEDIRS
- Fix sandbox to throw error on bad executable

* Tue Apr 6 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-4
- Fix spacing in templates 

* Wed Mar 31 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-3
- Fix semanage return codes

* Tue Mar 30 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-2
- Fix sepolgen to confirm to the "Reference Policy Style Guide" 

* Tue Mar 23 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-1
- Update to upstream 
	* Add avc's since boot from Dan Walsh.
	* Fix unit tests from Dan Walsh.

* Tue Mar 23 2010 Dan Walsh <dwalsh@redhat.com> 2.0.81-4
- Update to upstream - sepolgen
	* Add since-last-boot option to audit2allow from Dan Walsh.
	* Fix sepolgen output to match what Chris expects for upstream
	  refpolicy from Dan Walsh.

* Mon Mar 22 2010 Dan Walsh <dwalsh@redhat.com> 2.0.81-3
- Allow restorecon on > 2 Gig files

* Tue Mar 16 2010 Dan Walsh <dwalsh@redhat.com> 2.0.81-2
- Fix semanage handling of boolean options
- Update translations

* Fri Mar 12 2010 Dan Walsh <dwalsh@redhat.com> 2.0.81-1
- Update to upstream
	* Add dontaudit flag to audit2allow from Dan Walsh.

* Thu Mar 11 2010 Dan Walsh <dwalsh@redhat.com> 2.0.80-2
- Use --rbind in sandbox init scripts

* Mon Mar 8 2010 Dan Walsh <dwalsh@redhat.com> 2.0.80-1
- Update to upstream
	* Module enable/disable support from Dan Walsh.

* Mon Mar 1 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-5
- Rewrite of sandbox script, add unit test for sandbox 
- Update translations

* Mon Mar 1 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-4
- Fix patch for dontaudit rules from audit2allow for upstream acceptance

* Fri Feb 26 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-3
- Fixes for fixfiles

* Wed Feb 17 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-2
- Fix sandbox to complain if mount-shared has not been run
- Fix to use /etc/sysconfig/sandbox

* Tue Feb 16 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-1
- Update to upstream
	* Fix double-free in newrole
- Fix python language handling

* Thu Feb 11 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-21
- Fix display of command in sandbox

* Fri Feb 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-20
- Catch OSError in semanage

* Wed Feb 3 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-19
- Fix seobject and fixfiles

* Fri Jan 29 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-17
- Change seobject to use translations properly

* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-16
- Cleanup spec file
Resolves: 555835

* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-15
- Add use_resolve to sepolgen

* Wed Jan 27 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-14
- Add session capability to sandbox 
- sandbox -SX -H ~/.homedir -t unconfined_t -l s0:c15 /etc/gdm/Xsession

* Thu Jan 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-13
- Fix executable template for fifo files

* Tue Jan 19 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-12
- Fix patch xod xmodmap
- Exit 0 from script

* Thu Jan 14 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-11
- Run with the same xdmodmap in sandbox as outside
- Patch from Josh Cogliati

* Fri Jan 8 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-10
- Fix sepolgen to not generate user sh section on non user policy

* Fri Jan 8 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-9
- Add -e to semanage man page
- Add -D qualifier to audit2allow to generate dontaudit rules

* Wed Jan 6 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-8
- Speed up audit2allow processing of audit2why comments

* Fri Dec 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-7
- Fixes to sandbox man page

* Thu Dec 17 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-6
- Add setools-libs-python to requires for gui

* Wed Dec 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-5
- If restorecond running as a user has no files to watch then it should exit.  (NFS Homedirs)

* Thu Dec 10 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-4
- Move sandbox man page to base package

* Tue Dec 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-3
- Fix audit2allow to report constraints, dontaudits, types, booleans

* Fri Dec 4 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-2
- Fix restorecon -i to ignore enoent

* Tue Dec 1 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-1
- Update to upstream
	* Remove non-working OUTFILE from fixfiles from Dan Walsh.
	* Additional exception handling in chcat from Dan Walsh.

	* fix sepolgen to read a "type 1403" msg as a policy load by Stephen
	  Smalley <sds@tycho.nsa.gov>
	* Add support for Xen ocontexts from Paul Nuzzi.

* Tue Nov 24 2009 Dan Walsh <dwalsh@redhat.com> 2.0.77-1
- Update to upstream
	* Fixed bug preventing semanage node -a from working
	  from Chad Sellers
	* Fixed bug preventing semanage fcontext -l from working
	  from Chad Sellers
- Change semanage to use unicode

* Wed Nov 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.76-1
- Update to upstream
	* Remove setrans management from semanage, as it does not work
	  from Dan Walsh.
	* Move load_policy from /usr/sbin to /sbin from Dan Walsh.

* Mon Nov 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.75-3
- Raise exception if user tries to add file context with an embedded space

* Wed Nov 11 2009 Dan Walsh <dwalsh@redhat.com> 2.0.75-2
- Fix sandbox to setsid so it can run under mozilla without crashing the session

* Tue Nov 2 2009 Dan Walsh <dwalsh@redhat.com> 2.0.75-1
- Update to upstream
	* Factor out restoring logic from setfiles.c into restore.c

* Fri Oct 30 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-15
- Fix typo in seobject.py

* Fri Oct 30 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-14
- Allow semanage -i and semanage -o to generate customization files.
- semanage -o will generate a customization file that semanage -i can read and set a machines to the same selinux configuration

* Tue Oct 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-13
- Fix restorecond man page

* Mon Oct 19 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-12
- Add generation of the users context file to polgengui

* Fri Oct 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-11
- Remove tabs from system-config-selinux glade file

* Thu Oct 15 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-10
- Remove translations screen from system-config-selinux

* Wed Oct 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-9
- Move fixfiles man pages into the correct package
- Add genhomedircon to fixfiles restore

* Thu Oct 6 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-8
- Add check to sandbox to verify save changes - Chris Pardy
- Fix memory leak in restorecond - Steve Grubb

* Thu Oct 1 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-7
- Fixes Templates

* Thu Oct 1 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-6
- Fixes for polgengui to handle tcp ports correctly
- Fix semanage node -a

* Wed Sep 30 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-5
- Fixes for semanage -equiv, readded modules, --enable, --disable

* Sun Sep 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-4
- Close sandbox when eclipse exits

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-3
- Security fixes for seunshare
- Fix Sandbox to handle non file input to command.

* Thu Sep 17 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-2
- Security fixes for seunshare

* Thu Sep 17 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-1
- Update to upstream
	* Change semodule upgrade behavior to install even if the module
	  is not present from Dan Walsh.
	* Make setfiles label if selinux is disabled and a seclabel aware
	  kernel is running from Caleb Case.
	* Clarify forkpty() error message in run_init from Manoj Srivastava.

* Mon Sep 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-5
- Fix sandbox to handle relative paths

* Mon Sep 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-4
- Add symbolic link to load_policy

* Mon Sep 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-3
- Fix restorecond script to use force-reload

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-2
- Fix init script to show status in usage message

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-1
- Update to upstream
        * Add semanage dontaudit to turn off dontaudits from Dan Walsh.
        * Fix semanage to set correct mode for setrans file from Dan Walsh.
        * Fix malformed dictionary in portRecord from Dan Walsh.
	* Restore symlink handling support to restorecon based on a patch by
	Martin Orr.  This fixes the restorecon /dev/stdin performed by Debian
	udev scripts that was broken by policycoreutils 2.0.70.

* Thu Sep 3 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-15
- Add DAC_OVERRIED to seunshare

* Wed Sep  2 2009 Bill Nottingham <notting@redhat.com> 2.0.71-15
- Fix typo

* Fri Aug 28 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-14
- Add enable/disable patch

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.71-13
- rebuilt with new audit

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-12
- Tighten up controls on seunshare.c

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-11
- Add sandboxX

* Sat Aug 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-10
- Fix realpath usage to only happen on argv input from user

* Fri Aug 21 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.0.71-9
- Don't try to remove restorecond after last erase (done already in %%preun).
- Ensure scriptlets exit with status 0.
- Fix %%post and %%pr

* Thu Aug 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-7
- Fix glob handling of /..

* Wed Aug 19 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-6
- Redesign restorecond to use setfiles/restore functionality

* Wed Aug 19 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-5
- Fix sepolgen again

* Tue Aug 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-4
- Add --boot flag to audit2allow to get all AVC messages since last boot

* Tue Aug 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-3
- Fix semanage command

* Thu Aug 13 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-2
- exclude unconfined.if from sepolgen

* Thu Aug 13 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-1
- Fix chcat to report error on non existing file
- Update to upstream
	* Modify setfiles/restorecon checking of exclude paths.  Only check
	user-supplied exclude paths (not automatically generated ones based on
	lack of seclabel support), don't require them to be directories, and
	ignore permission denied errors on them (it is ok to exclude a path to
	which the caller lacks permission).

* Mon Aug 10 2009 Dan Walsh <dwalsh@redhat.com> 2.0.70-2
- Don't warn if the user did not specify the exclude if root can not stat file system

* Wed Aug 5 2009 Dan Walsh <dwalsh@redhat.com> 2.0.70-1
- Update to upstream
	* Modify restorecon to only call realpath() on user-supplied pathnames
	from Stephen Smalley.
	* Fix typo in fixfiles that prevented it from relabeling btrfs 
	  filesystems from Dan Walsh.

* Sun Jul 29 2009 Dan Walsh <dwalsh@redhat.com> 2.0.68-1
- Fix location of man pages
- Update to upstream
	* Modify setfiles to exclude mounts without seclabel option in
	/proc/mounts on kernels >= 2.6.30 from Thomas Liu.
	* Re-enable disable_dontaudit rules upon semodule -B from Christopher
	Pardy and Dan Walsh.
	* setfiles converted to fts from Thomas Liu.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.64-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.64-2
- fix multiple directory ownership of mandirs

* Fri Jun 26 2009 Dan Walsh <dwalsh@redhat.com> 2.0.64-1
- Update to upstream
	* Keep setfiles from spamming console from Dan Walsh.
	* Fix chcat's category expansion for users from Dan Walsh.
- Update po files
- Fix sepolgen

* Thu Jun 4 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-5
- Add sepolgen executable

* Mon Jun 1 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-4
- Fix Sandbox option handling
- Fix fixfiles handling of btrfs

* Tue May 26 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-3
- Fix sandbox to be able to execute files in homedir

* Fri May 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-2
- Change polgen.py to be able to generate policy

* Wed May 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-1
- Update to upstream
	* Fix transaction checking from Dan Walsh.
	* Make fixfiles -R (for rpm) recursive.
	* Make semanage permissive clean up after itself from Dan Walsh.
	* add /root/.ssh/* to restorecond.conf

* Wed Apr 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-14
- Fix audit2allow -a to retun /var/log/messages

* Wed Apr 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-13
- Run restorecond as a user service

* Thu Apr 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-12
- Add semanage module support

* Tue Apr 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-10
- Do not print \n, if count < 1000;

* Sat Apr 11 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-9
- Handle case where subs file does not exist

* Wed Apr 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-8
- Update po files
- Add --equiv command for semanage

* Tue Mar 31 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-7
- Cleanup creation of permissive domains
- Update po files

* Mon Mar 23 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-6
- Update po files

* Thu Mar 12 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-5
- Fix semanage transations

* Sat Mar 7 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-4
- Update polgengui templates to match current upstream policy

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-2
- Add /root/.ssh to restorecond.conf
- fixfiles -R package should recursively fix files

* Wed Feb 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-1
- Update to upstream
	* Add btrfs to fixfiles from Dan Walsh.
	* Remove restorecond error for matching globs with multiple hard links
 	  and fix some error messages from Dan Walsh.
	* Make removing a non-existant module a warning rather than an error
	  from Dan Walsh.
	* Man page fixes from Dan Walsh.

* Mon Feb 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-10
- Fix script created by polgengui to not refer to selinux-policy-devel

* Mon Feb 9 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-9
- Change initc scripts to use proper labeling on gui

* Mon Feb 9 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-8
- Add obsoletes to cause policycoreuils to update both python and non python version

* Fri Jan 30 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-7
- Dont report errors on glob match and multiple links

* Thu Jan 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-6
- Move sepolgen-ifgen to post python

* Wed Jan 21 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-4
- Fix Translations

* Tue Jan 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-3
- Add Domains Page to system-config-selinux
- Add ability to create dbus confined applications to polgen

* Wed Jan 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-2
- Split python into a separate package

* Tue Jan 13 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-1
- Update to upstream
	* chcat: cut categories at arbitrary point (25) from Dan Walsh
	* semodule: use new interfaces in libsemanage for compressed files
	  from Dan Walsh
	* audit2allow: string changes for usage

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> 2.0.60-7
- Don't error out when removing a non existing module

* Mon Dec 15 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-6
- fix audit2allow man page

* Wed Dec 10 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-5
- Fix Japanese translations

* Sat Dec 6 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-4
- Change md5 to hashlib.md5 in sepolgen

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.60-3
- Rebuild for Python 2.6

* Tue Dec 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-2
- Fix error checking in restorecond, for inotify_add_watch

* Mon Dec 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-1
- Update to upstream
	* semanage: use semanage_mls_enabled() from Stephen Smalley.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.59-2
- Rebuild for Python 2.6

* Tue Nov 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.59-1
- Update to upstream
	* fcontext add checked local records twice, fix from Dan Walsh. 

* Mon Nov 10 2008 Dan Walsh <dwalsh@redhat.com> 2.0.58-1
- Update to upstream
	* Allow local file context entries to override policy entries in
	semanage from Dan Walsh.
	* Newrole error message corrections from Dan Walsh.
	* Add exception to audit2why call in audit2allow from Dan Walsh.

* Fri Nov 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-12
- add compression

* Tue Nov 04 2008 Jesse Keating <jkeating@redhat.com> - 2.0.57-11
- Move the usermode-gtk requires to the -gui subpackage.

* Thu Oct 30 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-10
- Fix traceback in audit2why

* Wed Oct 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-9
- Make GUI use translations

* Wed Oct 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-8
- Fix typo in man page

* Mon Oct 28 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-7
- Handle selinux disabled correctly
- Handle manipulation of fcontext file correctly

* Mon Oct 27 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-6
- Add usermode-gtk requires

* Tue Oct 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-5
- Allow addition of local modifications of fcontext policy.

* Mon Oct 20 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-4
- Fix system-config-selinux booleanspage throwing and exception
- Update po files

* Fri Oct 17 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-3
- Fix text in newrole
- Fix revertbutton on booleans page in system-config-selinux

* Wed Oct 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-2
- Change semodule calls for libsemanage

* Wed Oct 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-1
- Update to upstream
	* Update po files from Dan Walsh.

* Fri Sep 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.56-1
- Fix semanage help display
- Update to upstream
	* fixfiles will now remove all files in /tmp and will check for
	  unlabeled_t in /tmp and /var/tmp from Dan Walsh.
	* add glob support to restorecond from Dan Walsh.
	* allow semanage to handle multi-line commands in a single transaction
	  from Dan Walsh.

* Thu Sep 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-8
- Only call gen_requires once in sepolgen

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-7
- Change Requires line to gnome-python2-gnome
- Fix spelling mistakes
- Require libselinux-utils

* Mon Sep 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-5
- Add node support to semanage

* Mon Sep 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-4
- Fix fixfiles to correct unlabeled_t files and remove .? files

* Wed Sep 3 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-2
- Add glob support to restorecond so it can check every file in the homedir

* Thu Aug 28 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-1
- Update to upstream
	* Merged semanage node support from Christian Kuester.

* Fri Aug 15 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-7
- Add require libsemanage-python

* Mon Aug 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-6
- Add missing html_util.py file

* Thu Aug 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-5
- Fixes for multiple transactions

* Wed Aug 6 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-2
- Allow multiple transactions in one semanage command

* Tue Aug 5 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-1
- Update to upstream
	* Add support for boolean files and group support for seusers from Dan Walsh.
	* Ensure that setfiles -p output is newline terminated from Russell Coker.

* Fri Aug 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.53-3
- Allow semanage user to add group lists % groupname

* Tue Jul 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.53-2
- Fix help 

* Tue Jul 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.53-1
- Update to upstream
	* Change setfiles to validate all file_contexts files when using -c from Stephen Smalley.

* Tue Jul 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-6
- Fix boolean handling
- Upgrade to latest sepolgen
- Update po patch

* Wed Jul 9 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-5
- Additial cleanup of boolean handling for semanage

* Tue Jul 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-4
- Handle ranges of ports in gui

* Tue Jul 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-3
- Fix indent problems in seobject

* Wed Jul 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-2
- Add lockdown wizard
- Allow semanage booleans to take an input file an process lots of booleans at once.

* Wed Jul 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-1
- Default prefix to "user"

* Tue Jul 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.50-2
- Remove semodule use within semanage
- Fix launching of polgengui from toolbar

* Mon Jun 30 2008 Dan Walsh <dwalsh@redhat.com> 2.0.50-1
- Update to upstream
	* Fix audit2allow generation of role-type rules from Karl MacMillan.

* Tue Jun 24 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-10
- Fix spelling of enforcement

* Mon Jun 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-8
- Fix sepolgen/audit2allow handling of roles

* Mon Jun 16 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-7
- Fix sepolgen-ifgen processing

* Thu Jun 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-6
- Add deleteall to semanage permissive, cleanup error handling

* Thu Jun 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-5
- Complete removal of rhpl requirement

* Wed Jun 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-4
- Add semanage permissive *

* Fri May 16 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-3
- Fix fixfiles to cleanup /tmp and /var/tmp

* Fri May 16 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-2
- Fix listing of types in gui

* Mon May 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-1
- Update to upstream
	* Remove security_check_context calls for prefix validation from semanage.
	* Change setfiles and restorecon to not relabel if the file already has the correct context value even if -F/force is specified.

* Mon May 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.47-3
- Remove /usr/share/locale/sr@Latn/LC_MESSAGES/policycoreutils.mo

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.47-2
- Add 	rm -rf /tmp/gconfd-* /tmp/pulse-* /tmp/orbit-* to fixfiles restore
- So that mislabeled files will get removed on full relabel

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.47-1
- Make restorecond not start by default
- Fix polgengui to allow defining of confined roles.
- Add patches from Lubomir Rintel <lkundrak@v3.sk> 
  * Add necessary runtime dependencies on setools-console for -gui
  * separate stderr when run seinfo commands
- Update to upstream
  * Update semanage man page for booleans from Dan Walsh.
  * Add further error checking to seobject.py for setting booleans.

* Fri Apr 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.0.46-5
- Uninvasive (ie no string or widget changes) HIG approximations 
  in selinux-polgenui

* Fri Apr 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.0.46-4
- Move s-c-selinux to the right menu

* Sun Apr 6 2008 Dan Walsh <dwalsh@redhat.com> 2.0.46-3
- Fix boolean descriptions
- Fix semanage man page

* Wed Mar 19 2008 Dan Walsh <dwalsh@redhat.com> 2.0.46-2
- Don't use prefix in gui

* Tue Mar 18 2008 Dan Walsh <dwalsh@redhat.com> 2.0.46-1
- Update to upstream
	* Update audit2allow to report dontaudit cases from Dan Walsh.
	* Fix semanage port to use --proto from Caleb Case.

* Fri Feb 22 2008 Dan Walsh <dwalsh@redhat.com> 2.0.44-1
- Update to upstream
	* Fix for segfault when conf file parse error occurs.

* Wed Feb 13 2008 Dan Walsh <dwalsh@redhat.com> 2.0.43-2
- Don't show tabs on polgengui

* Wed Feb 13 2008 Dan Walsh <dwalsh@redhat.com> 2.0.43-1
- Update to upstream
	* Merged fix fixfiles option processing from Vaclav Ovsik.
- Added existing users, staff and user_t users to polgengui

* Fri Feb 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.42-3
- Add messages for audit2allow DONTAUDIT

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 2.0.42-2
- Add ability to transition to roles via polgengui

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.42-1
- Update to upstream
	* Make semodule_expand use sepol_set_expand_consume_base to reduce
	  peak memory usage.

* Tue Jan 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.41-1
- Update to upstream
	* Merged audit2why fix and semanage boolean --on/--off/-1/-0 support from Dan Walsh.
	* Merged a second fixfiles -C fix from Marshall Miller.


* Thu Jan 24 2008 Dan Walsh <dwalsh@redhat.com> 2.0.39-1
- Don't initialize audit2allow for audit2why call.  Use default
- Update to upstream
	* Merged fixfiles -C fix from Marshall Miller.

* Thu Jan 24 2008 Dan Walsh <dwalsh@redhat.com> 2.0.38-1
- Update to upstream
  * Merged audit2allow cleanups and boolean descriptions from Dan Walsh.
  * Merged setfiles -0 support by Benny Amorsen via Dan Walsh.
  * Merged fixfiles fixes and support for ext4 and gfs2 from Dan Walsh.

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.37-1
- Update to upstream
  * Merged replacement for audit2why from Dan Walsh.

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.36-2
- Cleanup fixfiles -f message in man page

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.36-1
- Update to upstream
	* Merged update to chcat, fixfiles, and semanage scripts from Dan Walsh.
	* Merged sepolgen fixes from Dan Walsh.

* Tue Jan 22 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-5
- handle files with spaces on upgrades

* Tue Jan 22 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-4
- Add support in fixfiles for ext4 ext4dev and gfs2

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-3
- Allow files with spaces to be used by setfiles

* Tue Jan 15 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-2
- Add descriptions of booleans to audit2allow

* Fri Jan 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-1
- Update to upstream
	* Merged support for non-interactive newrole command invocation from Tim Reed.

* Thu Jan 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.34-8
- Change to use selinux bindings to audit2why

* Tue Jan 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.34-7
- Fix fixfiles to handle no args

* Mon Dec 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-5
- Fix roles output when creating a module

* Mon Dec 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-4
- Handle files with spaces in fixfiles

* Fri Dec 21 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-3
- Catch SELINUX_ERR with audit2allow and generate policy

* Thu Dec 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-2
- Make sepolgen set error exit code when partial failure
- audit2why now checks booleans for avc diagnosis

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-1
- Update to upstream
	* Update Makefile to not build restorecond if
	  /usr/include/sys/inotify.h is not present

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.33-4
- Fix sepolgen to be able to parse Fedora 9 policy
      Handle ifelse statements
      Handle refpolicywarn inside of define
      Add init.if and inetd.if into parse
      Add parse_file to syntax error message

* Fri Dec 14 2007 Dan Walsh <dwalsh@redhat.com> 2.0.33-3
- Add scroll bar to fcontext gui page

* Tue Dec 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.33-2
- Add Russion Man pages

* Mon Dec 10 2007 Dan Walsh <dwalsh@redhat.com> 2.0.33-1
- Upgrade from NSA
	* Drop verbose output on fixfiles -C from Dan Walsh.
	* Fix argument handling in fixfiles from Dan Walsh.
	* Enhance boolean support in semanage, including using the .xml description when available, from Dan Walsh.
- Fix handling of final screen in polgengui

* Sun Dec 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.32-2
- Fix handling of disable selinux button in gui

* Mon Nov 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.32-1
- Upgrade from NSA
	* load_policy initial load option from Chad Sellers.

* Mon Nov 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-20
- Don't show error on missing policy.xml

* Mon Nov 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-19
- GUI Enhancements
  - Fix cgi generation
  - Use more patterns

* Mon Nov 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-18
- Remove codec hacking, which seems to be fixed in python

* Fri Nov 16 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-17
- Fix typo
- Change to upstream minimal privledge interfaces

* Fri Nov 16 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-16
- Fix fixfiles argument parsing

* Thu Nov 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-15
- Fix File Labeling add 

* Thu Nov 8 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-14
- Fix semanage to handle state where policy.xml is not installed

* Mon Nov 5 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-13
- Remove -v from restorecon in fixfiles

* Mon Nov 5 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-12
- Fix filter and search capabilities, add wait cursor

* Fri Nov 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-11
- Translate booleans via policy.xml
- Allow booleans to be set via semanage

* Thu Nov 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-10
- Require use of selinux-policy-devel

* Wed Oct 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-9
- Validate semanage fcontext input
- Fix template names for log files in gui

* Fri Oct 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-8
- Fix template to generate correct content

* Fri Oct 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-7
- Fix consolekit link to selinux-polgengui

* Thu Oct 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-6
- Fix the generation templates

* Tue Oct 16 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-5
- Fix enable/disable audit messages

* Mon Oct 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-4
- Add booleans page

* Mon Oct 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-3
- Lots of updates to gui

* Mon Oct 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-1
- Remove no.po
- Update to upstream
	* Fix semodule option handling from Dan Walsh.
	* Add deleteall support for ports and fcontexts in semanage from Dan Walsh.

* Thu Oct 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.29-2
- Fix semodule parameter checking

* Sun Oct 7 2007 Dan Walsh <dwalsh@redhat.com> 2.0.29-1
- Update to upstream
	* Add genhomedircon script to invoke semodule -Bn from Dan Walsh.
- Add deleteall for ports and fcontext

* Fri Oct 5 2007 Dan Walsh <dwalsh@redhat.com> 2.0.28-1
- Update to upstream
	* Update semodule man page for -D from Dan Walsh.
	* Add boolean, locallist, deleteall, and store support to semanage from Dan Walsh.

* Tue Oct 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-7
- Add genhomedircon script to rebuild file_context for shadow-utils

* Tue Oct 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-6
- Update translations

* Tue Oct 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-5
- Additional checkboxes for application policy

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-4
- Allow policy writer to select user types to transition to there users

* Thu Sep 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-3
- Fix bug in building policy with polgengui
- Creating ports correctly

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-1
- Update to upstream
	* Improve semodule reporting of system errors from Stephen Smalley.

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.26-3
- Show local changes with semanage

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.26-2
- Fixed spelling mistakes in booleans defs
- Update po

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.26-1
- Update to upstream
  * Fix setfiles selabel option flag setting for 64-bit from Stephen Smalley.

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-15
- Fix wording in policy generation tool

* Fri Sep 14 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-14
- Fix calls to _admin interfaces

* Tue Sep 13 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-13
- Upgrade version of sepolgen from NSA
	* Expand the sepolgen parser to parse all current refpolicy modules from Karl MacMillan.
	* Suppress generation of rules for non-denials from Karl MacMillan (take 3).

* Tue Sep 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-12
- Remove bogus import libxml2 

* Mon Sep 10 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-11
- Lots of fixes for polgengui

* Thu Sep 6 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-10
- Change Requires /bin/rpm to rpm

* Wed Sep 5 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-9
- Bump libsemanage version for disable dontaudit
- New gui features for creating admin users

* Fri Aug 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-8
- Fix generated code for admin policy

* Fri Aug 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-7
- Lots of fixes for role templates

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-6
- Add more role_templates

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-5
- Update genpolgui to add creation of user domains

* Mon Aug 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-4
- Fix location of sepolgen-ifgen

* Sat Aug 25 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-3
- Add selinux-polgengui to desktop

* Fri Aug 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-2
- Cleanup spec

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-1
- Update semodule man page
	* Fix genhomedircon searching for USER from Todd Miller
	* Install run_init with mode 0755 from Dan Walsh.
	* Fix chcat from Dan Walsh.
	* Fix fixfiles pattern expansion and error reporting from Dan Walsh.	
	* Optimize genhomedircon to compile regexes once from Dan Walsh.
	* Fix semanage gettext call from Dan Walsh.

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.23-2
- Update semodule man page

* Mon Aug 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.23-1
- Update to match NSA
  	* Disable dontaudits via semodule -D

* Wed Aug 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-13
- Speed up genhomedircon by an order of magnitude by compiling regex
- Allow semanage fcontext -a -t <<none>> /path to work

* Fri Jul 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-11
- Fixfiles update required to match new regex

* Fri Jul 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-10
- Update booleans translations

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 2.0.22-9
- rebuild for toolchain bug

* Tue Jul 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-8
- Add requires libselinux-python 

* Mon Jul 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-7
- Fix fixfiles to report incorrect rpm
- Patch provided by Tony Nelson 

* Fri Jul 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-6
- Clean up spec file

* Thu Jul 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-5
- Require newer libselinux version

* Fri Jul 7 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-4
- Fix checking for conflicting directory specification in genhomedircon

* Mon Jun 25 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-3
- Fix spelling mistakes in GUI

* Fri Jun 22 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-2
- Fix else path in chcat

* Thu Jun 21 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-1
- Update to match NSA
	* Rebase setfiles to use new labeling interface.

* Wed Jun 13 2007 Dan Walsh <dwalsh@redhat.com> 2.0.21-2
- Add filter to all system-config-selinux lists

* Wed Jun 13 2007 Dan Walsh <dwalsh@redhat.com> 2.0.21-1
- Update to match NSA
	* Fixed setsebool (falling through to error path on success).

* Mon Jun 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.20-1
- Update to match NSA
	* Merged genhomedircon fixes from Dan Walsh.
	* Merged setfiles -c usage fix from Dan Walsh.
	* Merged restorecon fix from Yuichi Nakamura.
	* Dropped -lsepol where no longer needed.

* Mon Jun 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-5
- Fix translations code,  Add more filters to gui

* Mon Jun 4 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-4
- Fix setfiles -c to make it work

* Mon Jun 4 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-3
- Fix french translation to not crash system-config-selinux

* Fri Jun 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-2
- Fix genhomedircon to work in stage2 builds of anaconda

* Fri May 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-1
- Update to match NSA

* Thu May 17 2007 Dan Walsh <dwalsh@redhat.com> 2.0.16-2
- Fixes for polgentool templates file

* Tue May 4 2007 Dan Walsh <dwalsh@redhat.com> 2.0.16-1
- Updated version of policycoreutils
	* Merged support for modifying the prefix via semanage from Dan Walsh.
- Fixed genhomedircon to find homedirs correctly.

* Tue May 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.15-1
- Updated version of policycoreutils
	* Merged po file updates from Dan Walsh.
- Fix semanage to be able to modify prefix in user record

* Mon Apr 30 2007 Dan Walsh <dwalsh@redhat.com> 2.0.14-2
- Fix title on system-config-selinux

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> 2.0.14-1
- Updated version of policycoreutils
	* Build fix for setsebool.

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> 2.0.13-1
- Updated version of policycoreutils
	* Merged setsebool patch to only use libsemanage for persistent boolean changes from Stephen Smalley.
	* Merged genhomedircon patch to use the __default__ setting from Dan Walsh.
	* Dropped -b option from load_policy in preparation for always preserving booleans across reloads in the kernel.

* Tue Apr 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.10-2
- Fixes for polgengui

* Tue Apr 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.10-1
- Updated version of policycoreutils
	* Merged chcat, fixfiles, genhomedircon, restorecond, and restorecon patches from Dan Walsh.

* Fri Apr 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-10
- Fix genhomedircon to handle non user_u for the default user

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-9
- More cleanups for gui

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-8
- Fix size and use_tmp problem on gui

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-7
- Fix restorecon crash

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-6
- Change polgengui to a druid

* Tue Apr 16 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-5
- Fully path script.py

* Mon Apr 16 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-4
- Add -l flag to restorecon to not traverse file systems

* Sat Apr 14 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-3
- Fixes for policygengui

* Fri Apr 13 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-2
- Add polgengui

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-1
- Updated version of sepolgen
	* Merged seobject setransRecords patch to return the first alias from Xavier Toth.

* Wed Apr 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.8-1
- Updated version of sepolgen
	* Merged updates to sepolgen-ifgen from Karl MacMillan.
	* Merged updates to sepolgen parser and tools from Karl MacMillan.
	  This includes improved debugging support, handling of interface 
	  calls with list parameters, support for role transition rules,
	  updated range transition rule support, and looser matching.

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-11
- Don't generate invalid context with genhomedircon

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-10
- Add filter to booleans page

* Tue Apr 3 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-9
- Fix polgen.py to not generate udp rules on tcp input

* Fri Mar 30 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-8
- system-config-selinux should be able to run on a disabled system,
- at least enough to get it enabled.

* Thu Mar 29 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-7
- Many fixes to polgengui

* Fri Mar 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-6
- Updated version of sepolgen
	* Merged patch to discard self from types when generating requires from Karl MacMillan.

* Fri Mar 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-5
- Change location of audit2allow and sepol-ifgen to sbin
- Updated version of sepolgen
	* Merged patch to move the sepolgen runtime data from /usr/share to /var/lib to facilitate a read-only /usr from Karl MacMillan.

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-4
- Add polgen gui
- Many fixes to system-config-selinux

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-3
- service restorecond status needs to set exit value correctly

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-2
- Fix gui

* Thu Mar 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-1
- Update to upstream
	* Merged restorecond init script LSB compliance patch from Steve Grubb.
  -sepolgen
	* Merged better matching for refpolicy style from Karl MacMillan
	* Merged support for extracting interface paramaters from interface calls from Karl MacMillan
	* Merged support for parsing USER_AVC audit messages from Karl MacMillan.

* Tue Feb 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.6-3
- Update to upstream
  -sepolgen
	* Merged support for enabling parser debugging from Karl MacMillan.
- Add sgrupp cleanup of restorcon init script

* Mon Feb 26 2007 Dan Walsh <dwalsh@redhat.com> 2.0.6-2
- Add Bill Nottinham patch to run restorcond condrestart in postun

* Fri Feb 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.6-1
- Update to upstream
  - policycoreutils
	* Merged newrole O_NONBLOCK fix from Linda Knippers.
	* Merged sepolgen and audit2allow patches to leave generated files 
	  in the current directory from Karl MacMillan.
	* Merged restorecond memory leak fix from Steve Grubb.
  -sepolgen
	* Merged patch to leave generated files (e.g. local.te) in current directory from Karl MacMillan.
	* Merged patch to make run-tests.py use unittest.main from Karl MacMillan.
	* Merged patch to update PLY from Karl MacMillan.
	* Merged patch to update the sepolgen parser to handle the latest reference policy from Karl MacMillan.

* Thu Feb 22 2007 Dan Walsh <dwalsh@redhat.com> 2.0.3-2
- Do not fail on sepolgen-ifgen

* Thu Feb 22 2007 Dan Walsh <dwalsh@redhat.com> 2.0.3-1
- Update to upstream
	* Merged translations update from Dan Walsh.
	* Merged chcat fixes from Dan Walsh.
	* Merged man page fixes from Dan Walsh.
	* Merged seobject prefix validity checking from Dan Walsh.
	* Merged Makefile and refparser.py patch from Dan Walsh.
	  Fixes PYTHONLIBDIR definition and error handling on interface files.

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.2-3
- Updated newrole NONBlOCK patch

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.2-2
- Remove Requires: %%{name}-plugins

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Update to upstream
	* Merged seobject exception handler fix from Caleb Case.
	* Merged setfiles memory leak patch from Todd Miller.

* Thu Feb 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.1-2
- Cleanup man pages syntax
- Add sepolgen

* Mon Feb 12 2007 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Update to upstream
	* Merged small fix to correct include of errcodes.h in semodule_deps from Dan Walsh.

* Wed Feb 7 2007 Dan Walsh <dwalsh@redhat.com> 2.0.0-1
- Update to upstream
	* Merged new audit2allow from Karl MacMillan.
	  This audit2allow depends on the new sepolgen python module.
	  Note that you must run the sepolgen-ifgen tool to generate
	  the data needed by audit2allow to generate refpolicy. 
	* Fixed newrole non-pam build.
- Fix Changelog and spelling error in man page

* Thu Feb 1 2007 Dan Walsh <dwalsh@redhat.com> 1.34.1-4
- Fix audit2allow on missing translations

* Wed Jan 24 2007 Dan Walsh <dwalsh@redhat.com> 1.34.1-3
- More chcat fixes

* Wed Jan 24 2007 Dan Walsh <dwalsh@redhat.com> 1.34.1-2
- Change chcat to exec semodule so file context is maintained

* Wed Jan 24 2007 Dan Walsh <dwalsh@redhat.com> 1.34.1-1
- Fix system-config-selinux ports view
- Update to upstream
	* Fixed newrole non-pam build.
	* Updated version for stable branch.

* Wed Jan 17 2007 Dan Walsh <dwalsh@redhat.com> 1.33.15-1
- Update to upstream
	* Merged unicode-to-string fix for seobject audit from Dan Walsh.
	* Merged man page updates to make "apropos selinux" work from Dan Walsh.
* Tue Jan 16 2007 Dan Walsh <dwalsh@redhat.com> 1.33.14-1
	* Merged newrole man page patch from Michael Thompson.
	* Merged patch to fix python unicode problem from Dan Walsh.

* Tue Jan 16 2007 Dan Walsh <dwalsh@redhat.com> 1.33.12-3
- Fix handling of audit messages for useradd change
Resolves: #222159

* Fri Jan 12 2007 Dan Walsh <dwalsh@redhat.com> 1.33.12-2
- Update man pages by adding SELinux to header to fix apropos database
Resolves: #217881

* Tue Jan 9 2007 Dan Walsh <dwalsh@redhat.com> 1.33.12-1
- Want to update to match api
- Update to upstream
	* Merged newrole securetty check from Dan Walsh.
	* Merged semodule patch to generalize list support from Karl MacMillan.
Resolves: #200110

* Tue Jan 9 2007 Dan Walsh <dwalsh@redhat.com> 1.33.11-1
- Update to upstream
	* Merged fixfiles and seobject fixes from Dan Walsh.
	* Merged semodule support for list of modules after -i from Karl MacMillan. 

* Tue Jan 9 2007 Dan Walsh <dwalsh@redhat.com> 1.33.10-1
- Update to upstream
	* Merged patch to correctly handle a failure during semanage handle
	  creation from Karl MacMillan.
	* Merged patch to fix seobject role modification from Dan Walsh.

* Fri Jan 5 2007 Dan Walsh <dwalsh@redhat.com> 1.33.8-2
- Stop newrole -l from working on non secure ttys
Resolves: #200110

* Thu Jan 4 2007 Dan Walsh <dwalsh@redhat.com> 1.33.8-1
- Update to upstream
	* Merged patches from Dan Walsh to:
	  - omit the optional name from audit2allow
	  - use the installed python version in the Makefiles
	  - re-open the tty with O_RDWR in newrole

* Wed Jan 3 2007 Dan Walsh <dwalsh@redhat.com> 1.33.7-1
- Update to upstream
	* Patch from Dan Walsh to correctly suppress warnings in load_policy.

* Tue Jan 2 2007 Dan Walsh <dwalsh@redhat.com> 1.33.6-9
- Fix fixfiles script to use tty command correctly.  If this command fails, it 
should set the LOGFILE to /dev/null
Resolves: #220879

* Wed Dec 20 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-8
- Remove hard coding of python2.4 from Makefiles

* Tue Dec 19 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-7
- add exists switch to semanage to tell it not to check for existance of Linux user
Resolves: #219421

* Mon Dec 18 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-6
- Fix audit2allow generating reference policy
- Fix semanage to manage user roles properly 
Resolves: #220071

* Fri Dec 8 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-5
- Update po files
- Fix newrole to open stdout and stderr rdrw so more will work on MLS machines
Resolves: #216920

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.33.6-4
- rebuild for python 2.5

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-3
- Update po files
Resolves: #216920

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-2
- Update po files
Resolves: #216920

* Wed Nov 29 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-1
- Update to upstream
	* Patch from Dan Walsh to add an pam_acct_msg call to run_init
	* Patch from Dan Walsh to fix error code returns in newrole
	* Patch from Dan Walsh to remove verbose flag from semanage man page
	* Patch from Dan Walsh to make audit2allow use refpolicy Makefile
	  in /usr/share/selinux/<SELINUXTYPE>
	
* Wed Nov 29 2006 Dan Walsh <dwalsh@redhat.com> 1.33.5-4
- Fixing the Makefile line again to build with LSPP support
Resolves: #208838

* Wed Nov 29 2006 Dan Walsh <dwalsh@redhat.com> 1.33.5-3
- Don't report errors on restorecond when file system does not support XATTRS
Resolves: #217694

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 1.33.5-2
- Fix -q qualifier on load_policy
Resolves: #214827

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 1.33.5-1
- Merge to upstream
- Fix makefile line
Resolves: #208838

* Fri Nov 24 2006 Dan Walsh <dwalsh@redhat.com> 1.33.4-2
- Additional po changes
- Added all booleans definitions

* Wed Nov 22 2006 Dan Walsh <dwalsh@redhat.com> 1.33.4-1
- Upstream accepted my patches
	* Merged setsebool patch from Karl MacMillan. 
	  This fixes a bug reported by Yuichi Nakamura with
	  always setting booleans persistently on an unmanaged system.

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 1.33.2-2
- Fixes for the gui

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 1.33.2-1
- Upstream accepted my patches

* Fri Nov 17 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-9
- Add Amy Grifis Patch to preserve newrole exit status

* Thu Nov 16 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-8
- Fix display of gui

* Thu Nov 16 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-7
- Add patch by Jose Plans to make run_init use pam_acct_mgmt

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-6
- More fixes to gui

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-5
- Fix audit2allow to generate referene policy

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-4
- Add group sort for portsPage.py
- Add enable/disableaudit to modules page

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-3
- Add glade file

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-2
- Fix Module handling in system-config-selinux

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-1
- Update to upstream
	* Merged newrole patch set from Michael Thompson.
- Add policycoreutils-gui

* Thu Nov 9 2006 Dan Walsh <dwalsh@redhat.com> 1.32-3
- No longer requires rhpl

* Fri Nov 6 2006 Dan Walsh <dwalsh@redhat.com> 1.32-2
- Fix genhomedircon man page

* Fri Oct 9 2006 Dan Walsh <dwalsh@redhat.com> 1.32-1
- Add newrole audit patch from sgrubb
- Update to upstream
	* Merged audit2allow -l fix from Yuichi Nakamura.
	* Merged restorecon -i and -o - support from Karl MacMillan.
	* Merged semanage/seobject fix from Dan Walsh.
	* Merged fixfiles -R and verify changes from Dan Walsh.

* Fri Oct 6 2006 Dan Walsh <dwalsh@redhat.com> 1.30.30-2
- Separate out newrole into its own package

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 1.30.30-1
- Update to upstream
	* Merged newrole auditing of failures due to user actions from
	  Michael Thompson.

* Tue Sep 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-6
- Pass -i qualifier to restorecon  for fixfiles -R
- Update translations
 
* Tue Sep 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-5
- Remove recursion from fixfiles -R calls
- Fix semanage to verify prefix

* Tue Sep 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-4
- More translations
- Compile with -pie

* Mon Sep 18 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-3
- Add translations
- Fix audit2allow -l

* Thu Sep 14 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-2
- Rebuild

* Thu Sep 14 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-1
- Update to upstream
- Change -o to take "-" for stdout

* Wed Sep 13 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-9
- Add -h support for genhomedircon

* Wed Sep 13 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-8
- Fix fixfiles handling of -o

* Mon Sep 11 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-7
- Make restorecon return the number of changes files if you use the -n flag

* Fri Sep 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-6
- Change setfiles and restorecon to use stderr except for -o flag
- Also -o flag will now output files
 
* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-5
- Put back Erich's change

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-4
- Remove recursive switch when using rpm

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-3
- Fix fixfiles to handle multiple rpm and make -o work

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-2
- Apply patch

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-1
- Security fixes to run python in a more locked down manner
- More Translations
- Update to upstream
	* Merged fix for restorecon // handling from Erich Schubert.
	* Merged translations update and fixfiles fix from Dan Walsh.

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-5
- Change scripts to use /usr/sbin/python

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-4
- Add -i qualified to restorecon to tell it to ignore files that do not exist
- Fixfiles also modified for this change

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-3
- Ignore sigpipe

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-2
- Fix init script and add translations

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-1
- Update to upstream
	* Merged fix for restorecon symlink handling from Erich Schubert.

* Sat Aug 12 2006 Dan Walsh <dwalsh@redhat.com> 1.30.26-1
- Update to upstream
	* Merged semanage local file contexts patch from Chris PeBenito.
- Fix fixfiles log creation
- More translations

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 1.30.25-1
- Update to upstream
	* Merged patch from Dan Walsh with:
	  * audit2allow: process MAC_POLICY_LOAD events
	  * newrole:  run shell with - prefix to start a login shell
	  * po:  po file updates
	  * restorecond:  bail if SELinux not enabled
	  * fixfiles: omit -q 
	  * genhomedircon:  fix exit code if non-root
	  * semodule_deps:  install man page
	* Merged secon Makefile fix from Joshua Brindle.
	* Merged netfilter contexts support patch from Chris PeBenito.

* Wed Aug 2 2006 Dan Walsh <dwalsh@redhat.com> 1.30.22-3
- Fix audit2allow to handle reload of policy

* Wed Aug 2 2006 Dan Walsh <dwalsh@redhat.com> 1.30.22-2
- Stop restorecond init script when selinux is not enabled

* Tue Aug 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.22-1
- Update to upstream
	* Merged restorecond size_t fix from Joshua Brindle.
	* Merged secon keycreate patch from Michael LeMay.
	* Merged restorecond fixes from Dan Walsh.
	  Merged updated po files from Dan Walsh.
	* Merged python gettext patch from Stephen Bennett.
	* Merged semodule_deps from Karl MacMillan.

* Thu Jul 27 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-7
- Change newrole to exec a login shell to prevent suspend.

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-6
- Report error when selinux not enabled in restorecond

* Tue Jul 18 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-5
- Fix handling of restorecond

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-4
- Fix creation of restorecond pidfile

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-3
- Update translations
- Update to new GCC

* Mon Jul 10 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-2
- Add verbose flag to restorecond and update translations

* Tue Jul 4 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-1
- Update to upstream
	* Lindent.
	* Merged patch from Dan Walsh with:
	  * -p option (progress) for setfiles and restorecon.
	  * disable context translation for setfiles and restorecon.
	  * on/off values for setsebool.
	* Merged setfiles and semodule_link fixes from Joshua Brindle.
	
* Thu Jun 22 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-5
- Add progress indicator on fixfiles/setfiles/restorecon

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-4
- Don't use translations with matchpathcon

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-3
- Prompt for selinux-policy-devel package in audit2allow

* Mon Jun 19 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-2
- Allow setsebool to use on/off
- Update translations

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-1
- Update to upstream
	* Merged fix for setsebool error path from Serge Hallyn.
	* Merged patch from Dan Walsh with:
	*    Updated po files.
	*    Fixes for genhomedircon and seobject.
	*    Audit message for mass relabel by setfiles.

* Tue Jun 13 2006 James Antill <jantill@redhat.com> 1.30.12-5
- Update audit mass relabel to only compile in when audit is installed.

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-4
- Update to required versions
- Update translation

* Wed Jun 7 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-3
- Fix shell selection

* Mon Jun 5 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-2
- Add BuildRequires for gettext

* Mon Jun 5 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-1
	* Updated fixfiles script for new setfiles location in /sbin.

* Tue May 30 2006 Dan Walsh <dwalsh@redhat.com> 1.30.11-1
- Update to upstream
	* Merged more translations from Dan Walsh.
	* Merged patch to relocate setfiles to /sbin for early relabel
	  when /usr might not be mounted from Dan Walsh.
	* Merged semanage/seobject patch to preserve fcontext ordering in list.
	* Merged secon patch from James Antill.

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-4
- Fix seobject.py to not sort the file_context file.
- move setfiles to /sbin

* Wed May 24 2006 James Antill <jantill@redhat.com> 1.30.10-3
- secon man page and getopt fixes.
- Enable mass relabel audit, even though it doesn't work.

* Wed May 24 2006 James Antill <jantill@redhat.com> 1.30.10-2
- secon fixes for --self-exec etc.
- secon change from level => sensitivity, add clearance.
- Add mass relabel AUDIT patch, but disable it until kernel problem solved.

* Tue May 24 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-1
- Update to upstream
	* Merged patch with updates to audit2allow, secon, genhomedircon,
	  and semanage from Dan Walsh.

* Sat May 20 2006 Dan Walsh <dwalsh@redhat.com> 1.30.9-4
- Fix exception in genhomedircon

* Mon May 15 2006 James Antill <jantill@redhat.com> 1.30.9-3
- Add rhpl dependancy

* Mon May 15 2006 James Antill <jantill@redhat.com> 1.30.9-2
- Add secon man page and prompt options.

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 1.30.9-1
- Update to upstream
	* Fixed audit2allow and po Makefiles for DESTDIR= builds.
	* Merged .po file patch from Dan Walsh.
	* Merged bug fix for genhomedircon.

* Wed May 10 2006 Dan Walsh <dwalsh@redhat.com> 1.30.8-2
- Fix exception on bad file_context

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.8-1
- Update to upstream
	* Merged fix warnings patch from Karl MacMillan.
	* Merged patch from Dan Walsh.
	  This includes audit2allow changes for analysis plugins,
	  internationalization support for several additional programs 
	  and added po files, some fixes for semanage, and several cleanups.
	  It also adds a new secon utility.

* Sun May 7 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-5
- Fix genhomedircon to catch duplicate homedir problem

* Thu May 4 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-4
- Add secon program
- Add translations

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-3
- Fix check for "msg"

* Mon Apr 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-2
- Ship avc.py

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-1
- Add /etc/samba/secrets.tdb to restorecond.conf
- Update from upstream
	* Merged semanage prefix support from Russell Coker.
	* Added a test to setfiles to check that the spec file is
	  a regular file.

* Thu Apr 06 2006 Karsten Hopp <karsten@redhat.de> 1.30.4-4
- added some missing buildrequires
- added Requires: initscripts for /sbin/service

* Thu Apr 06 2006 Karsten Hopp <karsten@redhat.de> 1.30.4-3
- use absolute path /sbin/service

* Wed Apr 5 2006 Dan Walsh <dwalsh@redhat.com> 1.30.4-2
- Fix audit2allow to not require ausearch.
- Fix man page
- Add libflashplayer to restorecond.conf

* Wed Mar 29 2006 Dan Walsh <dwalsh@redhat.com> 1.30.4-1
- Update from upstream
	* Merged audit2allow fixes for refpolicy from Dan Walsh.
	* Merged fixfiles patch from Dan Walsh.
	* Merged restorecond daemon from Dan Walsh.
	* Merged semanage non-MLS fixes from Chris PeBenito.
	* Merged semanage and semodule man page examples from Thomas Bleher.

* Tue Mar 28 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-4
- Clean up reference policy generation in audit2allow

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-3
- Add IN_MOVED_TO to catch renames

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-2
- make restorecond only ignore non directories with lnk > 1

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-1
- Make audit2allow translate dontaudit as well as allow rules
- Update from upstream
	* Merged semanage labeling prefix patch from Ivan Gyurdiev.

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30-5
- Fix audit2allow to retrieve dontaudit rules

* Mon Mar 20 2006 Dan Walsh <dwalsh@redhat.com> 1.30-4
- Open file descriptor to make sure file does not change from underneath.

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30-3
- Fixes for restorecond attack via symlinks
- Fixes for fixfiles

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30-2
- Restorecon has to handle suspend/resume

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30-1
- Update to upstream

* Fri Mar 10 2006 Dan Walsh <dwalsh@redhat.com> 1.29.27-1
- Add restorecond

* Fri Mar 10 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-6
- Remove prereq

* Mon Mar 6 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-5
- Fix audit2allow to generate all rules

* Fri Mar 3 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-4
- Minor fixes to chcat and semanage

* Sat Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-3
- Add missing setsebool man page

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-2
- Change audit2allow to use devel instead of refpolicy

* Mon Feb 20 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-1
- Update from upstream
	* Merged semanage bug fix patch from Ivan Gyurdiev.
	* Merged improve bindings patch from Ivan Gyurdiev.
	* Merged semanage usage patch from Ivan Gyurdiev.
	* Merged use PyList patch from Ivan Gyurdiev.

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 1.29.23-1
- Update from upstream
	* Merged newrole -V/--version support from Glauber de Oliveira Costa.
	* Merged genhomedircon prefix patch from Dan Walsh.
	* Merged optionals in base patch from Joshua Brindle.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.29.20-2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Dan Walsh <dwalsh@redhat.com> 1.29.20-2
- Fix auditing to semanage
- Change genhomedircon to use new prefix interface in libselinux

* Tue Feb 07 2006 Dan Walsh <dwalsh@redhat.com> 1.29.20-1
- Update from upstream
	* Merged seuser/user_extra support patch to semodule_package 
	  from Joshua Brindle.
	* Merged getopt type fix for semodule_link/expand and sestatus
	  from Chris PeBenito.
- Fix genhomedircon output

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.29.18-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 3 2006 Dan Walsh <dwalsh@redhat.com> 1.29.18-2
- Add auditing to semanage

* Thu Feb 2 2006 Dan Walsh <dwalsh@redhat.com> 1.29.18-1
- Update from upstream
	* Merged clone record on set_con patch from Ivan Gyurdiev.

* Mon Jan 30 2006 Dan Walsh <dwalsh@redhat.com> 1.29.17-1
- Update from upstream
	* Merged genhomedircon fix from Dan Walsh.
	* Merged seusers.system patch from Ivan Gyurdiev.
	* Merged improve port/fcontext API patch from Ivan Gyurdiev.
	* Merged genhomedircon patch from Dan Walsh.

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 1.29.15-1
- Update from upstream
	* Merged newrole audit patch from Steve Grubb.
	* Merged seuser -> seuser local rename patch from Ivan Gyurdiev.
	* Merged semanage and semodule access check patches from Joshua Brindle.
* Wed Jan 25 2006 Dan Walsh <dwalsh@redhat.com> 1.29.12-1
- Add a default of /export/home

* Wed Jan 25 2006 Dan Walsh <dwalsh@redhat.com> 1.29.11-3
- Cleanup of the patch

* Wed Jan 25 2006 Dan Walsh <dwalsh@redhat.com> 1.29.11-2
- Correct handling of symbolic links in restorecon

* Wed Jan 25 2006 Dan Walsh <dwalsh@redhat.com> 1.29.11-1
- Added translation support to semanage
- Update from upstream
	* Modified newrole and run_init to use the loginuid when
	  supported to obtain the Linux user identity to re-authenticate,
	  and to fall back to real uid.  Dropped the use of the SELinux
	  user identity, as Linux users are now mapped to SELinux users
	  via seusers and the SELinux user identity space is separate.
	* Merged semanage bug fixes from Ivan Gyurdiev.
	* Merged semanage fixes from Russell Coker.
	* Merged chcat.8 and genhomedircon patches from Dan Walsh.

* Thu Jan 19 2006 Dan Walsh <dwalsh@redhat.com> 1.29.9-2
- Fix genhomedircon to work on MLS policy

* Thu Jan 19 2006 Dan Walsh <dwalsh@redhat.com> 1.29.9-1
- Update to match NSA
	* Merged chcat, semanage, and setsebool patches from Dan Walsh.

* Thu Jan 19 2006 Dan Walsh <dwalsh@redhat.com> 1.29.8-4
- Fixes for "add"-"modify" error messages
- Fixes for chcat

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 1.29.8-3
- Add management of translation file to semaange and seobject

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 1.29.8-2
- Fix chcat -l -L to work while not root

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 1.29.8-1
- Update to match NSA
	* Merged semanage fixes from Ivan Gyurdiev.
	* Merged semanage fixes from Russell Coker.
	* Merged chcat, genhomedircon, and semanage diffs from Dan Walsh.

* Tue Jan 14 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-4
- Update chcat to manage user categories also

* Sat Jan 14 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-3
- Add check for root for semanage, genhomedircon 

* Sat Jan 14 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-2
- Add ivans patch

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-1
- Update to match NSA
	* Merged newrole cleanup patch from Steve Grubb.
	* Merged setfiles/restorecon performance patch from Russell Coker.
	* Merged genhomedircon and semanage patches from Dan Walsh.
	* Merged remove add_local/set_local patch from Ivan Gyurdiev.

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-3
- Fixes for mls policy

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-2
- Update semanage and split out seobject
- Fix labeleing of home_root

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-1
- Update to match NSA
	* Added filename to semodule error reporting.

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.29.4-1
- Update to match NSA
	* Merged genhomedircon and semanage patch from Dan Walsh.
	* Changed semodule error reporting to include argv[0].

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 1.29.3-1
- Update to match NSA
	* Merged semanage getpwnam bug fix from Serge Hallyn (IBM).
	* Merged patch series from Ivan Gyurdiev.
	  This includes patches to:
	  - cleanup setsebool
	  - update setsebool to apply active booleans through libsemanage
	  - update semodule to use the new semanage_set_rebuild() interface
	  - fix various bugs in semanage
	* Merged patch from Dan Walsh (Red Hat).
	  This includes fixes for restorecon, chcat, fixfiles, genhomedircon,
	  and semanage.

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 1.29.2-10
- Fix restorecon to not say it is changing user section when -vv is specified

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-9
- Fixes for semanage, patch from Ivan and added a test script

* Sat Dec 24 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-8
- Fix getpwnam call

* Fri Dec 23 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-7
- Anaconda fixes

* Thu Dec 22 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-6
- Turn off try catch block to debug anaconda failure

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-5
- More fixes for chcat

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-4
- Add try catch for files that may not exists
 
* Mon Dec 19 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-3
- Remove commands from genhomedircon for installer

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-1
- Fix genhomedircon to work in installer
- Update to match NSA
	* Merged patch for chcat script from Dan Walsh.

* Fri Dec 9 2005 Dan Walsh <dwalsh@redhat.com> 1.29.1-2
- More fixes to chcat

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 8 2005 Dan Walsh <dwalsh@redhat.com> 1.29.1-1
- Update to match NSA
	* Merged fix for audit2allow long option list from Dan Walsh.
	* Merged -r option for restorecon (alias for -R) from Dan Walsh.
	* Merged chcat script and man page from Dan Walsh.

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.28-1
- Update to match NSA
- Add gfs support

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.37-1
- Update to match NSA
- Add chcat to policycoreutils, adding +/- syntax
`
* Tue Dec 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.36-2
- Require new version of libsemanage

* Mon Dec 5 2005 Dan Walsh <dwalsh@redhat.com> 1.27.36-1
- Update to match NSA
	* Changed genhomedircon to warn on use of ROLE in homedir_template
	  if using managed policy, as libsemanage does not yet support it.

* Sun Dec 4 2005 Dan Walsh <dwalsh@redhat.com> 1.27.35-1
- Update to match NSA
	* Merged genhomedircon bug fix from Dan Walsh.
	* Revised semodule* man pages to refer to checkmodule and
	  to include example sections.

* Thu Dec 1 2005 Dan Walsh <dwalsh@redhat.com> 1.27.33-1
- Update to match NSA
	* Merged audit2allow --tefile and --fcfile support from Dan Walsh.
	* Merged genhomedircon fix from Dan Walsh.
	* Merged semodule* man pages from Dan Walsh, and edited them.
	* Changed setfiles to set the MATCHPATHCON_VALIDATE flag to
	  retain validation/canonicalization of contexts during init.

* Wed Nov 30 2005 Dan Walsh <dwalsh@redhat.com> 1.27.31-1
- Update to match NSA
	* Changed genhomedircon to always use user_r for the role in the
	  managed case since user_get_defrole is broken.
- Add te file capabilities to audit2allow
- Add man pages for semodule

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 1.27.30-1
- Update to match NSA
	* Merged sestatus, audit2allow, and semanage patch from Dan Walsh.
	* Fixed semodule -v option.

* Mon Nov 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.29-1
- Update to match NSA
	* Merged audit2allow python script from Dan Walsh.
	  (old script moved to audit2allow.perl, will be removed later).
	* Merged genhomedircon fixes from Dan Walsh.
	* Merged semodule quieting patch from Dan Walsh
	  (inverts default, use -v to restore original behavior).

* Thu Nov 17 2005 Dan Walsh <dwalsh@redhat.com> 1.27.28-3
- Audit2allow
	* Add more error checking
	* Add gen policy package
	* Add gen requires

* Wed Nov 16 2005 Dan Walsh <dwalsh@redhat.com> 1.27.28-2
- Update to match NSA
	* Merged genhomedircon rewrite from Dan Walsh.
- Rewrite audit2allow to python

* Mon Nov 14 2005 Dan Walsh <dwalsh@redhat.com> 1.27.27-5
- Fix genhomedircon to work with non libsemanage systems

* Fri Nov 11 2005 Dan Walsh <dwalsh@redhat.com> 1.27.27-3
- Patch genhomedircon to use libsemanage.py stuff

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 1.27.27-1
- Update to match NSA
	* Merged setsebool cleanup patch from Ivan Gyurdiev.

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 1.27.26-4
- Fix genhomedircon to use seusers file, temporary fix until swigified semanage

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.27.26-1
	* Added -B (--build) option to semodule to force a rebuild.
	* Reverted setsebool patch to call semanage_set_reload_bools().
	* Changed setsebool to disable policy reload and to call
	  security_set_boolean_list to update the runtime booleans.
	* Changed setfiles -c to use new flag to set_matchpathcon_flags()
	  to disable context translation by matchpathcon_init().

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.27.23-1
- Update to match NSA
	* Changed setfiles for the context canonicalization support.
	* Changed setsebool to call semanage_is_managed() interface
	  and fall back to security_set_boolean_list() if policy is
	  not managed.
	* Merged setsebool memory leak fix from Ivan Gyurdiev.
	* Merged setsebool patch to call semanage_set_reload_bools()
	  interface from Ivan Gyurdiev.

* Mon Nov 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.20-1
- Update to match NSA
	* Merged setsebool patch from Ivan Gyurdiev.
	  This moves setsebool from libselinux/utils to policycoreutils,
	  and rewrites it to use libsemanage for permanent boolean changes.

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.27.19-2
- Rebuild to use latest libselinux, libsemanage, and libsepol

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.27.19-1
- Update to match NSA
	* Merged semodule support for reload, noreload, and store options
	  from Joshua Brindle.
	* Merged semodule_package rewrite from Joshua Brindle.

* Thu Oct 20 2005 Dan Walsh <dwalsh@redhat.com> 1.27.18-1
- Update to match NSA
	* Cleaned up usage and error messages and releasing of memory by
   	  semodule_* utilities.
	* Corrected error reporting by semodule.
	* Updated semodule_expand for change to sepol interface.
	* Merged fixes for make DESTDIR= builds from Joshua Brindle.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.27.14-1
- Update to match NSA
	* Updated semodule_package for sepol interface changes.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.27.13-1
- Update to match NSA
	* Updated semodule_expand/link for sepol interface changes.

* Sat Oct 15 2005 Dan Walsh <dwalsh@redhat.com> 1.27.12-1
- Update to match NSA
	* Merged non-PAM Makefile support for newrole and run_init from Timothy Wood.

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 1.27.11-1
- Update to match NSA
	* Updated semodule_expand to use get interfaces for hidden sepol_module_package type.
	* Merged newrole and run_init pam config patches from Dan Walsh (Red Hat).
	* Merged fixfiles patch from Dan Walsh (Red Hat).
	* Updated semodule for removal of semanage_strerror.


* Thu Oct 13 2005 Dan Walsh <dwalsh@redhat.com> 1.27.7-2
- Fix run_init.pamd and spec file

* Wed Oct 12 2005 Dan Walsh <dwalsh@redhat.com> 1.27.7-1
- Update to match NSA
	* Updated semodule_link and semodule_expand to use shared libsepol.
	Fixed audit2why to call policydb_init prior to policydb_read (still
	uses the static libsepol).

* Mon Oct 10 2005 Dan Walsh <dwalsh@redhat.com> 1.27.6-1
- Update to match NSA
	* Updated for changes to libsepol. 
	Changed semodule and semodule_package to use the shared libsepol.
	Disabled build of semodule_link and semodule_expand for now.
	Updated audit2why for relocated policydb internal headers,
	still needs to be converted to a shared lib interface.

* Fri Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.5-3
- Update newrole pam file to remove pam-stack
- Update run_init pam file to remove pam-stack

* Thu Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.5-1
- Update to match NSA
	* Fixed warnings in load_policy.
	* Rewrote load_policy to use the new selinux_mkload_policy()
	interface provided by libselinux.

* Wed Oct 5 2005 Dan Walsh <dwalsh@redhat.com> 1.27.3-2
- Rebuild with newer libararies 

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.3-1
- Update to match NSA
	* Merged patch to update semodule to the new libsemanage API
	and improve the user interface from Karl MacMillan (Tresys).
	* Modified semodule for the create/connect API split.

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.2-2
- More fixes to stop find from following nfs paths

* Wed Sep 21 2005 Dan Walsh <dwalsh@redhat.com> 1.27.2-1
- Update to match NSA
	* Merged run_init open_init_pty bug fix from Manoj Srivastava
	  (unblock SIGCHLD).  Bug reported by Erich Schubert.

* Tue Sep 20 2005 Dan Walsh <dwalsh@redhat.com> 1.27.1-1
- Update to match NSA
	* Merged error shadowing bug fix for restorecon from Dan Walsh.
	* Merged setfiles usage/man page update for -r option from Dan Walsh.
	* Merged fixfiles -C patch to ignore :s0 addition on update
	  to a MCS/MLS policy from Dan Walsh.

* Thu Sep 15 2005 Dan Walsh <dwalsh@redhat.com> 1.26-3
- Add chcat script for use with chcon.

* Tue Sep 13 2005 Dan Walsh <dwalsh@redhat.com> 1.26-2
- Fix restorecon to exit with error code

* Mon Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.26-1
	* Updated version for release.

* Tue Sep 6 2005 Dan Walsh <dwalsh@redhat.com> 1.25.9-2
- Add prereq for mount command

* Thu Sep 1 2005 Dan Walsh <dwalsh@redhat.com> 1.25.9-1
- Update to match NSA
	* Changed setfiles -c to translate the context to raw format
	prior to calling libsepol.

* Fri Aug 26 2005 Dan Walsh <dwalsh@redhat.com> 1.25.7-3
- Use new version of libsemange and require it for install

* Fri Aug 26 2005 Dan Walsh <dwalsh@redhat.com> 1.25.7-2
- Ignore s0 in file context

* Thu Aug 25 2005 Dan Walsh <dwalsh@redhat.com> 1.25.7-1
- Update to match NSA
	* Merged patch for fixfiles -C from Dan Walsh.

* Tue Aug 23 2005 Dan Walsh <dwalsh@redhat.com> 1.25.6-1
- Update to match NSA
	* Merged fixes for semodule_link and sestatus from Serge Hallyn (IBM).
	  Bugs found by Coverity.

* Mon Aug 22 2005 Dan Walsh <dwalsh@redhat.com> 1.25.5-3
- Fix fixfiles to call sort -u followed by sort -d.

* Wed Aug 17 2005 Dan Walsh <dwalsh@redhat.com> 1.25.5-2
- Change fixfiles to ignore /home directory on updates

* Fri Aug 5 2005 Dan Walsh <dwalsh@redhat.com> 1.25.5-1
- Update to match NSA
	* Merged patch to move module read/write code from libsemanage
	  to libsepol from Jason Tang (Tresys).

* Thu Jul 28 2005 Dan Walsh <dwalsh@redhat.com> 1.25.4-1
- Update to match NSA
	* Changed semodule* to link with libsemanage.

* Wed Jul 27 2005 Dan Walsh <dwalsh@redhat.com> 1.25.3-1
- Update to match NSA
	* Merged restorecon patch from Ivan Gyurdiev.

* Mon Jul 18 2005 Dan Walsh <dwalsh@redhat.com> 1.25.2-1
- Update to match NSA
	* Merged load_policy, newrole, and genhomedircon patches from Red Hat.

* Thu Jul 7 2005 Dan Walsh <dwalsh@redhat.com> 1.25.1-1
- Update to match NSA
	* Merged loadable module support from Tresys Technology.

* Wed Jun 29 2005 Dan Walsh <dwalsh@redhat.com> 1.24-1
- Update to match NSA
	* Updated version for release.

* Tue Jun 14 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-4
- Fix Ivan's patch for user role changes 

* Sat May 28 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-3
- Add Ivan's patch for user role changes in genhomedircon

* Thu May 26 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-2
- Fix warning message on reload of booleans


* Fri May 20 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-1
- Update to match NSA
	* Merged fixfiles and newrole patch from Dan Walsh.
	* Merged audit2why man page from Dan Walsh.

* Thu May 19 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-2
- Add call to pam_acct_mgmt in newrole.

* Tue May 17 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-1
- Update to match NSA
	* Extended audit2why to incorporate booleans and local user 
	  settings when analyzing audit messages.

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 1.23.9-1
- Update to match NSA
	* Updated audit2why for sepol_ prefixes on Flask types to
	  avoid namespace collision with libselinux, and to 
	  include <selinux/selinux.h> now.

* Fri May 13 2005 Dan Walsh <dwalsh@redhat.com> 1.23.8-1
- Fix fixfiles to accept -f
- Update to match NSA
	* Added audit2why utility.

* Fri Apr 29 2005 Dan Walsh <dwalsh@redhat.com> 1.23.7-1
- Change -f flag in fixfiles to remove stuff from /tmp
- Change -F flag to pass -F flag  to restorecon/fixfiles.  (IE Force relabel).

* Thu Apr 14 2005 Dan Walsh <dwalsh@redhat.com> 1.23.6-1
- Update to match NSA
	* Fixed signed/unsigned pointer bug in load_policy.
	* Reverted context validation patch for genhomedircon.

* Wed Apr 13 2005 Dan Walsh <dwalsh@redhat.com> 1.23.5-1
- Update to match NSA
	* Reverted load_policy is_selinux_enabled patch from Dan Walsh.
	  Otherwise, an initial policy load cannot be performed using
	  load_policy, e.g. for anaconda.


* Mon Apr 11 2005 Dan Walsh <dwalsh@redhat.com> 1.23.4-3
- remove is_selinux_enabled check from load_policy  (Bad idea)

* Mon Apr 11 2005 Dan Walsh <dwalsh@redhat.com> 1.23.4-1
- Update to version from NSA
	* Merged load_policy is_selinux_enabled patch from Dan Walsh.
	* Merged restorecon verbose output patch from Dan Walsh.
	* Merged setfiles altroot patch from Chris PeBenito.

* Thu Apr 7 2005 Dan Walsh <dwalsh@redhat.com> 1.23.3-2
- Don't run load_policy on a non SELinux kernel.

* Wed Apr 6 2005 Dan Walsh <dwalsh@redhat.com> 1.23.3-1
- Update to version from NSA
        * Merged context validation patch for genhomedircon from Eric Paris.
- Fix verbose output of restorecon

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 1.23.2-1
- Update to version from NSA
	* Changed setfiles -c to call set_matchpathcon_flags(3) to
	  turn off processing of .homedirs and .local.

* Tue Mar 15 2005 Dan Walsh <dwalsh@redhat.com> 1.23.1-1
- Update to released version from NSA
	* Merged rewrite of genhomedircon by Eric Paris.
	* Changed fixfiles to relabel jfs since it now supports security xattrs
	  (as of 2.6.11).  Removed reiserfs until 2.6.12 is released with 
	  fixed support for reiserfs and selinux.

* Thu Mar 10 2005 Dan Walsh <dwalsh@redhat.com> 1.22-2
- Update to released version from NSA
- Patch genhomedircon to handle passwd in different places.

* Wed Mar 9 2005 Dan Walsh <dwalsh@redhat.com> 1.21.22-2
- Fix genhomedircon to not put bad userad error in file_contexts.homedir

* Tue Mar 8 2005 Dan Walsh <dwalsh@redhat.com> 1.21.22-1
- Cleanup error reporting

* Tue Mar 1 2005 Dan Walsh <dwalsh@redhat.com> 1.21.21-1
	* Merged load_policy and genhomedircon patch from Dan Walsh.

* Mon Feb 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.20-3
- Fix genhomedircon to add extr "\n"

* Fri Feb 24 2005 Dan Walsh <dwalsh@redhat.com> 1.21.20-2
- Fix genhomedircon to handle blank users

* Fri Feb 24 2005 Dan Walsh <dwalsh@redhat.com> 1.21.20-1
- Update to latest from NSA
- Add call to libsepol

* Thu Feb 23 2005 Dan Walsh <dwalsh@redhat.com> 1.21.19-4
- Fix genhomedircon to handle root 
- Fix fixfiles to better handle file system types

* Wed Feb 23 2005 Dan Walsh <dwalsh@redhat.com> 1.21.19-2
- Fix genhomedircon to handle spaces in SELINUXPOLICYTYPE

* Tue Feb 22 2005 Dan Walsh <dwalsh@redhat.com> 1.21.19-1
- Update to latest from NSA
        * Merged several fixes from Ulrich Drepper.

* Mon Feb 21 2005 Dan Walsh <dwalsh@redhat.com> 1.21.18-2
- Apply Uli patch
	* The Makefiles should use the -Wall option even if compiled in beehive
	* Add -W, too
	* use -Werror when used outside of beehive.  This could also be used unconditionally
	* setfiles/setfiles.c: fix resulting warning
	* restorecon/restorecon.c: Likewise
	* run_init/open_init_pty.c: argc hasn't been checked, the program would crash if
called without parameters.  ignore the return value of nice properly.
	* run_init: don't link with -ldl lutil
	* load_policy: that's the bad bug.  pointer to unsigned int is passed, size_t is
written to.  fails on 64-bit archs
	* sestatus: signed vs unsigned problem
	* newrole: don't link with -ldl

* Sat Feb 19 2005 Dan Walsh <dwalsh@redhat.com> 1.21.18-1
- Update to latest from NSA
	* Changed load_policy to fall back to the original policy upon
	  an error from sepol_genusers().

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.21.17-2
- Only restorecon on ext[23], reiser and xfs

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.21.17-1
- Update to latest from NSA
	* Merged new genhomedircon script from Dan Walsh.
	* Changed load_policy to call sepol_genusers().

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.21.15-9
- Remove Red Hat rhpl usage
- Add back in original syntax 
- Update man page to match new syntax

* Fri Feb 11 2005 Dan Walsh <dwalsh@redhat.com> 1.21.15-8
- Fix genhomedircon regular expression
- Fix exclude in restorecon 

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.21.15-5
- Trap failure on write 
- Rewrite genhomedircon to generate file_context.homedirs
- several passes

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.21.15-1
- Update from NSA
	* Changed relabel Makefile target to use restorecon.

* Wed Feb 9 2005 Dan Walsh <dwalsh@redhat.com> 1.21.14-1
- Update from NSA
	* Merged restorecon patch from Dan Walsh.

* Tue Feb 8 2005 Dan Walsh <dwalsh@redhat.com> 1.21.13-1
- Update from NSA
	* Merged further change to fixfiles -C from Dan Walsh.
	* Merged updated fixfiles script from Dan Walsh.
- Fix error handling of restorecon


* Mon Feb 7 2005 Dan Walsh <dwalsh@redhat.com> 1.21.12-2
- Fix sestatus for longer booleans

* Wed Feb 2 2005 Dan Walsh <dwalsh@redhat.com> 1.21.12-1
- More cleanup of fixfiles sed patch
	* Merged further patches for restorecon/setfiles -e and fixfiles -C. 

* Wed Feb 2 2005 Dan Walsh <dwalsh@redhat.com> 1.21.10-2
- More cleanup of fixfiles sed patch

* Mon Jan 31 2005 Dan Walsh <dwalsh@redhat.com> 1.21.10-1
- More cleanup of fixfiles sed patch
- Upgrade to latest from NSA
	* Merged patch for open_init_pty from Manoj Srivastava.

* Fri Jan 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.9-1
- More cleanup of sed patch
- Upgrade to latest from NSA
	* Merged updated fixfiles script from Dan Walsh.
	* Merged updated man page for fixfiles from Dan Walsh and re-added unzipped.
	* Reverted fixfiles patch for file_contexts.local; 
	  obsoleted by setfiles rewrite.
	* Merged error handling patch for restorecon from Dan Walsh.
	* Merged semi raw mode for open_init_pty helper from Manoj Srivastava.
	* Rewrote setfiles to use matchpathcon and the new interfaces
	  exported by libselinux (>= 1.21.5).


* Fri Jan 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.7-3
- Fix fixfiles patch
- Upgrade to latest from NSA
	* Prevent overflow of spec array in setfiles.
- Add diff comparason between file_contexts to fixfiles
- Allow restorecon to give an warning on file not found instead of exiting

* Thu Jan 27 2005 Dan Walsh <dwalsh@redhat.com> 1.21.5-1
- Upgrade to latest from NSA
	* Merged newrole -l support from Darrel Goeddel (TCS).
- Fix genhomedircon STARTING_UID

* Wed Jan 26 2005 Dan Walsh <dwalsh@redhat.com> 1.21.4-1
- Upgrade to latest from NSA
	* Merged fixfiles patch for file_contexts.local from Dan Walsh.

* Fri Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.21.3-2
- Temp file needs to be created in /etc/selinux/POLICYTYPE/contexts/files/ directory.

* Fri Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.21.3-1
- Upgrade to latest from NSA
	* Fixed restorecon to not treat errors from is_context_customizable()
	  as a customizable context.
	* Merged setfiles/restorecon patch to not reset user field unless
	  -F option is specified from Dan Walsh.
	* Merged open_init_pty helper for run_init from Manoj Srivastava.
	* Merged audit2allow and genhomedircon man pages from Manoj Srivastava.

* Fri Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-3
- Don't change user componant if it is all that changed unless forced.
- Change fixfiles to concatinate file_context.local for setfiles

* Thu Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-1
- Update to latest from NSA

* Mon Jan 10 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-2
- Fix restorecon segfault

* Mon Jan 3 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-1
- Update to latest from NSA
	* Merged fixfiles rewrite from Dan Walsh.
	* Merged restorecon patch from Dan Walsh.

* Mon Jan 3 2005 Dan Walsh <dwalsh@redhat.com> 1.19.3-1
- Update to latest from NSA
	* Merged fixfiles and restorecon patches from Dan Walsh.
	* Don't display change if only user part changed.

* Mon Jan 3 2005 Dan Walsh <dwalsh@redhat.com> 1.19.2-4
- Fix fixfiles handling of rpm
- Fix restorecon to not warn on symlinks unless -v -v 
- Fix output of verbose to show old context as well as new context

* Mon Dec 29 2004 Dan Walsh <dwalsh@redhat.com> 1.19.2-1
- Update to latest from NSA
	* Changed restorecon to ignore ENOENT errors from matchpathcon.
	* Merged nonls patch from Chris PeBenito.

* Mon Dec 20 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-1
- Update to latest from NSA
	* Removed fixfiles.cron.
	* Merged run_init.8 patch from Dan Walsh.

* Thu Nov 18 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-3
- Fix run_init.8 to refer to correct location of initrc_context

* Wed Nov 3 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-1
- Upgrade to latest from NSA

* Wed Oct 27 2004 Steve Grubb <sgrubb@redhat.com> 1.17.7-3
- Add code to sestatus to output the current policy from config file

* Fri Oct 22 2004 Dan Walsh <dwalsh@redhat.com> 1.17.7-2
- Patch audit2allow to return self and no brackets if only one rule

* Fri Oct 22 2004 Dan Walsh <dwalsh@redhat.com> 1.17.7-1
- Update to latest from NSA
- Eliminate fixfiles.cron

* Tue Oct 12 2004 Dan Walsh <dwalsh@redhat.com> 1.17.6-2
- Only run fixfiles.cron once a week, and eliminate null message

* Fri Oct 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.6-1
- Update with NSA
	* Added -l option to setfiles to log changes via syslog.
	* Merged -e option to setfiles to exclude directories.
	* Merged -R option to restorecon for recursive descent.
* Fri Oct 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-6
- Add -e (exclude directory) switch to setfiles 
- Add syslog to setfiles

* Fri Sep 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-5
- Add -R (recursive) switch to restorecon.

* Thu Sep 23 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-4
- Change to only display to terminal if tty is specified

* Tue Sep 21 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-3
- Only display to stdout if logfile not specified

* Mon Sep 9 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-2
- Add Steve Grubb patch to cleanup log files.

* Mon Aug 30 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-1
- Add optargs
- Update to match NSA

* Wed Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.4-1
- Add fix to get cdrom info from /proc/media in fixfiles.

* Wed Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-4
- Add Steve Grub patches for 
	* Fix fixfiles.cron MAILTO
	* Several problems in sestatus

* Wed Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-3
- Add -q (quiet) qualifier to load_policy to not report warnings

* Tue Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-2
- Add requires for libsepol >= 1.1.1

* Tue Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-1
- Update to latest from upstream

* Mon Aug 23 2004 Dan Walsh <dwalsh@redhat.com> 1.17.2-1
- Update to latest from upstream
- Includes Colin patch for verifying file_contexts

* Sun Aug 22 2004 Dan Walsh <dwalsh@redhat.com> 1.17.1-1
- Update to latest from upstream

* Mon Aug 16 2004 Dan Walsh <dwalsh@redhat.com> 1.15.7-1
- Update to latest from upstream

* Thu Aug 12 2004 Dan Walsh <dwalsh@redhat.com> 1.15.6-1
- Add Man page for load_policy

* Tue Aug 10 2004 Dan Walsh <dwalsh@redhat.com> 1.15.5-1
-  new version from NSA uses libsepol

* Mon Aug 2 2004 Dan Walsh <dwalsh@redhat.com> 1.15.3-2
- Fix genhomedircon join command

* Thu Jul 29 2004 Dan Walsh <dwalsh@redhat.com> 1.15.3-1
- Latest from NSA

* Mon Jul 26 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-4
- Change fixfiles to not change when running a check

* Tue Jul 20 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-3
- Fix restorecon getopt call to stop hang on IBM Arches

* Mon Jul 19 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-2
- Only mail files less than 100 lines from fixfiles.cron
- Add Russell's fix for genhomedircon

* Fri Jul 16 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-1
- Latest from NSA

* Thu Jul 8 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-2
- Add ro warnings 

* Thu Jul 8 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-1
- Latest from NSA
- Fix fixfiles.cron to delete outfile

* Tue Jul 6 2004 Dan Walsh <dwalsh@redhat.com> 1.14.1-2
- Fix fixfiles.cron to not run on non SELinux boxes
- Fix several problems in fixfiles and fixfiles.cron

* Wed Jun 30 2004 Dan Walsh <dwalsh@redhat.com> 1.14.1-1
- Update from NSA
- Add cron capability to fixfiles

* Fri Jun 25 2004 Dan Walsh <dwalsh@redhat.com> 1.13.4-1
- Update from NSA

* Thu Jun 24 2004 Dan Walsh <dwalsh@redhat.com> 1.13.3-2
- Fix fixfiles to handle no rpm file on relabel

* Wed Jun 23 2004 Dan Walsh <dwalsh@redhat.com> 1.13.3-1
- Update latest from NSA
- Add -o option to setfiles to save output of any files with incorrect context.

* Tue Jun 22 2004 Dan Walsh <dwalsh@redhat.com> 1.13.2-2
- Add rpm support to fixfiles
- Update restorecon to add file input support

* Fri Jun 18 2004 Dan Walsh <dwalsh@redhat.com> 1.13.2-1
- Update with NSA Latest

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jun 12 2004 Dan Walsh <dwalsh@redhat.com> 1.13.1-2
- Fix run_init to use policy formats

* Wed Jun 2 2004 Dan Walsh <dwalsh@redhat.com> 1.13.1-1
- Update from NSA

* Tue May 25 2004 Dan Walsh <dwalsh@redhat.com> 1.13-3
- Change location of file_context file

* Tue May 25 2004 Dan Walsh <dwalsh@redhat.com> 1.13-2
- Change to use /etc/sysconfig/selinux to determine location of policy files

* Fri May 21 2004 Dan Walsh <dwalsh@redhat.com> 1.13-1
- Update to latest from NSA
- Change fixfiles to prompt before deleteing /tmp files

* Tue May 18 2004 Dan Walsh <dwalsh@redhat.com> 1.12-2
- have restorecon ingnore <<none>>
- Hand matchpathcon the file status

* Thu May 14 2004 Dan Walsh <dwalsh@redhat.com> 1.12-1
- Update to match NSA

* Mon May 10 2004 Dan Walsh <dwalsh@redhat.com> 1.11-4
- Move location of log file to /var/tmp

* Mon May 10 2004 Dan Walsh <dwalsh@redhat.com> 1.11-3
- Better grep command for bind

* Fri May 7 2004 Dan Walsh <dwalsh@redhat.com> 1.11-2
- Eliminate bind and context mounts

* Wed May 5 2004 Dan Walsh <dwalsh@redhat.com> 1.11-1
- update to match NSA

* Wed Apr 28 2004 Dan Walsh <dwalsh@redhat.com> 1.10-4
- Log fixfiles to the /tmp directory

* Wed Apr 21 2004 Colin Walters <walters@redhat.com> 1.10-3
- Add patch to fall back to authenticating via uid if
  the current user's SELinux user identity is the default
  identity
- Add BuildRequires pam-devel

* Mon Apr 12 2004 Dan Walsh <dwalsh@redhat.com> 1.10-2
- Add man page, thanks to Richard Halley

* Thu Apr 8 2004 Dan Walsh <dwalsh@redhat.com> 1.10-1
- Upgrade to latest from NSA

* Fri Apr 2 2004 Dan Walsh <dwalsh@redhat.com> 1.9.2-1
- Update with latest from gentoo and NSA

* Thu Apr 1 2004 Dan Walsh <dwalsh@redhat.com> 1.9.1-1
- Check return codes in sestatus.c

* Mon Mar 29 2004 Dan Walsh <dwalsh@redhat.com> 1.9-19
- Fix sestatus to not double free
- Fix sestatus.conf to be unix format

* Mon Mar 29 2004 Dan Walsh <dwalsh@redhat.com> 1.9-18
- Warn on setfiles failure to relabel.

* Mon Mar 29 2004 Dan Walsh <dwalsh@redhat.com> 1.9-17
- Updated version of sestatus

* Mon Mar 29 2004 Dan Walsh <dwalsh@redhat.com> 1.9-16
- Fix fixfiles to checklabel properly

* Fri Mar 26 2004 Dan Walsh <dwalsh@redhat.com> 1.9-15
- add sestatus

* Thu Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1.9-14
- Change free call to freecon
- Cleanup

* Tue Mar 23 2004 Dan Walsh <dwalsh@redhat.com> 1.9-12
- Remove setfiles-assoc patch
- Fix restorecon to not crash on missing dir

* Thu Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-11
- Eliminate trailing / in restorecon

* Thu Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-10
- Add Verbosity check

* Thu Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-9
- Change restorecon to not follow symlinks.  It is too difficult and confusing
- to figure out the file context for the file pointed to by a symlink.

* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-8
- Fix restorecon
* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-7
- Read restorecon patch

* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-6
- Change genhomedircon to take POLICYSOURCEDIR from command line

* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-5
- Add checkselinux
- move fixfiles and restorecon to /sbin

* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-4
- Restore patch of genhomedircon

* Mon Mar 15 2004 Dan Walsh <dwalsh@redhat.com> 1.9-3
- Add setfiles-assoc patch to try to freeup memory use

* Mon Mar 15 2004 Dan Walsh <dwalsh@redhat.com> 1.9-2
- Add fixlabels

* Mon Mar 15 2004 Dan Walsh <dwalsh@redhat.com> 1.9-1
- Update to latest from NSA

* Wed Mar 10 2004 Dan Walsh <dwalsh@redhat.com> 1.6-8
- Increase the size of buffer accepted by setfiles to BUFSIZ.

* Tue Mar 9 2004 Dan Walsh <dwalsh@redhat.com> 1.6-7
- genhomedircon should complete even if it can't read /etc/default/useradd

* Tue Mar 9 2004 Dan Walsh <dwalsh@redhat.com> 1.6-6
- fix restorecon to relabel unlabled files.

* Fri Mar 5 2004 Dan Walsh <dwalsh@redhat.com> 1.6-5
- Add genhomedircon from tresys
- Fixed patch for restorecon

* Thu Feb 26 2004 Dan Walsh <dwalsh@redhat.com> 1.6-4
- exit out when selinux is not enabled

* Thu Feb 26 2004 Dan Walsh <dwalsh@redhat.com> 1.6-3
- Fix minor bugs in restorecon

* Thu Feb 26 2004 Dan Walsh <dwalsh@redhat.com> 1.6-2
- Add restorecon c program 

* Tue Feb 24 2004 Dan Walsh <dwalsh@redhat.com> 1.6-1
- Update to latest tarball from NSA

* Thu Feb 19 2004 Dan Walsh <dwalsh@redhat.com> 1.4-9
- Add sort patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Dan Walsh <dwalsh@redhat.com> 1.4-7
- remove mods to run_init since init scripts don't require it anymore

* Wed Jan 28 2004 Dan Walsh <dwalsh@redhat.com> 1.4-6
- fix genhomedircon not to return and error 

* Wed Jan 28 2004 Dan Walsh <dwalsh@redhat.com> 1.4-5
- add setfiles quiet patch

* Tue Jan 27 2004 Dan Walsh <dwalsh@redhat.com> 1.4-4
- add checkcon to verify context match file_context

* Wed Jan 7 2004 Dan Walsh <dwalsh@redhat.com> 1.4-3
- fix command parsing restorecon

* Tue Jan 6 2004 Dan Walsh <dwalsh@redhat.com> 1.4-2
- Add restorecon

* Sat Dec 6 2003 Dan Walsh <dwalsh@redhat.com> 1.4-1
- Update to latest NSA 1.4

* Tue Nov 25 2003 Dan Walsh <dwalsh@redhat.com> 1.2-9
- Change run_init.console to run as run_init_t

* Tue Oct 14 2003 Dan Walsh <dwalsh@redhat.com> 1.2-8
- Remove dietcc since load_policy is not in mkinitrd
- Change to use CONSOLEHELPER flag

* Tue Oct 14 2003 Dan Walsh <dwalsh@redhat.com> 1.2-7
- Don't authenticate run_init when used with consolehelper

* Wed Oct 01 2003 Dan Walsh <dwalsh@redhat.com> 1.2-6
- Add run_init consolehelper link

* Wed Sep 24 2003 Dan Walsh <dwalsh@redhat.com> 1.2-5
- Add russell spead up patch to deal with file path stems

* Fri Sep 12 2003 Dan Walsh <dwalsh@redhat.com> 1.2-4
- Build load_policy with diet gcc in order to save space on initrd

* Fri Sep 12 2003 Dan Walsh <dwalsh@redhat.com> 1.2-3
- Update with NSA latest

* Thu Aug 7 2003 Dan Walsh <dwalsh@redhat.com> 1.2-1
- remove i18n
- Temp remove gtk support

* Thu Aug 7 2003 Dan Walsh <dwalsh@redhat.com> 1.1-4
- Remove wnck requirement

* Thu Aug 7 2003 Dan Walsh <dwalsh@redhat.com> 1.1-3
- Add gtk support to run_init

* Tue Aug 5 2003 Dan Walsh <dwalsh@redhat.com> 1.1-2
- Add internationalization

* Mon Jun 2 2003 Dan Walsh <dwalsh@redhat.com> 1.0-1
- Initial version


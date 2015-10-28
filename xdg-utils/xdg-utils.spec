
%define pre rc3

Summary: Basic desktop integration functions 
Name:    xdg-utils
Version: 1.1.0
Release: 0.41.%{pre}%{?dist}

URL:     http://portland.freedesktop.org/ 
%if 0%{?pre:1}
Source0: http://people.freedesktop.org/~rdieter/xdg-utils/xdg-utils-%{version}%{?pre:-%{pre}}.tar.gz
Source1: xdg-utils-git_checkout.sh
%else
Source0: http://portland.freedesktop.org/download/xdg-utils-%{version}%{?pre:-%{pre}}.tar.gz
%endif
License: MIT 

## upstream patches
Patch1: 0001-xdg-screensaver-should-control-X11-s-screensaver-in-.patch
Patch2: 0002-xdg-open-command-injection-vulnerability-BR66670.patch
Patch3: 0003-xdg-mime-dereference-symlinks-when-using-mimetype-or.patch
Patch4: 0004-xdg-screensaver-Change-screensaver_freedesktop-s-int.patch
Patch5: 0005-xdg-open-better-fix-for-command-injection-vulnerabil.patch
Patch6: 0006-xdg-open-Improve-performance-of-get_key-function.patch
Patch7: 0007-Add-changelog-for-prior-commit.patch
Patch8: 0008-xdg-open-safer-xdg-open-BR89130.patch
Patch9: 0009-one-more-s-arg-target-rename-fix-for-prior-commit.patch
Patch10: 0010-xdg-mime-do-not-report-multiple-desktop-files-BR6032.patch
Patch11: 0011-add-ChangeLog-entry-for-previous-commit.patch

# make sure BuildArch comes *after* patches, to ensure %%autosetup works right
# http://bugzilla.redhat.com/1084309
BuildArch: noarch

BuildRequires: gawk
BuildRequires: xmlto text-www-browser

Requires: coreutils
Requires: desktop-file-utils
Requires: which

%description
The %{name} package is a set of simple scripts that provide basic
desktop integration functions for any Free Desktop, such as Linux.
They are intended to provide a set of defacto standards.  
This means that:
*  Third party software developers can rely on these xdg-utils
   for all of their simple integration needs.
*  Developers of desktop environments can make sure that their
   environments are well supported
*  Distribution vendors can provide custom versions of these utilities

The following scripts are provided at this time:
* xdg-desktop-icon      Install icons to the desktop
* xdg-desktop-menu      Install desktop menu items
* xdg-email             Send mail using the user's preferred e-mail composer
* xdg-icon-resource     Install icon resources
* xdg-mime              Query information about file type handling and
                        install descriptions for new file types
* xdg-open              Open a file or URL in the user's preferred application
* xdg-screensaver       Control the screensaver
* xdg-settings          Get various settings from the desktop environment


%prep
%autosetup -n %{name}-%{version}%{?pre:-%{pre}} -p1


%build
%configure

%if 0%{?snap:1}
make scripts-clean -C scripts 
make man scripts %{?_smp_mflags} -C scripts
%endif
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc ChangeLog LICENSE README TODO
%{_bindir}/xdg-desktop-icon
%{_bindir}/xdg-desktop-menu
%{_bindir}/xdg-email
%{_bindir}/xdg-icon-resource
%{_bindir}/xdg-mime
%{_bindir}/xdg-open
%{_bindir}/xdg-screensaver
%{_bindir}/xdg-settings
%{_mandir}/man1/xdg-desktop-icon.1*
%{_mandir}/man1/xdg-desktop-menu.1*
%{_mandir}/man1/xdg-email.1*
%{_mandir}/man1/xdg-icon-resource.1*
%{_mandir}/man1/xdg-mime.1*
%{_mandir}/man1/xdg-open.1*
%{_mandir}/man1/xdg-screensaver.1*
%{_mandir}/man1/xdg-settings.1*


%changelog
* Sat Oct 24 2015 builder - 1.1.0-0.41.rc3
- Rebuild for new 4.0 release.


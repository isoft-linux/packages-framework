Summary: Utilities for manipulating .desktop files
Name: desktop-file-utils
Version: 0.22
Release: 3
URL: http://www.freedesktop.org/software/desktop-file-utils
Source0: %{name}-%{version}.tar.xz
License: GPL
Group: Development/Tools
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: glib2-devel >= 2.12.0

Obsoletes: desktop-file-validator

Patch0: desktop-file-utils-0.12-make-vendor-optional.patch
Patch1:	desktop-file-utils-0.12-add-more-category.patch
%description
.desktop files are used to describe an application for inclusion in
GNOME or KDE menus.  This package contains desktop-file-validate which
checks whether a .desktop file complies with the specification at
http://www.freedesktop.org/standards/, and desktop-file-install 
which installs a desktop file to the standard directory, optionally 
fixing it up in the process.

%prep
%setup -q
%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post

%preun

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


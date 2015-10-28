Name:           gphoto2
Version:        2.5.8
Release:        2
Summary:        Software for accessing digital cameras
License:        GPLv2+
Url:            http://www.gphoto.org/
Source0:        http://downloads.sourceforge.net/gphoto/%{name}-%{version}.tar.bz2

BuildRequires:  libgphoto2-devel >= %{version}, gettext
BuildRequires:  libjpeg-devel, readline-devel
BuildRequires:  libtool
BuildRequires:  libltdl-devel, popt-devel
BuildRequires:  libexif-devel

%description
The gPhoto2 project is a universal, free application and library
framework that lets you download images from several different
digital camera models, including the newer models with USB
connections. Note that
a) for some older camera models you must use the old "gphoto" package.
b) for USB mass storage models you must use the driver in the kernel

This package contains the command-line utility gphoto2.

Other (GUI) frontends are available separately.


%prep
%setup -q 


%build
%configure
make %{?_smp_mflags}


%install
%make_install INSTALL="install -p"
rm $RPM_BUILD_ROOT%{_docdir}/%{name}/test-hook.sh
%find_lang %{name}


%files -f %{name}.lang
%{_bindir}/gphoto2
%{_mandir}/man1/gphoto2.1*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.5.8-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


Name:           libfprint
Version:        0.6.0
Release:        2
Summary:        Toolkit for fingerprint scanner

License:        LGPLv2+
URL:            http://www.freedesktop.org/wiki/Software/fprint/libfprint
# git://anongit.freedesktop.org/libfprint/libfprint
Source0: libfprint.tar.gz

#Source0:        http://freedesktop.org/~hadess/%{name}-%{version}.tar.xz

BuildRequires:  libusb-devel glib2-devel gtk2-devel nss-devel
BuildRequires:  doxygen autoconf automake libtool

%description
libfprint offers support for consumer fingerprint reader devices.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name} 

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure --disable-static 
make %{?_smp_mflags}
pushd doc
make docs
popd

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_prefix}/lib/udev/rules.d/60-fprint-autosuspend.rules

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.6.0-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


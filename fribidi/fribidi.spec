Summary: Library implementing the Unicode Bidirectional Algorithm
Name: fribidi
Version: 0.19.6
Release: 1
URL: http://fribidi.org
Source: http://fribidi.org/download/%{name}-%{version}.tar.bz2
License: LGPLv2+ and UCD
Group: System Environment/Libraries

%description
A library to handle bidirectional scripts (for example Hebrew, Arabic),
so that the display is done in the proper way; while the text data itself
is always written in logical order.

%package devel
Summary: Libraries and include files for FriBidi
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Include files and libraries needed for developing applications which use
FriBidi.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install INSTALL="install -p"

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README AUTHORS COPYING ChangeLog THANKS NEWS TODO
%{_bindir}/fribidi
%{_libdir}/libfribidi.so.*

%files devel
%{_includedir}/fribidi
%{_libdir}/libfribidi.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/%{name}_*.gz

%changelog

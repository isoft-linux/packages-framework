%global apiver 1.0
%define cairover 1.10.0

Summary:          C++ API for the cairo graphics library
Name:             cairomm
Version:          1.11.2
Release:          1 
URL:              http://www.cairographics.org
License:          LGPLv2+
Group:            System Environment/Libraries
Source:           http://www.cairographics.org/releases/%{name}-%{version}.tar.gz
BuildRequires:    cairo-devel >= %{cairover}
BuildRequires:    pkgconfig
BuildRequires:    libsigc++-devel

%description
Cairomm is the C++ API for the cairo graphics library. It offers all the power
of cairo with an interface familiar to C++ developers, including use of the 
Standard Template Library where it makes sense.

%package        devel
Summary:        Headers for developing programs that will use %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       cairo-devel >= %{cairover}
Requires:       libsigc++-devel

%description    devel
Cairomm is the C++ API for the cairo graphics library. It offers all the power
of cairo with an interface familiar to C++ developers, including use of the 
Standard Template Library where it makes sense.

This package contains the libraries and header files needed for
developing %{name} applications.

%package        doc
Summary:        Developer's documentation for the cairomm library
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       libsigc++-doc

%description      doc
This package contains developer's documentation for the cairomm
library. Cairomm is the C++ API for the cairo graphics library.

The documentation can be viewed either through the devhelp
documentation browser or through a web browser.

If using a web browser the documentation is installed in the gtk-doc
hierarchy and can be found at /usr/share/doc/cairomm-1.0

%prep
%setup -q 

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rpmclean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README NEWS
%{_libdir}/lib*.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiver}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/%{name}-%{apiver}

%files doc
%doc %{_datadir}/doc/%{name}-%{apiver}/
%doc %{_datadir}/devhelp/

%changelog

Name:       ibus-qt
Version:    1.3.3
Release:    10
Summary:    Qt IBus library and Qt input method plugin
License:    GPLv2+
URL:        http://code.google.com/p/ibus/
Source0:    https://github.com/ibus/ibus-qt/releases/download/%{version}/%{name}-%{version}-Source.tar.gz

BuildRequires:  cmake
BuildRequires:  qt4-devel
BuildRequires:  dbus-devel
BuildRequires:  ibus-devel
BuildRequires:  libicu-devel
BuildRequires:  doxygen
Requires:       ibus

%description
Qt IBus library and Qt input method plugin.

%package devel
Summary:    Development tools for ibus qt
Requires:   %{name} = %{version}-%{release}

%description devel
The ibus-qt-devel package contains the header files for ibus qt library.

%package docs
Summary:    Development documents for ibus qt
Requires:   %{name} = %{version}-%{release}

%description docs
The ibus-qt-docs package contains developer documentation for ibus qt library.

%prep
%setup -q -n %{name}-%{version}-Source
# %%patch0 -p1

%build
export PATH=/usr/lib/qt4/bin:$PATH

%cmake \
    -DCMAKE_INSTALL_PREFIX=%{_usr} \
    -DLIBDIR=%{_libdir}

make \
    VERBOSE=1 \
    C_DEFINES="$RPM_OPT_FLAGS" \
    CXX_DEFINES="$RPM_OPT_FLAGS" \
    %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# -f {name}.lang
%doc AUTHORS README INSTALL
%{_libdir}/libibus-qt.so.*
%{_libdir}/qt4/plugins/inputmethods/libqtim-ibus.so

%files devel
%{_includedir}/*
%{_libdir}/libibus-qt.so

%changelog
* Fri Dec 16 2016 sulit - 1.3.3-10
- rebuild ibus-qt

* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 1.3.3-9
- Rebuild with icu 56.1

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.3.3-8
- Rebuild for new 4.0 release.


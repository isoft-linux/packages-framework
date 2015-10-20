Name:       opencc
Version:    1.0.2
Release:    4%{?dist}
Summary:    Libraries for Simplified-Traditional Chinese Conversion
License:    ASL 2.0
Group:      System Environment/Libraries
URL:        https://github.com/BYVoid/OpenCC
# Source URL: https://github.com/BYVoid/OpenCC/archive/ver.%{version}.tar.gz
Source0:    OpenCC-ver.%{version}.tar.gz
Patch1:     opencc-fixes-cmake.patch

BuildRequires:  gettext
BuildRequires:  cmake
BuildRequires:  doxygen

%description
OpenCC is a library for converting characters and phrases between
Traditional Chinese and Simplified Chinese.

%package doc
Summary:    Documentation for OpenCC
Group:      Applications/Text
Requires:   %{name} = %{version}-%{release}

%description doc
Doxygen generated documentation for OpenCC.


%package tools
Summary:    Command line tools for OpenCC
Group:      Applications/Text
Requires:   %{name} = %{version}-%{release}

%description tools
Command line tools for OpenCC, including tools for conversion via CLI and
for building dictionaries.


%package devel
Summary:    Development files for OpenCC
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n OpenCC-ver.%{version}
%patch1 -p1 -b .cmake

%build
%cmake . -DENABLE_GETTEXT:BOOL=ON -DBUILD_DOCUMENTATION:BOOL=ON
make VERBOSE=1 %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%check
ctest

#%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS LICENSE README.md
%{_libdir}/lib*.so.*
%{_datadir}/opencc/
%exclude %{_datadir}/opencc/doc

%files doc
%{_datadir}/opencc/doc

%files tools
%{_bindir}/*
#%{_datadir}/man/man1/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog

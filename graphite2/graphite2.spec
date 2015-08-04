Name:           graphite2
Version:        1.2.4
Release:        1
Summary:        Font rendering capabilities for complex non-Roman writing systems
Group:          Development/Tools

License:        LGPLv2+ and (Netscape or GPLv2 or LGPLv2)
URL:            http://sourceforge.net/projects/silgraphite/
Source0:        http://downloads.sourceforge.net/silgraphite/graphite2-%{version}.tgz
Patch1:         graphite2-1.2.0-cmakepath.patch

BuildRequires:  cmake
BuildRequires:  freetype-devel

Obsoletes:      silgraphite < 2.3.1-5

%description
Graphite2 is a project within SILs Non-Roman Script Initiative and Language
Software Development groups to provide rendering capabilities for complex
non-Roman writing systems. Graphite can be used to create smart fonts capable
of displaying writing systems with various complex behaviors. With respect to
the Text Encoding Model, Graphite handles the "Rendering" aspect of writing
system implementation.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Files for developing with graphite2
Group: Development/Libraries

Obsoletes: silgraphite-devel < 2.3.1-5

%description devel
Includes and definitions for developing with graphite2.

%prep
%setup -q
%patch1 -p1 -b .cmake

%build
%cmake -DGRAPHITE2_COMPARE_RENDERER=OFF .
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

rpmclean
%check
ctest

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/gr2fonttest
%{_libdir}/libgraphite2.so.3.0.1
%{_libdir}/libgraphite2.so.3

%files devel
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/graphite2-release.cmake
%{_libdir}/%{name}/graphite2.cmake
%{_includedir}/%{name}
%{_libdir}/libgraphite2.so
%{_libdir}/pkgconfig/graphite2.pc

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


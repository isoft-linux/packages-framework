Name:           vala
Version:        0.30.0
Release:        2
Summary:        A modern programming language for GNOME

# Most files are LGPLv2.1+, curses.vapi is 2-clause BSD
License:        LGPLv2+ and BSD
URL:            http://live.gnome.org/Vala
Source0:        http://download.gnome.org/sources/vala/0.7/vala-%{version}.tar.xz

BuildRequires:  flex bison

%description
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

valac, the Vala compiler, is a self-hosting compiler that translates
Vala source code into C source and header files. It uses the GObject
type system to create classes and interfaces declared in the Vala source
code. It's also planned to generate GIDL files when gobject-
introspection is ready.

The syntax of Vala is similar to C#, modified to better fit the GObject
type system.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

This package contains development files for %{name}. This is not necessary for
using the %{name} compiler.


%package        tools
Summary:        Tools for creating projects and bindings for %{name}
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-vapigen = %{version}-%{release}
Obsoletes:      %{name}-vapigen < %{version}-%{release}

%description    tools
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

This package contains tools to generate Vala projects, as well as API bindings
from existing C libraries, allowing access from Vala programs.


%package        doc
Summary:        Documentation for %{name}
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-docs = %{version}-%{release}
Obsoletes:      %{name}-docs < %{version}-%{release}


%description    doc
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.

This package contains documentation in a devhelp HTML book.



%prep
%setup -q

%build
%configure --enable-vapigen
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`/codegen/.libs
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/libvala*.la

%check
#set LD_LIBRARY_PATH to use libvala in this package.
LD_LIBRARY_PATH=`pwd`/codegen/.libs make check ||:


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/vala*
%{_datadir}/vala*
%{_libdir}/libvala*.so.*
%{_mandir}/*/valac*

%files devel
%defattr(-,root,root,-)
%{_includedir}/vala-*
%{_libdir}/libvala*.so
%{_libdir}/pkgconfig/libvala*.pc
%{_datadir}/pkgconfig/*.pc
%{_datadir}/aclocal/*

%files tools
%defattr(-,root,root,-)
%{_bindir}/*gen*
%{_bindir}/vapicheck*
%{_libdir}/vala*
%{_mandir}/*/*gen*

%files doc
%defattr(-,root,root,-)
%{_datadir}/devhelp/books/vala*



%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.30.0-2
- Rebuild for new 4.0 release.

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


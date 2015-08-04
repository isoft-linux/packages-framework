Name:           luajit
Version:        2.0.4
Release:        2%{?dist}
Summary:        Just-In-Time Compiler for Lua
License:        MIT
URL:            http://luajit.org/
Source0:        http://luajit.org/download/LuaJIT-%{version}.tar.gz

%description
LuaJIT implements the full set of language features defined by Lua 5.1.
The virtual machine (VM) is API- and ABI-compatible to the standard
Lua interpreter and can be deployed as a drop-in replacement.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q -n LuaJIT-%{version}
echo '#!/bin/sh' > ./configure
chmod +x ./configure

# preserve timestamps (cicku)
sed -i -e '/install -m/s/-m/-p -m/' Makefile

%build
%configure
# Q= - enable verbose output
# E= @: - disable @echo messages
# NOTE: we use amalgamated build as per documentation suggestion doc/install.html
make amalg Q= E=@: PREFIX=%{_prefix} TARGET_STRIP=: \
           CFLAGS="%{optflags}" \
           %{?_smp_mflags}

%install
# PREREL= - disable -betaX suffix
# INSTALL_TNAME - executable name
%make_install PREFIX=%{_prefix} LDCONFIG="/sbin/ldconfig -n"

rm -rf _tmp_html ; mkdir _tmp_html
cp -a doc _tmp_html/html

# Remove static .a
find %{buildroot} -type f -name *.a -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README
%{_bindir}/%{name}
%{_bindir}/%{name}-%{version}
%{_libdir}/libluajit*.so.*
%{_mandir}/man1/luajit*
%{_datadir}/%{name}-%{version}/

%files devel
%doc _tmp_html/html/
%{_includedir}/luajit-2.0/
%{_libdir}/libluajit*.so
%{_libdir}/pkgconfig/*.pc

%changelog

Name:           libssh
Version:        0.7.0
Release:        4
Summary:        A library implementing the SSH protocol
License:        LGPLv2+
URL:            http://www.libssh.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        https://red.libssh.org/attachments/download/140/libssh-0.7.0.tar.xz
Patch0:         https://red.libssh.org/attachments/download/143/0001-Reintroduce-ssh_forward_listen-Fixes-194.patch

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel

%description
The ssh library was designed to be used by programmers needing a working SSH
implementation by the mean of a library. The complete control of the client is
made by the programmer. With libssh, you can remotely execute programs, transfer
files, use a secure and transparent tunnel for your remote programs. With its
Secure FTP implementation, you can play with remote files easily, without
third-party programs others than libcrypto (from openssl).

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       cmake

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%setup -q
%patch0 -p1
# Remove examples, they are not packaged and do not build on EPEL 5
sed -i -e 's|add_subdirectory(examples)||g' CMakeLists.txt
rm -rf examples

%build
if test ! -e "obj"; then
  mkdir obj
fi
pushd obj

%cmake \
    %{_builddir}/%{name}-%{version}
make %{?_smp_mflags} VERBOSE=1
make doc

popd

%install
pushd obj
make DESTDIR=%{buildroot} install
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%doc AUTHORS BSD ChangeLog COPYING README
%{_libdir}/libssh.so.*
%{_libdir}/libssh_threads.so.*

%files devel
%doc obj/doc/html
%{_includedir}/libssh/callbacks.h
%{_includedir}/libssh/legacy.h
%{_includedir}/libssh/libssh.h
%{_includedir}/libssh/libsshpp.hpp
%{_includedir}/libssh/server.h
%{_includedir}/libssh/sftp.h
%{_includedir}/libssh/ssh2.h
%dir  %{_libdir}/cmake/libssh
%{_libdir}/cmake/libssh/libssh-config-version.cmake
%{_libdir}/cmake/libssh/libssh-config.cmake
%{_libdir}/pkgconfig/libssh.pc
%{_libdir}/pkgconfig/libssh_threads.pc
%{_libdir}/libssh.so
%{_libdir}/libssh_threads.so

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.7.0-4
- Rebuild for new 4.0 release.


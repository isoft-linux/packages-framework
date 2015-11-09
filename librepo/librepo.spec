%global gitrev d9bed0d
# gitrev is output of: git rev-parse --short HEAD

%if 0
# Do not build bindings for python3 for RHEL <= 7
%bcond_with python3
# python-flask is not in RHEL7
%bcond_with tests
%else
%bcond_without python3
# %bcond_without tests
%endif

Name:           librepo
Version:        1.7.16
Release:        4
Summary:        Repodata downloading library

License:        LGPLv2+
URL:            https://github.com/Tojaj/librepo
# Use the following commands to generate the tarball:
#  git clone https://github.com/Tojaj/librepo.git
#  cd librepo
#  utils/make_tarball.sh %{gitrev}
Source0:        librepo-%{gitrev}.tar.xz

BuildRequires:  check-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  glib2-devel >= 2.22.0
BuildRequires:  gpgme-devel
BuildRequires:  libattr-devel
BuildRequires:  libcurl-devel >= 7.19.0
BuildRequires:  openssl-devel

# prevent provides from nonstandard paths:
%filter_provides_in %{python_sitearch}/.*\.so$
%if %{with python3}
%filter_provides_in %{python3_sitearch}/.*\.so$
%endif
%filter_setup

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package devel
Summary:        Repodata downloading library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for librepo.

%package -n python-librepo
Summary:        Python bindings for the librepo library
BuildRequires:  pygpgme
BuildRequires:  python2-devel
%if %{with tests}
BuildRequires:  python-flask
BuildRequires:  python-nose
%endif
BuildRequires:  python-sphinx
BuildRequires:  pyxattr
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python-librepo
Python bindings for the librepo library.

%if %{with python3}
%package -n python3-librepo
Summary:        Python 3 bindings for the librepo library
BuildRequires:  python3-pygpgme
BuildRequires:  python3-devel
BuildRequires:  python3-flask
BuildRequires:  python3-nose
BuildRequires:  python3-sphinx
BuildRequires:  python3-pyxattr
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-librepo
Python 3 bindings for the librepo library.
%endif

%prep
%setup -q -n librepo

%if %{with python3}
rm -rf py3
mkdir ../py3
cp -a . ../py3/
mv ../py3 ./
%endif

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo .
make %{?_smp_mflags}

%if %{with python3}
pushd py3
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DPYTHON_DESIRED:str=3 .
make %{?_smp_mflags}
popd
%endif

%check
%if %{with tests}
#make ARGS="-V" test

%if %{with python3}
pushd py3
#make ARGS="-V" test
popd
%endif
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT
%if %{with python3}
pushd py3
make install DESTDIR=$RPM_BUILD_ROOT
popd
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING README.md
#%{_libdir}/librepo.so.*
/usr/lib64/librepo.so.*

%files devel
#%{_libdir}/librepo.so
#%{_libdir}/pkgconfig/librepo.pc
/usr/lib64/librepo.so
/usr/lib64/pkgconfig/librepo.pc
%{_includedir}/librepo/

%files -n python-librepo
%{python_sitearch}/librepo/

%if %{with python3}
%files -n python3-librepo
%{python3_sitearch}/
%endif

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.7.16-4
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.7.16-3
- Rebuild for new 4.0 release.


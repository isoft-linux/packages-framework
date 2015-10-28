%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

Summary:       Python bindings for CUPS
Name:          python-cups
Version:       1.9.72
Release:       3%{?dist}
URL:           http://cyberelk.net/tim/software/pycups/
Source:        http://cyberelk.net/tim/data/pycups/pycups-%{version}.tar.bz2
License:       GPLv2+
BuildRequires: cups-devel
BuildRequires: python2-devel python3-devel

%description
This package provides Python bindings for CUPS API,
known as pycups. It was written for use with
system-config-printer, but can be put to other uses as well.

%package -n python3-cups
Summary:       Python3 bindings for CUPS API, known as pycups.

%description -n python3-cups
This package provides Python bindings for CUPS API,
known as pycups. It was written for use with
system-config-printer, but can be put to other uses as well.

This is a ported release for python 3

%prep
%setup -q -n pycups-%{version}

rm -rf %{py3dir}
cp -a . %{py3dir}

%build
make CFLAGS="%{optflags} -fno-strict-aliasing"

pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd


%install
make install DESTDIR="%{buildroot}"

pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
chmod 755 %{buildroot}%{python3_sitearch}/cups*.so
popd



%files
%doc COPYING README NEWS TODO
%{python_sitearch}/cups.so
%{python_sitearch}/pycups*.egg-info

%files -n python3-cups
%doc COPYING README NEWS
%{python3_sitearch}/cups.cpython-3*.so
%{python3_sitearch}/pycups*.egg-info
%{_rpmconfigdir}/fileattrs/psdriver.attr
%{_rpmconfigdir}/postscriptdriver.prov

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.9.72-3
- Rebuild for new 4.0 release.


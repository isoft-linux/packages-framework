%global gittag0 3.0

Name:           fonttools
Version:        3.0
Release:        2%{?dist}
Summary:        A tool to convert True/OpenType fonts to XML and back
License:        BSD
URL:            https://github.com/behdad/%{name}/
Source0:        https://github.com/behdad/%{name}/archive/%{gittag0}.tar.gz#/%{name}-%{version}.tar.gz

Requires:       python3-fonttools
BuildArch:      noarch
Provides:       ttx = %{version}-%{release}

%description
TTX/FontTools is a tool for manipulating TrueType and OpenType fonts. It is
written in Python and has a BSD-style, open-source license. TTX can dump
TrueType and OpenType fonts to an XML-based text format and vice versa.

%package -n python2-fonttools
Summary:        Python 2 fonttools library
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:  python2-devel
BuildRequires:  numpy
BuildArch:      noarch
Requires:       numpy

%description -n python2-fonttools
TTX/FontTools is a tool for manipulating TrueType and OpenType fonts. It is
written in Python and has a BSD-style, open-source license. TTX can dump
TrueType and OpenType fonts to an XML-based text format and vice versa.


%package -n python3-fonttools
Summary:        Python 3 fonttools library
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildArch:      noarch
Requires:       python3-numpy

%description -n python3-fonttools
TTX/FontTools is a tool for manipulating TrueType and OpenType fonts. It is
written in Python and has a BSD-style, open-source license. TTX can dump
TrueType and OpenType fonts to an XML-based text format and vice versa.

%prep
%setup -qc
pushd %{name}-%{version}
mv LICENSE.txt Doc/documentation.html Doc/changes.txt ../
popd
pwd
mv %{name}-%{version} python2

pushd python2
rm -rf *.egg-info
popd

cp -a python2 python3
find python2 -name '*.py' | xargs sed -i 's|^#!python|#!%{__python2}|'
find python3 -name '*.py' | xargs sed -i 's|^#!python|#!%{__python3}|'

%build
pushd python2
%{__python2} setup.py build
popd
pushd python3
%{__python3} setup.py build
popd

%install
pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
popd

pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
popd

%files
%{_bindir}/pyftinspect
%{_bindir}/pyftmerge
%{_bindir}/pyftsubset
%{_bindir}/ttx
%{_mandir}/man1/ttx.1.gz

%files -n python2-fonttools
%license LICENSE.txt
%doc changes.txt documentation.html
%{python2_sitelib}/FontTools.pth
%{python2_sitelib}/FontTools

%files -n python3-fonttools
%license LICENSE.txt
%doc changes.txt documentation.html
%{python3_sitelib}/FontTools.pth
%{python3_sitelib}/FontTools

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.0-2
- Rebuild for new 4.0 release.

* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- Updated to version 3.0

%global with_python3 0%{!?_without_python3:1}

%global srcname docutils

Name:           python-%{srcname}
Version:        0.12
Release:        0.5.20140510svn7747%{?dist}
Summary:        System for processing plaintext documentation

# See COPYING.txt for information
License:        Public Domain and BSD and Python and GPLv3+
URL:            http://docutils.sourceforge.net
#Source0:        http://downloads.sourceforge.net/docutils/%{srcname}-%{version}.tar.gz
# Sometimes we need snapshots.  Instructions below:
# svn co -r 7687 svn://svn.code.sf.net/p/docutils/code/trunk/docutils
# cd docutils
# python setup.py sdist
# The tarball is in dist/docutils-VERSION.tar.gz
Source0:        %{srcname}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:       noarch

BuildRequires:  python2-devel
BuildRequires: python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python
%endif

Requires: python-imaging
Provides: docutils = %{version}-%{release}
Obsoletes: docutils < %{version}-%{release}

%description
The Docutils project specifies a plaintext markup language, reStructuredText,
which is easy to read and quick to write.  The project includes a python
library to parse rST files and transform them into other useful formats such
as HTML, XML, and TeX as well as commandline tools that give the enduser
access to this functionality.

Currently, the library supports parsing rST that is in standalone files and
PEPs (Python Enhancement Proposals).  Work is underway to parse rST from
Python inline documentation modules and packages.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        System for processing plaintext documentation for python3
# This module is optional and not yet available for python3
Requires: python3-imaging

%description -n python3-%{srcname}
The Docutils project specifies a plaintext markup language, reStructuredText,
which is easy to read and quick to write.  The project includes a python
library to parse rST files and transform them into other useful formats such
as HTML, XML, and TeX as well as commandline tools that give the enduser
access to this functionality.

Currently, the library supports parsing rST that is in standalone files and
PEPs (Python Enhancement Proposals).  Work is underway to parse rST from
Python inline documentation modules and packages.

This package contains the module, ported to run under python3.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}

# Remove shebang from library files
for file in docutils/utils/{code_analyzer.py,punctuation_chars.py,error_reporting.py,smartquotes.py} docutils/utils/math/{latex2mathml.py,math2html.py} docutils/writers/xetex/__init__.py; do
sed -i -e '/#! *\/usr\/bin\/.*/{1D}' $file
done

iconv -f ISO88592 -t UTF8 tools/editors/emacs/IDEAS.rst > tmp
mv tmp tools/editors/emacs/IDEAS.rst

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}

CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf %{buildroot}

# Must do the python3 install first because the scripts in /usr/bin are
# overwritten by setup.py install (and we want the python2 version to be the
# default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

# docutils setup.py runs 2to3 on a copy of the tests and puts it in sitelib.
rm -rf %{buildroot}%{python3_sitelib}/test

# Flash file is used for testing docutils but shouldn't be in the installed package.
mv docs/user/rst/images/biohazard.swf ./biohazard.swf 
popd

rm -rf %{buildroot}%{_bindir}/*
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}

for file in %{buildroot}/%{_bindir}/*.py; do
    mv $file `dirname $file`/`basename $file .py`
done

# We want the licenses but don't need this build file
rm -f licenses/docutils.conf

# Flash file is used for testing docutils but shouldn't be in the installed package.
mv docs/user/rst/images/biohazard.swf ./biohazard.swf 

%check
mv  biohazard.swf docs/user/rst/images/biohazard.swf
python test/alltests.py
rm docs/user/rst/images/biohazard.swf

%if 0%{?with_python3}
pushd %{py3dir}
mv  biohazard.swf docs/user/rst/images/biohazard.swf
python3 test3/alltests.py
rm docs/user/rst/images/biohazard.swf
popd
%endif

%clean
rm -rf %{buildroot}

%files
%doc BUGS.txt COPYING.txt FAQ.txt HISTORY.txt README.txt RELEASE-NOTES.txt 
%doc THANKS.txt licenses docs tools/editors
%{_bindir}/*
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc BUGS.txt COPYING.txt FAQ.txt HISTORY.txt README.txt RELEASE-NOTES.txt 
%doc THANKS.txt licenses docs tools/editors
%{python3_sitelib}/*
%endif

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 0.12-0.5.20140510svn7747
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.12-0.4.20140510svn7747
- Rebuild for new 4.0 release.


%global py2_incdir %(python -c 'import distutils.sysconfig; print(distutils.sysconfig.get_python_inc())')
%global py3_incdir %(python3 -c 'import distutils.sysconfig; print(distutils.sysconfig.get_python_inc())')
%global py2_libbuilddir %(python -c 'import sys; import sysconfig; print("lib.{p}-{v[0]}.{v[1]}".format(p=sysconfig.get_platform(), v=sys.version_info))')
%global py3_libbuilddir %(python3 -c 'import sys; import sysconfig; print("lib.{p}-{v[0]}.{v[1]}".format(p=sysconfig.get_platform(), v=sys.version_info))')

%global name3 python3-pillow
# bootstrap building docs (pillow is required by docutils, docutils are
#  required by sphinx; pillow build-requires sphinx)
%global with_docs 1

%global with_python3 1

# Refer to the comment for Source0 below on how to obtain the source tarball
# The saved file has format python-pillow-Pillow-$version-$ahead-g$shortcommit.tar.gz
%global commit 0222a059d62723fe056daa17f007f87dc46595b4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global ahead 0

# If ahead is 0, the tarball corresponds to a release version, otherwise to a git snapshot
%if %{ahead} > 0
%global snap .git%{shortcommit}
%endif

Name:           python-pillow
Version:        2.8.2
Release:        2%{?snap}%{?dist}
Summary:        Python image processing library

# License: see http://www.pythonware.com/products/pil/license.htm
License:        MIT
URL:            http://python-pillow.github.io/

# Obtain the tarball for a certain commit via:
#  wget --content-disposition https://github.com/python-pillow/Pillow/tarball/$commit
Source0:        https://github.com/python-pillow/Pillow/tarball/%{commit}/python-pillow-Pillow-%{version}-%{ahead}-g%{shortcommit}.tar.gz

#BuildRequires:  tk-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zlib-devel
BuildRequires:  freetype-devel
BuildRequires:  lcms2-devel
BuildRequires:  ghostscript
BuildRequires:  openjpeg2-devel
BuildRequires:  libwebp-devel
BuildRequires:  libtiff-devel

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
#BuildRequires:  tkinter
#BuildRequires:  PyQt4
#BuildRequires:  numpy
%if 0%{?with_docs}
BuildRequires:  python-sphinx
BuildRequires:  python-sphinx-theme-better
%endif # with_docs
BuildRequires:  python-cffi

%if %{with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
#BuildRequires:  python3-tkinter
#BuildRequires:  python3-PyQt4
#BuildRequires:  python3-numpy
%if 0%{?with_docs}
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-theme-better
%endif # with_docs
BuildRequires:  python3-cffi
%endif

# For EpsImagePlugin.py
Requires:       ghostscript

Provides:       python-imaging = %{version}-%{release}
Obsoletes:      python-imaging <= 1.1.7-12

#%filter_provides_in %{python_sitearch}
#%filter_provides_in %{python3_sitearch}
#%filter_setup

%description
Python image processing library, fork of the Python Imaging Library (PIL)

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are four subpackages: tk (tk interface), qt (PIL image wrapper for Qt),
devel (development) and doc (documentation).


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python-devel, libjpeg-devel, zlib-devel
Provides:       python-imaging-devel = %{version}-%{release}
Obsoletes:      python-imaging-devel <= 1.1.7-12

%description devel
Development files for %{name}.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.


#%package tk
#Summary:        Tk interface for %{name}
#Group:          System Environment/Libraries
#Requires:       %{name}%{?_isa} = %{version}-%{release}
#Requires:       tkinter
#Provides:       python-imaging-tk = %{version}-%{release}
#Obsoletes:      python-imaging-tk <= 1.1.7-12
#
#%description tk
#Tk interface for %{name}.
#
#%package qt
#Summary:        PIL image wrapper for Qt
#Group:          System Environment/Libraries
#Requires:       %{name}%{?_isa} = %{version}-%{release}
#Requires:       PyQt4
#Provides:       python-imaging-qt = %{version}-%{release}
#
#%description qt
#PIL image wrapper for Qt.


%if %{with_python3}
%package -n %{name3}
Summary:        Python 3 image processing library
Provides:       python3-imaging = %{version}-%{release}

%description -n %{name3}
%{_description}


%package -n %{name3}-devel
Summary:        Development files for %{name3}
Group:          Development/Libraries
Requires:       %{name3}%{?_isa} = %{version}-%{release}
Requires:       python3-devel, libjpeg-devel, zlib-devel

%description -n %{name3}-devel
Development files for %{name3}.


%package -n %{name3}-doc
Summary:        Documentation for %{name3}
Group:          Documentation
Requires:       %{name3} = %{version}-%{release}
BuildArch:      noarch

%description -n %{name3}-doc
Documentation for %{name3}.


#%package -n %{name3}-tk
#Summary:        Tk interface for %{name3}
#Group:          System Environment/Libraries
#Requires:       %{name3}%{?_isa} = %{version}-%{release}
#Requires:       tkinter
#
#%description -n %{name3}-tk
#Tk interface for %{name3}.
#
#%package -n %{name3}-qt
#Summary:        PIL image wrapper for Qt
#Group:          System Environment/Libraries
#Requires:       %{name3}%{?_isa} = %{version}-%{release}
#Requires:       python3-PyQt4
#
#%description -n %{name3}-qt
#PIL image wrapper for Qt.

%endif


%prep
%setup -q -n python-pillow-Pillow-%{shortcommit}

# Strip shebang on non-executable file
sed -i 1d PIL/OleFileIO.py

# Fix file encoding
iconv --from=ISO-8859-1 --to=UTF-8 PIL/WalImageFile.py > PIL/WalImageFile.py.new && \
touch -r PIL/WalImageFile.py PIL/WalImageFile.py.new && \
mv PIL/WalImageFile.py.new PIL/WalImageFile.py

# Make sample scripts non-executable
chmod -x Scripts/diffcover-run.sh
chmod -x Scripts/diffcover-install.sh

%if %{with_python3}
# Create Python 3 source tree
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
# Build Python 2 modules
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_docs}
pushd docs
PYTHONPATH=$PWD/../build/%py2_libbuilddir make html
rm -f _build/html/.buildinfo
popd
%endif # with_docs

%if %{with_python3}
# Build Python 3 modules
pushd %{py3dir}
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python3}|'
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%if 0%{?with_docs}
pushd docs
PYTHONPATH=$PWD/../build/%py3_libbuilddir make html SPHINXBUILD=sphinx-build-%python3_version
rm -f _build/html/.buildinfo
popd
%endif # with_docs
popd
%endif


%install
# Install Python 2 modules
install -d %{buildroot}/%{py2_incdir}/Imaging
install -m 644 libImaging/*.h %{buildroot}/%{py2_incdir}/Imaging
%{__python} setup.py install --skip-build --root %{buildroot}

# Fix non-standard-executable-perm
chmod 0755 %{buildroot}%{python_sitearch}/PIL/*.so

%if %{with_python3}
# Install Python 3 modules
pushd %{py3dir}
install -d %{buildroot}/%{py3_incdir}/Imaging
install -m 644 libImaging/*.h %{buildroot}/%{py3_incdir}/Imaging
%{__python3} setup.py install --skip-build --root %{buildroot}
popd

# Fix non-standard-executable-perm
chmod 0755 %{buildroot}%{python3_sitearch}/PIL/*.so
%endif

# The scripts are packaged in %%doc
rm -rf %{buildroot}%{_bindir}


%check
# Check Python 2 modules
ln -s $PWD/Images $PWD/build/%py2_libbuilddir/Images
cp -R $PWD/Tests $PWD/build/%py2_libbuilddir/Tests
cp -R $PWD/selftest.py $PWD/build/%py2_libbuilddir/selftest.py
pushd build/%py2_libbuilddir
PYTHONPATH=$PWD %{__python} selftest.py
popd

%if %{with_python3}
# Check Python 3 modules
pushd %{py3dir}
ln -s $PWD/Images $PWD/build/%py3_libbuilddir/Images
cp -R $PWD/Tests $PWD/build/%py3_libbuilddir/Tests
cp -R $PWD/selftest.py $PWD/build/%py3_libbuilddir/selftest.py
pushd build/%py3_libbuilddir
PYTHONPATH=$PWD %{__python3} selftest.py
popd
popd
%endif


%files
%doc README.rst CHANGES.rst
%license docs/COPYING
%{python_sitearch}/*
# These are in subpackages
%exclude %{python_sitearch}/PIL/_imagingtk*
%exclude %{python_sitearch}/PIL/ImageTk*
%exclude %{python_sitearch}/PIL/SpiderImagePlugin*
%exclude %{python_sitearch}/PIL/ImageQt*

%files devel
%{py2_incdir}/Imaging/

%files doc
%doc Scripts
%if 0%{?with_docs}
%doc docs/_build/html
%endif # with_docs

#%files tk
#%{python_sitearch}/PIL/_imagingtk*
#%{python_sitearch}/PIL/ImageTk*
#%{python_sitearch}/PIL/SpiderImagePlugin*
#
#%files qt
#%{python_sitearch}/PIL/ImageQt*

%if %{with_python3}
%files -n %{name3}
%doc README.rst CHANGES.rst
%license docs/COPYING
%{python3_sitearch}/*
# These are in subpackages
%exclude %{python3_sitearch}/PIL/_imagingtk*
%exclude %{python3_sitearch}/PIL/ImageTk*
%exclude %{python3_sitearch}/PIL/SpiderImagePlugin*
%exclude %{python3_sitearch}/PIL/ImageQt*

%files -n %{name3}-devel
%{py3_incdir}/Imaging/

%files -n %{name3}-doc
%doc Scripts
%if 0%{?with_docs}
%doc docs/_build/html
%endif # with_docs

#%files -n %{name3}-tk
#%{python3_sitearch}/PIL/_imagingtk*
#%{python3_sitearch}/PIL/ImageTk*
#%{python3_sitearch}/PIL/SpiderImagePlugin*
#
#%files -n %{name3}-qt
#%{python3_sitearch}/PIL/ImageQt*
#
%endif

%changelog

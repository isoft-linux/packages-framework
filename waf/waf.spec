%global with_python3 1

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%{!?python3_version: %global python3_version %(%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])")}

# Enable building without html docs (e.g. in case no recent sphinx is
# available)
%global with_docs 1

# For pre-releases
%undefine prerel

Name:           waf
Version:        1.8.15
Release:        %{?prerel:0.}2%{?prerel:.%prerel}%{?dist}
Summary:        A Python-based build system
# The entire source code is BSD apart from pproc.py (taken from Python 2.5)
License:        BSD and Python
URL:            https://github.com/waf-project/waf
# Original tarfile can be found at
# https://waf.io/waf-%%{version}.tar.bz2 or
# http://www.freehackers.org/%7Etnagy/release/waf-%%{version}.tar.bz2
# We remove:
# - docs/book, licensed CC BY-NC-ND
# - Waf logos, licensed CC BY-NC
Source:         waf-%{version}%{?prerel}.stripped.tar.bz2
Patch0:         waf-1.8.11-libdir.patch
Patch1:         waf-1.6.9-logo.patch
Patch2:         waf-1.8.11-sphinx-no-W.patch
Patch3:         waf-1.8.15-sphinx-theme.patch

BuildArch:      noarch

#if waf/waf-python3 exist, build will fail
BuildConflicts: waf waf-python3
BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # with_python3
%if 0%{?with_docs}
BuildRequires:  python-sphinx
BuildRequires:  graphviz
BuildRequires:  ImageMagick
%endif # with_docs
%if "%{?python2_version}" != ""
# Seems like automatic ABI dependency is not detected since the files are
# going to a non-standard location
Requires:       python(abi) = %{python2_version}
%endif


# the demo suite contains a perl module, which draws in unwanted
# provides and requires
%global __requires_exclude_from %{_docdir}
%global __provides_exclude_from %{_docdir}
# for EPEL, we need the old filters
%global __perl_provides %{nil}
%global __perl_requires %{nil}


%description
Waf is a Python-based framework for configuring, compiling and
installing applications. It is a replacement for other tools such as
Autotools, Scons, CMake or Ant.


%if 0%{?with_python3}
%package -n %{name}-python3
Summary:        Python3 support for %{name}
%if "%{?python3_version}" != ""
Requires:       python(abi) = %{python3_version}
%endif

%description -n %{name}-python3
Waf is a Python-based framework for configuring, compiling and
installing applications. It is a replacement for other tools such as
Autotools, Scons, CMake or Ant.

This package contains the Python 3 version of %{name}.
%endif # with_python3


%if 0%{?with_docs}
%package -n %{name}-doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
# obsolete the previous docs subpackage - guideline specifies -doc
# since: Fedora 18, RHEL 7 (mark the provides/obsoletes RHEL only after
# we no longer need to provide upgrade paths from affected Fedora releases)
Provides:       %{name}-docs = %{version}-%{release}
Obsoletes:      %{name}-docs < 1.6.11-2

%description -n %{name}-doc
Waf is a Python-based framework for configuring, compiling and
installing applications. It is a replacement for other tools such as
Autotools, Scons, CMake or Ant.

This package contains the HTML documentation for %{name}.
%endif # with_docs


%prep
%setup -q
# also search for waflib in /usr/share/waf
%patch0 -p1
# do not try to use the (removed) waf logos
%patch1 -p1
# do not add -W when running sphinx-build
%patch2 -p1
# support sphinx < 1.3
%patch3 -p1


%build
extras=
for f in waflib/extras/*.py ; do
  f=$(basename "$f" .py);
  if [ "$f" != "__init__" ]; then
    extras="${extras:+$extras,}$f" ;
  fi
done
./waf-light --make-waf --strip --tools="$extras"

%if 0%{?with_docs}
# build html docs
pushd docs/sphinx
../../waf -v configure build
popd
%endif # with_docs


%install
# use waf so it unpacks itself
mkdir _temp ; pushd _temp
cp -av ../waf .
%{__python2} ./waf >/dev/null 2>&1
pushd .waf-%{version}-*
find . -name '*.py' -printf '%%P\0' |
  xargs -0 -I{} install -m 0644 -p -D {} %{buildroot}%{_datadir}/waf/{}
popd
%if 0%{?with_python3}
# use waf so it unpacks itself
%{__python3} ./waf >/dev/null 2>&1
pushd .waf3-%{version}-*
find . -name '*.py' -printf '%%P\0' |
  xargs -0 -I{} install -m 0644 -p -D {} %{buildroot}%{_datadir}/waf3/{}
popd
%endif # with_python3
popd

# install the frontend
install -m 0755 -p -D waf-light %{buildroot}%{_bindir}/waf-%{python2_version}
ln -s waf-%{python2_version} %{buildroot}%{_bindir}/waf-2
%if 0%{?with_python3}
install -m 0755 -p -D waf-light %{buildroot}%{_bindir}/waf-%{python3_version}
ln -s waf-%{python3_version} %{buildroot}%{_bindir}/waf-3
%endif # with_python3
ln -s waf-%{python2_version} %{buildroot}%{_bindir}/waf

# remove shebangs from and fix EOL for all scripts in wafadmin
find %{buildroot}%{_datadir}/ -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' -e 's|\r$||g' {} \;

# fix waf script shebang line
sed -i "1c#! %{__python2}" %{buildroot}%{_bindir}/waf-%{python2_version}
%if 0%{?with_python3}
sed -i "1c#! %{__python3}" %{buildroot}%{_bindir}/waf-%{python3_version}
%endif # with_python3

# remove x-bits from everything going to doc
find demos utils -type f -exec chmod 0644 {} \;

# remove hidden file
rm -f docs/sphinx/build/html/.buildinfo

%if 0%{?with_python3}
# do byte compilation
%py_byte_compile %{__python2} %{buildroot}%{_datadir}/waf
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/waf3
%endif # with_python3


%files
%doc README TODO ChangeLog demos
%{_bindir}/waf
%{_bindir}/waf-%{python2_version}
%{_bindir}/waf-2
%{_datadir}/waf


%if 0%{?with_python3}
%files -n %{name}-python3
%doc README TODO ChangeLog demos
%{_bindir}/waf-%{python3_version}
%{_bindir}/waf-3
%{_datadir}/waf3
%endif # with_python3


%if 0%{?with_docs}
%files -n %{name}-doc
%doc docs/sphinx/build/html
%endif # with_docs


%changelog

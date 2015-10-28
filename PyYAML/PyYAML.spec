%global with_python3 1

Name:           PyYAML
Version:        3.11
Release:        9%{?dist}
Summary:        YAML parser and emitter for Python

License:        MIT
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/%{name}-%{version}.tar.gz
BuildRequires:  python-devel, python-setuptools, libyaml-devel
BuildRequires:  Cython
BuildRequires:  libyaml-devel
Provides:       python-yaml = %{version}-%{release}
Provides:       python-yaml%{?_isa} = %{version}-%{release}
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-Cython
%endif
# debian patch, upstream ticket http://pyyaml.org/ticket/247 and
# https://bitbucket.org/xi/pyyaml/issue/35/test-fails-on-be-s390-x-ppc64
Patch0: debian-big-endian-fix.patch

# CVE-2014-9130 assert failure when processing wrapped strings
# https://bugzilla.redhat.com/show_bug.cgi?id=1204829
Patch1: PyYAML-CVE-2014-9130.patch

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%if 0%{?with_python3}
%package -n python3-PyYAML
Summary: YAML parser and emitter for Python

%description -n python3-PyYAML
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.
%endif


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .be
chmod a-x examples/yaml-highlight/yaml_hl.py

%patch1 -p1

# remove pre-generated file
rm -rf ext/_yaml.c


%build
# regenerate ext/_yaml.c
CFLAGS="${RPM_OPT_FLAGS}" %{__python} setup.py --with-libyaml build_ext

%if 0%{?with_python3}
rm -rf %{py3dir}
# ext/_yaml.c is needed
cp -a . %{py3dir}
pushd %{py3dir}
CFLAGS="${RPM_OPT_FLAGS}" %{__python3} setup.py --with-libyaml build
popd
%endif

CFLAGS="${RPM_OPT_FLAGS}" %{__python} setup.py --with-libyaml build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif


%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGES PKG-INFO README examples
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-PyYAML
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGES PKG-INFO README examples
%{python3_sitearch}/*
%endif


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.11-9
- Rebuild for new 4.0 release.


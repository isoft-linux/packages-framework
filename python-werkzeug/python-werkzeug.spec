%if 1
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%global srcname Werkzeug

Name:           python-werkzeug
Version:        0.9.6
Release:        2
Summary:        The Swiss Army knife of Python web development 

Group:          Development/Libraries
License:        BSD
URL:            http://werkzeug.pocoo.org/
Source0:        http://pypi.python.org/packages/source/W/Werkzeug/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

%description
Werkzeug
========

Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility
modules.  It includes a powerful debugger, full featured request and
response objects, HTTP utilities to handle entity tags, cache control
headers, HTTP dates, cookie handling, file uploads, a powerful URL
routing system and a bunch of community contributed addon modules.

Werkzeug is unicode aware and doesn't enforce a specific template
engine, database adapter or anything else.  It doesn't even enforce
a specific way of handling requests and leaves all that up to the
developer. It's most useful for end user applications which should work
on as many server environments as possible (such as blogs, wikis,
bulletin boards, etc.).


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation and examples for %{name}.


%if 0%{?with_python3}
%package -n python3-werkzeug
Summary:        The Swiss Army knife of Python web development
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx

%description -n python3-werkzeug
Werkzeug
========

Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility
modules.  It includes a powerful debugger, full featured request and
response objects, HTTP utilities to handle entity tags, cache control
headers, HTTP dates, cookie handling, file uploads, a powerful URL
routing system and a bunch of community contributed addon modules.

Werkzeug is unicode aware and doesn't enforce a specific template
engine, database adapter or anything else.  It doesn't even enforce
a specific way of handling requests and leaves all that up to the
developer. It's most useful for end user applications which should work
on as many server environments as possible (such as blogs, wikis,
bulletin boards, etc.).


%package -n python3-werkzeug-doc
Summary:        Documentation for python3-werkzeug
Group:          Documentation
Requires:       python3-werkzeug = %{version}-%{release}

%description -n python3-werkzeug-doc
Documentation and examples for python3-werkzeug.
%endif


%prep
%setup -q -n %{srcname}-%{version}
%{__sed} -i 's/\r//' LICENSE
%{__sed} -i '1d' werkzeug/testsuite/multipart/collect.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif


%build
%{__python} setup.py build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x
pushd docs
make html
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x
pushd docs
make html
popd
popd
%endif


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc
popd
%endif


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE PKG-INFO CHANGES
%{python_sitelib}/*

%files doc
%defattr(-,root,root,-)
%doc docs/_build/html examples

%if 0%{?with_python3}
%files -n python3-werkzeug
%defattr(-,root,root,-)
%doc AUTHORS LICENSE PKG-INFO CHANGES
%{python3_sitelib}/*

%files -n python3-werkzeug-doc
%defattr(-,root,root,-)
%doc docs/_build/html examples
%endif


%changelog

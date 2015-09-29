%global with_python3 1

%global srcname Flask
%global srcversion 0.10.1

Name:           python-flask
Version:        0.10.1
Release:        6
Epoch:          1
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions

Group:          Development/Libraries
License:        BSD
URL:            http://flask.pocoo.org/
Source0:        http://pypi.python.org/packages/source/F/Flask/%{srcname}-%{srcversion}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools python-werkzeug python-sphinx
Requires:       python-werkzeug

# if we're not on rhel, 0%%{?rhel} < 7, so we need to also check for 0%{?rhel}
%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires:  python-jinja2-26
BuildRequires:  python-itsdangerous
Requires:       python-jinja2-26
Requires:       python-itsdangerous
%else
BuildRequires:  python-jinja2
BuildRequires:  python-itsdangerous
Requires:       python-jinja2
Requires:       python-itsdangerous
%endif

%description
Flask is called a “micro-framework” because the idea to keep the core
simple but extensible. There is no database abstraction layer, no form
validation or anything else where different libraries already exist
that can handle that. However Flask knows the concept of extensions
that can add this functionality into your application as if it was
implemented in Flask itself. There are currently extensions for object
relational mappers, form validation, upload handling, various open
authentication technologies and more.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description doc
Documentation and examples for %{name}.

%if 0%{?with_python3}
%package -n python3-flask
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-jinja2
BuildRequires:  python3-werkzeug
BuildRequires:  python3-sphinx
BuildRequires:  python3-itsdangerous
Requires:       python3-jinja2
Requires:       python3-werkzeug
Requires:       python3-itsdangerous

%description -n python3-flask
Flask is called a “micro-framework” because the idea to keep the core
simple but extensible. There is no database abstraction layer, no form
validation or anything else where different libraries already exist
that can handle that. However Flask knows the concept of extensions
that can add this functionality into your application as if it was
implemented in Flask itself. There are currently extensions for object
relational mappers, form validation, upload handling, various open
authentication technologies and more.


%package -n python3-flask-doc
Summary:        Documentation for python3-flask
Group:          Documentation
Requires:       python3-flask = %{epoch}:%{version}-%{release}

%description -n python3-flask-doc
Documentation and examples for python3-flask.
%endif


%prep
%setup -q -n %{srcname}-%{srcversion}
%{__sed} -i "/platforms/ a\    requires=['Jinja2 (>=2.4)']," setup.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Need to install flask in the setuptools "develop" mode to build docs
# The BuildRequires on Werkzeug, Jinja2 and Sphinx is due to this as well.
export PYTHONPATH=%{buildroot}%{python_sitelib}
%{__python} setup.py develop --install-dir %{buildroot}%{python_sitelib}
make -C docs html

rm -rf %{buildroot}%{python_sitelib}/site.py
rm -rf %{buildroot}%{python_sitelib}/site.py[co]
rm -rf %{buildroot}%{python_sitelib}/easy-install.pth
rm -rf docs/_build/html/.buildinfo
rm -rf examples/minitwit/*.pyc
rm -rf examples/flaskr/*.pyc
rm -rf examples/jqueryexample/*.pyc

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# Need to install flask in the setuptools "develop" mode to build docs
# The BuildRequires on Werkzeug, Jinja2 and Sphinx is due to this as well.
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%{__python3} setup.py develop --install-dir %{buildroot}%{python3_sitelib}
make -C docs html

rm -rf %{buildroot}%{python3_sitelib}/site.py
rm -rf %{buildroot}%{python3_sitelib}/site.py[co]
rm -rf %{buildroot}%{python3_sitelib}/easy-install.pth
rm -rf %{buildroot}%{python3_sitelib}/__pycache__/site.cpython-3?.pyc
rm -rf docs/_build/html/.buildinfo
rm -rf examples/minitwit/*.pyc
rm -rf examples/flaskr/*.pyc
rm -rf examples/jqueryexample/*.pyc
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
%doc AUTHORS LICENSE PKG-INFO CHANGES README
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.egg-link
%{python_sitelib}/flask

%files doc
%doc docs/_build/html examples

%if 0%{?with_python3}
%files -n python3-flask
%doc AUTHORS LICENSE PKG-INFO CHANGES README
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/*.egg-link
%{python3_sitelib}/flask

%files -n python3-flask-doc
%doc docs/_build/html examples
%endif


%changelog
* Wed Aug 26 2015 Cjacker <cjacker@foxmail.com>
- initial build

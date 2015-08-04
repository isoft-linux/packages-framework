%global with_python3 1

# Enable building without docs to avoid a circular dependency between this
# and python-sphinx:
%global with_docs 1 

Name:		python-jinja2
Version:	2.7.3
Release:	3
Summary:	General purpose template engine
Group:		Development/Languages
License:	BSD
URL:		http://jinja.pocoo.org/
Source0:	http://pypi.python.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz
# see https://github.com/mitsuhiko/jinja2/pull/259
Patch0:		99d0f3165ace0befd9eafd661be6e0c23d5f9ba5.patch
BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	python-markupsafe
%if 0%{?with_docs}
BuildRequires:	python-sphinx
%endif # with_docs
Requires:	python-babel >= 0.8
Requires:	python-markupsafe
Requires:	python-setuptools
%if 0%{?with_python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-markupsafe
%endif # with_python3


%description
Jinja2 is a template engine written in pure Python.  It provides a
Django inspired non-XML syntax but supports inline expressions and an
optional sandboxed environment.

If you have any exposure to other text-based template languages, such
as Smarty or Django, you should feel right at home with Jinja2. It's
both designer and developer friendly by sticking to Python's
principles and adding functionality useful for templating
environments.


%if 0%{?with_python3}
%package -n python3-jinja2
Summary:	General purpose template engine
Group:		Development/Languages
Requires:	python3-markupsafe
Requires:	python3-setuptools
# babel isn't py3k ready yet, and is only a weak dependency
#Requires:	 python3-babel >= 0.8


%description -n python3-jinja2
Jinja2 is a template engine written in pure Python.  It provides a
Django inspired non-XML syntax but supports inline expressions and an
optional sandboxed environment.

If you have any exposure to other text-based template languages, such
as Smarty or Django, you should feel right at home with Jinja2. It's
both designer and developer friendly by sticking to Python's
principles and adding functionality useful for templating
environments.
%endif # with_python3


%prep
%setup -q -n Jinja2-%{version}
%patch0 -p1

# cleanup
find . -name '*.pyo' -o -name '*.pyc' -delete

# fix EOL
sed -i 's|\r$||g' LICENSE

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python} setup.py build

# for now, we build docs using Python 2.x and use that for both
# packages.
%if 0%{?with_docs}
make -C docs html PYTHONPATH=$(pwd)
%endif # with_docs

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
%{__python} setup.py install -O1 --skip-build \
	    --root %{buildroot}

# remove hidden file
rm -rf docs/_build/html/.buildinfo

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build \
	    --root %{buildroot}
popd
%endif # with_python3


%check
make test


%if 0%{?with_python3}
pushd %{py3dir}
make test
popd
%endif # with_python3


%files
%doc AUTHORS CHANGES LICENSE
%if 0%{?with_docs}
%doc docs/_build/html
%endif # with_docs
%doc ext
%doc examples
%{python_sitelib}/*
%exclude %{python_sitelib}/jinja2/_debugsupport.c


%if 0%{?with_python3}
%files -n python3-jinja2
%doc AUTHORS CHANGES LICENSE
%if 0%{?with_docs}
%doc docs/_build/html
%endif # with_docs
%doc ext
%doc examples
%{python3_sitelib}/*
%exclude %{python3_sitelib}/jinja2/_debugsupport.c
%endif # with_python3


%changelog

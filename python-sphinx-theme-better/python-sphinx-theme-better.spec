%global with_python3 1

Name:           python-sphinx-theme-better
Version:        0.1.5
Release:        7%{?dist}
Summary:        A Better Sphinx Theme

License:        BSD
URL:            https://github.com/irskep/sphinx-better-theme
Source0:        https://pypi.python.org/packages/source/s/sphinx-better-theme/sphinx-better-theme-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
%if %{with_python3}
BuildRequires:  python3-devel
%endif

Requires:       python-sphinx

%description
This is a modified version of the default Sphinx theme with the following goals:
 * Remove frivolous colors, especially hard-coded ones
 * Improve readability by limiting width and using more whitespace
 * Encourage visual customization through CSS, not themeconf
 * Use semantic markup


%if %{with_python3}
%package -n python3-sphinx-theme-better
Summary:        A Better Sphinx Theme
Requires:       python3-sphinx

%description -n python3-sphinx-theme-better
This is a modified version of the default Sphinx theme with the following goals:
 * Remove frivolous colors, especially hard-coded ones
 * Improve readability by limiting width and using more whitespace
 * Encourage visual customization through CSS, not themeconf
 * Use semantic markup
%endif

%prep
%setup -q -n sphinx-better-theme-%{version}


%build
%{__python2} setup.py build

%if %{with_python3}
%{__python3} setup.py build
%endif


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%if %{with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif


%files
%doc LICENSE Readme.rst
%{python2_sitelib}/*

%if %{with_python3}
%files -n python3-sphinx-theme-better
%doc LICENSE Readme.rst
%{python3_sitelib}/*
%endif


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.1.5-7
- Rebuild for new 4.0 release.


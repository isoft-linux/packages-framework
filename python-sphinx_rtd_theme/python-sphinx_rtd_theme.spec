%global with_py3 1

%global pkgname sphinx_rtd_theme

Name:           python-%{pkgname}
Version:        0.1.8
Release:        2%{?dist}
Summary:        Sphinx theme for readthedocs.org

License:        MIT
URL:            https://github.com/snide/sphinx_rtd_theme
Source0:        https://pypi.python.org/packages/source/s/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%if 0%{?with_py3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

Requires:       font(fontawesome)
Requires:       font(lato)

%description
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.

%if 0%{?with_py3}
%package -n python3-%{pkgname}
Summary:        Sphinx theme for readthedocs.org
Requires:       font(fontawesome)
Requires:       font(lato)

%description -n python3-%{pkgname}
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.
%endif

%prep
%setup -q -c

# Prepare for python3 build
cp -a %{pkgname}-%{version} python3-%{pkgname}-%{version}

%build
# Python 2 build
pushd %{pkgname}-%{version}
%{__python2} setup.py build
popd

%if 0%{?with_py3}
# Python 3 build
pushd python3-%{pkgname}-%{version}
%{__python3} setup.py build
popd
%endif

%install
# Python 2 install
pushd %{pkgname}-%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
popd

# Don't use the bundled fonts
rm %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/*.{svg,woff}
rm %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/fontawesome*.ttf
rm %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/Lato*.ttf
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.svg \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.ttf \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.woff \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/lato/Lato-Bold.ttf \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/lato/Lato-Regular.ttf \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/

%if 0%{?with_py3}
# Python 3 install
pushd python3-%{pkgname}-%{version}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd

# Don't use the bundled fonte
rm %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/*.{svg,woff}
rm %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/fontawesome*.ttf
rm %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/Lato*.ttf
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.svg \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.ttf \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.woff \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/lato/Lato-Bold.ttf \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/lato/Lato-Regular.ttf \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
%endif
 
%files
%doc %{pkgname}-%{version}/README.rst
%license %{pkgname}-%{version}/LICENSE
%{python2_sitelib}/%{pkgname}*
 
%if 0%{?with_py3}
%files -n python3-%{pkgname}
%doc python3-%{pkgname}-%{version}/README.rst
%license python3-%{pkgname}-%{version}/LICENSE
%{python3_sitelib}/%{pkgname}*
%endif

%changelog

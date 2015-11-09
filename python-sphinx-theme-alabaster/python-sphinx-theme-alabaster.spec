%global with_python3 1
%global pypi_name alabaster
%global srcname sphinx-theme-%{pypi_name}

Name:           python-%{srcname}
Version:        0.7.6
Release:        4%{?dist}
Summary:        Configurable sidebar-enabled Sphinx theme

License:        BSD
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
This theme is a modified "Kr" Sphinx theme from @kennethreitz (especially as
used in his Requests project), which was itself originally based on @mitsuhiko's
theme used for Flask & related projects.


%package -n     python3-%{srcname}
Summary:        Configurable sidebar-enabled Sphinx theme
BuildArch:      noarch
BuildRequires:  python3-devel
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
This theme is a modified "Kr" Sphinx theme from @kennethreitz (especially as
used in his Requests project), which was itself originally based on @mitsuhiko's
theme used for Flask & related projects.


%prep
%setup -qn %{pypi_name}-%{version}

# Remove bundled eggs
rm -rf %{pypi_name}.egg-info


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
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}-%{version}-py%{python2_version}.egg-info/
%{python2_sitelib}/%{pypi_name}/

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/%{pypi_name}/


%changelog

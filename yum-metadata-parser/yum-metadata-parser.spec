%{!?python_sitelib_platform: %define python_sitelib_platform %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Summary: A fast metadata parser for yum
Name: yum-metadata-parser
Version: 1.1.4
Release: 15
Source0: http://linux.duke.edu/projects/yum/download/%{name}/%{name}-%{version}.tar.gz
Source1: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
Patch0: BZ-612409-handle-2GB-rpms.patch
Patch1: UPSTREAM-py-3-split.patch
Patch2: UPSTREAM-weak-deps.patch
Patch3: UPSTREAM-index-weak-deps.patch
Patch4: UPSTREAM-fix-minor-mem-leak.patch
License: GPLv2
Group: Development/Libraries
URL: http://linux.duke.edu/projects/yum/
Conflicts: yum < 3.2.0
BuildRequires: python-devel
BuildRequires: glib2-devel
BuildRequires: libxml2-devel
BuildRequires: sqlite-devel
BuildRequires: pkgconfig
Requires: glib2 >= 2.15
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Fast metadata parser for yum implemented in C.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

cp %{SOURCE1} .

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license gpl-2.0.txt
%doc README AUTHORS ChangeLog
%{python_sitelib_platform}/_sqlitecache.so
%{python_sitelib_platform}/sqlitecachec.py
%{python_sitelib_platform}/sqlitecachec.pyc
%{python_sitelib_platform}/sqlitecachec.pyo
%{python_sitelib_platform}/*egg-info

%changelog

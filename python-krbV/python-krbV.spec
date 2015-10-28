%{!?python_sitearch: %global python_sitearch %([ -x %{__python} ] && %{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" || :)}

Name: python-krbV
Version: 1.0.90
Release: 11
Summary: Python extension module for Kerberos 5

License: LGPLv2+

URL: http://fedorahosted.org/python-krbV/
Source: http://fedorahosted.org/python-krbV/attachment/wiki/Releases/python-krbV-%{version}.tar.bz2

BuildRequires: python-devel
BuildRequires: krb5-devel >= 1.2.2
BuildRequires: /bin/awk

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
python-krbV allows python programs to use Kerberos 5 authentication and security.

%prep
%setup -q

%build
export LIBNAME="%{_lib}"
export CFLAGS="%{optflags} -Wextra"
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__rm} -f %{buildroot}/%{python_sitearch}/*.la

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README COPYING krbV-code-snippets.py
%{python_sitearch}/krbVmodule.so

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.90-11
- Rebuild for new 4.0 release.


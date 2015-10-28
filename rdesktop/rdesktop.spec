%define debug_package %{nil} 
Name:           rdesktop
Version:        1.6.0
Release:        2
Summary:        X client for remote desktop into Windows Terminal Server

License:        GPL
URL:            http://www.rdesktop.org/
Source0:        %{name}-%{version}.tar.gz
Patch0: 	rdesktop-1.4.1-printf-info-for-rdesktop-ui.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl-devel

%description
rdesktop is an open source client for Windows NT Terminal Server and
Windows 2000 & 2003 Terminal Services, capable of natively speaking 
Remote Desktop Protocol (RDP) in order to present the user's NT
desktop. Unlike Citrix ICA, no server extensions are required.

%prep
%setup -q
%patch0 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING README doc/{AUTHORS,ChangeLog,HACKING,TODO,*.txt}
%{_bindir}/rdesktop
%{_datadir}/rdesktop/
%{_mandir}/man1/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.6.0-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


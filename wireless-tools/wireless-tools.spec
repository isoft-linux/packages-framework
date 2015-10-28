%define pre_version .pre9

Summary: Wireless ethernet configuration tools
License: GPL
Name: wireless-tools
Version: 30
Release: 2%{pre_version}
Epoch: 1
URL: http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/Tools.html
Source: http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/wireless_tools.%{version}%{?pre_version}.tar.gz
Patch2: wireless-fix-makefile.patch
ExcludeArch: s390 s390x

%description
This package contain the Wireless tools, used to manipulate
the Wireless Extensions. The Wireless Extension is an interface
allowing you to set Wireless LAN specific parameters and get the
specific stats for wireless networking equipment.

%package devel
Summary: Development headers for the wireless-tools package
Requires: wireless-tools = %{epoch}:%{version}-%{release}

%description devel
Development headers for the wireless-tools package.


%prep
%setup -n wireless_tools.%{version}
%patch2 -p1

sed '/BUILD_STATIC =/d' -i Makefile
%build
make clean
make OPT_FLAGS="$RPM_OPT_FLAGS" BUILD_SHARED=1 FORCE_WEXT_VERSION=16

%install
%{__rm} -rf $RPM_BUILD_ROOT

%{__mkdir_p} $RPM_BUILD_ROOT{/sbin,%{_mandir}/man8,%{_includedir},%{_libdir}}

make install INSTALL_DIR=$RPM_BUILD_ROOT/sbin \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc INSTALL README DISTRIBUTIONS.txt
/sbin/*
%{_mandir}/man*/*
%{_libdir}/libiw.so.30

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libiw.so


%changelog
* Sat Oct 24 2015 builder - 1:30-2.pre9
- Rebuild for new 4.0 release.


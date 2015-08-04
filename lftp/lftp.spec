Summary:	A sophisticated file transfer program
Name:		lftp
Version:	4.6.0
Release:    1	
License:	GPLv3+
Group:		Applications/Internet
URL:		http://lftp.yar.ru/
Source0:	ftp://ftp.yar.ru/lftp/lftp-%{version}.tar.xz
BuildRequires:	ncurses-devel, gnutls-devel, pkgconfig, readline-devel, gettext

%description
LFTP is a sophisticated ftp/http file transfer program. Like bash, it has job
control and uses the readline library for input. It has bookmarks, built-in
mirroring, and can transfer several files in parallel. It is designed with
reliability in mind.

%prep
%setup -q

%build
export CC=clang
export CXX=clang++
%configure \
    --with-modules \
    --disable-static \
    --with-gnutls \
    --without-openssl \
    --disable-nls

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/lftp/*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/lftp/%{version}/*.so

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/lftp.conf
%{_bindir}/*
%{_mandir}/*/*
%dir %{_libdir}/lftp
%dir %{_libdir}/lftp/%{version}
%{_libdir}/lftp/%{version}/*.so
%{_libdir}/liblftp-jobs.so.*
%{_libdir}/liblftp-tasks.so.*


%changelog

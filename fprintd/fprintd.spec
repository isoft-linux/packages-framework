Name:		fprintd
Version:	0.6.0
Release:	1
Summary:	D-Bus service for Fingerprint reader access

Group:		System Environment/Daemons
License:	GPLv2+
Source0:	http://freedesktop.org/~hadess/%{name}-%{version}.tar.xz
Url:		http://www.freedesktop.org/wiki/Software/fprint/fprintd
ExcludeArch:    s390 s390x

BuildRequires:	dbus-glib-devel
BuildRequires:	pam-devel
BuildRequires:	libfprint-devel >= 0.1.0
BuildRequires:	polkit-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:  autoconf automake libtool

%description
D-Bus service to access fingerprint readers.

%package pam
Summary:	PAM module for fingerprint authentication
Requires:	%{name} = %{version}-%{release}
# Note that we obsolete pam_fprint, but as the configuration
# is different, it will be mentioned in the release notes
Provides:	pam_fprint = %{version}-%{release}
Obsoletes:	pam_fprint < 0.2-3

Group:		System Environment/Base
License:	GPLv2+

%description pam
PAM module that uses the fprintd D-Bus service for fingerprint
authentication.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Group:		Development/Libraries
License:	GFDLv1.1+

%description devel
Development documentation for fprintd, the D-Bus service for
fingerprint readers access.

%prep
%setup -q -n %{name}-%{version}

%build
%configure --libdir=/%{_lib}/ --enable-gtk-doc --enable-pam

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/fprint

rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_fprintd.{a,la,so.*}

%find_lang %{name}
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING AUTHORS TODO
%{_bindir}/fprintd-*
%{_libexecdir}/fprintd
# FIXME This file should be marked as config when it does something useful
%{_sysconfdir}/fprintd.conf
%{_sysconfdir}/dbus-1/system.d/net.reactivated.Fprint.conf
%{_datadir}/dbus-1/system-services/net.reactivated.Fprint.service
/usr/lib/systemd/system/fprintd.service
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
%{_localstatedir}/lib/fprint
%{_mandir}/man1/fprintd.1.gz

%files pam
%defattr(-,root,root,-)
%doc pam/README
/%{_lib}/security/pam_fprintd.so

%files devel
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Device.xml
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Manager.xml

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


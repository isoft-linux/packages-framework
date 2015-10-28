Name:    liblogging
Version: 1.0.4
Release: 6%{?dist}
Summary: An easy to use logging library
License: BSD
URL:     http://www.liblogging.org/
Source0: http://download.rsyslog.com/liblogging/liblogging-%{version}.tar.gz

%package stdlog
Summary: An easy to use logging library - stdlog component
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: dos2unix

%package stdlog-devel
Summary: An easy to use logging library - stdlog development files
Requires: %{name}-stdlog%{_isa} = %{version}-%{release}
Requires: pkgconfig

%description
liblogging (the upstream project) is a collection of several components.
Namely: stdlog, journalemu, rfc3195.

%description stdlog
liblogging (the upstream project) is a collection of several components.
Namely: stdlog, journalemu, rfc3195.
The stdlog component of liblogging can be viewed as an enhanced version of the
syslog(3) API. It retains the easy semantics, but makes the API more
sophisticated "behind the scenes" with better support for multiple threads
and flexibility for different log destinations (e.g. syslog and systemd
journal).

%description stdlog-devel
This package contains development files for the %{name}-stdlog package.

%prep
%setup -q

%build
%configure \
  --disable-journal \
  --disable-rfc3195 \
  --disable-static \
  --enable-stdlog \

make V=1 %{?_smp_mflags}
dos2unix COPYING

%install
make DESTDIR=%{buildroot} install
# not packing stdlogctl yet
rm -f \
  %{buildroot}%{_bindir}/stdlogctl \
  %{buildroot}%{_libdir}/liblogging-stdlog.la \
  %{buildroot}%{_mandir}/man1/stdlogctl.1 \

%post stdlog -p /sbin/ldconfig

%postun stdlog -p /sbin/ldconfig

%files stdlog
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc ChangeLog
%{_libdir}/liblogging-stdlog.so.*

%files stdlog-devel
%defattr(-,root,root,-)
%{_includedir}/liblogging
%{_libdir}/liblogging-stdlog.so
%{_libdir}/pkgconfig/liblogging-stdlog.pc
%{_mandir}/man3/stdlog.3.gz

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.4-6
- Rebuild for new 4.0 release.


Name: fprint_demo 
Version: 0.4 
Release: 1
Summary: fprint demo application

License: GPL
URL: http://www.freedesktop.org/wiki/Software/fprint/fprint_demo/
#git clone git://github.com/dsd/fprint_demo.git 
Source0: fprint_demo.tar.gz

#udev rules to control device permission, avoid sudo fprint_demo.
#this files should be here since applications should not read/write device directly, it should be done via fprintd.
Source1: 61-fprint-permissions.rules

BuildRequires: libfprint-devel gtk2-devel	
Requires: fprintd 

%description
%{summary}

%prep
%setup -q -n %{name}

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_libdir}/udev/rules.d/
install -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/udev/rules.d/

%post
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database -q > /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database -q > /dev/null ||:


%files
%{_bindir}/fprint_demo
%{_libdir}/udev/rules.d/*.rules
%{_datadir}/applications/fprint_demo.desktop
%{_datadir}/icons/hicolor/*/apps/fprint_demo.*


%changelog
* Fri Aug 07 2015 Cjacker <cjacker@foxmail.com>
- initial build.

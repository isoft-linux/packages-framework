Summary:        Theme engines for GTK+ 2.0
Name:           gtk2-engines
Version:        2.20.2
Release: 	 	5	
License:        GPL
Source:         gtk-engines-%{version}.tar.bz2

Requires:       gtk2 >= 2.8.20
Conflicts:  	gnome-themes < 2.8.0
BuildRequires:    gtk2-devel >= 2.2.0
Obsoletes:      gnome-theme-clearlooks <= %{clearlooks_version}

URL:            ftp://ftp.gnome.org/pub/GNOME/sources/gtk-engines

%description
The gtk2-engines package contains shared objects and configuration
files that implement a number of GTK+ theme engines. Theme engines
provide different looks for GTK+, some of which resemble other
toolkits or operating systems. This package is for GTK+ 2.0, 

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains pkgconfig file for %{name}.


%prep
%setup -q -n gtk-engines-%{version}

%build
%configure \
    --disable-crux \
    --disable-hc \
    --disable-lighthouseblue \
    --disable-metal \
    --disable-mist \
    --disable-redmond  \
    --disable-smooth  \
    --disable-thinice 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# no .la, please
find $RPM_BUILD_ROOT%{_libdir} -name "*.la" | xargs rm 

# sanitize permissions
find $RPM_BUILD_ROOT%{_datadir}/themes -type d -exec chmod 755 {} \;
find $RPM_BUILD_ROOT%{_datadir}/themes -type f -name "*.png" -exec chmod 644 {} \;
find $RPM_BUILD_ROOT%{_datadir}/themes -name "gtkrc*" -exec chmod 644 {} \;

# no thanks
rm -rf $RPM_BUILD_ROOT%{_datadir}/themes/Redmond
rm -rf $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/2.4.0/engines/libredmond95.so

%find_lang gtk-engines

%clean
rm -rf $RPM_BUILD_ROOT

%files -f gtk-engines.lang
%defattr(644, root, root, 755)
%doc COPYING README ChangeLog
%attr (755, root, root) %{_libdir}/gtk-2.0/*/engines/*.so
%dir %{_datadir}/gtk-engines
%{_datadir}/gtk-engines/*
%dir %{_datadir}/themes/Clearlooks
%{_datadir}/themes/Clearlooks/*
%dir %{_datadir}/themes/Industrial
%{_datadir}/themes/Industrial/*

%files devel
%defattr(644, root, root, 755)
%{_libdir}/pkgconfig/*.pc


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.20.2-5
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


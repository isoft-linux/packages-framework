Summary:        Adwaita theme engines for GTK+ 3.0
Name:           gnome-themes-standard
Version:        3.16.2
Release: 	 	6 
License:        GPL
Group:          System Environment/Libraries
Source:         %{name}-%{version}.tar.xz
Requires:       gtk3
BuildRequires:  gtk3-devel
BuildRequires:  gtk2-devel
BuildRoot:      /var/tmp/%{name}-%{version}-root

%description
Adwaita, gnome standard theme engines for GTK+ 3.0

%package gtk2 
Summary: Adwaita theme engine for GTK+ 2.0
Group:   System Environment/Libraries

%description gtk2
Adwaita theme engine for GTK+ 2.0
%prep
%setup -q 
%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf %{buildroot}/%{_datadir}/locale
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%{_datadir}/themes/*
%{_datadir}/icons/*
%exclude %{_datadir}/themes/HighContrast/gtk-2.0

%files gtk2
%defattr(644, root, root, 755)
%{_libdir}/gtk-2.0/2.10.0/engines/libadwaita.so
%{_datadir}/themes/HighContrast/gtk-2.0

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


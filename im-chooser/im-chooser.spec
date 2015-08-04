Name:		im-chooser
Version:	1.6.4
Release:	7
License:	GPLv2+ and LGPLv2+
URL:		http://fedorahosted.org/im-chooser/
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libSM-devel imsettings-devel >= 1.3.0
BuildRequires:	desktop-file-utils intltool gettext

Source0:	http://fedorahosted.org/releases/i/m/%{name}/%{name}-%{version}.tar.bz2

Summary:	Desktop Input Method configuration tool
Group:		Applications/System
Obsoletes:	im-chooser-gnome3 < 1.4.2-2
Provides:	im-chooser-gnome3 = %{version}-%{release}
Requires:	%{name}-common = %{version}-%{release}

%description
im-chooser is a GUI configuration tool to choose the Input Method
to be used or disable Input Method usage on the desktop.

%package	common
Summary:	Common files for im-chooser subpackages
Group:		Applications/System
Requires:	imsettings >= 1.3.0
Obsoletes:	im-chooser < 1.5.0.1

%description	common
im-chooser is a GUI configuration tool to choose the Input Method
to be used or disable Input Method usage on the desktop.

This package contains the common libraries/files to be used in
im-chooser subpackages.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="/usr/bin/install -p"

desktop-file-install \
	--add-category=X-GNOME-PersonalSettings			\
	--delete-original					\
	--dir=$RPM_BUILD_ROOT%{_datadir}/applications		\
	$RPM_BUILD_ROOT%{_datadir}/applications/im-chooser.desktop

rm -rf $RPM_BUILD_ROOT%{_libdir}/libimchooseui.{so,la,a}

# disable panel so far
rm -rf $RPM_BUILD_ROOT%{_libdir}/control-center-1/panels/libim-chooser.so
rm -rf $RPM_BUILD_ROOT%{_datadir}/applications/im-chooser-panel.desktop

%find_lang %{name}


%post	common
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun	common
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans	common
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/im-chooser
%{_datadir}/applications/im-chooser.desktop
%{_mandir}/man1/im-chooser.1*

%files	common -f %{name}.lang
%{_libdir}/libimchooseui.so.*
%{_datadir}/icons/hicolor/*/apps/im-chooser.png
%dir %{_datadir}/imchooseui
%{_datadir}/imchooseui/imchoose.ui

%changelog

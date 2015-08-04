Summary: DjVu viewers, encoders, and utilities
Name: djvulibre
Version: 3.5.25.3
Release: 9
License: GPLv2+
Group: Applications/Publishing
URL: http://djvu.sourceforge.net/
Source0: http://downloads.sourceforge.net/djvu/%{name}-%{version}.tar.gz
Patch0: djvulibre-3.5.22-cdefs.patch
Patch1: djvulibre-3.5.25.3-cflags.patch

BuildRequires: libjpeg-turbo-devel
BuildRequires: libtiff-devel
BuildRequires: hicolor-icon-theme

%description
DjVu is a web-centric format and software platform for distributing documents
and images. DjVu can advantageously replace PDF, PS, TIFF, JPEG, and GIF for
distributing scanned documents, digital documents, or high-resolution pictures.
DjVu content downloads faster, displays and renders faster, looks nicer on a
screen, and consume less client resources than competing formats. DjVu images
display instantly and can be smoothly zoomed and panned with no lengthy
re-rendering.

DjVuLibre is a free (GPL'ed) implementation of DjVu, including viewers,
decoders, simple encoders, and utilities. The browser plugin is in its own
separate sub-package.


%package libs
Summary: Library files for DjVuLibre
Group: System Environment/Libraries

%description libs
Library files for DjVuLibre.


%package devel
Summary: Development files for DjVuLibre
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for DjVuLibre.


%prep
%setup -q -n %{name}-3.5.25
autoreconf
%patch0 -p1 -b .cdefs
%patch1 -p1 -b .cflags


%build 
%configure --without-qt --enable-threads

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

# Fix for the libs to get stripped correctly (still required in 3.5.20-2)
find %{buildroot}%{_libdir} -name '*.so*' | xargs %{__chmod} +x

# Remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvutoxml
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvused
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cjb2
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/csepdjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuserve
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvm
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuxmlparser
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvutxt
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/ddjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvumake
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cpaldjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuextract
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/c44
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvups
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvudump
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvmcvt
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/bzz

# MIME types (icons and desktop file) - this installs icon files under
# /usr/share/icons/hicolor/ and an xml file under /usr/share/mime/image/
# Taken from {_datadir}/djvu/osi/desktop/register-djvu-mime install
# See also the README file in the desktopfiles directory of the source distribution
pushd desktopfiles
for i in 22 32 48 64 ; do
    install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/
    cp -a ./hi${i}-djvu.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/image-vnd.djvu.mime.png
#    cp -a ./hi${i}-djvu.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/gnome-mime-image-vnd.djvu.png
done
popd

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/djvu/
%{_datadir}/icons/hicolor/22x22/mimetypes/*
%{_datadir}/icons/hicolor/32x32/mimetypes/*
%{_datadir}/icons/hicolor/64x64/mimetypes/*
%{_datadir}/icons/hicolor/48x48/mimetypes/*


%files libs
%defattr(-,root,root,-)
%doc README COPYRIGHT COPYING NEWS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/*.*
%{_includedir}/libdjvu/
%{_libdir}/pkgconfig/ddjvuapi.pc
%{_libdir}/*.so


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


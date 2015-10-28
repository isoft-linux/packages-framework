Summary:        Image loading, saving, rendering, and manipulation library
Name:           imlib2
Version:        1.4.7
Release:        2
License:        Imlib2
URL:            http://docs.enlightenment.org/api/imlib2/html/
Source0:        http://downloads.sourceforge.net/enlightenment/%{name}-%{version}.tar.bz2
BuildRequires:  libjpeg-devel libpng-devel libtiff-devel
BuildRequires:  giflib-devel freetype-devel >= 2.1.9-4 libtool bzip2-devel
BuildRequires:  libX11-devel libXext-devel pkgconfig

%description
Imlib 2 is a library that does image file loading and saving as well
as rendering, manipulation, arbitrary polygon support, etc.  It does
ALL of these operations FAST. Imlib2 also tries to be highly
intelligent about doing them, so writing naive programs can be done
easily, without sacrificing speed.  This is a complete rewrite over
the Imlib 1.x series. The architecture is more modular, simple, and
flexible.


%package devel
Summary:        Development package for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel libXext-devel freetype-devel >= 2.1.9-4 pkgconfig

%description devel
This package contains development files for %{name}.

Imlib 2 is a library that does image file loading and saving as well
as rendering, manipulation, arbitrary polygon support, etc.  It does
ALL of these operations FAST. Imlib2 also tries to be highly
intelligent about doing them, so writing naive programs can be done
easily, without sacrificing speed.  This is a complete rewrite over
the Imlib 1.x series. The architecture is more modular, simple, and
flexible.

%prep
%setup -q

%build
asmopts="--disable-mmx --disable-amd64"
%ifarch x86_64
asmopts="--disable-mmx --enable-amd64"
%else
%ifarch %{ix86}
asmopts="--enable-mmx --disable-amd64"
%endif
%endif

#autoreconf -ifv

# stop -L/usr/lib[64] getting added to imlib2-config
export x_libs=" "
%configure --disable-static --with-pic --without-id3 $asmopts
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

sed -i "s#@my_libs@##g" $RPM_BUILD_ROOT%{_bindir}/imlib2-config
# remove demos and their dependencies
rm $RPM_BUILD_ROOT%{_bindir}/imlib2_*
rm -rf $RPM_BUILD_ROOT%{_datadir}/imlib2/data/


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libImlib2.so.*
%dir %{_libdir}/imlib2/
%dir %{_libdir}/imlib2/filters/
%{_libdir}/imlib2/filters/*.so
%dir %{_libdir}/imlib2/loaders/
%{_libdir}/imlib2/loaders/*.so

%files devel
%defattr(-,root,root,-)
%doc doc/*.gif doc/*.html
%{_bindir}/imlib2-config
%{_includedir}/Imlib2.h
%{_libdir}/libImlib2.so
%{_libdir}/pkgconfig/imlib2.pc


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.4.7-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


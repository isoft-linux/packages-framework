%global man_ext .gz

Name:           mpg123
Version:        1.19.0
Release:        2%{?dist}
Summary:        MPEG audio player
Group:          Applications/Multimedia
License:        GPLv2+ and LGPLv2
URL:            http://mpg123.org/
Source:         http://downloads.sourceforge.net/mpg123/mpg123-%{version}.tar.bz2
Patch0:         mpg123-1.19.0-armv7hl.patch
BuildRequires:  libtool-ltdl-devel SDL-devel
BuildRequires:  alsa-lib-devel pulseaudio-libs-devel openal-devel
BuildRequires:  libtool automake autoconf
Requires:       libmpg123%{?_isa} = %{version}-%{release}

%description
Real time command line MPEG audio player for Layer 1, 2 and Layer3.


%package -n libmpg123
Summary:        MPEG audio Layer 1, 2 and Layer3 library
Group:          System Environment/Libraries

%description -n libmpg123
MPEG audio Layer 1, 2 and Layer3 library.


%package -n libmpg123-devel
Summary:        Development files for mpg123
Group:          Development/Libraries
Requires:       libmpg123%{?_isa} = %{version}-%{release}

%description -n libmpg123-devel
The libmpg123-devel package contains libraries and header files for
developing applications that use libmpg123.


%prep
%setup -q
%patch0 -p1
# for patch0
autoreconf -i -f

%build
%configure --with-audio=pulse,alsa --with-default-audio=pulse
# Get rid of /usr/lib64 rpath on 64bit
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%post -n libmpg123 -p /sbin/ldconfig
%postun -n libmpg123 -p /sbin/ldconfig


%files
%{_bindir}/mpg123
%{_bindir}/mpg123-id3dump
%{_bindir}/mpg123-strip
%dir %{_libdir}/mpg123
%{_libdir}/mpg123/output_alsa.*
%{_libdir}/mpg123/output_dummy.*
%{_libdir}/mpg123/output_pulse.*
%{_mandir}/man1/mpg123.1%{man_ext}

%files -n libmpg123
%{_libdir}/libmpg123.so.*

%files -n libmpg123-devel
%{_includedir}/mpg123.h
%{_libdir}/libmpg123.so
%{_libdir}/pkgconfig/libmpg123.pc


%changelog

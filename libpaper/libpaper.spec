%global nmu +nmu3

Name:		libpaper
Version:	1.1.24
Release:	12%{?dist}
Summary:	Library and tools for handling papersize
License:	GPLv2
URL:		http://packages.qa.debian.org/libp/libpaper.html
Source0:	http://ftp.debian.org/debian/pool/main/libp/libpaper/%{name}_%{version}%{nmu}.tar.gz
# Filed upstream as:
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=481213
Patch2:		libpaper-useglibcfallback.patch
BuildRequires:	libtool, gettext, gawk

%description
The paper library and accompanying files are intended to provide a 
simple way for applications to take actions based on a system- or 
user-specified paper size. This release is quite minimal, its purpose 
being to provide really basic functions (obtaining the system paper name 
and getting the height and width of a given kind of paper) that 
applications can immediately integrate.

%package devel
Summary:	Headers/Libraries for developing programs that use libpaper
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains headers and libraries that programmers will need 
to develop applications which use libpaper.

%prep
%setup -q -n %{name}-%{version}%{nmu}
%patch2 -p1 -b .useglibcfallback
libtoolize

%build
touch AUTHORS NEWS
aclocal
autoconf
automake -a
%configure --disable-static
# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo '# Simply write the paper name. See papersize(5) for possible values' > $RPM_BUILD_ROOT%{_sysconfdir}/papersize
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/libpaper.d
for i in cs da de es fr gl hu it ja nl pt_BR sv tr uk vi; do
	mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/;
	msgfmt debian/po/$i.po -o $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/%{name}.mo;
done
%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc COPYING ChangeLog README
%config(noreplace) %{_sysconfdir}/papersize
%dir %{_sysconfdir}/libpaper.d
%{_bindir}/paperconf
%{_libdir}/libpaper.so.*
%{_sbindir}/paperconfig
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%{_includedir}/paper.h
%{_libdir}/libpaper.so
%{_mandir}/man3/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.1.24-12
- Rebuild for new 4.0 release.


%define	snapshot 20170104

Summary: Library for encoding and decoding H264/AVC video streams
Name: x264
Version: 0
Release: 0.10.%{snapshot}
License: GPL
URL: http://developers.videolan.org/x264.html
Source0: last_x264.tar.bz2
BuildRequires: gettext
%ifarch %{ix86}
BuildRequires: nasm
%endif
%ifarch x86_64
BuildRequires: yasm
%endif

%description
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package devel
Summary: Development files for the x264 library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%prep
%setup -q -n x264-snapshot-%{snapshot}-2245

%build
./configure \
	--prefix=%{_prefix} \
	--exec-prefix=%{_exec_prefix} \
	--bindir=%{_bindir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--extra-cflags="$RPM_OPT_FLAGS" \
	--enable-pthread \
	--enable-debug \
	--enable-shared \
	--disable-gtk \
	--enable-pic

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
%clean
%{__rm} -rf %{buildroot}

%post 
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(644, root, root, 0755)
%attr(755,root,root) %{_bindir}/x264
%{_libdir}/libx264.so.*

%files devel
%defattr(644, root, root, 0755)
%doc doc/ratecontrol.txt doc/vui.txt
%{_includedir}/*.h
%{_libdir}/libx264.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Jan 05 2017 sulit - 0-0.10.20170104
- upgrade x264 to 20170104

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0-0.9.20150713
- Rebuild for new 4.0 release.


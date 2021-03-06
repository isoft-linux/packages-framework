#%define snapshot 20150714
Summary: Library for encoding H265/MPEG-H HEVC video streams
Name: x265
Version: 2.2
Release: 1
License: GPL
URL: http://www.videolan.org/developers/x265.html
#hg clone http://hg.videolan.org/x265
Source0: http://ftp.videolan.org/pub/videolan/%{name}/%{name}_%{version}.tar.gz
BuildRequires: gettext
BuildRequires: cmake
%ifarch %{ix86}
BuildRequires: nasm
%endif
%ifarch x86_64
BuildRequires: yasm
%endif

%description
x265 is a free software library and application for encoding video streams into the H.265/MPEG-H HEVC compression format

%package devel
Summary: Development files for the x265 library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development headers and libraries for the x265 library

%prep
%setup -q -n %{name}_%{version}

%build
pushd build/linux
%cmake ../../source
popd

%{__make} %{?_smp_mflags} -C build/linux

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install -C build/linux

rm -rf %{buildroot}%{_libdir}/*.a
%clean
%{__rm} -rf %{buildroot}

%post 
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(644, root, root, 0755)
%attr(755,root,root) %{_bindir}/x265
%{_libdir}/libx265.so.*

%files devel
%defattr(644, root, root, 0755)
%{_includedir}/*.h
%{_libdir}/libx265.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Jan 05 2017 sulit - 2.2-1
- upgrade x265 to 2.2

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0-0.2.20150714
- Rebuild for new 4.0 release.


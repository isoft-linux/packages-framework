Summary: Theora Video Compression Codec
Name: libtheora
Version: 1.1.1
Release: 1 
Epoch: 0
License: BSD
Group: System Environment/Libraries
URL: http://www.theora.org
Source0: http://downloads.xiph.org/releases/theora/%{name}-%{version}.tar.bz2
Patch0: libtheora-clang.patch
BuildRequires: libogg-devel >= 2:1.1
BuildRequires: libvorbis-devel
BuildRequires: libpng-devel

%description
Theora is Xiph.Org's first publicly released video codec, intended
for use within the Ogg's project's Ogg multimedia streaming system.
Theora is derived directly from On2's VP3 codec; Currently the two are
nearly identical, varying only in encapsulating decoder tables in the
bitstream headers, but Theora will make use of this extra freedom
in the future to improve over what is possible with VP3.


%package devel
Summary: Development tools for Theora applications
Group: Development/Libraries
Requires:	libogg-devel >= 2:1.1
Requires:	libtheora = %{epoch}:%{version}-%{release}
Requires:	pkgconfig
# the new experimental decoder is now part of the regular libtheora
# we do not obsolete theora-exp itself as that had a different soname and we
# do not want to break deps, however we do now provide the same headers as
# theora-exp-devel did.
Obsoletes:	theora-exp-devel
Provides:	theora-exp-devel

%description devel
The libtheora-devel package contains the header files and documentation 
needed to develop applications with libtheora.


%prep
%setup -q
#%patch0 -p1


%build
#./autogen.sh --disable-SDL
%configure --enable-shared --disable-static --disable-SDL --disable-examples
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README COPYING 
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/theora
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.



Summary: Musepack audio decoding library
Name:	 libmpcdec
Version: 1.2.6
Release: 15%{?dist}

License: BSD 
Group: 	 System Environment/Libraries
URL: 	 http://www.musepack.net/
Source0: http://files.musepack.net/source/libmpcdec-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Musepack is an audio compression format with a strong emphasis on high quality.
It's not lossless, but it is designed for transparency, so that you won't be
able to hear differences between the original wave file and the much smaller
MPC file.
It is based on the MPEG-1 Layer-2 / MP2 algorithms, but has rapidly developed
and vastly improved and is now at an advanced stage in which it contains
heavily optimized and patentless code.

%package devel
Summary: Development files for the Musepack audio decoding library
Group:	 Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q


%build
%configure --disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

#Unpackaged files
rm -fv $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT 


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/libmpcdec.so.5*

%files devel
%defattr(-,root,root,-)
%{_includedir}/mpcdec/
%{_libdir}/libmpcdec.so


%changelog

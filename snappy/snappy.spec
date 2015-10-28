Name:           snappy
Version:        1.1.3
Release:        2%{?dist}
Summary:        Fast compression and decompression library

License:        BSD
URL:            http://code.google.com/p/snappy/
Source0:        https://github.com/google/snappy/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Snappy is a compression/decompression library. It does not aim for maximum 
compression, or compatibility with any other compression library; instead, it 
aims for very high speeds and reasonable compression. For instance, compared to 
the fastest mode of zlib, Snappy is an order of magnitude faster for most 
inputs, but the resulting compressed files are anywhere from 20% to 100% 
bigger. 


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure CXXFLAGS="%{optflags} -DNDEBUG" --disable-static
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/snappy/
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libsnappy.so.*

%files devel
%defattr(-,root,root,-)
%doc format_description.txt framing_format.txt
%{_includedir}/snappy*.h
%{_libdir}/libsnappy.so


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.1.3-2
- Rebuild for new 4.0 release.


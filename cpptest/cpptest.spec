Name:           cpptest
Version:        1.1.2
Release:        5%{?dist}
Summary:        A portable and powerful and simple unit testing framework for C++

License:        LGPLv2+
URL:            http://%{name}.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  doxygen

%description
CppTest is a portable and powerful, yet simple, unit testing framework
for handling automated tests in C++. The focus lies on usability and
extendability.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}, pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
#%patch0 -p1
%build
%configure --disable-static --enable-doc
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc NEWS COPYING AUTHORS ChangeLog
%{_libdir}/*.so.*
%{_datadir}/doc/cpptest

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog

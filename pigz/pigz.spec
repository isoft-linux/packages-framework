Name:           pigz
Version:        2.3.3
Release:        4
Summary:        Parallel implementation of gzip

License:        zlib
URL:            http://www.zlib.net/pigz/
Source0:        http://www.zlib.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  zlib-devel
BuildRequires:  ncompress

%description
pigz, which stands for parallel implementation of gzip,
is a fully functional replacement for gzip that exploits
multiple processors and multiple cores to the hilt when compressing data.

%prep
%setup -q

%build
make CC=gcc %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
install -p -D pigz $RPM_BUILD_ROOT%{_bindir}/pigz
pushd $RPM_BUILD_ROOT%{_bindir}; ln pigz unpigz; popd
install -p -D pigz.1 -m 0644 $RPM_BUILD_ROOT%{_datadir}/man/man1/pigz.1

%check
make CC=gcc tests CFLAGS="$RPM_OPT_FLAGS"

%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc pigz.pdf README
%{_bindir}/pigz
%{_bindir}/unpigz
%{_datadir}/man/man1/pigz.*


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.3.3-4
- Rebuild for new 4.0 release.


Name:          opus-tools
Version:       0.1.7
Release:       4%{?dist}
Summary:       A set of tools for the opus audio codec

Group:         System Environment/Libraries
License:       BSD and GPLv2
URL:           http://www.opus-codec.org/
Source0:       http://downloads.xiph.org/releases/opus/%{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: flac-devel
BuildRequires: libogg-devel
BuildRequires: opus-devel

%description
The Opus codec is designed for interactive speech and audio transmission over 
the Internet. It is designed by the IETF Codec Working Group and incorporates 
technology from Skype's SILK codec and Xiph.Org's CELT codec.

This is a set of tools for the opus codec.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%check
make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_bindir}/opus*
%{_datadir}/man/man1/opus*

%changelog

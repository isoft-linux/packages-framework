Name:		openal
Version:	1.15.1
Release:	1
Summary:    OpenAL Soft is an LGPL-licensed, cross-platform, software implementation of the OpenAL 3D audio API	

Group:		System Environment/Libraries
License:	LGPL
URL:		http://kcat.strangesoft.net/openal.html
Source0:	%{name}-soft-%{version}.tar.bz2

BuildRequires:	alsa-lib-devel pulseaudio-libs-devel
Requires:   alsa-lib pulseaudio-lib	

%description
%{summary}

%package devel
Summary:    Development files for %{name} 
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the development files for %{name}.

%prep
%setup -q -n %{name}-soft-%{version}


%build
pushd build
%cmake ..
make %{?_smp_mflags}
popd

%install
pushd build
make install DESTDIR=%{buildroot}
popd


%files
%doc %{_datadir}/openal/alsoftrc.sample
%{_libdir}/*.so.*
%{_bindir}/makehrtf
%{_bindir}/openal-info

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*


%changelog


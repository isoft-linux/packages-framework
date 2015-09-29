Name: intel-gpu-tools
Version: 1.12
Release: 1
Summary: Tools for development and testing of the Intel DRM driver

License: MIT
URL: http://cgit.freedesktop.org/xorg/app/intel-gpu-tools/	
Source0: http://xorg.freedesktop.org/archive/individual/app/intel-gpu-tools-%{version}.tar.bz2
Patch0: intel-gpu-tools-wrong-doc.patch
BuildRequires:  libdrm-devel cairo-devel libpciaccess-devel python3 swig xorg-x11-util-macros

%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
export LANG=en_US.utf8
#autoreconf -ivf
%configure --disable-tests --without-libunwind --enable-gtk-doc-html
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%{_bindir}/*
%{_libdir}/intel_aubdump.so
%{_libexecdir}/intel-gpu-tools
%{_datadir}/intel-gpu-tools
%{_libdir}/pkgconfig/intel-gen4asm.pc
%{_datadir}/gtk-doc/html/intel-gpu-tools/
%{_mandir}/man1/*

%changelog
* Sat Sep 12 2015 Cjacker <cjacker@foxmail.com>
- update to 1.12

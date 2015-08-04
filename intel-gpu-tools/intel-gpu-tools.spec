Name:		intel-gpu-tools
Version:    1.11	
Release:	1
Summary:	Tools for development and testing of the Intel DRM driver

License:    MIT
URL:	    http://cgit.freedesktop.org/xorg/app/intel-gpu-tools/	
Source0:    %{name}-%{version}.tar.bz2
Patch0:     intel-gpu-tools-wrong-doc.patch
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
%patch0 -p1

%build
export LANG=en_US.utf8
autoreconf -ivf
%configure --disable-tests --without-libunwind
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%{_bindir}/*
%{_libdir}/I915ChipsetPython.so
%{_libdir}/pkgconfig/intel-gen4asm.pc
%{_datadir}/gtk-doc/html/intel-gpu-tools/
%{_mandir}/man1/*


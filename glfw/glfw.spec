Name:           glfw
Version:        3.1.1
Release:        3%{?dist}
Summary:        A cross-platform multimedia library
License:        zlib
URL:            http://www.glfw.org/index.html
Source0:        http://sourceforge.net/projects/glfw/files/glfw/%{version}/glfw-%{version}.tar.bz2

BuildRequires:  cmake
BuildRequires:  libX11-devel, libXi-devel, libXinerama-devel, libXrandr-devel, libXcursor-devel
BuildRequires:  mesa-libGL-devel, mesa-libGLU-devel

%description
GLFW is a free, Open Source, multi-platform library for OpenGL application
development that provides a powerful API for handling operating system specific
tasks such as opening an OpenGL window, reading keyboard, mouse, joystick and
time input, creating threads, and more.

%package        devel
Summary:        Support for developing C application
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       xorg-x11-proto-devel
Requires:       pkgconfig

%description devel
The glfw-devel package contains header files for developing glfw
applications.

%prep
%setup -q
find . -type f | xargs sed -i 's/\r//'

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} .
make %{?_smp_mflags} all

%install
make %{?_smp_mflags} install PREFIX=%{_prefix} LIBDIR=%{_lib} DESTDIR=%{buildroot}

%post   -p  /sbin/ldconfig
%postun -p  /sbin/ldconfig

%files
%doc README.md COPYING.txt
%{_libdir}/libglfw.so.*

%files devel
%{_includedir}/GLFW/glfw3.h
%{_includedir}/GLFW/glfw3native.h
%{_libdir}/libglfw.so
%{_libdir}/pkgconfig/glfw3.pc
%{_libdir}/cmake/glfw/glfw3Config.cmake
%{_libdir}/cmake/glfw/glfw3ConfigVersion.cmake
%{_libdir}/cmake/glfw/glfwTargets-noconfig.cmake
%{_libdir}/cmake/glfw/glfwTargets.cmake

%changelog
* Sun Dec 13 2015 Cjacker <cjacker@foxmail.com> - 3.1.1-3
- Initial build


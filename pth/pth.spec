Summary:        The GNU Portable Threads library
Name:           pth
Version:        2.0.7
Release:        26
License:        LGPLv2+
URL:            http://www.gnu.org/software/pth/
Source:         ftp://ftp.gnu.org/gnu/pth/pth-%{version}.tar.gz
Source1:        ftp://ftp.gnu.org/gnu/pth/pth-%{version}.tar.gz.sig

Patch4: pth-2.0.7-linux3.patch

%description
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution ("multithreading") inside server applications.
All threads run in the same address space of the server application,
but each thread has it's own individual program-counter, run-time
stack, signal mask and errno variable.

%package devel
Summary:        Development headers and libraries for GNU Pth
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for GNU Pth.


%prep
%setup -q
%patch4 -p1 -b .no-linux3


%build
OUR_CFLAGS="${RPM_OPT_FLAGS} -D_FILE_OFFSET_BITS=64"

%ifarch %{arm}
OUR_CFLAGS=$(echo "${OUR_CFLAGS}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2/-D_FORTIFY_SOURCE=0/g')
# guard
echo "${OUR_CFLAGS}" | grep FORTIFY_SOURCE=0
%endif

CFLAGS="${OUR_CFLAGS}"
%configure --disable-static ac_cv_func_sigstack='no'

# this is necessary; without it make -j fails
make pth_p.h
make %{?_smp_mflags}


%check
make test

%install
%make_install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/*.so.*

%files devel
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/*/*
%{_datadir}/aclocal/*


%changelog

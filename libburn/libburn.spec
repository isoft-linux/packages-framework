Summary:        Library for reading, mastering and writing optical discs
Name:           libburn
Version:        1.3.6
Release:        1
License:        GPLv2+
Group:          System Environment/Libraries
URL:            http://libburnia-project.org/
Source0:        http://files.libburnia-project.org/releases/%{name}-%{version}.tar.gz
BuildRequires:  intltool, gettext, doxygen
BuildRequires:  autoconf, automake, libtool, pkgconfig

%description
Libburn is a library by which preformatted data get onto optical media:
CD, DVD and BD (Blu-Ray). It also offers a facility for reading data
blocks from its drives without using the normal block device I/O, which
has advantages and disadvantages. It seems appropriate, nevertheless,
to do writing and reading via same channel. On several Linux systems,
the block device driver needs reloading of the drive tray in order to
make available freshly written data. The libburn read function does not
need such a reload. The code of libburn is independent of cdrecord.

%package        devel
Summary:        Development files for libburn
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description    devel
The libburn-devel package contains libraries and header files for
developing applications that use libburn.

%package -n     cdrskin
Summary:        Limited cdrecord compatibility wrapper to ease migration to libburn
Group:          Applications/Multimedia
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n cdrskin
A limited cdrecord compatibility wrapper which allows to use some libburn 
features from the command line.

%prep
%setup -q

%build
export CC=clang
export CXX=clang++
%configure --disable-static
make %{?_smp_mflags}
doxygen doc/doxygen.conf

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%files -n cdrskin
%defattr(-,root,root,-)
%{_mandir}/*/*
%{_bindir}/cdrskin

%changelog

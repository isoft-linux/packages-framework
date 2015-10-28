Name:		chmlib
Summary:	Library for dealing with ITSS/CHM format files
Version:	0.40
Release:    2	
License:	LGPLv2+
Url:		http://www.jedrea.com/chmlib/
Source0:	http://www.jedrea.com/chmlib/%{name}-%{version}.tar.bz2
Patch1:		chmlib-0001-Patch-to-fix-integer-types-problem-by-Goswin-von-Bre.patch
Patch3:		chmlib-0003-Fix-for-extract_chmLib-confusing-empty-files-with-di.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
CHMLIB is a library for dealing with ITSS/CHM format files. Right now, it is
a very simple library, but sufficient for dealing with all of the .chm files
I've come across. Due to the fairly well-designed indexing built into this
particular file format, even a small library is able to gain reasonably good
performance indexing into ITSS archives.

%package devel
Summary:	Library for dealing with ITSS/CHM format files - development files
Requires:	%{name} = %{version}-%{release}

%description devel
Files needed for developing apps using chmlib.

%prep
%setup -q
%patch1 -p1 -b .types
%patch3 -p1 -b .files_dirs

%build
%configure --enable-examples --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/chm_http
%{_bindir}/enum_chmLib
%{_bindir}/enumdir_chmLib
%{_bindir}/extract_chmLib
%{_bindir}/test_chmLib
%{_libdir}/libchm.so.*
%doc README AUTHORS COPYING NEWS

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libchm.so

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.40-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


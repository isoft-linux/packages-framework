Summary: Very high compression ratio file archiver
Name: p7zip
Version: 15.09
Release: 2%{?dist}
License: LGPLv2 and (LGPLv2+ or CPL) and Commercial
Group: Applications/Archiving
URL: http://p7zip.sourceforge.net/
Source0: http://downloads.sf.net/p7zip/p7zip_%{version}_src_all.tar.bz2
Patch0: p7zip-cmake.patch

BuildRequires: cmake
# BuildRequires: wxGTK3-devel wxGTK-devel # for 7zG GUI
%ifarch %{ix86}
BuildRequires: nasm
%endif
%ifarch x86_64
BuildRequires: yasm
%endif

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org/.


%package plugins
Summary: Additional plugins for p7zip
Group: Applications/Archiving

%description plugins
Additional plugins that can be used with 7z to extend its abilities.
This package contains also a virtual file system for Midnight Commander.


%prep
%setup -q -n %{name}_%{version}
%patch0 -p1
# Move docs early so that they don't get installed by "make install" and we
# can include them in %%doc
mv DOC docs
mv ChangeLog README TODO docs/
# And fix useless executable bit while we're at it
find docs    -type f -exec chmod -x {} \;
find contrib -type f -exec chmod -x {} \;


%build
pushd CPP/7zip/CMAKE/
./generate.sh
popd
%ifarch %{ix86}
cp -f makefile.linux_x86_asm_gcc_4.X makefile.machine
%endif
%ifarch x86_64
cp -f makefile.linux_amd64_asm makefile.machine
%endif
%ifarch ppc ppc64
cp -f makefile.linux_any_cpu_gcc_4.X makefile.machine
%endif

make %{?_smp_mflags} all2 \
    OPTFLAGS="%{optflags}" \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}


%install
make install \
    DEST_DIR=%{buildroot} \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}


%files
%doc docs/*
%{_bindir}/7za
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7za
%{_libexecdir}/p7zip/7zCon.sfx
%{_mandir}/man1/7za.1*
%exclude %{_mandir}/man1/7zr.1*

%files plugins
%doc contrib/
%{_bindir}/7z
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7z
%{_libexecdir}/p7zip/7z.so
%{_libexecdir}/p7zip/Codecs/
#{_libexecdir}/p7zip/Formats/
%{_mandir}/man1/7z.1*


%changelog
* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 15.09-2
- Update to 15.09


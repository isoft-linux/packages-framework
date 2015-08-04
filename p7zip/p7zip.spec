Summary: Very high compression ratio file archiver
Name: p7zip
Version: 9.20.1
Release: 10
# Files under C/Compress/Lzma/ are dual LGPL or CPL
License: LGPLv2 and (LGPLv2+ or CPL)
Group: Applications/Archiving
URL: http://p7zip.sourceforge.net/
# RAR sources removed since their license is incompatible with the LGPL
#Source: http://downloads.sf.net/p7zip/p7zip_%{version}_src_all.tar.bz2
# VERSION=
# wget http://downloads.sf.net/p7zip/p7zip_${VERSION}_src_all.tar.bz2
# tar xjvf p7zip_${VERSION}_src_all.tar.bz2
# rm -rf p7zip_${VERSION}/CPP/7zip/{Archive,Compress,Crypto}/Rar*
# rm -f p7zip_${VERSION}/DOCS/unRarLicense.txt
# tar --numeric-owner -cjvf p7zip_${VERSION}_src_all-norar.tar.bz2 p7zip_${VERSION}
Source: p7zip_%{version}_src_all-norar.tar.bz2
Patch0: p7zip_9.20.1-norar.patch
Patch1: p7zip_9.20.1-install.patch
Patch2: p7zip_9.20.1-nostrip.patch
Patch3: p7zip_9.20.1-execstack.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
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
%patch0 -p1 -b .norar
%patch1 -p1 -b .install
%patch2 -p1 -b .nostrip
%patch3 -p1 -b .execstack
# Move docs early so that they don't get installed by "make install" and we
# can include them in %%doc
mv DOCS docs
mv ChangeLog README TODO docs/
# And fix useless executable bit while we're at it
find docs    -type f -exec chmod -x {} \;
find contrib -type f -exec chmod -x {} \;


%build
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
rm -rf %{buildroot}
make install \
    DEST_DIR=%{buildroot} \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc docs/*
%{_bindir}/7za
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7za
%{_libexecdir}/p7zip/7zCon.sfx
%{_mandir}/man1/7za.1*
%exclude %{_mandir}/man1/7zr.1*

%files plugins
%defattr(-,root,root,-)
%doc contrib/
%{_bindir}/7z
%{_libexecdir}/p7zip/7z
%{_libexecdir}/p7zip/7z.so
#{_libexecdir}/p7zip/Codecs/
#{_libexecdir}/p7zip/Formats/
%{_mandir}/man1/7z.1*


%changelog

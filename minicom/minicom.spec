Name: minicom
Summary: A text-based modem control and terminal emulation program
Version: 2.7
Release: 5%{?dist}
URL: http://alioth.debian.org/projects/minicom/
License: GPL+ and GPLv2+ and GPLv2 and LGPLv2+ Public Domain and Copyright only
Group: Applications/Communications
ExcludeArch: s390 s390x

Source0: https://alioth.debian.org/frs/download.php/file/3977/minicom-2.7.tar.gz

BuildRequires: lockdev-devel ncurses-devel autoconf automake gettext-devel
Requires: lockdev lrzsz


%description
Minicom is a simple text-based modem control and terminal emulation
program somewhat similar to MSDOS Telix. Minicom includes a dialing
directory, full ANSI and VT100 emulation, an (external) scripting
language, and other features.


%prep
%setup -q

cp -pr doc doc_
rm -f doc_/Makefile*


%build
#./autogen.sh
autoreconf --verbose --force --install
%configure
make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_sysconfdir}

%find_lang %{name}


%files -f %{name}.lang
%doc ChangeLog AUTHORS NEWS TODO doc_/*
# DO NOT MAKE minicom SUID/SGID anything.
%{_bindir}/minicom
%{_bindir}/runscript
%{_bindir}/xminicom
%{_bindir}/ascii-xfr
%{_mandir}/man1/*


%changelog

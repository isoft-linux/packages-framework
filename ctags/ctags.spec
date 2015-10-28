Summary: A C programming language indexing and/or cross-reference tool
Name: ctags
Version: 5.8
Release: 18%{?dist}
License: GPLv2+ and LGPLv2+ and Public Domain
URL: http://ctags.sourceforge.net/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0: ctags-5.7-destdir.patch
Patch1: ctags-5.7-segment-fault.patch
Patch2: ctags-5.8-css.patch
Patch3: ctags-5.8-ocaml-crash.patch
Patch4: ctags-5.8-cssparse.patch
Patch5: ctags-5.8-memmove.patch
Patch6: ctags-5.8-format-security.patch
Patch7: ctags-CVE-2014-7204.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Ctags generates an index (or tag) file of C language objects found in
C source and header files.  The index makes it easy for text editors or
other utilities to locate the indexed items.  Ctags can also generate a
cross reference file which lists information about the various objects
found in a set of C language files in human readable form.  Exuberant
Ctags improves on ctags because it can find all types of C language tags,
including macro definitions, enumerated values (values inside enum{...}),
function and method definitions, enum/struct/union tags, external
function prototypes, typedef names and variable declarations.  Exuberant
Ctags is far less likely to be fooled by code containing #if preprocessor
conditional constructs than ctags.  Exuberant ctags supports output of
Emacs style TAGS files and can be used to print out a list of selected
objects found in source files.

Install ctags if you are going to use your system for C programming.

%package etags
Summary: Exuberant Ctags for emacs tag format
Requires: ctags = %{version}-%{release}
Requires: /usr/sbin/alternatives

%description etags
This package will generate tags in a format which GNU Emacs understand,
it's a alternativ implementation of the GNU etags program.
Note: some command line options is not compatible with GNU etags.


%prep
%setup -q
%patch0 -p1 -b .destdir
%patch1 -p1 -b .crash
%patch2 -p1 -b .css-support
%patch3 -p1 -b .ocaml-crash
%patch4 -p1 -b .cssparse-crash
%patch5 -p1 -b .memmove
%patch6 -p1 -b .fmt-sec
%patch7 -p1 -b .CVE-2014-7204

%build
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

pushd %{buildroot}%{_bindir}
ln -s ctags etags.ctags
popd

pushd %{buildroot}%{_mandir}/man1
ln -s ctags.1.gz etags.ctags.1.gz
popd

%posttrans etags
/usr/sbin/alternatives --install /usr/bin/etags emacs.etags /usr/bin/etags.ctags 20 \
   --slave /usr/share/man/man1/etags.1.gz emacs.etags.man /usr/share/man/man1/ctags.1.gz

%postun etags
/usr/sbin/alternatives --remove etags /usr/bin/etags.ctags || :

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc COPYING EXTENDING.html FAQ NEWS README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files etags
%defattr(-, root, root, -)
%doc COPYING
%{_bindir}/etags.%{name}
%{_mandir}/man1/etags.%{name}.1*

%changelog
* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 5.8-18
- Rebuild for new 4.0 release.


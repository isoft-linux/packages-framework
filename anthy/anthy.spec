%define use_utf8_dict 1
%define pkg  anthy

Name:  anthy
Version: 9100h
Release: 29%{?dist}
# The entire source code is LGPLv2+ and dictionaries is GPLv2. the corpus data is under Public Domain.
License: LGPLv2+ and GPLv2 and Public Domain
URL:  http://sourceforge.jp/projects/anthy/

Source0: http://osdn.dl.sourceforge.jp/anthy/37536/anthy-%{version}.tar.gz
Source1: %{name}-init.el
Patch0:  %{name}-fix-typo-in-dict.patch
Patch1:  %{name}-fix-typo-in-dict-name.patch
Patch10: %{name}-corpus.patch
Patch11: %{name}-fix-elisp.patch
Patch12: %{name}-aarch64.patch
Patch13: %{name}-fix-segfault.patch

Summary: Japanese character set input library

%description
Anthy provides the library to input Japanese on the applications, such as
X applications. and the user dictionaries and the users information
which is used for the conversion, is stored into their own home directory.
So Anthy is secure than other conversion server.

%package devel
Summary: Header files and library for developing programs which uses Anthy
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
The anthy-devel package contains the development files which is needed to build
the programs which uses Anthy.


%prep
%setup -q #-a 2
%patch0 -p1 -b .0-typo
%patch1 -p1 -b .1-typo-name
%patch10 -p1 -b .10-corpus
%patch11 -p1 -b .11-elisp
%patch12 -p1 -b .12-aarch64
%patch13 -p1 -b .13-segv

# Convert to utf-8
for file in ChangeLog doc/protocol.txt; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%if %{use_utf8_dict}
function normalize_extra_dict() {
 sed -e 's/^\([^  ]*\)t[  ]*\(#[A-Z0-9\*]*\)[  ]*\([^  ]*\)$/\1 \2 \3/g' $1 > $1.norm
}
function dict_conv() {
 iconv -f euc-jp -t utf-8 $1 > $1.utf8
}
function gen_dict_args() {
 if ! test -f $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in-orig; then
  cp -a $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in{,-orig}
 fi
 cat <<_EOF_ > $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in
# Generated by rpm script
set_input_encoding utf8
read @top_srcdir@/alt-cannadic/gcanna.ctd.utf8
read @top_srcdir@/alt-cannadic/gcannaf.ctd.utf8
read @top_srcdir@/alt-cannadic/gtankan.ctd.utf8
read @top_srcdir@/alt-cannadic/extra/g-jiritu-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gc-fullname-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gt-tankanji_kanji-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gt-tankanji_hikanji-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gf-fuzoku-34.t.norm
read @top_srcdir@/mkworddic/adjust.t.utf8
read @top_srcdir@/mkworddic/compound.t.utf8
read @top_srcdir@/mkworddic/extra.t.utf8
read @top_srcdir@/alt-cannadic/g_fname.t
#
build_reverse_dict
set_dict_encoding utf8
read_uc @top_srcdir@/mkworddic/udict.utf8
write anthy.wdic
done
_EOF_
touch -r $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in{-orig,}
}

(
 cd alt-cannadic
 for i in gcanna.ctd gcannaf.ctd gtankan.ctd; do
  dict_conv $i
 done
 cd extra
 for i in g-jiritu-34.t gc-fullname-34.t gf-fuzoku-34.t gt-tankanji_hikanji-34.t gt-tankanji_kanji-34.t; do
  normalize_extra_dict $i
 done
);(
 cd mkworddic
 for i in adjust.t compound.t extra.t udict zipcode.t; do
  dict_conv $i
 done
)
gen_dict_args
%endif


%build
%configure --disable-static
# fix rpath issue
sed -ie 's/^hardcode_libdir_flag_spec.*$'/'hardcode_libdir_flag_spec=" -D__LIBTOOL_IS_A_FOOL__ "/' libtool
LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/src-main/.libs:$RPM_BUILD_DIR/%{name}-%{version}/src-worddic/.libs make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# remove unnecessary files
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.{la,a}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/*
%{_sysconfdir}/*
%{_libdir}/lib*.so.*
%{_datadir}/anthy/

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 9100h-29
- Rebuild for new 4.0 release.


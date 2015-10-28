Name:       m17n-db
Summary:    Multilingualization datafiles for m17n-lib
Version:    1.7.0
Release:    5%{?dist}
License:    LGPLv2+
URL:        http://www.nongnu.org/m17n
Source0:    http://download-mirror.savannah.gnu.org/releases/m17n/%{name}-%{version}.tar.gz
## Till the Inscript2 gets upstreamed in m17n-db, use this source
Source1:    https://fedorahosted.org/releases/i/n/inscript2/inscript2-20120320.tar.gz
# Following is awaiting for upstream commit
Source2:    https://raw.githubusercontent.com/gnuman/m17n-inglish-mims/master/minglish/minglish.mim
BuildArch:  noarch
BuildRequires: gettext

Obsoletes:  m17n-contrib < 1.1.14-4.fc20
Provides:   m17n-contrib = 1.1.14-4.fc20

# Fedora speicifc patches
Patch0:     %{name}-1.6.5-bn-itrans-bug182227.patch
Patch1:     %{name}-1.6.5-kn-itrans_key-summary_bug228806.patch
Patch2:     %{name}-1.6.5-kn-inscript-ZWNJ-bug440007.patch
Patch3:     %{name}-1.6.5-number_pad_itrans-222634.patch
Patch4:     %{name}-1.7.0-fix-e-mappings.patch

%description
This package contains multilingualization (m17n) datafiles for m17n-lib
which describe input maps, encoding maps, OpenType font data and
font layout text rendering for languages.

%package extras
Summary:  Extra m17n-db files
Requires: %{name} = %{version}-%{release}

Obsoletes:  m17n-contrib-extras < 1.1.14-4.fc20
Provides:   m17n-contrib-extras = 1.1.14-4.fc20

%description extras
m17n-db extra files for input maps that are less used.

%package devel
Summary:  Development files for m17n-db
Requires: %{name} = %{version}-%{release}

%description devel
m17n-db development files


%prep
%setup -q 
pushd MIM
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p2
%patch4 -p2
popd

##extract inscript2 maps
tar xzf %{SOURCE1}

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# don't ship unijoy map for now
rm $RPM_BUILD_ROOT%{_datadir}/m17n/bn-unijoy.mim
rm $RPM_BUILD_ROOT%{_datadir}/m17n/icons/bn-unijoy.png

#removing ispell.mim for rh#587927
rm $RPM_BUILD_ROOT%{_datadir}/m17n/ispell.mim

#install inscript2 keymaps
pwd
cp -p inscript2/IM/* $RPM_BUILD_ROOT%{_datadir}/m17n/
cp -p inscript2/icons/* $RPM_BUILD_ROOT%{_datadir}/m17n/icons

# install minglish keymap
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/m17n

# For installing the translation files
%find_lang %name

%files 
%doc AUTHORS COPYING README
%dir %{_datadir}/m17n
%{_datadir}/m17n/mdb.dir
%{_datadir}/m17n/*.tbl
%{_datadir}/m17n/scripts
%{_datadir}/m17n/*.flt
# keymaps
%{_datadir}/m17n/a*.mim
%{_datadir}/m17n/b*.mim
%{_datadir}/m17n/c*.mim
%{_datadir}/m17n/d*.mim
%{_datadir}/m17n/e*.mim
%{_datadir}/m17n/f*.mim
%{_datadir}/m17n/g*.mim
%{_datadir}/m17n/h*.mim
%{_datadir}/m17n/i*.mim
%{_datadir}/m17n/k*.mim
%{_datadir}/m17n/l*.mim
%{_datadir}/m17n/m*.mim
%{_datadir}/m17n/n*.mim
%{_datadir}/m17n/o*.mim
%{_datadir}/m17n/p*.mim
%{_datadir}/m17n/r*.mim
%{_datadir}/m17n/s*.mim
%{_datadir}/m17n/t*.mim
%{_datadir}/m17n/u*.mim
%{_datadir}/m17n/v*.mim
%{_datadir}/m17n/y*.mim
# icons for keymaps
%{_datadir}/m17n/icons/*.png
%exclude %{_datadir}/m17n/zh-*.mim
%exclude %{_datadir}/m17n/icons/zh*.png
%exclude %{_datadir}/m17n/ja-*.mim
%exclude %{_datadir}/m17n/icons/ja*.png

%files extras -f %{name}.lang
%{_datadir}/m17n/zh-*.mim
%{_datadir}/m17n/icons/zh*.png
%{_datadir}/m17n/ja*.mim
%{_datadir}/m17n/icons/ja*.png
%{_datadir}/m17n/*.fst
%{_datadir}/m17n/*.map
%{_datadir}/m17n/*.tab
%{_datadir}/m17n/*.lnm
%{_datadir}/m17n/LOCALE.*

%files devel
%{_bindir}/m17n-db
%{_datadir}/pkgconfig/m17n-db.pc

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.7.0-5
- Rebuild for new 4.0 release.


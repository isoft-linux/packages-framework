%global snapshot 1

Name:       ibus-libpinyin
Version:    1.6.92
Release:    3
Summary:    Intelligent Pinyin engine based on libpinyin for IBus
License:    GPLv2+
URL:        https://github.com/libpinyin/ibus-libpinyin
Source0:    http://downloads.sourceforge.net/libpinyin/ibus-libpinyin/%{name}-%{version}.tar.gz
%if %snapshot
Patch0:     ibus-libpinyin-1.7.x-head.patch
%endif

Requires:       pygobject3
Requires:       ibus >= 1.5.4
BuildRequires:  gettext-devel
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  sqlite-devel
BuildRequires:  libuuid-devel
BuildRequires:  lua-devel
BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
BuildRequires:  ibus-devel >= 1.5.4
BuildRequires:  libpinyin-devel >= 0.9.91

# Requires(post): sqlite

Requires:   ibus >= 1.2.0
Requires:   libpinyin >= 0.9.91
Requires:   libpinyin-data%{?_isa} >= 0.9.91

Obsoletes: ibus-pinyin < 1.4.0-17

%description
It includes a Chinese Pinyin input method and a Chinese ZhuYin (Bopomofo) 
input method based on libpinyin for IBus.

%prep
%setup -q
%if %snapshot
%patch0 -p1 -b .head
%endif

%build
export CC=cc
export CXX=c++

%configure --disable-static \
           --disable-opencc \
           --disable-boost

# make -C po update-gmo
make %{?_smp_mflags}

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/ibus-setup-libpinyin.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/ibus-setup-libbopomofo.desktop

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%find_lang %{name}

%post
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%postun
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%files -f %{name}.lang
%{_datadir}/applications/ibus-setup-libpinyin.desktop
%{_datadir}/applications/ibus-setup-libbopomofo.desktop
%{_libexecdir}/ibus-engine-libpinyin
%{_libexecdir}/ibus-setup-libpinyin
%{_datadir}/ibus-libpinyin/phrases.txt
%{_datadir}/ibus-libpinyin/icons
%{_datadir}/ibus-libpinyin/setup
%{_datadir}/ibus-libpinyin/base.lua
%{_datadir}/ibus-libpinyin/user.lua
%{_datadir}/ibus-libpinyin/db/english.db
%{_datadir}/ibus-libpinyin/db/strokes.db
%dir %{_datadir}/ibus-libpinyin
%dir %{_datadir}/ibus-libpinyin/db
%{_datadir}/ibus/component/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.6.92-3
- Rebuild for new 4.0 release.


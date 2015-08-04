%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%global libchewing_python_dir %{python_sitearch}/libchewing

%global im_name_zh_TW 新酷音輸入法
%global name_zh_TW %{im_name_zh_TW}函式庫

Name:           libchewing
Version:        0.4.0
Release:        5%{?dist}
Summary:        Intelligent phonetic input method library for Traditional Chinese
Summary(zh_TW): %{name_zh_TW}

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://chewing.csie.net/
Source0:        https://github.com/chewing/%{name}/archive/v%{version}.tar.gz
Source1:         https://raw.githubusercontent.com/chewing/%{name}/v%{version}/contrib/python/chewing.py

BuildRequires:  autoconf automake libtool pkgconfig texinfo 
BuildRequires:  sqlite-devel
Requires: sqlite

%description
libchewing is an intelligent phonetic input method library for Chinese.

It provides the core algorithm and logic that can be used by various
input methods. The Chewing input method is a smart bopomofo phonetics
input method that is useful for inputting Mandarin Chinese.

%description -l zh_TW
%{name_zh_TW}提供實做了核心選字演算法，以便輸入法程式調用。

%{im_name_zh_TW}是一種智慧型注音/拼音猜字輸入法，透過智慧型的字庫分析、習慣記錄學習與預測分析，
使拼字輸入的人為選字機率降至最低，進而提升中文輸入、打字的效率。

%package -n %{name}-devel
Summary:        Development files for libchewing
Summary(zh_TW): %{name_zh_TW}開發者套件
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n %{name}-devel
Headers and other files needed to develop applications using the %{name}
library.

%description -l zh_TW  -n %{name}-devel
%{name_zh_TW}開發者套件提供了開發%{im_name_zh_TW}相關程式所需的檔案，
像是標頭檔(header files)，以及函式庫。


%package -n %{name}-python
Summary:        Python binding for libchewing
Summary(zh_TW): %{name_zh_TW} python 綁定
Group:          Development/Libraries
BuildRequires:  python2-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python

%description -n %{name}-python
Python binding of libchewing.

%description -l zh_TW -n %{name}-python
%{name_zh_TW} python 綁定

%prep
%setup -q
mkdir -p contrib/python
cp -p %SOURCE1 contrib/python

%build
CFLAGS="%{optflags} -g -DLIBINSTDIR='%{_libdir}'"
autoreconf -ivf
%configure --disable-static
make V=1 RPM_CFLAGS="%{optflags}" %{_smp_mflags}

%install
make DESTDIR=%{buildroot} install INSTALL="install -p"
rm %{buildroot}%{_libdir}/libchewing.la

mkdir -p %{buildroot}%{libchewing_python_dir}
cp -p contrib/python/chewing.py %{buildroot}%{libchewing_python_dir}

mkdir -p %{buildroot}%{_libdir}/chewing
touch %{buildroot}%{libchewing_python_dir}/__init__.py

rm -rf %{buildroot}/%{_infodir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean

%files
%doc README.md AUTHORS COPYING NEWS TODO
%{_datadir}/%{name}/*
%{_libdir}/*.so.*

%files devel
%dir %{_includedir}/chewing
%{_includedir}/chewing/*
%{_libdir}/pkgconfig/chewing.pc
%{_libdir}/*.so

%files python
%{libchewing_python_dir}

%changelog

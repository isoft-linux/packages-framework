Name: qt5-qttranslations 
Version: 5.5.1
Release: 3
Summary: Translations of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qttranslations-opensource-src-%{version}.tar.xz 

Source1: qt_zh_CN.ts 

BuildRequires: qt5-qtbase-devel 
Requires: qt5-qtbase

BuildArch: noarch

%description
Translations of Qt

%prep
%setup -q -n qttranslations-opensource-src-%{version}
cp %{SOURCE1} translations/qt_zh_CN.ts

%build
qmake-qt5

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}


%files
%{_datadir}/qt5/translations/*.qm

%changelog
* Mon Dec 28 2015 kun.li@i-soft.com.cn - 5.5.1-3
- update qt_zh_CN.ts

* Sat Oct 24 2015 builder - 5.5.1-2
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1


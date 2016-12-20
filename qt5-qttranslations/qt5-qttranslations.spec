Name: qt5-qttranslations 
Version: 5.7.1
Release: 1
Summary: Translations of Qt

License: LGPLv2 with exceptions or GPLv3 with exceptions 

URL: http://qt-project.org 
Source0: qttranslations-opensource-src-%{version}.tar.xz 

BuildRequires: qt5-qtbase-devel 
BuildRequires: qt5-qttools-devel 
Requires: qt5-qtbase

BuildArch: noarch

%description
Translations of Qt

%prep
%setup -q -n qttranslations-opensource-src-%{version}

%build
qmake-qt5

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}


%files
%{_datadir}/qt5/translations/*.qm

%changelog
* Tue Dec 20 2016 sulit - 5.7.1-1
- upgrade qt5-qttranslations to 5.7.1

* Tue Jun 21 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.7.0-1
- 5.7.0

* Wed Apr 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 5.6.0-1
- Release 5.6.0

* Tue Dec 29 2015 kun.li@i-soft.com.cn - 5.5.1-5
- update qt_zh_CN.ts

* Mon Dec 28 2015 kun.li@i-soft.com.cn - 5.5.1-4
- update qt_zh_CN.ts

* Sat Oct 24 2015 builder - 5.5.1-2
- Rebuild for new 4.0 release.

* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- update to 5.5.1


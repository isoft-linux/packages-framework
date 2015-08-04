Name:	    qt5-qttranslations	
Version:	5.5.0
Release:	1
Summary:    Translations of Qt

Group:	    Extra/Runtime/Data
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qttranslations-opensource-src-%{version}.tar.xz	

BuildRequires:  qt5-qtbase-devel 
Requires:   qt5-qtbase

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



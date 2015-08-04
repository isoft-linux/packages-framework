Name:	    qt5-qtwebkit-examples	
Version:	5.5.0
Release:	1
Summary:    WebKit examples of Qt

Group:	    Extra/Runtime/Library
License:    LGPLv2 with exceptions or GPLv3 with exceptions	

URL:	    http://qt-project.org	
Source0:    qtwebkit-examples-opensource-src-%{version}.tar.xz	

BuildRequires:  qt5-qtbase-devel qt5-qtwebkit-devel

%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Extra/Development/Library
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n qtwebkit-examples-opensource-src-%{version}

%build

%install
rm -rf %{buildroot}

if [ -d "examples/" ]; then
    mkdir -p %{buildroot}%{_libdir}/qt5/examples
    cp -r examples/* %{buildroot}%{_libdir}/qt5/examples/
    rm -rf %{buildroot}%{_libdir}/qt5/examples/*.pro
fi


%files
%{_libdir}/qt5/examples/*

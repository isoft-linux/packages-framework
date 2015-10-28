%global with_python3 1

Name:			python-ply
Summary: 		Python Lex-Yacc
Version:		3.4
Release:		9%{?dist}
License:		BSD
URL:			http://www.dabeaz.com/ply/
Source0:		http://www.dabeaz.com/ply/ply-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:		noarch
BuildRequires:		python-devel

%if 0%{?with_python3}
BuildRequires:          /usr/bin/2to3
BuildRequires:          python3-devel
%endif # if with_python3

%description
PLY is a straightforward lex/yacc implementation. Here is a list of its 
essential features:
* It is implemented entirely in Python.
* It uses LR-parsing which is reasonably efficient and well suited for larger 
  grammars.
* PLY provides most of the standard lex/yacc features including support 
  for empty productions, precedence rules, error recovery, and support 
  for ambiguous grammars.
* PLY is straightforward to use and provides very extensive error checking.
* PLY doesn't try to do anything more or less than provide the basic lex/yacc 
  functionality. In other words, it's not a large parsing framework or a 
  component of some larger system. 

%if 0%{?with_python3}
%package -n python3-ply
Summary:        Python Lex-Yacc
Requires:       python3-setuptools

%description -n python3-ply
PLY is a straightforward lex/yacc implementation. Here is a list of its 
essential features:
* It is implemented entirely in Python.
* It uses LR-parsing which is reasonably efficient and well suited for larger 
  grammars.
* PLY provides most of the standard lex/yacc features including support 
  for empty productions, precedence rules, error recovery, and support 
  for ambiguous grammars.
* PLY is straightforward to use and provides very extensive error checking.
* PLY doesn't try to do anything more or less than provide the basic lex/yacc 
  functionality. In other words, it's not a large parsing framework or a 
  component of some larger system.
%endif # with_python3

%prep
%setup -q -n ply-%{version}
sed -i 's|/usr/local/bin/python|/usr/bin/python|g' example/yply/yply.py
chmod -x example/yply/yply.py example/newclasscalc/calc.py example/classcalc/calc.py example/cleanup.sh

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'

# The README states: "You should not convert PLY using
# 2to3--it is not necessary and may in fact break the implementation."
#
# However, one of the example files contains python 2 "print" syntax, which
# lead to syntax errors during byte-compilation
#
# So we fix this file with 2to3:
pushd %{py3dir}
  2to3 --write --nobackups ply/cpp.py
popd
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES README example/
%{python_sitelib}/ply/
%{python_sitelib}/ply*.egg-info

%if 0%{?with_python3}
%files -n python3-ply
%defattr(-,root,root,-)
%doc CHANGES README example/
%{python3_sitelib}/ply/
%{python3_sitelib}/ply*.egg-info
%endif # with_python3

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.4-9
- Rebuild for new 4.0 release.


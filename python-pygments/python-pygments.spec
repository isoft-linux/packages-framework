%global with_python3 1


%global upstream_name Pygments

Name:           python-pygments
Version:        1.6
Release:        4%{?dist}
Summary:        Syntax highlighting engine written in Python

Group:          Development/Libraries
License:        BSD
URL:            http://pygments.org/
Source0:        http://pypi.python.org/packages/source/P/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel >= 2.4, python-setuptools, python-nose
%if 0%{?with_python3}
BuildRequires:  python3-devel, python3-setuptools
BuildRequires: python3-nose
%endif # if with_python3
Requires:       python-setuptools, python-imaging


%description
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!

%if 0%{?with_python3}
%package -n python3-pygments
Summary:        Syntax highlighting engine written in Python 3
Group:          Development/Libraries
Requires:       python3-setuptools

%description -n python3-pygments
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!
%endif # if with_python3

%prep
%setup -q -n Pygments-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%build
%{__python} setup.py build
%{__sed} -i 's/\r//' LICENSE

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT

# Run the Python 3 build first so that the Python 2 version of
# /usr/bin/pygmentize "wins":
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
pushd docs
install -d %{buildroot}%{_mandir}/man1
mv pygmentize.1 $RPM_BUILD_ROOT%{_mandir}/man1/pygmentize.1
mv build html
mv src reST
popd


%clean
rm -rf $RPM_BUILD_ROOT


%check
make test

# python3-nose is available from f15 on
%if 0%{?with_python3}
pushd %{py3dir}
make test
popd
%endif # with_python3


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES docs/html docs/reST LICENSE TODO
# For noarch packages: sitelib
%{python_sitelib}/*
%{_bindir}/pygmentize
%lang(en) %{_mandir}/man1/pygmentize.1.gz

%if 0%{?with_python3}
%files -n python3-pygments
%defattr(-,root,root,-)
%doc AUTHORS CHANGES docs/html docs/reST LICENSE TODO
%{python3_sitelib}/*
%endif # with_python3


%changelog

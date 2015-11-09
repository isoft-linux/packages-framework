%global with_python3 1
%global oname   beautifulsoup4

Name:           python-beautifulsoup4
Version:        4.4.0
Release:        3
Summary:        HTML/XML parser for quick-turnaround applications like screen-scraping
License:        MIT
URL:            http://www.crummy.com/software/BeautifulSoup/
Source0:        https://pypi.python.org/packages/source/b/beautifulsoup4/beautifulsoup4-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-html5lib
BuildRequires:  python-devel
BuildRequires:  python-setuptools

Requires:       python-html5lib

BuildRequires:  python-lxml
Requires:       python-lxml

%if 0%{?with_python3}
BuildRequires:  python-tools
BuildRequires:  python3-html5lib
BuildRequires:  python3-lxml
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Beautiful Soup is a Python HTML/XML parser designed for quick
turnaround projects like screen-scraping. Three features make it
powerful:

Beautiful Soup won't choke if you give it bad markup.

Beautiful Soup provides a few simple methods and Pythonic idioms for
navigating, searching, and modifying a parse tree.

Beautiful Soup automatically converts incoming documents to Unicode
and outgoing documents to UTF-8.

Beautiful Soup parses anything you give it.

Valuable data that was once locked up in poorly-designed websites is
now within your reach. Projects that would have taken hours take only
minutes with Beautiful Soup.

%if 0%{?with_python3}
%package -n     python3-beautifulsoup4
Summary:        HTML/XML parser for quick-turnaround applications like screen-scraping
Requires:       python3-html5lib
Requires:       python3-lxml
Obsoletes:      python3-BeautifulSoup < 1:3.2.1-2

%description -n python3-beautifulsoup4
Beautiful Soup is a Python HTML/XML parser designed for quick
turnaround projects like screen-scraping. Three features make it
powerful:

Beautiful Soup won't choke if you give it bad markup.

Beautiful Soup provides a few simple methods and Pythonic idioms for
navigating, searching, and modifying a parse tree.

Beautiful Soup automatically converts incoming documents to Unicode
and outgoing documents to UTF-8.

Beautiful Soup parses anything you give it.

Valuable data that was once locked up in poorly-designed websites is
now within your reach. Projects that would have taken hours take only
minutes with Beautiful Soup.

This is the Python 3 build of Beautiful Soup.

%endif # if with_python3

%prep
%setup -q -n %{oname}-%{version}
mv AUTHORS.txt AUTHORS.txt.iso
iconv -f ISO-8859-1 -t UTF-8 -o AUTHORS.txt AUTHORS.txt.iso
touch -r AUTHORS.txt.iso AUTHORS.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
2to3 --write --nobackups .
%{__python3} setup.py build
%endif

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%check
%if 0%{?rhel} && 0%{?rhel} <= 6
PYTHONPATH=$(pwd) nosetests
%else
# Some tests fails
%{__python} -m unittest discover -s bs4 || :
%endif

%if 0%{?with_python3}
pushd %{py3dir}
# Some tests fails
%{__python3} -m unittest discover -s bs4 || :
%endif

%files
%doc *.txt
%{python_sitelib}/beautifulsoup4-%{version}*.egg-info
%{python_sitelib}/bs4

%if 0%{?with_python3}
%files -n python3-beautifulsoup4
%doc *.txt
%{python3_sitelib}/beautifulsoup4-%{version}*.egg-info
%{python3_sitelib}/bs4
%endif

%changelog
* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 4.4.0-3
- Rebuild with python 3.5

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.4.0-2
- Rebuild for new 4.0 release.


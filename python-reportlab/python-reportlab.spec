%global cmapdir %(echo `rpm -qls ghostscript | grep CMap | awk '{print $2}'`)

Name:           python-reportlab
Version:        3.1.8
Release:        6%{?dist}
Summary:        Python 2.x library for generating PDFs and graphics
License:        BSD
URL:            http://www.reportlab.org/
Source0:        https://pypi.python.org/packages/source/r/reportlab/reportlab-%{version}.tar.gz
Patch0:         reportlab-3.1.8-font-locations.patch
BuildRequires:  freetype-devel
# For query the version of gs only.
BuildRequires:  ghostscript
BuildRequires:  python2-devel
BuildRequires:  python-pillow
Requires:       dejavu-sans-fonts
Requires:       python-pillow

%description
This is the ReportLab PDF Toolkit. It allows rapid creation of rich PDF 
documents, and also creation of charts in a variety of bitmap and vector 
formats.

%package -n     python3-reportlab
Summary:        Python 3.x library for generating PDFs and graphics
BuildRequires:  python3-devel
BuildRequires:  python3-pillow
Requires:       dejavu-sans-fonts
Requires:       python3-pillow

%description -n python3-reportlab
This is the ReportLab PDF Toolkit. It allows rapid creation of rich PDF 
documents, and also creation of charts in a variety of bitmap and vector 
formats.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-docs < %{version}-%{release}

%description    doc                  
Contains the documentation for ReportLab.

%prep
%setup -qn reportlab-%{version}
%patch0 -p1 -b .fonts
# clean up hashbangs from libraries
find src -name '*.py' | xargs sed -i -e '/^#!\//d'
# patch the CMap path by adding Fedora ghostscript path before the match
sed -i '/\~\/\.local\/share\/fonts\/CMap/i''\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ '\'%{cmapdir}\''\,' src/reportlab/rl_settings.py
rm -rf %{py3dir}
cp -a . %{py3dir}

%build
CFLAGS="%{optflags}" %{__python2} setup.py build
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
# a bit of a horrible hack due to a chicken-and-egg problem. The docs
# require reportlab, which isn't yet installed, but is at least built.
PYTHONPATH="`pwd`/`ls -d build/lib*`" %{__python2} docs/genAll.py

%install
%{__python2} setup.py install --prefix=%{_prefix} -O1 --skip-build --root %{buildroot}
pushd %{py3dir}
%{__python3} setup.py install --prefix=%{_prefix} -O1 --skip-build --root=%{buildroot}
popd
# Remove bundled fonts
rm -rf %{buildroot}%{python2_sitearch}/reportlab/fonts

%check
#%{__python2} setup.py tests

%files
%doc README.txt CHANGES.txt LICENSE.txt
%{python2_sitearch}/reportlab/
%{python2_sitearch}/reportlab-%{version}-py%{python2_version}.egg-info

%files -n python3-reportlab
%doc README.txt CHANGES.txt LICENSE.txt
%{python3_sitearch}/reportlab/
%{python3_sitearch}/reportlab-%{version}-py%{python3_version}.egg-info

%files doc
%doc demos/ tools/
#%doc docs/*.pdf

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.1.8-6
- Rebuild for new 4.0 release.


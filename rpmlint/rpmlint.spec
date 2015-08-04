Name:           rpmlint
Version:        1.6
Release:        4
Summary:        Tool for checking common errors in RPM packages
Group:          Development/Tools
License:        GPLv2
URL:            http://sourceforge.net/projects/rpmlint/
Source0:        http://downloads.sourceforge.net/project/rpmlint/%{name}-%{version}.tar.xz
Source1:        %{name}.config
Source2:        %{name}-CHANGES.package.old
Source3:        %{name}-etc.config

# EL-4 specific config
Source4:        %{name}.config.el4
# EL-5 specific config
Source5:        %{name}.config.el5

BuildArch:      noarch
BuildRequires:  python >= 2.4
BuildRequires:  python-rpm >= 4.4
BuildRequires:  sed >= 3.95
BuildRequires:	pytest
BuildRequires:  bash-completion
Requires:       python-rpm >= 4.4.2.2
Requires:       python >= 2.4
Requires:	    perl
Requires:       python-magic
Requires:       python-enchant
Requires:       cpio
Requires:       binutils
Requires:       desktop-file-utils
Requires:       gzip
Requires:       bzip2
Requires:       xz
# Needed for man page check in FilesCheck.py
Requires:	%{_bindir}/groff

%description
rpmlint is a tool for checking common errors in RPM packages.  Binary
and source packages as well as spec files can be checked.


%prep
%setup -q
sed -i -e /MenuCheck/d Config.py
cp -p config config.example
install -pm 644 %{SOURCE2} CHANGES.package.old
install -pm 644 %{SOURCE3} config


%build
make COMPILE_PYC=1


%install
rm -rf %{buildroot}
touch rpmlint.pyc rpmlint.pyo # just for the %%exclude to work everywhere
make install DESTDIR=$RPM_BUILD_ROOT ETCDIR=%{_sysconfdir} MANDIR=%{_mandir} \
  LIBDIR=%{_datadir}/rpmlint BINDIR=%{_bindir}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/rpmlint/config

install -pm 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/rpmlint/config.el4
install -pm 644 %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/rpmlint/config.el5
pushd $RPM_BUILD_ROOT%{_bindir}
ln -s rpmlint el4-rpmlint
ln -s rpmlint el5-rpmlint
popd

%check
make check


%files
%doc COPYING ChangeLog CHANGES.package.old README config.example
%config(noreplace) %{_sysconfdir}/rpmlint/
%{_datadir}/bash-completion/
#%{_sysconfdir}/bash_completion.d/
%{_bindir}/rpmdiff
%{_bindir}/el*-rpmlint
%{_bindir}/rpmlint
%{_datadir}/rpmlint/
%exclude %{_datadir}/rpmlint/rpmlint.py[co]
%{_mandir}/man1/rpmdiff.1*
%{_mandir}/man1/rpmlint.1*

%changelog

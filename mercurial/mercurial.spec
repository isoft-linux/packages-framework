%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Mercurial -- a distributed SCM
Name: mercurial
Version: 3.4.2
Release: 3%{?dist}

License: GPLv2+
URL: http://www.selenic.com/mercurial/
Source0: http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
BuildRequires: python python-devel
BuildRequires: pkgconfig gettext python-docutils

Requires: python
Provides: hg = %{version}-%{release}

%description
Mercurial is a fast, lightweight source control management system designed
for efficient handling of very large distributed projects.

Quick start: http://www.selenic.com/mercurial/wiki/index.cgi/QuickStart
Tutorial: http://www.selenic.com/mercurial/wiki/index.cgi/Tutorial
Extensions: http://www.selenic.com/mercurial/wiki/index.cgi/CategoryExtension

%package hgk
Summary:	Hgk interface for mercurial
Requires:	hg = %{version}-%{release}, tk


%description hgk
A Mercurial extension for displaying the change history graphically
using Tcl/Tk.  Displays branches and merges in an easily
understandable way and shows diffs for each revision.  Based on
gitk for the git SCM.

Adds the "hg view" command.  See 
http://www.selenic.com/mercurial/wiki/index.cgi/UsingHgk for more
documentation.

%prep
%setup -q -n %{name}-%{version}

%build
make all

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT --prefix %{_prefix} --record=%{name}.files
make install-doc DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

grep -v -e 'hgk.py*' -e %{python_sitearch}/mercurial/ -e %{python_sitearch}/hgext/ < %{name}.files > %{name}-base.files
grep 'hgk.py*' < %{name}.files > %{name}-hgk.files

install -D -m 755 contrib/hgk       $RPM_BUILD_ROOT%{_libexecdir}/mercurial/hgk
install -m 755 contrib/hg-ssh       $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

cat >hgk.rc <<EOF
[extensions]
# enable hgk extension ('hg help' shows 'view' as a command)
hgk=

[hgk]
path=%{_libexecdir}/mercurial/hgk
EOF
install -m 644 hgk.rc $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

cat > certs.rc <<EOF
# see: http://mercurial.selenic.com/wiki/CACertificates
[web]
cacerts = /etc/pki/tls/certs/ca-bundle.crt
EOF
install -m 644 certs.rc $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

mv $RPM_BUILD_ROOT%{python_sitearch}/mercurial/locale $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/mercurial/locale


%find_lang hg

grep -v locale %{name}-base.files > %{name}-base-filtered.files

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-base-filtered.files -f hg.lang
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING doc/README doc/hg*.txt doc/hg*.html *.cgi contrib/*.fcgi contrib/*.wsgi
%doc %attr(644,root,root) %{_mandir}/man?/hg*.gz
%doc %attr(644,root,root) contrib/*.svg
%{_bindir}/hg-ssh
%dir %{_sysconfdir}/mercurial
%dir %{_sysconfdir}/mercurial/hgrc.d
%{python_sitearch}/mercurial
%{python_sitearch}/hgext
%config(noreplace) %{_sysconfdir}/mercurial/hgrc.d/certs.rc

%files hgk -f %{name}-hgk.files
%defattr(-,root,root,-)
%{_libexecdir}/mercurial/
%{_sysconfdir}/mercurial/hgrc.d/hgk.rc

%check
#skip test, takes too much time
#cd tests && %{__python} run-tests.py

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3.4.2-3
- Rebuild for new 4.0 release.

* Tue Jul 14 2015 Cjacker <cjacker@foxmail.com>
- update to 3.4.2

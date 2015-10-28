%global dbver_rel 4.0
# When you change dbver_snap, rebuild also foomatic against this build to pick up new IEEE 1284 Device IDs.
# The postscriptdriver tags get put onto foomatic, because that's there the actual CUPS driver lives.
%global dbver_snap 20150415

Summary: Database of printers and printer drivers
Name: foomatic-db
Version: %{dbver_rel}
Release: 40.%{dbver_snap}%{?dist}
License: GPLv2+
Requires: %{name}-filesystem = %{version}-%{release}
Requires: %{name}-ppds = %{version}-%{release}

Source0: http://www.openprinting.org/download/foomatic/foomatic-db-%{dbver_rel}-%{dbver_snap}.tar.gz

Url: http://www.openprinting.org
BuildArch: noarch

# Make sure we get postscriptdriver tags.
BuildRequires: python-cups

# Build requires cups so that configure knows where to put PPDs.
BuildRequires: cups

%description
This is the database of printers, printer drivers, and driver options
for Foomatic.

The site http://www.openprinting.org/ is based on this database.

%package filesystem
Summary: Directory layout for the foomatic package
License: Public Domain

%description filesystem

Directory layout for the foomatic package.

%package ppds
Summary: PPDs from printer manufacturers
License: GPLv2+ and MIT
# We ship a symlink in a directory owned by cups
BuildRequires: cups
Requires: cups
Requires: sed
Requires: %{name}-filesystem = %{version}-%{release}

%description ppds
PPDs from printer manufacturers.

%prep
%setup -q -n foomatic-db-%{dbver_snap}

# Use sed instead of perl in the PPDs (bug #512739).
find db/source/PPD -type f -name '*.ppd' | xargs perl -pi -e 's,perl -p,sed,'

%build
%configure
make PREFIX=%{_prefix}

%install
make	DESTDIR=%buildroot PREFIX=%{_prefix} install

# Convert absolute symlink to relative.
rm -f %{buildroot}%{_datadir}/cups/model/foomatic-db-ppds
ln -sf ../../foomatic/db/source/PPD %{buildroot}%{_datadir}/cups/model/foomatic-db-ppds

%files filesystem
%dir %{_datadir}/foomatic
%dir %{_datadir}/foomatic/db
%dir %{_datadir}/foomatic/db/source

%files
%doc db/source/PPD/Kyocera/*.htm
%doc README
%{_datadir}/foomatic/db/oldprinterids
%{_datadir}/foomatic/db/source/printer
%{_datadir}/foomatic/db/source/driver
%{_datadir}/foomatic/db/source/opt
%{_datadir}/foomatic/xmlschema

%files ppds
%doc COPYING
%{_datadir}/foomatic/db/source/PPD
%{_datadir}/cups/model/foomatic-db-ppds

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 4.0-40.20150415
- Rebuild for new 4.0 release.


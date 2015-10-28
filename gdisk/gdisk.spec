Summary:       An fdisk-like partitioning tool for GPT disks
Name:          gdisk
Version:       1.0.0 
Release:       2
License:       GPLv2
URL:           http://www.rodsbooks.com/gdisk/
Source0:       http://downloads.sourceforge.net/gptfdisk/gptfdisk-%{version}.tar.gz
BuildRequires: popt-devel
BuildRequires: libicu-devel
BuildRequires: libuuid-devel
BuildRequires: ncurses-devel
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%description
An fdisk-like partitioning tool for GPT disks. GPT fdisk features a
command-line interface, fairly direct manipulation of partition table
structures, recovery tools to help you deal with corrupt partition
tables, and the ability to convert MBR disks to GPT format.

%prep
%setup -q -n gptfdisk-%{version}
chmod 0644 gdisk_test.sh

%build
%{__make} CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" 

%install
%{__rm} -rf %{buildroot}
for f in gdisk sgdisk cgdisk fixparts ; do 
    %{__install} -D -p -m 0755 $f %{buildroot}%{_sbindir}/$f
    %{__install} -D -p -m 0644 $f.8 %{buildroot}%{_mandir}/man8/$f.8
done

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc COPYING README gdisk_test.sh
%{_sbindir}/gdisk
%{_sbindir}/cgdisk
%{_sbindir}/sgdisk
%{_sbindir}/fixparts
%{_mandir}/man8/gdisk.8*
%{_mandir}/man8/cgdisk.8*
%{_mandir}/man8/sgdisk.8*
%{_mandir}/man8/fixparts.8*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 1.0.0-2
- Rebuild for new 4.0 release.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.


Name:           fuse-sshfs
Version:        2.5
Release:        3%{?dist}
Summary:        FUSE-Filesystem to access remote filesystems via SSH

License:        GPLv2
URL:            http://fuse.sourceforge.net/sshfs.html
Source0:        http://downloads.sourceforge.net/fuse/sshfs-fuse-%{version}.tar.gz
Provides:       sshfs = %{version}-%{release}
Requires:       fuse >= 2.2
Requires:	openssh-clients
BuildRequires:  fuse-devel >= 2.2
BuildRequires:  glib2-devel >= 2.0
BuildRequires:	openssh-clients

%description
This is a FUSE-filesystem client based on the SSH File Transfer Protocol.
Since most SSH servers already support this protocol it is very easy to set
up: i.e. on the server side there's nothing to do.  On the client side
mounting the filesystem is as easy as logging into the server with ssh.

%prep
%setup -q -n sshfs-fuse-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc AUTHORS ChangeLog COPYING FAQ.txt NEWS README
%{_bindir}/sshfs
%{_mandir}/man1/sshfs.1.gz

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.5-3
- Initial build


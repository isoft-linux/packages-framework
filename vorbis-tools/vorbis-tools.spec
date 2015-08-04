Summary:	The Vorbis General Audio Compression Codec tools
Name:		vorbis-tools
Version:	1.4.0
Release:	21%{?dist}
Epoch:		1
Group:		Applications/Multimedia
License:	GPLv2
URL:		http://www.xiph.org/
Source:		http://downloads.xiph.org/releases/vorbis/%{name}-%{version}.tar.gz
Patch0:		vorbis-tools-1.4.0-bz887540.patch

# http://thread.gmane.org/gmane.comp.multimedia.ogg.vorbis.devel/5729
Patch1:		vorbis-tools-1.4.0-man-page.patch

# http://thread.gmane.org/gmane.comp.multimedia.ogg.vorbis.devel/5738
Patch2:		vorbis-tools-1.4.0-bz1003607.patch

# update po files from translationproject.org (#1116650)
Patch3:		vorbis-tools-1.4.0-bz1116650.patch

# do not use stack variable out of its scope of validity (#1185558)
Patch4:		vorbis-tools-1.4.0-bz1185558.patch

# validate count of channels in the header (CVE-2014-9638 and CVE-2014-9639)
Patch5:		vorbis-tools-1.4.0-CVE-2014-9638-CVE-2014-9639.patch

BuildRequires:	libflac-devel
BuildRequires:	gettext
BuildRequires:	libao-devel
BuildRequires:	libcurl-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libspeex-devel
Obsoletes:	vorbis < %{epoch}:%{version}-%{release}
Provides:	vorbis = %{epoch}:%{version}-%{release}

%description
Ogg Vorbis is a fully open, non-proprietary, patent- and royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates from 16 to 128 kbps/channel.

The vorbis package contains an encoder, a decoder, a playback tool, and a
comment editor.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1


%build
# fix FTBFS if "-Werror=format-security" flag is used (#1025257)
export CFLAGS="$RPM_OPT_FLAGS -Wno-error=format-security"

# uncomment this when debugging
#CFLAGS="$CFLAGS -O0"

%configure
make %{?_smp_mflags}
make %{?_smp_mflags} update-gmo -C po


%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}*
%find_lang %{name}


%files -f %{name}.lang
%doc AUTHORS COPYING README ogg123/ogg123rc-example
%{_bindir}/*
%{_mandir}/man1/*


%changelog

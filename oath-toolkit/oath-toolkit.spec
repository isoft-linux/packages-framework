Name:          oath-toolkit
Version:       2.6.0
Release:       2%{?dist}
License:       GPLv3+
Group:         System Environment/Libraries
Summary:       One-time password components
BuildRequires: pam-devel, gtk-doc, libtool, libltdl-devel
BuildRequires: xmlsec1-devel, xmlsec1-openssl-devel, autoconf, automake
Source0:       http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz
URL:           http://www.nongnu.org/oath-toolkit/
# Escape leading single quotes in man pages which are misinterpreted as macros,
# patch sent upstream, upstream ticket #108312
Patch0:        oath-toolkit-2.0.2-man-fix.patch
# Fix invalid reads due to references to old (freed) xmlDoc,
# upstream ticket #108736
Patch1:        oath-toolkit-2.4.1-retain-original-xmldoc.patch

%description
The OATH Toolkit provide components for building one-time password
authentication systems. It contains shared libraries, command line tools and a
PAM module. Supported technologies include the event-based HOTP algorithm
(RFC4226) and the time-based TOTP algorithm (RFC6238). OATH stands for Open
AuTHentication, which is the organization that specify the algorithms. For
managing secret key files, the Portable Symmetric Key Container (PSKC) format
described in RFC6030 is supported.

%package -n liboath
Summary:          Library for OATH handling
Group:            Development/Libraries
License:          LGPLv2+
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# https://fedorahosted.org/fpc/ticket/174
Provides:         bundled(gnulib)

%description -n liboath
OATH stands for Open AuTHentication, which is the organization that
specify the algorithms. Supported technologies include the event-based
HOTP algorithm (RFC4226) and the time-based TOTP algorithm (RFC6238).

%package -n liboath-devel
Summary:  Development files for liboath
Group:    Development/Libraries
License:  LGPLv2+
Requires: liboath%{?_isa} = %{version}-%{release}

%description -n liboath-devel
Development files for liboath.

%package -n liboath-doc
Summary:   Documentation files for liboath
Group:     Development/Libraries
License:   LGPLv2+
Requires:  liboath = %{version}-%{release}
Requires:  gtk-doc
BuildArch: noarch

%description -n liboath-doc
Documentation files for liboath.

%package -n libpskc
Summary:          Library for PSKC handling
Group:            Development/Libraries
License:          LGPLv2+
Requires:         xml-common
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# https://fedorahosted.org/fpc/ticket/174
Provides:         bundled(gnulib)

%description -n libpskc
Library for managing secret key files, the Portable Symmetric Key
Container (PSKC) format described in RFC6030 is supported.

%package -n libpskc-devel
Summary:  Development files for libpskc
Group:    Development/Libraries
License:  LGPLv2+
Requires: libpskc%{?_isa} = %{version}-%{release}

%description -n libpskc-devel
Development files for libpskc.

%package -n libpskc-doc
Summary:   Documentation files for libpskc
Group:     Development/Libraries
License:   LGPLv2+
Requires:  libpskc = %{version}-%{release}
Requires:  gtk-doc
BuildArch: noarch

%description -n libpskc-doc
Documentation files for libpskc.

%package -n oathtool
Summary:  A command line tool for generating and validating OTPs
License:  GPLv3+
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)

%description -n oathtool
A command line tool for generating and validating OTPs.

%package -n pskctool
Summary:  A command line tool for manipulating PSKC data
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)
Requires: xmlsec1-openssl%{?_isa}

%description -n pskctool
A command line tool for manipulating PSKC data.

%package -n pam_oath
Summary:  A PAM module for pluggable login authentication for OATH
Group:    Development/Libraries
Requires: pam

%description -n pam_oath
A PAM module for pluggable login authentication for OATH.

%prep
%setup -q
%patch0 -p1 -b .man-fix
%patch1 -p1 -b .retain-original-xmldoc.patch

autoreconf -fi

%build
%configure --with-pam-dir=%{_libdir}/security

make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

# Remove static objects and libtool files
rm -f %{buildroot}%{_libdir}/*.{a,la}
rm -f %{buildroot}%{_libdir}/security/*.la

# Make /etc/liboath directory
mkdir -p -m 0600 %{buildroot}%{_sysconfdir}/liboath

%post -n liboath -p /sbin/ldconfig

%postun -n liboath -p /sbin/ldconfig

%post -n libpskc -p /sbin/ldconfig

%postun -n libpskc -p /sbin/ldconfig

%files -n liboath
%doc liboath/COPYING
%attr(0600, root, root) %dir %{_sysconfdir}/liboath
%{_libdir}/liboath.so.*

%files -n liboath-devel
%{_includedir}/liboath
%{_libdir}/liboath.so
%{_libdir}/pkgconfig/liboath.pc

%files -n liboath-doc
%{_mandir}/man3/oath*
%{_datadir}/gtk-doc/html/liboath/*

%files -n libpskc
%doc libpskc/README
%{_libdir}/libpskc.so.*
%{_datadir}/xml/pskc

%files -n libpskc-devel
%{_includedir}/pskc
%{_libdir}/libpskc.so
%{_libdir}/pkgconfig/libpskc.pc

%files -n libpskc-doc
%{_mandir}/man3/pskc*
%{_datadir}/gtk-doc/html/libpskc/*

%files -n oathtool
%doc oathtool/COPYING
%{_bindir}/oathtool
%{_mandir}/man1/oathtool.*

%files -n pskctool
%{_bindir}/pskctool
%{_mandir}/man1/pskctool.*

%files -n pam_oath
%doc pam_oath/README pam_oath/COPYING
%{_libdir}/security/pam_oath.so

%changelog

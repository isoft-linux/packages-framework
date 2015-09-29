%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Support for using OpenSSL in python scripts
Name: m2crypto
Version: 0.21.1
Release: 20%{?dist}
Source0: http://pypi.python.org/packages/source/M/M2Crypto/M2Crypto-%{version}.tar.gz
# https://bugzilla.osafoundation.org/show_bug.cgi?id=2341
Patch0: m2crypto-0.21.1-timeouts.patch
# This is only precautionary, it does fix anything - not sent upstream
Patch1: m2crypto-0.21.1-gcc_macros.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12972
Patch2: m2crypto-0.20.2-fips.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12973
Patch3: m2crypto-0.20.2-check.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13005
Patch4: m2crypto-0.21.1-memoryview.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13020
Patch5: m2crypto-0.21.1-smime-doc.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12999
Patch6: m2crypto-0.21.1-AES_crypt.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13044
Patch7: m2crypto-0.21.1-IPv6.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13049
Patch8: m2crypto-0.21.1-https-proxy.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13066
Patch9: m2crypto-0.21.1-certs.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13072
Patch10: m2crypto-0.21.1-ssl23.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13098
Patch11: m2crypto-0.21.1-SSL_CTX_new.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13073
Patch12: m2crypto-0.21.1-sni.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13100
Patch13: m2crypto-0.21.1-supported-ec.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13101
Patch14: m2crypto-0.21.1-tests-no-SIGHUP.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13103
Patch15: m2crypto-0.21.1-tests-no-export-ciphers.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13104
Patch16: m2crypto-0.21.1-tests-random-ports.patch
# https://github.com/martinpaljak/M2Crypto/issues/42
Patch17: m2crypto-0.21.1-tests-x509_name.patch
# https://github.com/martinpaljak/M2Crypto/pull/75
Patch18: m2crypto-0.21.1-swig-3.0.5.patch
# Upstream commit d21f63895d5953f4133ceed7a3e959f1cbed6f22
Patch19: m2crypto-0.21.1-tests-no-ssl23-1.patch
# https://github.com/martinpaljak/M2Crypto/pull/76
Patch20: m2crypto-0.21.1-tests-no-ssl23-2.patch
# Not sent upstream, upstream has deleted the test instead
Patch21: m2crypto-0.21.1-tests-smime-sha256.patch

License: MIT
Group: System Environment/Libraries
URL: http://wiki.osafoundation.org/bin/view/Projects/MeTooCrypto
BuildRequires: openssl, openssl-devel, python2-devel, python-setuptools
BuildRequires: perl, pkgconfig, swig, which

%filter_provides_in %{python_sitearch}/M2Crypto/__m2crypto.so
%filter_setup

%description
This package allows you to call OpenSSL functions from python scripts.

%prep
%setup -q -n M2Crypto-%{version}
%patch0 -p1 -b .timeouts
%patch1 -p1 -b .gcc_macros
%patch2 -p1 -b .fips
%patch3 -p1 -b .check
%patch4 -p1 -b .memoryview
%patch5 -p0
%patch6 -p0 -b .AES_crypt
%patch7 -p1 -b .IPv6
%patch8 -p1 -b .https-proxy
%patch9 -p0 -b .certs
openssl x509 -in tests/x509.pem -out tests/x509.der -outform DER
%patch10 -p0 -b .ssl23
%patch11 -p1 -b .SSL_CTX_new
%patch12 -p1 -b .sni
%patch13 -p1 -b .supported-ec
%patch14 -p1 -b .tests-no-SIGHUP
%patch15 -p1 -b .tests-no-export-ciphers
%patch16 -p1 -b .tests-random-ports
%patch17 -p1 -b .tests-x509_name
%patch18 -p1 -b .swig-3.0.5
%patch19 -p1 -b .no-ssl23-1
%patch20 -p1 -b .no-ssl23-2
%patch21 -p1 -b .tests-smime-sha256

# Red Hat opensslconf.h #includes an architecture-specific file, but SWIG
# doesn't follow the #include.

# Determine which arch opensslconf.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif
%ifarch sparcv9
basearch=sparc
%endif

gcc -E -dM - < /dev/null | grep -v __STDC__ \
	| sed 's/^\(#define \([^ ]*\) .*\)$/#undef \2\n\1/' > SWIG/gcc_macros.h

%build
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

# -cpperraswarn is necessary for including opensslconf-${basearch} directly
SWIG_FEATURES=-cpperraswarn %{__python} setup.py build

%install
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

%{__python} setup.py install --root=$RPM_BUILD_ROOT

for i in medusa medusa054; do
	sed -i -e '1s,#! /usr/local/bin/python,#! %{__python},' \
		demo/$i/http_server.py
done

# Windows-only
rm demo/Zope/starts.bat
# Fix up documentation permissions
find demo tests -type f -perm -111 -print0 | xargs -0 chmod a-x

grep -rl '/usr/bin/env python' demo tests \
	| xargs sed -i "s,/usr/bin/env python,%{__python},"

rm tests/*.{pem,py}.* # Patch backup files

%check
%{__python} setup.py test

%files
%doc CHANGES LICENCE README demo
%{python_sitearch}/M2Crypto
%{python_sitearch}/M2Crypto-*.egg-info

%changelog

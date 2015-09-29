%if 1
%global with_python3 1
%endif

Name:           pygpgme
Version:        0.3
Release:        13
Summary:        Python module for working with OpenPGP messages

Group:          Development/Languages
License:        LGPLv2+
URL:            http://cheeseshop.python.org/pypi/pygpgme
# pygpgme is being developed for Ubuntu and built for Ubuntu out of
# launchpad's source control.  if we need to create a snapshot, here's how:
#
# Steps to create snapshot:
# bzr branch lp:pygpgme -r69
# cd pygpgme
# patch -p0 < ../pygpgme-examples.patch
# python setup.py sdist
# tarball is in dist/pygpgme-0.1.tar.gz
#Source0:        pygpgme-0.1.tar.gz
Source0:        http://cheeseshop.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Source1:	https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
# 2013-08-22: Upstreamed 2013-05-14, upstream unresponsive:
# https://bugs.launchpad.net/pygpgme/+bug/1002421
# https://bugs.launchpad.net/pygpgme/+bug/1002421/+attachment/3676331/+files/gpgme-pubkey-hash-algo.patch
Patch0:         pygpgme-pubkey-hash-algo.patch
# 2013-08-22: Upstreamed 2013-06-19, upstream unresponsive:
# https://bugs.launchpad.net/pygpgme/+bug/1192545
# https://bugs.launchpad.net/pygpgme/+bug/1192545/+attachment/3707307/+files/pygpgme-no-encrypt-to.patch
Patch1:         pygpgme-no-encrypt-to.patch
BuildRequires:  python2-devel
BuildRequires:  gpgme-devel

%if 0%{?with_python3}
BuildRequires: python3-devel
%endif

%filter_provides_in %{python_sitearch}/gpgme/_gpgme.so
%filter_setup

%description
PyGPGME is a Python module that lets you sign, verify, encrypt and decrypt
files using the OpenPGP format.  It is built on top of GNU Privacy Guard and
the GPGME library.

%if 0%{?with_python3}
%package -n python3-pygpgme
Summary: Python3 module for working with OpenPGP messages
Group:   Development/Languages

%description -n python3-pygpgme
PyGPGME is a Python module that lets you sign, verify, encrypt and decrypt
files using the OpenPGP format.  It is built on top of GNU Privacy Guard and
the GPGME library.  This package installs the module for use with python3.
%endif

%prep
%setup -q
%patch0 -p0 -b .pubkey-hash-algo
%patch1 -p0 -b .no-encrypt-to

cp %{SOURCE1} .

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
chmod 0755 $RPM_BUILD_ROOT%{python_sitearch}/gpgme/_gpgme.so

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
chmod 0755 $RPM_BUILD_ROOT%{python3_sitearch}/gpgme/*.so
popd
%endif # with_python3

%clean
rm -rf $RPM_BUILD_ROOT

%check
### Can't run the tests unconditionally because they depend on importing a private key.
# gpg2 on which our gpgme library depends does not import private keys so this
# won't work.  The issue in the real world is not so big as we  don't
# manipulate private keys outside of a keyring that often.
# We'll run this and ignore errors so we can manually look for problems more easily
# Use the installed gpgme because it has the built compiled module
mv gpgme gpgme.bak
ln -s $RPM_BUILD_ROOT%{python_sitearch}/gpgme .
#make check || :
find tests -name '*.pyc' -delete

%files
%defattr(-,root,root,-)
%doc README PKG-INFO examples tests
%{!?_licensedir:%global license %%doc}
%license lgpl-2.1.txt
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-pygpgme
%defattr(-,root,root,-)
%doc README PKG-INFO examples tests
%{!?_licensedir:%global license %%doc}
%license lgpl-2.1.txt
%{python3_sitearch}/*
%endif # with_python3

%changelog

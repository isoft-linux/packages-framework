%global with_python3 1

Name:           python-keyring
Version:        5.0
Release:        2%{?dist}
Summary:        Python 2 library to store and access passwords safely
License:        MIT and Python
URL:            http://bitbucket.org/kang/python-keyring-lib/
Source0:        http://pypi.python.org/packages/source/k/keyring/keyring-%{version}.zip
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Obsoletes:      %{name}-kwallet < %{version}-%{release}
Obsoletes:      %{name}-gnome < %{version}-%{release}

%description
The Python keyring lib provides a easy way to access the system keyring
service from python. It can be used in any application that needs safe
password storage.
        
The keyring services supported by the Python keyring lib:
        
* **OSXKeychain**: supports the Keychain service in Mac OS X.
* **KDEKWallet**: supports the KDE's Kwallet service.
* **GnomeKeyring**: for GNOME environment.
* **SecretServiceKeyring**: for newer GNOME and KDE environments.
* **WinVaultKeyring**: supports the Windows Credential Vault
        
Besides these native password storing services provided by operating systems.
Python keyring lib also provides following build-in keyrings.
    
* **Win32CryptoKeyring**: for Windows 2k+.
* **CryptedFileKeyring**: a command line interface keyring base on PyCrypto.
* **UncryptedFileKeyring**: a keyring which leaves passwords directly in file.

%if 0%{?with_python3}
%package -n     python3-keyring
Summary:        Python 3 library to access the system keyring service
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-keyring
The Python keyring lib provides a easy way to access the system keyring
service from python. It can be used in any application that needs safe
password storage.
        
The keyring services supported by the Python keyring lib:
        
* **OSXKeychain**: supports the Keychain service in Mac OS X.
* **KDEKWallet**: supports the KDE's Kwallet service.
* **GnomeKeyring**: for GNOME environment.
* **SecretServiceKeyring**: for newer GNOME and KDE environments.
* **WinVaultKeyring**: supports the Windows Credential Vault
        
Besides these native password storing services provided by operating systems.
Python keyring lib also provides following build-in keyrings.
    
* **Win32CryptoKeyring**: for Windows 2k+.
* **CryptedFileKeyring**: a command line interface keyring base on PyCrypto.
* **UncryptedFileKeyring**: a keyring which leaves passwords directly in file.
%endif

%prep
%setup -qn keyring-%{version}
rm -frv keyring.egg-info
# Drop redundant shebangs.
sed -i '1{\@^#!/usr/bin/env python@d}' keyring/cli.py
# Drop slags from upstream of using his own versioning system.
sed -i -e "\@use_vcs_version@s/^.*$/\tversion = \"%{version}\",/g" \
       -e {/\'hgtools\'/d} setup.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
cp -a %{buildroot}%{_bindir}/keyring %{buildroot}%{_bindir}/keyring-%{python3_version}
popd
%endif
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Failed on Koji due to X environment not available.
#%check
#%if 0%{?with_python3}
#pushd %{py3dir}
#%{__python3} setup.py ptr
#nosetests-%{python3_version}
#popd
#%endif
#%{__python2} setup.py ptr
#nosetests

%files
%doc CHANGES.rst README.rst CONTRIBUTORS.txt
%{_bindir}/keyring
%{python2_sitelib}/keyring
%{python2_sitelib}/keyring-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-keyring
%doc CHANGES.rst README.rst CONTRIBUTORS.txt
%{_bindir}/keyring-%{python3_version}
%{python3_sitelib}/keyring-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/keyring
%endif

%changelog

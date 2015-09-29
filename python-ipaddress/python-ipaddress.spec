%global pyname ipaddress

Name:           python-%{pyname}
Version:        1.0.7
Release:        4
Summary:        Port of the python 3.3+ ipaddress module to 2.6+

License:        Python
URL:            https://pypi.python.org/pypi/%{pyname}/%{version}
Source0:        https://pypi.python.org/packages/source/i/%{pyname}/%{pyname}-1.0.7.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

%description
ipaddress provides the capabilities to create, manipulate and operate
on IPv4 and IPv6 addresses and networks.

The functions and classes in this module make it straightforward to
handle various tasks related to IP addresses, including checking
whether or not two hosts are on the same subnet, iterating over all
hosts in a particular subnet, checking whether or not a string
represents a valid IP address or network definition, and so on.

%prep
%setup -q -n %{pyname}-%{version}


%build
%{__python2} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%doc README.txt
%{python2_sitelib}/*


%changelog

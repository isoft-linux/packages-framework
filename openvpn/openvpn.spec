%define plugins down-root auth-pam

Name:              openvpn
Version:           2.3.7
Release:           2
Summary:           A full-featured SSL VPN solution
URL:               http://openvpn.net/
Source0:           http://openvpn.net/release/%{name}-%{version}.tar.gz
Source1:           http://openvpn.net/signatures/%{name}-%{version}.tar.gz.asc

Source2:           roadwarrior-server.conf
Source3:           roadwarrior-client.conf

# Systemd service
Source4:           openvpn@.service
# Tmpfile.d config
Source5:           %{name}-tmpfile.conf

License:           GPLv2
Group:             Applications/Internet
BuildRequires:     systemd-devel
BuildRequires:     lzo-devel
BuildRequires:     openssl-devel
BuildRequires:     pam-devel
BuildRequires:     pkcs11-helper-devel >= 1.11
BuildRequires:     systemd-units
# For /sbin/ip.
BuildRequires:     iproute
# For /sbin/ip.
Requires:          iproute

Requires(pre):     /usr/sbin/adduser
Requires(post):    systemd-units
Requires(preun):   systemd-units
Requires(postun):  systemd-units

# Filter out the perl(Authen::PAM) dependency.
# No perl dependency is really needed at all.
%{?perl_default_filter}

%description
OpenVPN is a robust and highly flexible tunneling application that uses all
of the encryption, authentication, and certification features of the
OpenSSL library to securely tunnel IP networks over a single UDP or TCP
port.  It can use the Marcus Franz Xaver Johannes Oberhumer's LZO library
for compression.

%prep
%setup -q -n %{name}-%{version}%{?prerelease:_%{prerelease}}

sed -i -e 's,%{_datadir}/openvpn/plugin,%{_libdir}/openvpn/plugin,' doc/openvpn.8

# %%doc items shouldn't be executable.
find contrib sample -type f -perm /100 \
    -exec chmod a-x {} \;

%build
%configure \
    --enable-pthread \
    --enable-password-save \
    --enable-iproute2 \
    --with-iproute-path=/sbin/ip \
    --enable-plugins \
    --enable-plugin-down-root \
    --enable-plugin-auth-pam \
    --enable-pkcs11 \
    --enable-x509-alt-username \
    --enable-systemd 
%{__make}

%install

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mkdir -p %{buildroot}%{_unitdir}
install -D -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/

rm -rf %{buildroot}%{_initrddir}

install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

cp %{SOURCE2} %{SOURCE3} sample/sample-config-files/

find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f

# tmpfiles.d
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
install -m 0644 %{SOURCE5} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m 0710 %{buildroot}%{_localstatedir}/run/%{name}/

%pre
getent group openvpn &>/dev/null || groupadd -r openvpn
getent passwd openvpn &>/dev/null || \
    /usr/sbin/adduser -r -g openvpn -s /sbin/nologin -c OpenVPN \
        -d /etc/openvpn openvpn

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable openvpn.service > /dev/null 2>&1 || :
    /bin/systemctl stop openvpn.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
# Normally, we'd try a restart here, but in this case, it could be troublesome.

%files
%doc contrib sample
%{_mandir}/man8/%{name}.8*
%{_sbindir}/%{name}
#%{_datadir}/%{name}/
%{_includedir}/openvpn-plugin.h
%{_libdir}/%{name}/
%{_unitdir}/%{name}@.service
%attr(0710,root,openvpn) %dir %{_localstatedir}/run/%{name}/
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%config %dir %{_sysconfdir}/%{name}/

%changelog

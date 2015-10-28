Summary:        Extension for creating pdf-Files with CUPS
Summary(fr):    Extension de CUPS pour créer des fichiers PDF
Name:           cups-pdf
Version:        2.6.1
Release:        14%{?dist}
URL:            http://www.cups-pdf.de/
License:        GPLv2+

Source0:        http://www.physik.uni-wuerzburg.de/~vrbehr/cups-pdf/src/%{name}_%{version}.tar.gz

# Default value for Out ${DESKTOP}
Patch1:         cups-pdf-conf.patch
# Handle ${DESKTOP} from config
Patch2:         cups-pdf-desktop.patch
# Handle new lines in title
Patch3:         cups-pdf-title.patch
# Fix build warning
Patch4:         cups-pdf-build.patch
# Report error/success in log
Patch5:         cups-pdf-result.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cups-devel

Requires:       ghostscript, cups
Requires(post): %{_bindir}/pgrep
Requires(post): bash coreutils grep sed

# These are the defaults paths defined in config.h
# CUPS-PDF spool directory
%global CPSPOOL   %{_localstatedir}/spool/cups-pdf/SPOOL

# CUPS-PDF output directory
%global CPOUT     %{_localstatedir}/spool/cups-pdf

# CUPS-PDF log directory
%global CPLOG     %{_localstatedir}/log/cups

# CUPS-PDF cups-pdf.conf config file
%global ETCCUPS   %(cups-config --serverroot 2>/dev/null || echo %{_sysconfdir}/cups)

# Additional path to backend directory
%global CPBACKEND %(cups-config --serverbin  2>/dev/null || echo %{_libdir}/cups)/backend


%description
"cups-pdf" is a backend script for use with CUPS - the "Common UNIX Printing
System" (see more for CUPS under http://www.cups.org/). 
"cups-pdf" uses the ghostscript pdfwrite device to produce PDF Files.

This version has been modified to store the PDF files on the Desktop of the 
user. This behavior can be changed by editing the configuration file.

%description -l fr
"cups-pdf" est un script de traitement CUPS - le "Common UNIX Printing System"
(plus d'informations sur CUPS à l'adresse http://www.cups.org/). 
"cups-pdf" utilise ghostscript pour construire des fichiers au format PDF.

Cette version a été modifiée pour produire les fichiers PDF sur le bureau
de l'utilisateur (dossier Desktop du répertoire d'accueil de l'utilisateur).
Ce comportement peut être modifié en éditant le fichier de configuration.


%prep
echo CIBLE = %{name}-%{version}-%{release}
%setup -q -n %{name}-%{version}

%patch1 -p0 -b .oldconf
%patch2 -p0 -b .desktop
%patch3 -p0 -b .title
%patch4 -p0 -b .build
%patch5 -p0 -b .result


%build
pushd src
cc $RPM_OPT_FLAGS -o cups-pdf cups-pdf.c
popd

# Avoid perl dependencies
chmod -x contrib/pstitleiconv-0.2/pstitleiconv
chmod -x contrib/cups-pdf-dispatch-0.1/cups-pdf-dispatch
chmod -x contrib/SELinux-HOWTO/update-module


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{CPBACKEND}
mkdir -p %{buildroot}%{CPSPOOL}
mkdir -p %{buildroot}%{CPOUT}
mkdir -p %{buildroot}%{CPLOG}
mkdir -p %{buildroot}%{CPBACKEND}
mkdir -p %{buildroot}%{ETCCUPS}
mkdir -p %{buildroot}%{_datadir}/cups/model/
install -m644 extra/CUPS-PDF.ppd %{buildroot}%{_datadir}/cups/model/
install -m644 extra/cups-pdf.conf %{buildroot}%{ETCCUPS}/
install -m700 src/cups-pdf %{buildroot}%{CPBACKEND}/


%clean
rm -rf %{buildroot}


%post
(
if [ ! -d "/etc/cups/ppd" ]; then
  mkdir -p /etc/cups/ppd
fi

if [ ! -f "/etc/cups/ppd/CUPS-PDF.ppd" ]; then
  cp /usr/share/cups/model/CUPS-PDF.ppd /etc/cups/ppd/CUPS-PDF.ppd
fi

grep -q "Printer Cups-PDF" /etc/cups/printers.conf

if [ $? -eq 1 ]; then
   cat >> /etc/cups/printers.conf <<EOF
<Printer Cups-PDF>
UUID urn:uuid:e4a01409-204d-31c9-5871-4c10562a3ebb
Info Cups-PDF
DeviceURI cups-pdf:/
State Idle
StateTime 1438211065
ConfigTime 1441188293
Type 8388612
Accepting Yes
Shared Yes
JobSheets none none
QuotaPeriod 0
PageLimit 0
KLimit 0
OpPolicy default
ErrorPolicy stop-printer
</Printer>
EOF
fi
) ||:

%postun
if [ "$1" -eq "0" ]; then
  rm -rf /etc/cups/ppd/CUPS-PDF.ppd
  # Delete the printer
  line_num=1
  
  start_line_num=-1
  end_line_num=-1
  
  while read line 
  do
    if [ "$line"x = "<Printer Cups-PDF>"x ]; then
      start_line_num=$line_num
    fi
    if [ $start_line_num -ne -1 ]; then
      if [ "$line"x = "</Printer>"x ]; then
        end_line_num=$line_num
        break
      fi
    fi
    line_num=`expr $line_num + 1`
  done </etc/cups/printers.conf
  
  sed -i $start_line_num','$end_line_num'd' /etc/cups/printers.conf
fi ||:


%files
%defattr(-,root,root)
%doc ChangeLog COPYING README contrib/
%dir %{CPSPOOL}
%dir %{CPOUT}
%attr(700, root, root) %{CPBACKEND}/cups-pdf
%config(noreplace) %{ETCCUPS}/cups-pdf.conf
%{_datadir}/cups/model/CUPS-PDF.ppd

%changelog
* Mon Oct 26 2015 cjacker - 2.6.1-14
- Do not use lpadmin add or delete printer, use script instread.

* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 2.6.1-11
- Rebuild for new 4.0 release.


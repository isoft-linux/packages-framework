%global filippov_version 1.0.7pre44
%global fontdir %{_datadir}/fonts/default/Type1
%global catalogue /etc/X11/fontpath.d

Summary: Free versions of the 35 standard PostScript fonts.
Name: urw-fonts
Version: 2.4
Release: 23%{?dist}
Source: %{name}-%{filippov_version}.tar.bz2
URL: http://svn.ghostscript.com/ghostscript/tags/urw-fonts-1.0.7pre44/
# URW holds copyright, No version specified
License: GPL+
BuildArch: noarch
Requires(post): fontconfig
Requires(post): xorg-x11-font-utils
Requires(postun): fontconfig
Epoch: 3

%description 
Free good quality versions of the 35 standard PostScript(TM) fonts,
donated under the GPL by URW++ Design and Development GmbH.

Install the urw-fonts package if you need free versions of standard
PostScript fonts.

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{fontdir}
install -m 0644 *.afm *.pfb $RPM_BUILD_ROOT%{fontdir}/

# Touch ghosted files
touch $RPM_BUILD_ROOT%{fontdir}/{fonts.{dir,scale,cache-1},encodings.dir}

# Install catalogue symlink
mkdir -p $RPM_BUILD_ROOT%{catalogue}
ln -sf %{fontdir} $RPM_BUILD_ROOT%{catalogue}/fonts-default

%post
{
   umask 133
   mkfontscale %{fontdir} || :
   mkfontdir %{fontdir} || :
   fc-cache %{fontdir}
} &> /dev/null || :

%postun
{
   if [ "$1" = "0" ]; then
      fc-cache %{fontdir}
   fi
} &> /dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc COPYING README README.tweaks
%dir %{_datadir}/fonts/default
%dir %{fontdir}
%{catalogue}/fonts-default
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.dir
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.scale
%ghost %verify(not md5 size mtime) %{fontdir}/fonts.cache-1
%ghost %verify(not md5 size mtime) %{fontdir}/encodings.dir
%{fontdir}/*.afm
%{fontdir}/*.pfb

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 3:2.4-23
- Rebuild for new 4.0 release.

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 3:2.4-22
- Initial build. 


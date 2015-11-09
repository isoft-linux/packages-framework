%define _kde4_prefix %_prefix
%define _kde4_sysconfdir %_sysconfdir
%define _kde4_libdir %_libdir
%define _kde4_libexecdir %_libexecdir/kde4
%define _kde4_datadir %_datadir
%define _kde4_sharedir %_datadir
%define _kde4_iconsdir %_kde4_sharedir/icons
%define _kde4_configdir %_kde4_sharedir/config
%define _kde4_appsdir %_kde4_sharedir/kde4/apps
%define _kde4_docdir %_kde4_prefix/share/doc
%define _kde4_bindir %_kde4_prefix/bin
%define _kde4_sbindir %_kde4_prefix/sbin
%define _kde4_includedir %_kde4_prefix/include/kde4
%define _kde4_buildtype release
%define _kde4_macros_api 2

%define rpm_macros_dir %{_rpmconfigdir}/macros.d

Summary: KDE filesystem layout
Name: kde-filesystem
Version: 4
Release: 53%{?dist}

License: Public Domain
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# noarch->arch transition
Obsoletes: kde-filesystem < 4-36

# teamnames (locales) borrowed from kde-i18n packaging
Source1: teamnames

Source2: macros.kde4
# increment whenever dirs change in an incompatible way
# kde4 apps built using macros.kde4 should

Source3: applnk-hidden-directory

Provides: kde4-macros(api) = %{_kde4_macros_api} 

BuildRequires: gawk

Requires:  filesystem
Requires:  rpm

%description
This package provides some directories that are required/used by KDE. 


%prep


%build


%install
rm -f $RPM_BUILD_DIR/%{name}.list
rm -rf $RPM_BUILD_ROOT

## KDE3 
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/kde/{env,shutdown,kdm}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/{applications/kde,applnk,apps,autostart,config,config.kcfg,emoticons,mimelnk,services,servicetypes,templates,source}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/apps/konqueror/servicemenus
# not sure who best should own locolor, so we'll included it here, for now. -- Rex
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/locolor/{16x16,22x22,32x32,48x48}/{actions,apps,mimetypes}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applnk/{.hidden,Applications,Edutainment,Graphics,Internet,Settings,System,Toys,Utilities}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mimelnk/{all,application,audio,fonts,image,inode,interface,media,message,model,multipart,print,text,uri,video}
# do qt3 too?
# mkdir -p $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}/qt-3.3/plugins
mkdir -p $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}/kde3/plugins
mkdir -p $RPM_BUILD_ROOT%{_docdir}/HTML/en

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
 mkdir -p $RPM_BUILD_ROOT%{_docdir}/HTML/${locale}/common
 # do docs/common too, but it could be argued that apps/pkgs using or
 # depending on is a bug -- Rex
 mkdir -p $RPM_BUILD_ROOT%{_docdir}/HTML/${locale}/docs/
 ln -s ../common $RPM_BUILD_ROOT%{_docdir}/HTML/${locale}/docs/common
 echo "%lang($locale) %{_docdir}/HTML/$locale/" >> %{name}.list
done

# internal services shouldn't be displayed in menu
install -p -m644 -D %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/applnk/.hidden/.directory

## KDE4
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm \
         $RPM_BUILD_ROOT%{_kde4_sysconfdir}/kde/{env,shutdown,kdm} \
         $RPM_BUILD_ROOT%{_kde4_includedir} \
         $RPM_BUILD_ROOT%{_kde4_libexecdir} \
         $RPM_BUILD_ROOT%{_kde4_appsdir}/color-schemes \
         $RPM_BUILD_ROOT%{_kde4_appsdir}/solid/actions \
         $RPM_BUILD_ROOT%{_kde4_datadir}/applications/kde4 \
         $RPM_BUILD_ROOT%{_kde4_datadir}/{autostart,wallpapers} \
         $RPM_BUILD_ROOT%{_kde4_configdir} \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/config.kcfg \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/emoticons \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/kde4/services/ServiceMenus \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/kde4/servicetypes \
         $RPM_BUILD_ROOT%{_kde4_sharedir}/templates/.source \
         $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/{16x16,22x22,32x32,48x48}/{actions,apps,mimetypes} \
         $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/en/common
# do qt4 too?
# mkdir -p $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}/qt4/plugins
mkdir -p $RPM_BUILD_ROOT%{_kde4_prefix}/{lib,%{_lib}}/kde4/plugins/{gui_platform,styles}

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
  mkdir -p $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/${locale}/common
  echo "%lang($locale) %{_kde4_docdir}/HTML/$locale/" >> %{name}.list
done

# rpm macros
mkdir -p $RPM_BUILD_ROOT%{rpm_macros_dir}
cat >$RPM_BUILD_ROOT%{rpm_macros_dir}/macros.kde4<<EOF
%%_kde4_prefix %%_prefix
%%_kde4_sysconfdir %%_sysconfdir
%%_kde4_libdir %%_libdir
%%_kde4_libexecdir %%_libexecdir/kde4
%%_kde4_datadir %%_datadir
%%_kde4_sharedir %%_datadir
%%_kde4_iconsdir %%_kde4_sharedir/icons
%%_kde4_configdir %%_kde4_sharedir/config
%%_kde4_appsdir %%_kde4_sharedir/kde4/apps
%%_kde4_docdir %_kde4_prefix/share/doc
%%_kde4_bindir %%_kde4_prefix/bin
%%_kde4_sbindir %%_kde4_prefix/sbin
%%_kde4_includedir %%_kde4_prefix/include/kde4
%%_kde4_buildtype %_kde4_buildtype
%%_kde4_macros_api %_kde4_macros_api
EOF
cat %{SOURCE2} >> $RPM_BUILD_ROOT%{rpm_macros_dir}/macros.kde4

## Plasma5, forward compatibility
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/plasma-workspace/{env,shutdown}


%clean
rm -rf $RPM_BUILD_ROOT %{name}.list


%files -f %{name}.list
%defattr(-,root,root,-)

# KDE3
%{_sysconfdir}/kde/
%{_datadir}/applications/kde/
%{_datadir}/applnk/
%{_datadir}/apps/
%{_datadir}/autostart/
%{_datadir}/config/
%{_datadir}/config.kcfg/
%{_datadir}/emoticons/
%{_datadir}/icons/locolor
%{_datadir}/mimelnk/
%{_datadir}/services/
%{_datadir}/servicetypes/
%{_datadir}/templates/
%{_prefix}/lib/kde3/
%{_prefix}/%{_lib}/kde3/
%dir %{_docdir}/HTML/
%lang(en) %{_docdir}/HTML/en/

# KDE4
%{rpm_macros_dir}/macros.kde4
%{_kde4_sysconfdir}/kde/
%{_kde4_libexecdir}/
%{_kde4_includedir}/
%{_kde4_appsdir}/
%{_kde4_configdir}/
%{_kde4_sharedir}/config.kcfg/
%{_kde4_sharedir}/emoticons/
%{_kde4_sharedir}/kde4/
%{_kde4_sharedir}/templates/
%{_kde4_datadir}/applications/kde4/
%{_kde4_datadir}/autostart/
%{_kde4_datadir}/icons/locolor/
%{_kde4_datadir}/wallpapers/
%{_kde4_prefix}/lib/kde4/
%{_kde4_prefix}/%{_lib}/kde4/
%dir %{_kde4_docdir}/HTML/
%lang(en) %{_kde4_docdir}/HTML/en/

# Plasma5
%{_sysconfdir}/xdg/plasma-workspace/


%changelog
* Mon Nov 09 2015 Cjacker <cjacker@foxmail.com> - 4-53
- Remove Group from spec


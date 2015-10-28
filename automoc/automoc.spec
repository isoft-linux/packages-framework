#define snaptag .20080527svn811390
%define beta 0.9.88
%define beta_tag rc3

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Name:           automoc
Version:        1.0
Release:        0.25.%{?beta_tag}%{?dist}
Summary:        Automatic moc for Qt 4
Group:          Development/Tools
License:        BSD
URL:            http://www.kde.org
Source0:        ftp://ftp.kde.org/pub/kde/stable/automoc4/%{beta}/automoc4-%{beta}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstream patches
Patch1: 0001-fix-make-clean-it-s-SET_directory_properties-and-not.patch
Patch2: 0002-automoc-did-not-understand-.mm-files-objc.patch
Patch3: 0003-support-for-Objective-C-i.e.-mm-files-is-enough-to-i.patch
Patch4: 0004-auto-detect-case-insensitive-filesystem-on-OSX.patch
Patch5: 0005-add-a-ctest-config-file-see-http-my.cdash.org-index..patch
Patch6: 0006-support-for-nightly-builds-at-http-my.cdash.org-inde.patch
Patch7: 0007-rename-AutomocNightly.cmake-to-Automoc4Nightly-to-ma.patch
Patch8: 0008-chaneg-nightly-time.patch
Patch9: 0009-remove-the-warnings-again.patch
Patch10: 0010-add-some-comments.patch
Patch11: 0011-adapt-this-to-the-new-enhanced-KDECTestNightly.cmake.patch
Patch12: 0012-support-installing-in-the-nightly-build.patch
Patch13: 0013-add-documentation.patch
Patch14: 0014-first-attempt-at-cpack-ing-a-KDE-package-works-on-OS.patch
Patch15: 0015-put-the-apple-specific-stuff-in-here.patch
Patch16: 0016-move-the-cpack-bits-into-a-separate-cmake-file.patch
Patch17: 0017-Compile-and-link-on-Mac.patch
Patch18: 0018-Fix-framework-detection-on-Mac-where-Qt-is-installed.patch
Patch19: 0019-kdesupport-automoc-krazy2-fixes.patch
Patch20: 0020-Hack-the-hack.patch
Patch21: 0021-fix-stupid-typo.patch
Patch22: 0022-CMake-2.6.4-is-required-because-older-versions-don-t.patch
Patch23: 0023-Reverting-r1140777-as-causing-some-nasty-cmake-funky.patch
Patch24: 0024-add-cmake_policy-PUSH-POP-to-save-and-restore-the-or.patch
Patch25: 0025-allow-duplicate-target-names-also-in-the-automoc-mac.patch
Patch26: 0026-Fix-cmake_policy-call.patch
Patch27: 0027-add-some-changes-to-build-automoc-statically.patch
Patch28: 0028-AutoMoc-lazyInit-expects-the-app-to-get-6-parameter-.patch
Patch29: 0029-Fix-missing-include-dirs-current-source-and-build-di.patch
Patch30: 0030-Don-t-attempt-to-read-the-DEFINITIONS-property.patch
Patch31: 0031-Don-t-attempt-to-add-dependencies-which-do-not-exist.patch
Patch32: 0032-set-cmake_min_req-to-enable-newer-policies.patch
Patch33: 0033-cmake-2.8.9-sets-CMP0003-to-NEW-clean-up.patch

Provides: automoc4 = %{beta}

Requires:       cmake >= 2.8.9
BuildRequires:  cmake >= 2.8.9
BuildRequires:  qt4-devel
BuildRequires: kde-filesystem
%description
This package contains the automoc4 binary which is used to run moc on the
right source files in a Qt 4 or KDE 4 application.
Moc is the meta object compiler which is a widely used tool with Qt and
creates standard C++ files to provide syntactic sugar of the signal/slots
mechanism.


%prep
%autosetup -p1 -n automoc4-%{beta}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/automoc4
%{_kde4_libdir}/automoc4/


%changelog
* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 1.0-0.25.rc3
- Update


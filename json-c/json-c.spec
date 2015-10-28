%global reldate 20140410

Name:           json-c
Version:        0.12
Release:        7
Summary:        A JSON implementation in C
License:        MIT
URL:            https://github.com/json-c/json-c/wiki
Source0:        https://github.com/json-c/json-c/archive/json-c-%{version}-%{reldate}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%description
JSON-C implements a reference counting object model that allows you to easily
construct JSON objects in C, output them as JSON formatted strings and parse
JSON formatted strings back into the C representation of JSON objects.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn json-c-json-c-%{version}-%{reldate}
# Get rid of maintainer mode cflags.
sed -i 's|-Werror ||g' Makefile.am.inc
# Postponed.
# Bump the soname manually.
# sed -i 's#2:1:0#3:0:0#' Makefile.am

for doc in ChangeLog; do
 iconv -f iso-8859-1 -t utf8 $doc > $doc.new &&
 touch -r $doc $doc.new &&
 mv $doc.new $doc
done

%build
# Get rid of rpath.
autoreconf -fiv
%configure --enable-shared --disable-static --disable-rpath --enable-rdrand
%make_build

%install
%make_install

# Get rid of la files
find %{buildroot} -name '*.la' -delete -print

%check
make check

%pretrans devel -p <lua>
path = "%{_includedir}/json-c"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/libjson-c.so.*

%files devel
%doc AUTHORS ChangeLog README README.html
%{_includedir}/json-c/
%{_libdir}/libjson-c.so
%{_libdir}/pkgconfig/json-c.pc
%doc doc/html/*

%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.12-7
- Rebuild for new 4.0 release.


Name:           libgee
Version:        0.18.0
Release:        2
Summary:        GObject collection library

License:        LGPLv2+
URL:            http://live.gnome.org/Libgee
#VCS:           git:git://git.gnome.org/libgee
Source0:        http://download.gnome.org/sources/libgee/0.14/libgee-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
# Bootstrap requirements
BuildRequires:  autoconf automake libtool
BuildRequires:  vala >= 0.23.2

%description
libgee is a collection library providing GObject-based interfaces and
classes for commonly used data structures.

* Traversable
  o Iterable
    + Collection
      - List
        * BidirList
      - Set
        * SortedSet
          o BidirSortedSet
      - MultiSet
      - Queue
        * Deque
    + Map
      - SortedMap
        * BidirSortedMap
  o Iterator
    + BidirIterator
      - BidirListIterator
    + ListIterator
      - BidirListIterator
* MultiMap

The ArrayList, ArrauQueue, ConcurrentLinkedList, ConcurrentSet, HashSet,
HashMap, HashMultiSet, HashMultiMap, LinkedList, PriorityQueue, TreeSet,
TreeMap, TreeMultiSet, and TreeMultiMap classes provide a reasonable sample
implementation of those interfaces. In addition, a set of abstract
classes are provided to ease the implementation of new collections.

Around that, the API provide means to retrieve read-only views,
efficient sort algorithms, simple, bi-directional or index-based mutable
iterators depending on the collection type.

Libgee is written in Vala and can be used like any GObject-based C
library. It's planned to provide bindings for further languages.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%build
(if ! test -x configure; then
    NOCONFIGURE=1 ./autogen.sh;
    CONFIGFLAGS=--enable-gtk-doc;
 fi;
 %configure --disable-static $CONFIGFLAGS
)
make %{?_smp_mflags}


%check
make check


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING MAINTAINERS NEWS README
%{_libdir}/*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Gee-0.8.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gee-0.8.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Gee-0.8.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gee-0.8.vapi


%changelog
* Sat Oct 24 2015 Cjacker <cjacker@foxmail.com> - 0.18.0-2
- Rebuild for new 4.0 release.


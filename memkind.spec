#
# Conditional build:
%bcond_without	ndctl	# daxctl support

Summary:	User Extensible Heap Manager
Summary(pl.UTF-8):	Rozszerzalny zarządca sterty
Name:		memkind
Version:	1.10.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/memkind/memkind/releases
Source0:	https://github.com/memkind/memkind/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	30a59aec4c79a2504b6c0ec0ec5a070e
URL:		http://memkind.github.io/memkind
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
%{?with_ndctl:BuildRequires:	daxctl-devel >= 66}
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	numactl-devel
BuildRequires:	unzip
%{?with_ndctl:Requires:	daxctl-libs >= 66}
ExclusiveArch:	%{x8664} ppc64 ppc64le s390x aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The memkind library is an user extensible heap manager built on top of
jemalloc which enables control of memory characteristics and a
partitioning of the heap between kinds of memory. The kinds of memory
are defined by operating system memory policies that have been applied
to virtual address ranges. Memory characteristics supported by memkind
without user extension include control of NUMA and page size features.
The jemalloc non-standard interface has been extended to enable
specialized arenas to make requests for virtual memory from the
operating system through the memkind partition interface. Through the
other memkind interfaces the user can control and extend memory
partition features and allocate memory while selecting enabled
features.

%description -l pl.UTF-8
Biblioteka memkind to rozserzalny zarządca sterty, zbudowany w oparciu
o bibliotekę jemalloc, pozwalający kontrolować charakterystykę pamięci
i partycjonowanie sterty pomiędzy różne rodzaje pamięci. Rodzaje
pamięci są definiowane przez polityki pamięci systemu operacyjnego
nałożone na przedziały adresów wirtualnych. Charakterystyki pamięci
obsługiwane przez memkind bez rozszerzania przez użytkownika obejmują
sterowanie NUMA oraz rozmiary stron. Niestandardowy interfejs jemalloc
został rozszerzony, aby pozwolić specjalizowanym arenom wykonywać
żądania pamięci wirtualnej z systemu operacyjnego poprzez interfejs
partycjonowania memkind. Przez inne interfejsy memkind użytkownik może
sterować i rozszerzać możliwości partycjonowania, a także przydzielać
pamięć wybierając określone cechy.

%package devel
Summary:	Header files for Memkind User Extensible Heap Manager libraries
Summary(pl.UTF-8):	Pliki nagłówkowe Memkind - bibliotek rozszerzalnego zarządcy sterty
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_ndctl:Requires:	daxctl-devel >= 66}
BuildRequires:	numactl-devel

%description devel
Header files for Memkind User Extensible Heap Manager library.

%description devel -l pl.UTF-8
Pliki nagłówkowe Memkind - biblioteki rozszerzalnego zarządcy sterty.

%package static
Summary:	Static Memkind libraries
Summary(pl.UTF-8):	Statyczne biblioteki Memkind
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Memkind libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Memkind.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_ndctl:--disable-daxctl} \
	--enable-decorators \
	--disable-silent-rules \
	--enable-tls

%{__make}

%{__make} checkprogs

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/memkind

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/memkind-auto-dax-kmem-nodes
%attr(755,root,root) %{_bindir}/memkind-hbw-nodes
%attr(755,root,root) %{_libdir}/libmemkind.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmemkind.so.0
%attr(755,root,root) %{_libdir}/libautohbw.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libautohbw.so.0
%{_mandir}/man1/memkind-auto-dax-kmem-nodes.1*
%{_mandir}/man1/memkind-hbw-nodes.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmemkind.so
%attr(755,root,root) %{_libdir}/libautohbw.so
%{_includedir}/hbw_allocator.h
%{_includedir}/hbwmalloc.h
%{_includedir}/memkind.h
%{_includedir}/memkind_allocator.h
%{_includedir}/memkind_deprecated.h
%{_includedir}/pmem_allocator.h
%{_pkgconfigdir}/memkind.pc
%{_mandir}/man3/hbwmalloc.3*
%{_mandir}/man3/hbwallocator.3*
%{_mandir}/man3/pmemallocator.3*
%{_mandir}/man3/memkind*.3*
%{_mandir}/man7/autohbw.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libmemkind.a
%{_libdir}/libautohbw.a

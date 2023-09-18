#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Disassembler for the x86 and x86-64 class of instruction set architectures
Summary(pl.UTF-8):	Disasembler dla architektur z instrukcjami x86 i x86-64
Name:		udis86
Version:	1.7.2
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/vmt/udis86/tags
Source0:	https://github.com/vmt/udis86/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bb301006bf1087a4328ef153719e69d6
Patch0:		%{name}-ax_prog_sphinx_version.patch
Patch1:		%{name}-python3.patch
URL:		https://github.com/vmt/udis86
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
%{?with_apidocs:BuildRequires:	sphinx-pdg >= 1.1.3}
BuildRequires:	yasm >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Udis86 is a disassembler for the x86 and x86-64 class of instruction
set architectures. It consists of a C library called libudis86 which
provides a clean and simple interface to decode a stream of raw binary
data, and to inspect the disassembled instructions in a structured
manner.

%description -l pl.UTF-8
Udis86 to disasembler dla architektur z instrukcjami x86 i x86-64.
Składa się z biblioteki C o nazwie libudis86, dostarczającej czysty i
prosty interfejs do dekodowania strumienia surowych danych binarnych i
podglądania zdisasemblowanych instrukcji w sposób strukturalny.

%package devel
Summary:	Header files for libudis86 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libudis86
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libudis86 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libudis86.

%package static
Summary:	Static libudis86 library
Summary(pl.UTF-8):	Statyczna biblioteka libudis86
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libudis86 library.

%description static -l pl.UTF-8
Statyczna biblioteka libudis86.

%package apidocs
Summary:	API documentation for libudis86 library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libudis86
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libudis86 library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libudis86.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d build/m4
%{__libtoolize}
%{__aclocal} -I build/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared \
	%{!?with_static_libs:--disable-static} \
	--with-python="%{__python3}"
%{__make}

%if %{with apidocs}
%{__make} html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libudis86.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README
%attr(755,root,root) %{_bindir}/udcli
%attr(755,root,root) %{_libdir}/libudis86.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libudis86.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudis86.so
%{_includedir}/udis86.h
%{_includedir}/libudis86

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libudis86.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/manual/html/{_static,*.html,*.js}
%endif

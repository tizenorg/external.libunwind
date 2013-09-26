#
# spec file for package libunwind
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           libunwind
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pkgconfig
Url:            http://savannah.nongnu.org/projects/libunwind/
Summary:        Unwind Library
License:        MIT
Group:          System/Base
Version:        1.1
Release:        0
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
ExclusiveArch:  %ix86 ia64 x86_64 %arm ppc ppc64

Patch0:		dwarf_order.patch
Patch1:		x86_accessmem.patch
Patch2:		dwarf_memleak.patch
Patch3:		fix_symlink.patch
Patch4:		fix_builderror.patch
Patch5:		fix_unwindinfo_free.patch
Patch6:		disable_UNW_ARM_METHOD_FRAME.patch

%description
A portable and efficient C programming interface (API) to determine the
call chain of a program.



Authors:
--------
    David Mosberger <David.Mosberger@acm.org>

%package devel
Summary:        Unwind library
Group:          Development/Libraries/C and C++
Requires:       libunwind = %{version}-%{release}
Provides:       libunwind:%{_libdir}/libunwind.so

%description devel
A portable and efficient C programming interface (API) to determine the
call-chain of a program.



Authors:
--------
    David Mosberger <davidm@hpl.hp.com>

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
autoreconf -fi
export CFLAGS="-O2 -g -U_FORTIFY_SOURCE "
%configure
make %{?_smp_mflags}

%check
%if ! 0%{?qemu_user_space_build:1}
#make -k check || :
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f "%buildroot/%_libdir"/*.la
mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libunwind.so.8* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/libunwind.so.8 $RPM_BUILD_ROOT%{_libdir}/libunwind.so
# Check that ln did not create a dangling link
stat "%buildroot"/$(readlink -f "%buildroot/%_libdir/libunwind.so");

mkdir -p %{buildroot}/usr/share/license
cp COPYING %{buildroot}/usr/share/license/%{name}
cat LICENSE >> %{buildroot}/usr/share/license/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
/%_lib/lib*
%{_libdir}/lib*.so.*
%{_libdir}/libunwind.so
/usr/share/license/%{name}

%files devel
%defattr(-, root, root)
%{_prefix}/include/*
%{_libdir}/lib*.a
%{_libdir}/libunwind-*.so
%{_libdir}/pkgconfig/libunwind-generic.pc
%{_libdir}/pkgconfig/libunwind-ptrace.pc
%{_libdir}/pkgconfig/libunwind-setjmp.pc
%{_libdir}/pkgconfig/libunwind.pc
%ifarch %arm %ix86 x86_64
%{_libdir}/pkgconfig/libunwind-coredump.pc
%endif
%doc %{_mandir}/man?/*

%changelog

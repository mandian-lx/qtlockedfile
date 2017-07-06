%define upstream_version 2.4_1
%define version %(echo %{upstream_version} | sed 's,_,.,')

%define major	1
%define libname	%mklibname %{name} %{version}
%define devname	%mklibname %{name} -d

Summary:	QFile extension with advisory locking functions
Name:		qtlockedfile
Version:	%{version}
Release:	11
Group:		Development/KDE and Qt
License:	GPLv3 or LGPLv2 with exceptions
Url:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtlockedfile
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/%{name}-%{upstream_version}-opensource.tar.gz
Source1:	qtlockedfile.prf
# (Fedora) don't build examples
Patch0:		qtlockedfile-dont-build-example.patch
# (Fedora) Remove unnecessary linkage to libQtGui
Patch1:		qtlockedfile-dont-link-qtgui.patch
BuildRequires:	qt5-devel

%description
This class extends the QFile class with inter-process file locking
capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.

%package	-n %{libname}
Summary:	QFile extension with advisory locking functions
Group:		Development/KDE and Qt
Requires:	qt5-common

%description	-n %{libname}
This class extends the QFile class with inter-process file locking
capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.

This is the library package for %{name}

%package	-n %{devname}
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description	-n %{devname}
This package contains libraries and header files for developing applications
that use QtLockedFile.

%prep
%setup -qn %{name}-%{upstream_version}-opensource
%apply_patches

%build
touch .licenseAccepted
# Does not use GNU configure
./configure -library
%qmake_qt5
%make

%install
# libraries
mkdir -p %{buildroot}%{_qt5_libdir}
cp -a lib/* %{buildroot}%{_qt5_libdir}

# headers
mkdir -p %{buildroot}%{_qt5_includedir}/QtSolutions
cp -a \
    src/qtlockedfile.h \
    src/QtLockedFile \
    %{buildroot}%{_qt5_includedir}/QtSolutions

mkdir -p %{buildroot}%{_qt5_libdir}/mkspecs/features
cp -a %{SOURCE1} %{buildroot}%{_qt5_libdir}/mkspecs/features/

%files -n %{libname}
%{_qt5_libdir}/lib*.so.%{major}*

%files -n %{devname}
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%doc doc example
%{_qt5_libdir}/lib*.so
%{_qt5_includedir}/QtSolutions
%{_qt5_libdir}/mkspecs/features/%{name}.prf


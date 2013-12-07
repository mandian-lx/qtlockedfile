%define upstream_version 2.4_1
%define version %(echo %{upstream_version} | sed 's,_,.,')

%define major		1
%define libname		%mklibname %name %version
%define develname	%mklibname %name -d

Summary:	QFile extension with advisory locking functions
Name:		qtlockedfile
Version:	%{version}
Release:	6
Group:		Development/KDE and Qt
License:	GPLv3 or LGPLv2 with exceptions
URL:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtlockedfile
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/%{name}-%{upstream_version}-opensource.tar.gz
Source1:	qtlockedfile.prf
# (Fedora) don't build examples
Patch0:		qtlockedfile-dont-build-example.patch
# (Fedora) Remove unnecessary linkage to libQtGui
Patch1:		qtlockedfile-dont-link-qtgui.patch
BuildRequires:	qt4-devel

%description
This class extends the QFile class with inter-process file locking
capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.

%package	-n %libname
Summary:	QFile extension with advisory locking functions
Group:		Development/KDE and Qt
Requires:	qt4-common

%description	-n %libname
This class extends the QFile class with inter-process file locking
capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.

This is the library package for %{name}

%package	-n %develname
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}

%description	-n %develname
This package contains libraries and header files for developing applications
that use QtLockedFile.

%prep
%setup -q -n %{name}-%{upstream_version}-opensource
%patch0 -p1 -b .no-example
%patch1 -p1 -b .dont-link-qtgui

%build
touch .licenseAccepted
# Does not use GNU configure
./configure -library
%qmake_qt4
%make

%install
# libraries
mkdir -p %{buildroot}%{qt4lib}
cp -a lib/* %{buildroot}%{qt4lib}

# headers
mkdir -p %{buildroot}%{qt4include}/QtSolutions
cp -a \
    src/qtlockedfile.h \
    src/QtLockedFile \
    %{buildroot}%{qt4include}/QtSolutions

mkdir -p %{buildroot}%{qt4dir}/mkspecs/features
cp -a %{SOURCE1} %{buildroot}%{qt4dir}/mkspecs/features/

%files -n %libname
%defattr(-,root,root,-)
%{qt4lib}/lib*.so.%{major}*

%files -n %develname
%defattr(-,root,root,-)
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%doc doc example
%{qt4lib}/lib*.so
%{qt4include}/QtSolutions
%{qt4dir}/mkspecs/features/%{name}.prf



%changelog
* Tue Nov 22 2011 Alexander Khrukin <akhrukin@mandriva.org> 2.4.1-2
+ Revision: 732376
- imported package qtlockedfile


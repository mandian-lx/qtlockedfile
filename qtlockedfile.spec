%define commit 1fca9c330d8548d84fccb66407fbaf3aae122d17
%define shortcommit %(c=%{commit}; echo ${c:0:7})

%define project_name qt-solutions

%define upstream_version 2.4_1
%define version %(echo %{upstream_version} | sed 's,_,.,')

%define major	1
%define libname	%mklibname %{name} %{version}
%define devname	%mklibname %{name} -d

Summary:	QFile extension with advisory locking functions
Name:		qtlockedfile
Version:	%{version}
Release:	12
Group:		Development/KDE and Qt
License:	BSD
Url:		https://github.com/qtproject/qt-solutions/
Source0:	https://github.com/qtproject/qt-solutions/archive/%{commit}/%{project_name}-%{commit}.tar.gz
Source1:	qtlockedfile.prf
# (Fedora) don't build examples
Patch0:		qtlockedfile-dont-build-example.patch

BuildRequires:	qt5-devel

%description
This class extends the QFile class with inter-process file locking
capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	QFile extension with advisory locking functions
Group:		Development/KDE and Qt

%description -n %{libname}
This class extends the QFile class with inter-process file locking
capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.

This is the library package for %{name}

%files -n %{libname}
%{_qt5_libdir}/lib*.so.%{major}*

#--------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description	-n %{devname}
This package contains libraries and header files for developing applications
that use QtLockedFile.

%files -n %{devname}
%doc README.TXT
%doc doc example
%{_qt5_libdir}/lib*.so
%{_qt5_includedir}/QtSolutions
%{_qt5_libdir}/qt5/mkspecs/features/%{name}.prf

#--------------------------------------------------------------------

%prep
%setup -q -n %{project_name}-%{commit}/%{name}
%apply_patches

# fix incoherent-version-in-name
sed -i -e 's|-head|-%{version}|g' common.pri
sed -i -e 's|-head|-%{version}$|g' %{SOURCE1}

%build
# Accept license
touch .licenseAccepted

# Does not use GNU configure
./configure -library
%qmake_qt5
%make

%install
# libraries
install -dm 0755 %{buildroot}%{_qt5_libdir}/
cp -a lib/* %{buildroot}%{_qt5_libdir}/

# headers
install -dm 0755 %{buildroot}%{_qt5_includedir}/QtSolutions/
install -pm 0644 src/QtLockedFile %{buildroot}%{_qt5_includedir}/QtSolutions/
install -pm 0644 src/qtlockedfile.h %{buildroot}%{_qt5_includedir}/QtSolutions/

install -dm 0755 %{buildroot}%{_qt5_libdir}/qt5/mkspecs/features
install -pm 0644 %{SOURCE1} %{buildroot}%{_qt5_libdir}/qt5/mkspecs/features/


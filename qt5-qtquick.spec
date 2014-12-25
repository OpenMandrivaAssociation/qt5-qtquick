%define api 5
%define major %api

%define api 5
%define qtminor 4
%define qtsubminor 0

%define major_private 1
%define qtversion %{api}.%{qtminor}.%{qtsubminor}

%define qtdeclarative %mklibname qt%{api}declarative %{major}
%define qtdeclaratived %mklibname qt%{api}declarative -d
%define qtdeclaratived_p_d %mklibname qt%{api}declarative-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

%define qttarballdir qtquick1-opensource-src-%{qtversion}

Name:		qt5-qtquick
Version:	%{qtversion}
Release:	1
Summary:	Qt GUI toolkit
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt-project.org
Source0:	http://download.qt-project.org/official_releases/qt/%{api}.%{qtminor}/%{version}/submodules/%{qttarballdir}.tar.xz
BuildRequires:	qt5-qtbase-devel = %{version}
BuildRequires:	pkgconfig(Qt5Script) = %{version}
BuildRequires:	pkgconfig(Qt5Core) = %{version}
BuildRequires:	pkgconfig(Qt5Gui) = %{version}
BuildRequires:	pkgconfig(Qt5Widgets) = %{version}
BuildRequires:	qt5-qtscript-private-devel = %{version}
BuildRequires:	qt5-qtscripttools-private-devel = %{version}

%description
Qt GUI toolkit

#------------------------------------------------------------------------------

%package qmlviewer
Summary: Qt%{api} Qmlviewer Utility
Group: Development/KDE and Qt

%description qmlviewer
Qt%{api} Qmlviewer Utility.

This a tool for loading QML documents that makes it easy to quickly 
develop and debug QML applications.

%files qmlviewer
%{_qt5_bindir}/qmlviewer
%{_qt5_bindir}/qml1plugindump
%{_qt5_importdir}/*
%{_qt5_plugindir}/qml1tooling/libqmldbg_inspector.so
%{_qt5_plugindir}/qml1tooling/libqmldbg_tcp_qtdeclarative.so

#------------------------------------------------------------------------------
%package -n %{qtdeclarative}
Summary: Qt%{api} Lib
Group: System/Libraries

%description -n %{qtdeclarative}
Qt%{api} Lib.

%files -n %{qtdeclarative}
%{_qt5_libdir}/libQt5Declarative.so.%{api}*

#------------------------------------------------------------------------------

%package -n %{qtdeclaratived}
Summary: Devel files needed to build apps based on QtVersit
Group:    Development/KDE and Qt
Requires: %{qtdeclarative} = %version
Requires: qt5-qtbase-devel = %version

%description -n %{qtdeclaratived}
Devel files needed to build apps based on QtVersit.

%files -n %{qtdeclaratived}
%{_qt5_libdir}/libQt5Declarative.prl
%{_qt5_libdir}/libQt5Declarative.so
%{_qt5_libdir}/pkgconfig/Qt5Declarative.pc
%{_qt5_includedir}/QtDeclarative
%exclude %{_qt5_includedir}/QtDeclarative/%qtversion
%{_qt5_libdir}/cmake/Qt5Declarative/Qt5DeclarativeConfig.cmake
%{_qt5_libdir}/cmake/Qt5Declarative/Qt5DeclarativeConfigVersion.cmake
%{_qt5_libdir}/cmake/Qt5Declarative/Qt5Declarative_QTcpServerConnection.cmake
%{_qt5_libdir}/cmake/Qt5Declarative/Qt5Declarative_QtQuick1Plugin.cmake
%{_qt5_prefix}/mkspecs/modules/qt_lib_declarative.pri
%{_qt5_exampledir}/declarative

#------------------------------------------------------------------------------

%package -n	%{qtdeclaratived_p_d}
Summary:	Devel files needed to build apps based on QtVersit
Group:		Development/KDE and Qt
Requires:	%{qtdeclaratived} = %version
Requires:	pkgconfig(Qt5Core) = %version
Requires:	qt5-qtscript-private-devel = %version

%description -n %{qtdeclaratived_p_d}
Devel files needed to build apps based on QtVersit.

%files -n %{qtdeclaratived_p_d}
%{_qt5_includedir}/QtDeclarative/%qtversion
%{_qt5_prefix}/mkspecs/modules/qt_lib_declarative_private.pri

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir

%build
%qmake_qt5
%make

#------------------------------------------------------------------------------

%install
%makeinstall_std INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# Don't reference builddir neither /usr(/X11R6)?/ in .pc files.
perl -pi -e '\
s@-L/usr/X11R6/%{_lib} @@g;\
s@-I/usr/X11R6/include @@g;\
s@-L/%{_builddir}\S+@@g'\
    `find . -name \*.pc`

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
rm -f %{buildroot}%{_qt5_libdir}/lib*.a

Summary:        A toolkit for displaying OpenGL applications to thin clients
Name:           VirtualGL
Version:        2.3
Vendor:         The VirtualGL Project
URL:            http://www.virtualgl.org/
Group:          Applications/System
Source0:        http://prdownloads.sourceforge.net/virtualgl/VirtualGL-%{version}.tar.gz
Release:        2%{?dist}
License:        wxWidgets
%if 0%{?fedora} >=13
BuildRequires:  cmake
%else
BuildRequires:  cmake28
%endif
BuildRequires:  openssl-devel
BuildRequires:  turbojpeg-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  libXv-devel

%description
VirtualGL is a toolkit that allows most Unix/Linux OpenGL applications to be
remotely displayed with hardware 3D acceleration to thin clients, regardless
of whether the clients have 3D capabilities, and regardless of the size of the
3D data being rendered or the speed of the network.

Using the vglrun script, the VirtualGL "faker" is loaded into an OpenGL
application at run time.  The faker then intercepts a handful of GLX calls,
which it reroutes to the server's X display (the "3D X Server", which
presumably has a 3D accelerator attached.)  The GLX commands are also
dynamically modified such that all rendering is redirected into a Pbuffer
instead of a window.  As each frame is rendered by the application, the faker
reads back the pixels from the 3D accelerator and sends them to the
"2D X Server" for compositing into the appropriate X Window.

VirtualGL can be used to give hardware-accelerated 3D capabilities to VNC or
other X proxies that either lack OpenGL support or provide it through software
rendering.  In a LAN environment, VGL can also be used with its built-in
high-performance image transport, which sends the rendered 3D images to a
remote client (vglclient) for compositing on a remote X server.  VirtualGL
also supports image transport plugins, allowing the rendered 3D images to be
sent or captured using other mechanisms.

VirtualGL is based upon ideas presented in various academic papers on
this topic, including "A Generic Solution for Hardware-Accelerated Remote
Visualization" (Stegmaier, Magallon, Ertl 2002) and "A Framework for
Interactive Hardware Accelerated Remote 3D-Visualization" (Engel, Sommer,
Ertl 2000.)

%package devel
Summary:    Development headers and libraries for VirtualGL
BuildArch:  noarch
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   openssl-devel
Requires:   turbojpeg-devel
Requires:   libX11-devel
Requires:   libXext-devel
Requires:   mesa-libGL-devel
Requires:   mesa-libGLU-devel
Requires:   libXv-devel

%description devel
Development headers and libraries for VirtualGL.

%prep
%setup -q

%build
%cmake -DTJPEG_INCLUDE_DIR=%{_includedir} \
       -DTJPEG_LIBRARY=%{_libdir}/libturbojpeg.so \
       -DVGL_USESSL=ON -DVGL_LIBDIR=%{_libdir} \
       -DVGL_DOCDIR=%{_docdir}/%{name}-%{version}/ \
       -DVGL_FAKELIBDIR=%{_libdir}/fakelib/ .
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# renamed from glxinfo which provided by glx-utils
mv $RPM_BUILD_ROOT%{_bindir}/{,v}glxinfo

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n %{name}
%{_docdir}/%{name}-%{version}/
%{_bindir}/tcbench
%{_bindir}/nettest
%{_bindir}/cpustat
# renamed from glxinfo which provided by glx-utils
%{_bindir}/vglxinfo
%{_bindir}/vglclient
%{_bindir}/vglconfig
%{_bindir}/vglconnect
%{_bindir}/vglgenkey
%{_bindir}/vgllogin
%{_bindir}/vglserver_config
%{_bindir}/vglrun
%{_bindir}/glxspheres
%{_libdir}/libdlfaker.so
%{_libdir}/libgefaker.so
%{_libdir}/librrfaker.so
%{_libdir}/fakelib/

%files devel
%{_includedir}/rrtransport.h
%{_includedir}/rr.h


%changelog
* Wed Jun 6 2012 Gary Gatling <gsgatlin@eos.ncsu.edu> - 2.3-2
- Very minor edit for building on older fedora or RHEL 6 with the same specfile
  as newer fedora.
* Thu Feb 16 2012 Robin Lee <cheeselee@fedoraproject.org> - 2.3-1
- Specfile based on upstream and Mandriva specfiles

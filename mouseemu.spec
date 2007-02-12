Summary:	Emulates middle click and right click
Summary(pl.UTF-8):   Emulacja środkowego i prawego przycisku myszy
Name:		mouseemu
Version:	0.12
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.geekounet.org/powerbook/files/%{name}.tar.gz
# Source0-md5:	768efb6ead83c3ad900d56e7f4e24b79
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-nousb-noadb.patch
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	rc-scripts
Requires(post,preun):	chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emulates middle click and right click.

%description -l pl.UTF-8
Emulacja środkowego i prawego przycisku myszy.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__cc} %{rpmcflags} %{rpmldflags} -o mouseemu mouseemu.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}}

install mouseemu $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2}	$RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service mouseemu restart

%preun
if [ "$1" = "0" ]; then
	%service mouseemu stop
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}

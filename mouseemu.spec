Summary:	Emulates middle click and right click
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
Requires:	chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emulates middle click and right click.

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
if [ -f /var/lock/subsys/mouseemu ]; then
        /etc/rc.d/init.d/%{name} restart >&2
else
        echo "Run \"/etc/rc.d/init.d/%{name} start\" to start mouseemu daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/mouseemu ]; then
                /etc/rc.d/init.d/%{name} stop >&2
        fi
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/*
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}

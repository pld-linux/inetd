Summary:	The internet superserver daemon -- inetd
Summary(de):	Enthält die Netzwerkprogramm inetd 
Summary(fr):	Inclut les programm réseau inetd 
Summary(pl):	Super-serwer sieciowy -- inetd
Summary(tr):	inetd programlarýný içerir
Name:		inetd
Version:	0.11+
Release:	11
Copyright:	BSD
Group:		Daemons
Group(pl):	Serwery
# gdzies na ftp.uk.linux.org
URL:		ftp://sunsite.unc.edu/pub/Linux/system/network
Source0:	netkit-base-%{version}.tar.gz
Source1:	%{name}.inet.sh
Patch0:		%{name}.patch
Prereq:		/sbin/chkconfig
Provides:	inetdaemon
Requires:	rc-scripts
Requires:	rc-inetd >= 0.8.1
Requires:	/etc/rc.d/init.d/rc-inetd
Obsoletes:	netkit-base
Buildroot:	/tmp/%{name}-%{version}-root

%description
This package provides the inetd program, which is used for
basic networking.

%description -l pl
W pakieci tym znjduje siê super demon inetd, który kontroluje pracê 
wiêkszo¶ci serwisów sieciowych Linuxa.

%description -l de
Dieses Paket stellt das inetd-Programm bereit, der für elementare 
Netzwerkaufgaben benutzt wird. 

%description -l fr
Ce paquetage contient les programm inetd, tous deux utilisés pour
le réseau.

%description -l tr
Bu paket að hizmetlerinde kullanýlan temel yazýlýmlardan inetd 
içerir.

%prep
%setup -q -n netkit-base-%{version}
%patch -p1

%build
make OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT%{_prefix}/{sbin,share/man/{man8,man3}}

install inetd/inetd $RPM_BUILD_ROOT%{_sbindir}

install inetd/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install inetd/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

> $RPM_BUILD_ROOT/etc/inetd.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inet.script

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man[38]/* README ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
    /etc/rc.d/init.d/rc-inetd restart &>/dev/null
else
    echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inetd" 1>&2
fi

%preun
if [ $1 = "0" -a -f /var/lock/subsys/rc-inetd ]; then
    /etc/rc.d/init.d/rc-inetd stop &>/dev/null
fi


%files
%defattr(644,root,root,755)
%doc {README,ChangeLog}.gz

%attr(640,root,root) %ghost /etc/inetd.conf
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%attr(755,root,root) %{_sbindir}/inetd

%{_mandir}/man[38]/*

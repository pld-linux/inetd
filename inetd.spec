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
#gdzies na ftp.uk.linux.org
URL:		ftp://sunsite.unc.edu/pub/Linux/system/network
Source0:	netkit-base-%{version}.tar.gz
Source1:	%{name}.conf.default
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}.patch
Prereq:		/sbin/chkconfig
Provides:	inetd
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

install %{SOURCE1} $RPM_BUILD_ROOT/etc/inetd.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/inetd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/inetd

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man[38]/* README ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add inetd

if [ -f /var/lock/subsys/inetd ]; then
    /etc/rc.d/init.d/inetd restart &>/dev/null
fi

%preun
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del inetd
fi

if [ -f /var/lock/subsys/inetd ]; then
    /etc/rc.d/init.d/inetd stop &>/dev/null
fi

%files
%defattr(644,root,root,755)
%doc {README,ChangeLog}.gz

%config(noreplace) %verify(not size mtime md5) /etc/inetd.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
%attr(755,root,root) /etc/rc.d/init.d/inetd
%attr(755,root,root) %{_sbindir}/inetd

%{_mandir}/man[38]/*

%changelog
* Sat May 22 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [0.10-11]
- added inetd.sysconfig,
- fixed %preun && %post,
- fixes for correct build.

* Thu Apr 15 1999 Micha³ Kuratczyk <kura@pld.org.pl>
  [0.10-5]
- gzipping documentation (instead bzipping)
- removed man group from man pages

* Mon Nov 08 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [0.10-2d]
- fixed symlinks,
- fixed %post & %preun sections,
- added qmail in /etc/inetd.conf.

* Wed Oct 14 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [0.10-1d]
- build against GNU libc-2.1,
- removed ping,
- renamed to inetd,
- added default kerberized services,
- major changes - designed for PLD Tornado.
- start at RH spec.

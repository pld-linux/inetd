Summary:	The internet superserver daemon -- inetd
Summary(de):	Enthält die Netzwerkprogramm inetd 
Summary(fr):	Inclut les programm réseau inetd 
Summary(pl):	Super-serwer sieciowy -- inetd
Summary(tr):	inetd programlarýný içerir
Name:		inetd
Version:	0.10
Release:	5
Copyright:	BSD
Group:		Daemons
Group(pl):	Serwery
URL:		ftp://sunsite.unc.edu/pub/Linux/system/network
Source0:	netkit-base-%{version}.tar.gz
Source1:	%{name}.conf.default
Source2:	%{name}.init
Patch:		%{name}.patch
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
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/usr/{sbin,man/{man8,man3}}

install inetd/inetd $RPM_BUILD_ROOT%{_sbindir}

install inetd/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install inetd/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

install %{SOURCE1} $RPM_BUILD_ROOT/etc/inetd.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/inetd

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man[38]/* README ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add inetd

%preun
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del inetd
fi

%files
%defattr(644,root,root,755)
%doc {README,ChangeLog}.gz
%config(noreplace) %verify(not size mtime md5) /etc/inetd.conf

%attr(750,root,root) %config /etc/rc.d/init.d/inetd
%attr(755,root,root) %{_sbindir}/inetd
%{_mandir}/man[38]/*

%changelog
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

* Mon May 04 1998 Michael K. Johnson <johnsonm@redhat.com>
- fixed iniscript enhancement

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 23 1998 Michael K. Johnson
- enhanced initscript

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added %config(missingok) to init symlinks

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- turned off in runlevel 2
- added status, restart options to init script

* Mon Oct 13 1997 Erik Troan <ewt@redhat.com>
- added chkconfig support

* Wed Aug 27 1997 Erik Troan <ewt@redhat.com>
- fixed init.d symlinks
- fixed permissions on /etc/rc.d/inet

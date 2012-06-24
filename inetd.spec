Summary:	The internet superserver daemon -- inetd
Summary(de):	Enth�lt die Netzwerkprogramm inetd 
Summary(fr):	Inclut les programm r�seau inetd 
Summary(pl):	Super-serwer sieciowy -- inetd
Summary(tr):	inetd programlar�n� i�erir
Name:		inetd
Version:	0.17
Release:	2
License:	BSD
Group:		Daemons
Group(pl):	Serwery
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-base-%{version}.tar.gz
Source1:	inetd.inet.sh
Source2:	inetd.conf.5
Patch0:		netkit-base-configure.patch
Provides:	inetdaemon
Prereq:		rc-scripts
Requires:	rc-inetd >= 0.8.1
Requires:	/etc/rc.d/init.d/rc-inetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	netkit-base
Obsoletes:	inetdaemon
Obsoletes:	rlinetd
Obsoletes:	xinetd

%description
The netkit-base package contains the basic networking program inetd.
Inetd listens on certain Internet sockets for connection requests,
decides what program should receive each request, and starts up that
program.

%description -l de
Dieses Paket stellt das inetd-Programm bereit, der f�r elementare
Netzwerkaufgaben benutzt wird.

%description -l fr
Ce paquetage contient les programm inetd, tous deux utilis�s pour le
r�seau.

%description -l pl
W pakiecie tym zanjduje si� program inetd. Inetd wychwytuje ��dania
po��cze� na portach sieciowych odsy�aj�c je do uruchamianego przez
siebie konkretnego programu, kt�ry ma je obs�u�y�.

%description -l tr
Bu paket a� hizmetlerinde kullan�lan temel yaz�l�mlardan inetd i�erir.

%prep
%setup -q -n netkit-base-%{version}
%patch -p1

%build
./configure --with-c-compiler=gcc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8}}

install inetd/inetd $RPM_BUILD_ROOT%{_sbindir}

install inetd/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

> $RPM_BUILD_ROOT%{_sysconfdir}/inetd.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inet.script
install %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man5

gzip -9nf README ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart &>/dev/null
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inetd" 1>&2
fi

%preun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd stop 1>&2
fi

%files
%defattr(644,root,root,755)
%doc {README,ChangeLog}.gz

%attr(640,root,root) %ghost %{_sysconfdir}/inetd.conf
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%attr(755,root,root) %{_sbindir}/inetd

%{_mandir}/man[58]/*

Summary:	The Internet superserver daemon -- inetd
Summary(de):	Enth�lt die Netzwerkprogramm inetd
Summary(fr):	Inclut les programm r�seau inetd
Summary(pl):	Super-serwer sieciowy -- inetd
Summary(tr):	inetd programlar�n� i�erir
Name:		inetd
Version:	0.17
Release:	9
License:	BSD
Group:		Daemons
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-base-%{version}.tar.gz
# Source0-md5:	1f0193358e92559ec0f598b09ccbc0ec
Source1:	%{name}.inet.sh
Source2:	%{name}.conf.5
Source3:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source3-md5:	6e7cdb6277c4333a9c0d1e3e2231f29f
Patch0:		netkit-base-configure.patch
PreReq:		rc-scripts
Requires:	rc-inetd >= 0.8.1
Requires:	/etc/rc.d/init.d/rc-inetd
Requires:	tcp_wrappers
Provides:	inetdaemon
Obsoletes:	inetdaemon
Obsoletes:	netkit-base
Obsoletes:	rlinetd
Obsoletes:	xinetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
W pakiecie tym znajduje si� program inetd. Inetd wychwytuje ��dania
po��cze� na portach sieciowych, odsy�aj�c je do uruchamianego przez
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

bzip2 -dc %{SOURCE3} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

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
%doc README ChangeLog

%attr(640,root,root) %ghost %{_sysconfdir}/inetd.conf
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%attr(755,root,root) %{_sbindir}/inetd

%{_mandir}/man[58]/*

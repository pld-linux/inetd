Summary:	The Internet superserver daemon -- inetd
Summary(de.UTF-8):	Enthält die Netzwerkprogramm inetd
Summary(fr.UTF-8):	Inclut les programm réseau inetd
Summary(pl.UTF-8):	Super-serwer sieciowy -- inetd
Summary(tr.UTF-8):	inetd programlarını içerir
Name:		inetd
Version:	0.17
Release:	14
License:	BSD
Group:		Daemons
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-base-%{version}.tar.gz
# Source0-md5:	1f0193358e92559ec0f598b09ccbc0ec
Source1:	%{name}.inet.sh
Source2:	%{name}.conf.5
Source3:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source3-md5:	6e7cdb6277c4333a9c0d1e3e2231f29f
Patch0:		netkit-base-configure.patch
Patch1:		netkit-base-fixes.patch
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	rc-inetd >= 0.8.1
Requires:	rc-scripts
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

%description -l de.UTF-8
Dieses Paket stellt das inetd-Programm bereit, der für elementare
Netzwerkaufgaben benutzt wird.

%description -l fr.UTF-8
Ce paquetage contient les programm inetd, tous deux utilisés pour le
réseau.

%description -l pl.UTF-8
W pakiecie tym znajduje się program inetd. Inetd wychwytuje żądania
połączeń na portach sieciowych, odsyłając je do uruchamianego przez
siebie konkretnego programu, który ma je obsłużyć.

%description -l tr.UTF-8
Bu paket ağ hizmetlerinde kullanılan temel yazılımlardan inetd içerir.

%prep
%setup -q -n netkit-base-%{version}
%patch0 -p1
%patch1 -p1

%build
export RPM_OPT_FLAGS="%{rpmcflags}"
./configure \
	--with-c-compiler="%{__cc}"
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
%service -q rc-inetd restart

%preun
if [ "$1" = "0" ]; then
	%service -q rc-inetd restart
fi

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog README
%attr(640,root,root) %ghost %{_sysconfdir}/inetd.conf
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%attr(755,root,root) %{_sbindir}/inetd
%{_mandir}/man[58]/*
%lang(es) %{_mandir}/es/man8/inetd.8*
%lang(ja) %{_mandir}/ja/man8/inetd.8*
%lang(pl) %{_mandir}/pl/man8/inetd.8*

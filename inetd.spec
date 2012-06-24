Summary:	The internet superserver daemon -- inetd
Summary(de):	Enth�lt die Netzwerkprogramm inetd 
Summary(fr):	Inclut les programm r�seau inetd 
Summary(pl):	Super-serwer sieciowy -- inetd
Summary(tr):	inetd programlar�n� i�erir
Name:		inetd
Version:	0.11+
Release:	11
Copyright:	BSD
Group:		Daemons
Group(pl):	Serwery
# gdzies na ftp.uk.linux.org
URL:		ftp://sunsite.unc.edu/pub/Linux/system/network
Source0:	netkit-base-%{version}.tar.gz
Source1:	%{name}.conf.default
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}.patch
Prereq:		/sbin/chkconfig
Provides:	inetd
Requires:	rc-scripts
Obsoletes:	netkit-base
Buildroot:	/tmp/%{name}-%{version}-root

%description
This package provides the inetd program, which is used for
basic networking.

%description -l pl
W pakieci tym znjduje si� super demon inetd, kt�ry kontroluje prac� 
wi�kszo�ci serwis�w sieciowych Linuxa.

%description -l de
Dieses Paket stellt das inetd-Programm bereit, der f�r elementare 
Netzwerkaufgaben benutzt wird. 

%description -l fr
Ce paquetage contient les programm inetd, tous deux utilis�s pour
le r�seau.

%description -l tr
Bu paket a� hizmetlerinde kullan�lan temel yaz�l�mlardan inetd 
i�erir.

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

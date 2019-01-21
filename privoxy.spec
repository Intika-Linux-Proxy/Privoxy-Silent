%define privoxyconf %{_sysconfdir}/%{name}

%define reltype stable

Summary:	Privacy enhancing HTTP proxy
Name:		privoxy
Version:	3.0.28
Release:	%mkrel 8
License:	GPLv2+
Group:		Networking/Other
URL:		http://www.privoxy.org/
Source0:	http://www.privoxy.org/sf-download-mirror/Sources/%{version}%%20%%28stable%%29/%{name}-%{version}-%{reltype}-src.tar.gz
Source1:	http://www.privoxy.org/sf-download-mirror/Sources/%{version}%%20%%28stable%%29/%{name}-%{version}-%{reltype}-src.tar.gz.asc
Source2:	privoxy.logrotate
Source4:	%{name}.service
Patch0:		privoxy-3.0.21-mga-mdv-missing-user.filter.patch
# (cjw) add a "address-family-preference" option that allows disabling IPv6 DNS lookups,
#       forcing outgoing HTTP requests to be IPv4
Patch1:		privoxy-3.0.21-mga-address-family-preference.patch
# (cjw) from debian: don't translate documentation to locale-dependent 8-bit ascii
Patch2:		privoxy-3.0.21-mga-deb-8bit_manual.patch
# (cjw) documentation and default configuration changes and cleanups for mageia
Patch3:		privoxy-3.0.21-mga-mageia-specific-config.patch
Patch4:		privoxy-3.0.28-mga-intika-config-page.patch
Patch5:		privoxy-3.0.28-mga-intika-anonimyzer.patch
Patch6:		privoxy-3.0.28-mga-intika-shutup-no-answer.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Obsoletes:	junkbuster
Provides:	junkbuster = %{version}-%{release}
Provides:	webproxy
BuildRequires:	man
BuildRequires:	pkgconfig(libpcreposix)
BuildRequires:	pkgconfig(zlib)
# for manual
BuildRequires:	openjade
BuildRequires:	docbook-dtds
BuildRequires:	docbook-style-dsssl
BuildRequires:	w3m

%description
Privoxy is a web proxy with advanced filtering capabilities for protecting
privacy, filtering web page content, managing cookies, controlling access, and
removing ads, banners, pop-ups and other obnoxious Internet Junk. Privoxy has a
very flexible configuration and can be customized to suit individual needs and
tastes. Privoxy has application for both stand-alone systems and multi-user
networks.

Privoxy was previously called Internet Junkbuster.

To configure privoxy, go to http://config.privoxy.org/

Privoxy proxy is running on port 8118

%prep

%setup -n %{name}-%{version}-%{reltype} -q

# manpage should be in section 8
sed -i -e 's/^\(\.TH "PRIVOXY" \)"1"/\1"8"/g' privoxy.1 

%autopatch -p1

%build
#needed for build
autoreconf -fi

%serverbuild
%configure2_5x --with-user=daemon --with-group=daemon --disable-image-blocking --disable-client-tags --enable-graceful-termination=no --enable-external-filters=no --enable-editor=no --enable-trust-files=no --enable-toggle=no --enable-fuzz=no --disable-force
%make_build
make dok
make config-file

#remove backup files
rm -f doc/webserver/user-manual/*.bak

%install
mkdir -p %{buildroot}%{_sbindir} \
         %{buildroot}%{_mandir}/man8 \
         %{buildroot}/var/log/privoxy \
         %{buildroot}%{privoxyconf}/templates \
         %{buildroot}%{_sysconfdir}/logrotate.d

install -m 755 privoxy %{buildroot}%{_sbindir}/privoxy
install -m 644 privoxy.1 %{buildroot}%{_mandir}/man8/privoxy.8

# Install various config files
for i in *.action default.filter trust; do
	install -m 644 $i %{buildroot}%{privoxyconf}/
done
for i in templates/*; do
	install -m 644 $i %{buildroot}%{privoxyconf}/templates/
done
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -d -m 755 %{buildroot}%{_unitdir}
install -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}.service

# verify all file locations, etc. in the config file
# don't start with ^ or commented lines are not replaced
sed -e 's!^confdir.*!confdir /etc/privoxy!g' \
    -e 's!^logdir.*!logdir /var/log/privoxy!g' \
    < config  > %{buildroot}%{privoxyconf}/config

# create compatibility symlink
ln -s match-all.action %{buildroot}/%{privoxyconf}/standard.action

%triggerin -- msec < 0.17
for i in 0 1 2 3 4 5; do
  permfile="%{_sysconfdir}/security/msec/perm.$i"
  if grep -q '^/var/log/privoxy' $permfile; then
    perl -pi -e 's|^/var/log/privoxy\s.*|/var/log/prixovy\t\t\t\tdaemon.daemon\t700|' $permfile
  else
    echo -e "/var/log/prixovy\t\t\t\tdaemon.daemon\t700" >> $permfile
  fi
done


%post
%_post_service privoxy

%preun
%_preun_service privoxy

%files
%doc AUTHORS ChangeLog README  
%doc doc/webserver
%attr (0700,daemon,daemon) /var/log/privoxy
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sbindir}/*
%{_mandir}/man8/*

%defattr(664,daemon,daemon,755)
%dir %{privoxyconf}
%config(noreplace) %{privoxyconf}/config
%config            %{privoxyconf}/default.action
%config(noreplace) %{privoxyconf}/default.filter
%config(noreplace) %{privoxyconf}/templates
%config(noreplace) %{privoxyconf}/match-all.action
%config(noreplace) %{privoxyconf}/trust
%config(noreplace) %{privoxyconf}/user.action
%config(noreplace) %{privoxyconf}/regression-tests.action
%{privoxyconf}/standard.action
%{_unitdir}/%{name}.service


%changelog
* Mon Dec 31 2018 kekepower <kekepower> 3.0.28-1.mga7
+ Revision: 1347467
- Update to version 3.0.28
- Rediffed patches 1, 2 and 3

* Sun Sep 23 2018 umeabot <umeabot> 3.0.26-2.mga7
+ Revision: 1300378
- Mageia 7 Mass Rebuild

* Sun Oct 01 2017 cjw <cjw> 3.0.26-1.mga7
+ Revision: 1162080
- 3.0.26

* Thu Jan 28 2016 cjw <cjw> 3.0.24-1.mga6
+ Revision: 928359
- 3.0.24

* Mon Jan 26 2015 cjw <cjw> 3.0.23-1.mga5
+ Revision: 812362
- 3.0.23

* Sun Dec 28 2014 cjw <cjw> 3.0.22-1.mga5
+ Revision: 806998
- re-add patch1 as sent upstream (but config syntax may still change)
- patch4: fix doc build
+ solbu <solbu>
- Rename patches, according to policy
- Drop P1. Merged upstream
- New version

* Sun Oct 26 2014 cjw <cjw> 3.0.21-8.mga5
+ Revision: 793535
- patch2: from debian: do not generate high-ascii characters from sgml files
- patch3: mageia specific changes: make user manual available in web interface
- drop unneeded lynx build dependency
- fix removal of backup files in doc dir

* Sun Oct 26 2014 cjw <cjw> 3.0.21-7.mga5
+ Revision: 793357
- add documentation for the unofficial force-ipv4 config option

* Sat Oct 25 2014 cjw <cjw> 3.0.21-6.mga5
+ Revision: 793290
- patch1: add a "force-ipv4" boolean option to disable outgoing ipv6 requests

* Sat Oct 25 2014 cjw <cjw> 3.0.21-5.mga5
+ Revision: 793229
- restart the daemon on logrotate to make sure the old log file is closed
- add ExecReload to systemd service file

* Wed Oct 15 2014 umeabot <umeabot> 3.0.21-4.mga5
+ Revision: 744986
- Second Mageia 5 Mass Rebuild

* Tue Sep 16 2014 umeabot <umeabot> 3.0.21-3.mga5
+ Revision: 687786
- Mageia 5 Mass Rebuild

* Sat Oct 19 2013 umeabot <umeabot> 3.0.21-2.mga4
+ Revision: 522506
- Mageia 4 Mass Rebuild

* Tue Mar 12 2013 solbu <solbu> 3.0.21-1.mga3
+ Revision: 402171
- New version
- Rediff patch, and rename according to policy

* Fri Feb 08 2013 solbu <solbu> 3.0.19-4.mga3
+ Revision: 395301
- systemd integration
- Kill init script
- Fix License tag

* Sun Jan 13 2013 umeabot <umeabot> 3.0.19-3.mga3
+ Revision: 378216
- Mass Rebuild - https://wiki.mageia.org/en/Feature:Mageia3MassRebuild

* Sat Dec 01 2012 fwang <fwang> 3.0.19-2.mga3
+ Revision: 323740
- br pcreposix

* Wed Mar 07 2012 boklm <boklm> 3.0.19-1.mga2
+ Revision: 221204
- Version 3.0.19

* Wed Nov 23 2011 fwang <fwang> 3.0.18-1.mga2
+ Revision: 171273
- new version 3.0.18

* Wed Sep 07 2011 tv <tv> 3.0.17-1.mga2
+ Revision: 140084
- fix missing LSB keywords
- new release
- BR zlib
- patch : missing user.filter file (mdv#63573)

* Sun Mar 06 2011 ennael <ennael> 3.0.16-2.mga1
+ Revision: 65639
- imported package privoxy


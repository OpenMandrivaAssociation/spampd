Name:		spampd
Version:	2.30
Release:	7
Summary:	Spam Proxy Daemon
Source0:	http://www.wdg.us/Content/rd/mta/%{name}/%{name}-%{version}.tar.bz2
Patch0:		spampd-2.30-mdv.patch
URL:		http://www.wdg.us/index.cfm/rd/mta/spampd.htm
License:	GPLv2+
Group:		Networking/Mail
BuildArch:	noarch
BuildRequires:	perl
Requires(post,preun):	rpm-helper

%description
spampd is an SMTP/LMTP proxy that marks (or tags) spam using
SpamAssassin (http://www.SpamAssassin.org/). The proxy is designed
to be transparent to the sending and receiving mail servers and at no point
takes responsibility for the message itself. If a failure occurs within
spampd (or SpamAssassin) then the mail servers will disconnect and the
sending server is still responsible for retrying the message for as long
as it is configured to do so.

%prep
%setup -q
%patch0 -p1 -b .mdv
make spampd.8
chmod 644 *

%install
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_mandir}/man8
install -m 755 spampd %{buildroot}%{_sbindir}/spampd
install -m 755 spampd-rh-rc-script %{buildroot}%{_initrddir}/spampd
install -m 644 spampd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/spampd
install -m 644 spampd.8 %{buildroot}%{_mandir}/man8/spampd.8

%post
%_post_service spampd
if [ -x /usr/sbin/postconf ] && [ -z `/usr/sbin/postconf -h content_filter` ] && \
	grep -qs '^lmtp-filter\>' /etc/postfix/master.cf;then
		LISTEN=127.0.0.1:10025
		MAXCHILD=5
		[ -f /etc/sysconfig/spampd ] && . /etc/sysconfig/spampd
		postconf -e content_filter=lmtp-filter:${LISTEN}
		postconf -e receive_override_options=no_address_mappings
		postconf -e lmtp-filter_destination_concurrency_limit=${MAXCHILD}
fi

%preun
%_preun_service spampd

%files
%defattr(-,root,root,755)
%doc changelog.txt spampd.html
%{_sbindir}/spampd
%config(noreplace) %{_initrddir}/spampd
%config(noreplace) %{_sysconfdir}/sysconfig/spampd
%{_mandir}/man8/spampd.8*





%changelog
* Tue Sep 08 2009 Thierry Vignaud <tvignaud@mandriva.com> 2.30-6mdv2010.0
+ Revision: 434013
- rebuild

* Sat Aug 02 2008 Thierry Vignaud <tvignaud@mandriva.com> 2.30-5mdv2009.0
+ Revision: 260939
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tvignaud@mandriva.com> 2.30-4mdv2009.0
+ Revision: 252910
- rebuild
- fix no-buildroot-tag

* Tue Dec 18 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.30-2mdv2008.1
+ Revision: 131798
- fix prereq on rpm-helper
- kill re-definition of %%buildroot on Pixel's request


* Sun Jul 30 2006 Luca Berra <bluca@comedia.it>
+ 2006-07-30 21:24:55 (42827)
- force default umask (#24001)
  rework initscript
  spec cleanup

* Sun Jul 30 2006 Luca Berra <bluca@comedia.it>
+ 2006-07-30 17:37:14 (42815)
- import spampd-2.30-1mdk

* Sat Jan 21 2006 Luca Berra <bluca@vodka.it> 2.30-1mdk
- New release 2.30

* Fri Oct 15 2004 Luca Berra <bluca@vodka.it> 2.20-1mdk 
- 2.20

* Sun Feb 01 2004 Luca Berra <bluca@vodka.it> 2.12-2mdk 
- auto-add to postfix

* Sat Jan 17 2004 Luca Berra <bluca@vodka.it> 2.12-1mdk 
- 2.12
- use tar package

* Sun Nov 09 2003 Luca Berra <bluca@vodka.it> 2.11-2mdk
- fix description tag
- fixed init-script

* Sun Oct 05 2003 Luca Berra <bluca@vodka.it> 2.11-1mdk
- initial release


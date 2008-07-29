%define name	spampd
%define version	2.30
%define release	%mkrel 4

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Spam Proxy Daemon
Source:		http://www.wdg.us/Content/rd/mta/%{name}/%{name}-%{version}.tar.bz2
Patch:		spampd-2.30-mdv.patch
URL:		http://www.wdg.us/index.cfm/rd/mta/spampd.htm
License:	GPL
Group:		Networking/Mail
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
%patch -p1 -b .mdv
make spampd.8
chmod 644 *

%install
rm -rf %buildroot
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_mandir}/man8
install -m 755 spampd %{buildroot}%{_sbindir}/spampd
install -m 755 spampd-rh-rc-script %{buildroot}%{_initrddir}/spampd
install -m 644 spampd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/spampd
install -m 644 spampd.8 %{buildroot}%{_mandir}/man8/spampd.8

%clean
rm -rf $RPM_BUILD_ROOT

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




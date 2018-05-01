%define		plugin	check_iface
Summary:	Nagios/Icinga plugin for checking network interface speed
Name:		nagios-plugin-%{plugin}
Version:	1.0
Release:	1
License:	GPL
Group:		Networking
Source0:	https://raw.githubusercontent.com/wifibox/linux-admin-tools/master/nagios/plugins/check_net_iface
# Source0-md5:	30366d25cf1e3b035cf49f2d5d556cbe
URL:		https://github.com/wifibox/linux-admin-tools/blob/master/nagios/plugins/check_net_iface
Requires:	nagios-common
Requires:	nagios-plugins-libs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios/Icinga plugin for checking network interface speed.

%prep
%setup -q -n monitoring-plugin-%{plugin}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
install -p %{plugin}.sh $RPM_BUILD_ROOT%{plugindir}/%{plugin}
sed -e 's,@plugindir@,%{plugindir},' %{plugin}.cfg > $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}

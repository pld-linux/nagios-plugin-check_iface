%define		plugin	check_iface
Summary:	Nagios/Icinga plugin for checking network interface speed
Name:		nagios-plugin-%{plugin}
Version:	2.0
Release:	1
License:	GPL v3
Group:		Networking
Source0:	check_iface.py
# Source0-md5:	30366d25cf1e3b035cf49f2d5d556cbe
Source1:	check_iface.cfg
Requires:	nagios-common
Requires:       python3-netifaces
Requires:       python3-psutil
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		nrpeddir	/etc/nagios/nrpe.d
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios/Icinga plugin for checking network interface speed.

%prep
%setup -qTc
install %{SOURCE0} %{plugin}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}

install -p %{plugin} $RPM_BUILD_ROOT%{plugindir}/%{plugin}

install -d $RPM_BUILD_ROOT%{nrpeddir}
touch $RPM_BUILD_ROOT%{nrpeddir}/%{plugin}.cfg

cp -p %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/check_iface.cfg

%triggerin -- nagios-nrpe
%nagios_nrpe -a %{plugin} -f %{_sysconfdir}/%{plugin}.cfg

%triggerun -- nagios-nrpe
%nagios_nrpe -d %{plugin} -f %{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%ghost %{nrpeddir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}

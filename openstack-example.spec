%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
# %global sources_gpg_sign <get the Cryptographic Signatures of current release from https://releases.openstack.org/#cryptographic-signatures>
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global service example
%global with_doc 1
# Uncomment the following and edit for global description
#%global common_desc \
#Example is a service for OpenStack cloud.  \
#It does examplefunction. \
#The goal is exampletarget.

Name:           openstack-%{service}
Version:        XXX
Release:        XXX
Summary:        OpenStack Example Service
License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
Source1:        %{service}.logrotate
Source2:        openstack-example-server.service
Source3:        %{service}-dist.conf
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:      https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:      https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core
BuildRequires:  systemd
BuildRequires:  systemd-units
# Required to compile translation files
BuildRequires:  python3-babel

Requires:       openstack-%{service}-common = %{version}-%{release}

Requires(pre): shadow-utils
%{?systemd_requires}

%description
%{common_desc}

%package -n python3-%{service}
Summary:        Example Python libraries

# What dependencies are there to run this service?
Requires:       python3-oslo-db >= 2.0

%description -n python3-%{service}
%{common_desc}

This package contains the Example Python library.


%package -n python3-%{service}-tests
Summary:        Example unit tests
Requires:       python3-%{service} = %{version}-%{release}
# testing framework packages required to run unit tests or any additional package
# which is not required for python3-%{service} but it is for unit tests.
Requires:       python3-stestr

%description -n python3-%{service}-tests
%{common_desc}

This package contains the Example unit test files.

%package common
Summary:        Example common files
Requires:       python3-%{service} = %{version}-%{release}

%description common
%{common_desc}

# Tipically we create a subpackage for each independen service as api or conductor
# with the name of the service as api in this example
%package api
Summary:    OpenStack Example API service
Group:      Applications/System

Requires:   openstack-%{service}-common = %{version}-%{release}

%description api

%{common_desc}
This package contains Example common files.

This package contains OpenStack example service.

%if 0%{?with_doc}
%package doc
Summary:        Example documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme

%description doc
%{common_desc}

This package contains the documentation.
%endif


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f requirements.txt
rm -rf *{service}*.egg-info


%build
%py3_build

# Build default config file with oslo-config-generate if available
PYTHONPATH=. oslo-config-generator --config-dir=etc/oslo-config-generator/

%if 0%{?with_doc}
# generate html docs
sphinx-build -b html doc/source doc/build/html

# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif
# Generate i18n files
%{__python3} setup.py compile_catalog -d build/lib/%{service}/locale

%install
%py3_install

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}/usr/etc/%{service}/* %{buildroot}%{_sysconfdir}/%{service}

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{service}

# Install systemd units
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-example-server.service

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python3_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

%check
stestr run

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
getent passwd %{service} >/dev/null || \
    useradd -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
    -c "OpenStack Example Daemons" %{service}
exit 0


%post api
%systemd_post openstack-example-api.service

%preun api
%systemd_preun openstack-example-api.service

%postun api
%systemd_postun_with_restart openstack-example-api.service

%files -n python3-%{service}
%license LICENSE
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.egg-info
%exclude %{python3_sitelib}/%{service}/tests

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests

%files common -f %{service}.lang
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/%{service}
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{service}
%dir %{_datadir}/%{service}
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%dir %{_sharedstatedir}/%{service}
%dir %attr(0750, %{service}, root) %{_localstatedir}/log/%{service}

%files api
%license LICENSE
%{_bindir}/openstack-example-api
%{_unitdir}/openstack-example-api.service
%attr(-, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog


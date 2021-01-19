%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name example-dashboard
%global mod_name example_dashboard
%global with_doc 1

# tests are disabled by default
%bcond_with tests

Name:         openstack-example-ui
Version:      XXX
Release:      XXX
Summary:      The UI component for the OpenStack example service

License:      ASL 2.0
URL:          https://github.com/openstack/%{pypi_name}
Source0:      http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:     noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: git-core
# Required to compile translation files
BuildRequires: python-django
# openstack-dashboard is probably required for running tests
# if your project uses own tests, remove this, otherwise uncomment.
# BuildRequires: openstack-dashboard

BuildRequires: gettext

Requires: openstack-dashboard
Requires: python-pbr

%description
openstack-example-ui is a dashboard for example service

%if 0%{?with_doc}
%package doc
Summary: Documentation for example dashboard

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
Documentation files for example dashboard
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
# build
%py2_build
# Generate i18n files
pushd build/lib/%{mod_name}
django-admin compilemessages
popd

%if 0%{?with_doc}
# Build html documentation
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py2_install

# Move config to horizon
mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/
# replace XXX_example for a expression that match files for each specific dashboard
install -p -D -m 640 %{mod_name}/enabled/_XXX_example* %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/

# Remove .po and .pot (they are not required)
rm -f %{buildroot}%{python2_sitelib}/%{mod_name}/locale/*/LC_*/django*.po
rm -f %{buildroot}%{python2_sitelib}/%{mod_name}/locale/*pot

# Find language files
%find_lang django --all-name

%check
%if %{?with_tests}
%{__python2} setup.py test
%endif

%files -f django.lang
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{mod_name}
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_XXX_example*

%if 0%{?with_doc}
%files doc
%doc html
%license LICENSE
%endif

%changelog


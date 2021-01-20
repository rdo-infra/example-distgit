%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
# %global sources_gpg_sign <get the Cryptographic Signatures of current release from https://releases.openstack.org/#cryptographic-signatures>
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library example-library
%global module example_library
%global with_doc 1

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Example library
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:  https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz.asc
Source102:  https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%package -n python2-%{library}
Summary:    OpenStack Example library
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git-core
# Required to compile translation files (add only if exist)
BuildRequires:  python-babel

Requires:   python-oslo-config >= 2:3.4.0
# If translation files exist
Requires:       python-%{library}-lang = %{version}-%{release}

%description -n python2-%{library}
OpenStack example library.


%package -n python2-%{library}-tests
Summary:    OpenStack example library tests
Requires:   python2-%{library} = %{version}-%{release}

%description -n python2-%{library}-tests
OpenStack example library.

This package contains the example library test files.


%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{library}-doc
OpenStack example library.

This package contains the documentation.
%endif

# Add python-%{library}-lang if translation files exist
%package  -n python-%{library}-lang
Summary:   Translation files for example library

%description -n python-%{library}-lang
Translation files for example library

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    OpenStack Example library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core

Requires:   python3-oslo-config >= 2:3.4.0
# If translation files exist
Requires:       python-%{library}-lang = %{version}-%{release}

%description -n python3-%{library}
OpenStack example library.


%package -n python3-%{library}-tests
Summary:    OpenStack example library tests
Requires:   python3-%{library} = %{version}-%{release}

%description -n python3-%{library}-tests
OpenStack example library.

This package contains the example library test files.

%endif # with_python3


%description
OpenStack example library.


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

# Generate i18n files if translation files exist
%{__python2} setup.py compile_catalog -d build/lib/%{module}/locale

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Install i18n .mo files (.po and .pot are not required) if translation files exist
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{module}/locale/*/LC_*/%{module}*po
rm -f %{buildroot}%{python2_sitelib}/%{module}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{module}/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/%{module}/locale
%endif

# Find language files
%find_lang %{module} --all-name


%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc html README.rst
%endif

# Only if translation files exist
%files -n python-%{library}-lang -f %{module}.lang

%if 0%{?with_python3}
%files python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
# %global sources_gpg_sign <get the Cryptographic Signatures of current release from https://releases.openstack.org/#cryptographic-signatures>
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pname example_tests

%global service example-tests
%global with_doc 1
Name:           openstack-%{service}
Version:        XXX
Release:        XXX
Summary:        Example Test Framework
License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
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
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git-core

Requires:       python-pbr
Requires:       python-setuptools

# test dependencies requirements
BuildRequires:  python-hacking
BuildRequires:  python-mock
BuildRequires:  python-coverage

%description
This project contains example test framework.

%if 0%{?with_doc}
%package -n openstack-%{service}-doc
Summary:        OpenStack example tests Documentation

BuildRequires:  python-sphinx

Requires:    %{name} = %{version}-%{release}

%description -n openstack-%{service}-doc
It contains the documentation of example package.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%setup -q -n %{service}-%{upstream_version}
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{__python2} setup.py build

%if 0%{?with_doc}
# Build Documentation
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}


install -d -m 755 %{buildroot}%{_sysconfdir}/
mv %{buildroot}/usr/etc/* %{buildroot}%{_sysconfdir}/


%check
%{__python2} setup.py test

%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pname}
%{python2_sitelib}/%{pname}-*.egg-info
%{_bindir}/<test binary>
%{_sysconfdir}/<config path>/*

%if 0%{?with_doc}
%files -n openstack-%{example}-doc
%license LICENSE
%doc html
%endif

%changelog

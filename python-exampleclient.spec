%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
# %global sources_gpg_sign <get the Cryptographic Signatures of current release from https://releases.openstack.org/#cryptographic-signatures>
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global client python-exampleclient
%global sclient exampleclient
%global with_doc 1
# If a executable is provided by the package uncomment following line
#%global executable example
# The following is a multiline description example
#%global common_desc \
# This is a client library for Example built on the Example API. \
# It provides a Python API and a command line tool (example).

Name:       %{client}
Version:    XXX
Release:    XXX
Summary:    OpenStack Example client
License:    ASL 2.0
URL:        http://launchpad.net/%{client}/

Source0:    https://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:  https://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz.asc
Source102:  https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

%package -n python2-%{sclient}
Summary:    OpenStack Example client
%{?python_provide:%python_provide python2-%{sclient}}

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git-core
BuildRequires:  openstack-macros
# Test requirements should be added here as BuildRequires for tests in %check

Requires:   python-oslo-config >= 2:3.4.0

%description -n python2-%{sclient}
%{common_desc}


%package -n python2-%{sclient}-tests
Summary:    OpenStack example client tests
Requires:   python2-%{sclient} = %{version}-%{release}

# Test requirements should be added here as Requires.

%description -n python2-%{sclient}-tests
%{common_desc}

This package contains the example client test files.

if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack example client documentation

BuildRequires: python-sphinx
BuildRequires: python-openstackdocstheme

%description -n python-%{sclient}-doc
%{common_desc}

This package contains the documentation.
%endif

%if 0%{?with_python3}
%package -n python3-%{sclient}
Summary:    OpenStack Example client
%{?python_provide:%python_provide python3-%{sclient}}

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core
# Test requirements should be added here as BuildRequires if adding tests in %check

Requires:   python3-oslo-config >= 2:3.4.0

%description -n python3-%{sclient}
%{common_desc}


%package -n python3-%{sclient}-tests
Summary:    OpenStack example client tests
Requires:   python3-%{sclient} = %{version}-%{release}

# Test requirements should be added here as Requires.

%description -n python3-%{sclient}-tests
OpenStack example client tests

This package contains the example client test files.

%endif # with_python3


%description
%{common_desc}


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{client}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# If the client has man page uncomment following line
# %{__python2} setup.py build_sphinx --builder man

%install
%if 0%{?with_python3}
# If an executable is provided by the package uncomment following lines
#mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python3_version}
#ln -s ./%{executable}-%{python3_version} %{buildroot}%{_bindir}/%{executable}-3
%py3_install
# If an executable is provided by the package uncomment following lines
#mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python2_version}
#ln -s %{_bindir}/%{executable}-%{python2_version} %{buildroot}%{_bindir}/%{executable}-2
#ln -s %{_bindir}/%{executable}-2 %{buildroot}%{_bindir}/%{executable}
%endif

%py2_install
# If the client has man page uncomment following line
# install -p -D -m 644 man/%{executable}.1 %{buildroot}%{_mandir}/man1/%{executable}.1

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py testr

%files -n python2-%{sclient}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sclient}
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/%{sclient}/tests
# If the client has man page uncomment
#%{_mandir}/man1/%{executable}.1
# If an executable is provided by the package uncomment following lines
#%{_bindir}/%{executable}
#%{_bindir}/%{executable}-2
#%{_bindir}/%{executable}-%{python2_version}
#%endif

%files -n python2-%{sclient}-tests
%{python2_sitelib}/%{sclient}/tests

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html
%endif

%if 0%{?with_python3}
%files python3-%{sclient}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{sclient}/tests
# If the client has man page uncomment
#%{_mandir}/man1/%{executable}.1
# If an executable is provided by the package uncomment following lines
#%{_bindir}/%{executable}-3
#%{_bindir}/%{executable}-%{python3_version}
#%endif

%files -n python3-%{library}-tests
%{python3_sitelib}/%{sclient}/tests
%endif # with_python3

%changelog

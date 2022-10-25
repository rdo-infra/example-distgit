%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
# %global sources_gpg_sign <get the Cryptographic Signatures of current release from https://releases.openstack.org/#cryptographic-signatures>
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global client python-exampleclient
%global sclient exampleclient
%global with_doc 1
# Some clients only provide a openstack clientg plugin.
# If a executable is provided by the package uncomment following line
#%global executable example
# The following is a multiline description example
%global common_desc \
This is a client library for Example built on the Example API. \
It provides a Python API and a command line tool (example).

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
BuildRequires:  git-core
BuildRequires:  openstack-macros
# Test requirements should be added here as BuildRequires for tests in %check
Requires:   python3-oslo-config >= 2:3.4.0

%description -n python3-%{sclient}
%{common_desc}


%package -n python3-%{sclient}-tests
Summary:    OpenStack example client tests
Requires:   python3-%{sclient} = %{version}-%{release}

# testing framework packages required to run unit tests or any additional package
# which is not required for python3-%{service} but it is for unit tests.
Requires:       python3-stestr

%description -n python3-%{sclient}-tests
%{common_desc}

This package contains the example client test files.

if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack example client documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme

%description -n python-%{sclient}-doc
%{common_desc}

This package contains the documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{client}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py3_build

%if 0%{?with_doc}
# generate html docs and man pages
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
# If man pages are provided uncomment following lines
#sphinx-build -b man doc/source doc/build/man
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%py3_install
# If an executable is provided by the package uncomment following lines
#ln -s %{executable} %{buildroot}%{_bindir}/%{executable}-3
# If the client has man page uncomment following line
# install -p -D -m 644 man/%{executable}.1 %{buildroot}%{_mandir}/man1/%{executable}.1

%check
stestr run

%files -n python3-%{sclient}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{sclient}/tests
# If the client has man page uncomment
#%{_mandir}/man1/%{executable}.1
# If an executable is provided by the package uncomment following lines
#%{_bindir}/%{executable}
#%{_bindir}/%{executable}-3

%files -n python3-%{sclient}-tests
%{python3_sitelib}/%{sclient}/tests

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog

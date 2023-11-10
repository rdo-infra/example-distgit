%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
# %global sources_gpg_sign <get the Cryptographic Signatures of current release from https://releases.openstack.org/#cryptographic-signatures>
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global client python-exampleclient
%global sclient exampleclient
%global with_doc 1
# Some clients only provide a openstack client plugin.
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
License:    Apache-2.0
URL:        http://launchpad.net/%{client}/

Source0:    https://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:  https://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz.asc
Source102:  https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{sclient}
Summary:    OpenStack Example client
%{?python_provide:%python_provide python3-%{sclient}}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core

%description -n python3-%{sclient}
%{common_desc}


%package -n python3-%{sclient}-tests
Summary:    OpenStack example client tests
Requires:   python3-%{sclient} = %{version}-%{release}

# which is not required for python3-%{service} but it is for unit tests.
Requires:       python3-stestr

%description -n python3-%{sclient}-tests
%{common_desc}

This package contains the example client test files.

%if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack example client documentation

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

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%pyproject_install

# If an executable is provided by the package uncomment following lines
#ln -s %{executable} %{buildroot}%{_bindir}/%{executable}-3
# If the client has man page uncomment following line
# install -p -D -m 644 man/%{executable}.1 %{buildroot}%{_mandir}/man1/%{executable}.1

%check
%tox -e %{default_toxenv}

%files -n python3-%{sclient}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.dist-info
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

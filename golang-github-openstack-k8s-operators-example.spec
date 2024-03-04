%global debug_package %{nil}

# https://github.com/openstack-k8s-operators/example
%global goipath         github.com/openstack-k8s-operators/example

# The macro %%gometa needs Version:, %{commit} or %{tag} to be defined
# before the macro invocation, but as we set XXX as Version for DLRN, it fails.
# So we add a dummy tag and remove the distprefix (i.e .git<tag>) which
# is added at the end of the RPM if a tag is defined.
# At the end, it's a noop operation and the macro does not fail anymore
%{?dlrn: %global tag        0}
%{?dlrn: %global distprefix %{nil}}
# By default extractdir = %{repo}-%{version} with repo = os-diff
# but DLRN generates tarball with <project_name>-<version> as tarball name.
# FTR goname = project_name
%{?dlrn: %global extractdir %{goname}-%{version}}

# Be verbose and print every spec variable the macro sets.
%gometa -v

Name:                   %{goname}
Version:                XXX
Release:                XXX
Summary:                Golang Example Binary
License:                ASL 2.0
URL:                    %{gourl}
Source:                 %{gosource}

# If the dependencies are not packaged, one solution is to ask upstream
# to vendor them with "go mod vendor" and commit the folder.
# Then use ./vendor2provides.py <extracted tarball>/vendor/modules.txt
# to generates the "Provides bundled()" as below.
Provides:               bundled(golang(github.com/fsnotify/fsnotify)) = 1.6.0
Provides:               bundled(golang(github.com/go-ini/ini)) = 1.67.0


%description
This project is an example of Golang project providing a binary.

%gopkg

%prep
# -k keeps the vendor/ folder during the extraction of the tarball
%goprep -k

%build
%gobuild -o bin/new-binary %{goipath}

%install
install -m 0755 -vd             %{buildroot}%{_bindir}
install -m 0755 -vp bin/os-diff %{buildroot}%{_bindir}/

%files
%license LICENSE
%doc README.md
%{_bindir}/*

%changelog

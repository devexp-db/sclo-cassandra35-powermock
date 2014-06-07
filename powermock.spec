Name:           powermock
Version:        1.4.12
Release:        11%{?dist}
Summary:        A Java mocking framework

License:        ASL 2.0
URL:            http://code.google.com/p/powermock/
Source0:        powermock-%{version}.tar.xz
Source1:        make-powermock-sourcetarball.sh
# Disable broken tests.
Patch0:         powermock-disable-broken-tests.patch
# Fix cglib dependency of mockito
Patch2:         powermock-fix-cglib-mockito.patch
# Fix compatibility with JUnit3
Patch3:         powermock-fix-junit3-compat.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  maven-install-plugin
BuildRequires:  objenesis
BuildRequires:  junit4
BuildRequires:  mockito
BuildRequires:  easymock3
BuildRequires:  javassist

%global desc \
PowerMock is a framework that extend other mock libraries\
such as EasyMock with more powerful capabilities. PowerMock uses a\
custom classloader and bytecode manipulation to enable mocking of\
static methods, constructors, final classes and methods, private\
methods, removal of static initializers and more.

%description
%{desc}

%package common
Summary:        Common files for PowerMock

%description common
%{desc}

This package contains common files for all PowerMock modules.

%package reflect
Summary:        Reflection module of PowerMock
Requires:       %{name}-common = %{version}-%{release}

%description reflect
%{desc}

This package contains the reflection module of PowerMock.

%package core
Summary:        Core module of PowerMock
Requires:       %{name}-common = %{version}-%{release}

%description core
%{desc}

This package contains the core module of PowerMock.

%package junit4
Summary:        JUnit4 common module of PowerMock
Requires:       %{name}-common = %{version}-%{release}

%description junit4
%{desc}

This package contains the JUnit4 module of PowerMock.

%package api-support
Summary:        PowerMock API support module
Requires:       %{name}-common = %{version}-%{release}

%description api-support
%{desc}

This package contains support code for the PowerMock API extensions.

%package api-mockito
Summary:        PowerMock Mockito API module
Requires:       %{name}-common = %{version}-%{release}

%description api-mockito
%{desc}

This package contains the PowerMock Mockito API extension.

%package api-easymock
Summary:        PowerMock EasyMock API module
Requires:       %{name}-common = %{version}-%{release}

%description api-easymock
%{desc}

This package contains the PowerMock EasyMock API extension.


%package javadoc
Summary:        JavaDocs for %{name}

%description javadoc
%{desc}

This package contains the API documentation for %{name}.

%prep
%setup -q
%patch0
%patch2
%patch3

# Disable modules that we cannot build (yet).
%pom_disable_module module-test modules
%pom_disable_module junit4-legacy modules/module-impl
%pom_disable_module junit4-rule-agent modules/module-impl
%pom_disable_module junit3 modules/module-impl
%pom_disable_module testng modules/module-impl
%pom_disable_module testng-agent modules/module-impl
%pom_disable_module testng-common modules/module-impl
%pom_disable_module agent modules/module-impl
%pom_disable_module examples
%pom_disable_module release
%pom_disable_module classloading-xstream classloading

%pom_remove_plugin :rat-maven-plugin
%pom_remove_plugin :maven-source-plugin
%pom_xpath_remove "pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"

%mvn_package :powermock-core core
%mvn_package :powermock-classloading-base core
%mvn_package :powermock-classloading-objenesis core
%mvn_package :powermock-module-junit4 junit4
%mvn_package :powermock-module-junit4-rule junit4
%mvn_package :powermock-module-junit4-common junit4
%mvn_package :powermock-api-mockito api-mockito
%mvn_package :powermock-api-support api-support
%mvn_package :powermock-api-easymock api-easymock
%mvn_package :powermock-reflect reflect

%mvn_package org.powermock.tests: __noinstall

# poms are not neede by anything
%mvn_package ::pom: __noinstall

%build
%mvn_build

%install
%mvn_install

%files common
%dir %{_javadir}/%{name}
%doc LICENSE.txt
%files reflect -f .mfiles-reflect
%files core -f .mfiles-core
%files junit4 -f .mfiles-junit4
%files api-support -f .mfiles-api-support
%files api-mockito -f .mfiles-api-mockito
%files api-easymock -f .mfiles-api-easymock

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Michael Simacek <msimacek@redhat.com> - 1.4.12-10
- Enable api-easymock module

* Fri Mar 21 2014 Michael Simacek <msimacek@redhat.com> - 1.4.12-9
- Use mvn_build
- Drop manual requires
- Use pom macros instead of a patch
- Collapse description into a macro

* Fri Jul 26 2013 Alexander Kurtakov <akurtako@redhat.com> 1.4.12-8
- Build against easymock3.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4.12-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Roman Kennke <rkennke@redhat.com> 1.4.12-4
- Use svn export instead of svn checkout for creating source archive
- Remove 3rd party sources from source archive

* Mon May 07 2012 Roman Kennke <rkennke@redhat.com> 1.4.12-3
- Moved JARs to powermock subdirectory
- Removed .svn directories from created source package
- Removed 3rd party source files from created source package

* Mon Apr 30 2012 Roman Kennke <rkennke@redhat.com> 1.4.12-2
- Added javadoc subpackage

* Thu Apr 24 2012 Roman Kennke <rkennke@redhat.com> 1.4.12-1
- Initial package

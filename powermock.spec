Name:           powermock
Version:        1.6.2
Release:        3%{?dist}
Summary:        A Java mocking framework

License:        ASL 2.0
URL:            https://github.com/jayway/powermock
Source0:        https://github.com/jayway/%{name}/archive/%{name}-%{version}.tar.gz

# Fix cglib dependency of mockito
Patch2:         powermock-fix-cglib-mockito.patch
# Fix compatibility with JUnit3
Patch3:         powermock-fix-junit3-compat.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(cglib:cglib-nodep)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.sf.cglib:cglib)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(org.javassist:javassist)
BuildRequires:  mvn(org.mockito:mockito-all)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.objenesis:objenesis)
BuildRequires:  mvn(org.sonatype.oss:oss-parent:pom:)

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
%setup -q -n %{name}-%{name}-%{version}

%patch2
%patch3

# bundled sources of various libraries
rm -r modules/module-impl/agent

find -name '*.java' | xargs sed -i 's/org\.mockito\.cglib/net.sf.cglib/g'

# Assumes different JUnit version
rm modules/module-impl/junit4-common/src/test/java/org/powermock/modules/junit4/common/internal/impl/JUnitVersionTest.java

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

# poms are not needed by anything
%mvn_package ::pom: __noinstall

%build
%mvn_build

%install
%mvn_install

%files common
%dir %{_javadir}/%{name}
%license LICENSE.txt
%files reflect -f .mfiles-reflect
%files core -f .mfiles-core
%files junit4 -f .mfiles-junit4
%files api-support -f .mfiles-api-support
%files api-mockito -f .mfiles-api-mockito
%files api-easymock -f .mfiles-api-easymock

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Michael Simacek <msimacek@redhat.com> - 1.6.2-1
- Update to upstream version 1.6.2
- Update upstream URL
- Use upstream tarball since the bundled files are opensource and thus can be
  removed in %prep

* Tue Jun 10 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1.4.12-12
- Fix FTBFS by dropping obsolete junit4 surefire provider and
  changing BR to junit over junit4.
- Resolves RHBZ#1106669.

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

* Tue Apr 24 2012 Roman Kennke <rkennke@redhat.com> 1.4.12-1
- Initial package

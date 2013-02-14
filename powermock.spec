Name:           powermock
Version:        1.4.12
Release:        7%{?dist}
Summary:        A Java mocking framework
Group:          Development/Libraries

License:        ASL 2.0
URL:            http://code.google.com/p/powermock/
Source0:        powermock-%{version}.tar.xz
Source1:        make-powermock-sourcetarball.sh
# Disable broken tests.
Patch0:         powermock-disable-broken-tests.patch
# Disable modules that we cannot build (yet).
Patch1:         powermock-disable-modules.patch
# Fix cglib dependency of mockito
Patch2:         powermock-fix-cglib-mockito.patch
# Fix compatibility with JUnit3
Patch3:         powermock-fix-junit3-compat.patch

BuildArch:      noarch
BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  maven-local
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  objenesis
BuildRequires:  junit4
BuildRequires:  junit
BuildRequires:  mockito
BuildRequires:  easymock
BuildRequires:  javassist

Requires:       jpackage-utils
Requires:       java

%description
PowerMock is a framework that extend other mock libraries
such as EasyMock with more powerful capabilities. PowerMock uses a
custom classloader and bytecode manipulation to enable mocking of
static methods, constructors, final classes and methods, private
methods, removal of static initializers and more.

%package common
Summary:        Common files for PowerMock

%description common
PowerMock is a framework that extend other mock libraries
such as EasyMock with more powerful capabilities. PowerMock uses a
custom classloader and bytecode manipulation to enable mocking of
static methods, constructors, final classes and methods, private
methods, removal of static initializers and more.

This package contains common files for all PowerMock modules.

%package reflect
Summary:        Reflection module of PowerMock
Requires:       objenesis
Requires:       powermock-common

%description reflect
PowerMock is a framework that extend other mock libraries
such as EasyMock with more powerful capabilities. PowerMock uses a
custom classloader and bytecode manipulation to enable mocking of
static methods, constructors, final classes and methods, private
methods, removal of static initializers and more.

This package contains the reflection module of PowerMock.

%package core
Summary:        Core module of PowerMock
Requires:       powermock-reflect
Requires:       javassist
Requires:       powermock-common

%description core
PowerMock is a framework that extend other mock libraries
such as EasyMock with more powerful capabilities. PowerMock uses a
custom classloader and bytecode manipulation to enable mocking of
static methods, constructors, final classes and methods, private
methods, removal of static initializers and more.

This package contains the core module of PowerMock.

%package junit4
Summary:        JUnit4 common module of PowerMock
Requires:       powermock-core
Requires:       junit4
Requires:       powermock-common

%description junit4
PowerMock is a framework that extend other mock libraries
such as EasyMock with more powerful capabilities. PowerMock uses a
custom classloader and bytecode manipulation to enable mocking of
static methods, constructors, final classes and methods, private
methods, removal of static initializers and more.

This package contains the JUnit4 module of PowerMock.

%package api-support
Summary:        PowerMock API support module
Requires:       powermock-core
Requires:       powermock-common

%description api-support
PowerMock is a framework that extend other mock libraries
such as EasyMock with more powerful capabilities. PowerMock uses a
custom classloader and bytecode manipulation to enable mocking of
static methods, constructors, final classes and methods, private
methods, removal of static initializers and more.

This package contains support code for the PowerMock API extensions.

%package api-mockito
Summary:        PowerMock Mockito API module
Requires:       powermock-api-support
Requires:       mockito
Requires:       cglib
Requires:       powermock-common

%description api-mockito
PowerMock is a framework that extend other mock libraries
such as EasyMock with more powerful capabilities. PowerMock uses a
custom classloader and bytecode manipulation to enable mocking of
static methods, constructors, final classes and methods, private
methods, removal of static initializers and more.

This package contains the PowerMock Mockito API extension.

%package javadoc
Summary:        JavaDocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
PowerMock is a framework that extend other mock libraries
such as EasyMock with more powerful capabilities. PowerMock uses a
custom classloader and bytecode manipulation to enable mocking of
static methods, constructors, final classes and methods, private
methods, removal of static initializers and more.

This package contains the API documentation for %{name}.

%prep
%setup -q
%patch0
%patch1
%patch2
%patch3

%build
mvn-rpmbuild -DargLine=-XX:-UseSplitVerifier install javadoc:aggregate

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
cp -p reflect/target/powermock-reflect-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-reflect.jar
cp -p core/target/powermock-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-core.jar
cp -p modules/module-impl/junit4-common/target/powermock-module-junit4-common-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-junit4-common.jar
cp -p modules/module-impl/junit4/target/powermock-module-junit4-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-junit4.jar
cp -p api/support/target/powermock-api-support-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-api-support.jar
cp -p api/mockito/target/powermock-api-mockito-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-api-mockito.jar

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}.pom
install -pm 644 reflect/pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-reflect.pom
install -pm 644 core/pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-core.pom
install -pm 644 modules//pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-modules.pom
install -pm 644 modules/module-impl/junit4-common/pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-junit4-common.pom
install -pm 644 modules/module-impl/junit4/pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-junit4.pom
install -pm 644 api/pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-api.pom
install -pm 644 api/support/pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-api-support.pom
install -pm 644 api/mockito/pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-api-mockito.pom

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%add_maven_depmap JPP.%{name}-%{name}.pom
%add_maven_depmap JPP.%{name}-%{name}-modules.pom
%add_maven_depmap JPP.%{name}-%{name}-api.pom
%add_maven_depmap JPP.%{name}-%{name}-reflect.pom %{name}/%{name}-reflect.jar -f "reflect"
%add_maven_depmap JPP.%{name}-%{name}-core.pom %{name}/%{name}-core.jar -f "core"
%add_maven_depmap JPP.%{name}-%{name}-junit4-common.pom %{name}/%{name}-junit4-common.jar -f "junit4"
%add_maven_depmap JPP.%{name}-%{name}-junit4.pom %{name}/%{name}-junit4.jar -f "junit4"
%add_maven_depmap JPP.%{name}-%{name}-api-support.pom %{name}/%{name}-api-support.jar -f "api-support"
%add_maven_depmap JPP.%{name}-%{name}-api-mockito.pom %{name}/%{name}-api-mockito.jar -f "api-mockito"

%files common
%{_mavenpomdir}/JPP.%{name}-%{name}.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-modules.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-api.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt

%files reflect
%{_javadir}/%{name}/%{name}-reflect.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-reflect.pom
%{_mavendepmapfragdir}/%{name}-reflect
%doc LICENSE.txt

%files core
%{_javadir}/%{name}/%{name}-core.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-core.pom
%{_mavendepmapfragdir}/%{name}-core
%doc LICENSE.txt

%files junit4
%{_javadir}/%{name}/%{name}-junit4-common.jar
%{_javadir}/%{name}/%{name}-junit4.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-junit4-common.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-junit4.pom
%{_mavendepmapfragdir}/%{name}-junit4
%doc LICENSE.txt

%files api-support
%{_javadir}/%{name}/%{name}-api-support.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-api-support.pom
%{_mavendepmapfragdir}/%{name}-api-support
%doc LICENSE.txt

%files api-mockito
%{_javadir}/%{name}/%{name}-api-mockito.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-api-mockito.pom
%{_mavendepmapfragdir}/%{name}-api-mockito
%doc LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
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

#!/bin/sh

VERSION=1.4.12
SRCDIR=powermock-${VERSION}

svn export http://powermock.googlecode.com/svn/tags/powermock-${VERSION} ${SRCDIR}
rm -rf ${SRCDIR}/modules/module-impl/agent
rm -rf ${SRCDIR}/modules/module-impl/junit4-rule-agent/src/main/java/org/junit
tar -cvJf powermock-${VERSION}.tar.xz ${SRCDIR}


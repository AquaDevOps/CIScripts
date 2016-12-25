def maven_build(pom):
    return 'mvn -f %s clean install -U' % pom

def maven_generate(pom):
    return 'mvn archetype:generate -DgroupId=%s -DartifactId=%s -DpackageName=%s -Dversion=%s -DbaseDir=%s' % (
        pom.groupId, pom.artifactId, pom.package, pom.version, pom.path
        )

def maven_get(pom):
    return 'mvn dependency:get -DgroupId=%s -DartifactId=%s -Dversion=%s -U' % (
        pom.groupId, pom.artifactId, pom.version)

# versions:set -DnewVersion=dddd
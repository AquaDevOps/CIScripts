def maven(pom):
    return 'mvn -f %s clean install' % pom
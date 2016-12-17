@NonCPS
def parseJson(text) {
    content = new groovy.json.JsonSlurperClassic().parseText(text)
    return content
}
@NonCPS
def findStep(sequence, groupId, artifactId) {
    return sequence.find{step ->
        groupId == step.groupId && artifactId == step.artifactId
    }
}
@NonCPS
def modifyProperty(pom, properties) {
    node = pom.getProperties()
    properties.each{key, value ->
        node.setProperty(key, value)
    }
}
@NonCPS
def modifyParent(pom, version) {
    pom.getParent().setVersion(version)
}

node {
    def maven = "${tool('Local Maven')}/bin/mvn"
    def sequence

    stage('Checkout SCM') {
        checkout([
            $class: 'SubversionSCM',
            locations: [[
                local: "scm",
                remote: "${params.SCM_CODE_URL}",
                depthOption: 'infinity',
                credentialsId: params.SCM_CODE_CREDIT,
                ignoreExternalsOption: true,
            ]],
            workspaceUpdater: [$class: 'UpdateWithRevertUpdater'],
            ])
        checkout([
            $class: 'GitSCM',
            branches: [[name: '*/master']],
            extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'script']],
            userRemoteConfigs: [[
                url: params.SCM_SCRIPT_URL
            ]],
            doGenerateSubmoduleConfigurations: false,
            ])
    }

    stage('Maven Sequence') {
        sh([
            "python script/${params.SCM_SCRIPT_PATH}",
            "--root=scm",
            "--target=${params.BUILD_TARGET}",
            "--output=sequence",
            ].join(' '))
        sequence = parseJson(readFile(file: 'sequence', encoding: 'utf-8'))
        print('sequence count:' + sequence.size())
    }

    stage('Maven Config') {
        properties = "cfw-version=2.0.0-M2-SNAPSHOT"
        
        step = findStep(sequence, 'com.gsafety.cloudframework', 'cloud-parent-runenv')
        pom = readMavenPom(file: step.path)
        
        modifyProperty(pom, readProperties(text: properties))
        
        writeMavenPom(model: pom, file: step.path)
        
        version = '2.0.0-M2-SNAPSHOT'
        sh("${maven} -f ${step.path} versions:set -DnewVersion=${version}")
    }

    stage('Maven Prepare') {
        version = '2.0.0-M2-SNAPSHOT'

        for(step in sequence) {
            pom = readMavenPom(file: step.path)

            if (pom.getParent() != null) {
                modifyParent(pom, version)
            }

            writeMavenPom(model: pom, file: step.path)
            // sh("${maven} -f ${step.path} versions:update-parent -DnewVersion=${version}")
        }
    }

    stage('Maven Build') {
        floor = Integer.parseInt(params.BUILD_FLOOR)-1
        cell = sequence.size()
        for (i = floor; i < cell; i++) {
            println(String.format('building %03d : %s', i+1, sequence[i].path))
            sh("${maven} -f ${sequence[i].path} clean install -U")
        }
    }

    stage('Archive') {
        archive = "scm/${params.ARCHIVE}"
        println('archiving : ' + archive)
        archiveArtifacts(artifacts: archive, onlyIfSuccessful: true)
    }

    stage('Deploy') {
        println("Deploy Trigger: ${params.DEPLOY_TRIGGER}")
        if (params.DEPLOY_TRIGGER) {
            build(job: params.DEPLOY_JOB, parameters: [
                string(name: 'DEPLOY_SOURCE_JOB', value: env.JOB_NAME),
                string(name: 'DEPLOY_SOURCE_PATH', value: params.DEPLOY_SOURCE_PATH),
                string(name: 'DEPLOY_CONTAINER_URL', value: params.DEPLOY_CONTAINER_URL),
                string(name: 'DEPLOY_CONTAINER_PATH', value: params.DEPLOY_CONTAINER_PATH),
                ])
        }
    }

    stage('TEST') {
        // 尚未实现
    }
}
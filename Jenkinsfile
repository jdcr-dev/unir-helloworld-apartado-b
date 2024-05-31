pipeline {
    agent any    

    environment {
        STASH_CALCULADORA = 'CALCULADORA'
        STASH_RESULTADOS_UNIT = 'TEST_UNIT_RESULTS'
        STASH_RESULTADOS_REST = 'TEST_REST_RESULTS'
    }

    options {
        skipDefaultCheckout(true)
    }
    
    stages {
        stage('Get Code') {
            steps {
                git branch: 'feature_fix_coverage', url: 'https://github.com/jdcr-dev/unir-helloworld-apartado-b'
                
                // Correccion respecto a la practica anterior donde le hacia en otro stage y podia tener problemas
                stash name: STASH_CALCULADORA, includes: '**'
            }
            post {
                always {            
                    cleanWs()                    
                }
            }
        }
        
        stage('Static') {
            steps {
                unstash name: STASH_CALCULADORA

                bat '''
                    flake8 --exit-zero --format=pylint app > flake8.out
                '''
                recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], 
                    qualityGates:[
                        [threshold: 8, type: 'TOTAL', unstable: true], 
                        [threshold: 10, type:'TOTAL', unstable: false]],
                    enabledForFailure: true // https://github.com/jenkinsci/warnings-ng-plugin/blob/main/plugin/src/main/java/io/jenkins/plugins/analysis/core/steps/IssuesRecorder.java
            }
            post {
                always {            
                    cleanWs()                    
                }
            }
        }
        
        stage('Security Test') {
            steps {
                unstash name: STASH_CALCULADORA

                bat '''
                    bandit --exit-zero -r . -f custom -o bandit.out --severity-level medium --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                '''
            
                recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], 
                    qualityGates:[
                        [threshold: 2, type: 'TOTAL', unstable: true], 
                        [threshold: 4, type:'TOTAL', unstable: false]],
                    enabledForFailure: true
            }
            post {
                always {            
                    cleanWs()                    
                }
            }
        }                
        
        stage('Unit - Coverage') {
            steps {
                unstash name: STASH_CALCULADORA

                bat '''                                                                                                                                                                                      
                set PYTHONPATH=%WORKSPACE%
                coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest --junitxml=result-unit.xml test\\unit
                coverage xml
                '''
                catchError(buildResult:'UNSTABLE', stageResult: 'FAILURE') {
                    cobertura coberturaReportFile: 'coverage.xml', onlyStable: false, failUnstable: false, conditionalCoverageTargets: '100,80,90', lineCoverageTargets: '100,85,95'
                    junit 'result*.xml'
                }
            }
            post {
                always {            
                    cleanWs()                    
                }
            }
        }
        
        stage('Rest'){
            steps {
                unstash name: STASH_CALCULADORA
                
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {                            
                    bat '''                                                                                                                    
                        set FLASK_APP=app/api.py
                        start /B flask run                                                                                                         
                        
                        timeout /t 10 /nobreak 1> nul

                        set PYTHONPATH=%WORKSPACE%
                        pytest --junitxml=result-rest.xml --junitxml=result-rest.xml test/rest                        
                    '''
                    junit 'result*.xml'
                }
            }
            // post {
            //     always {            
            //         cleanWs()                    
            //     }
            // }
        }
        
        stage('Performance') {
            steps {
                bat 'D:\\Autoaprendizaje\\DevopsUnir\\apache-jmeter-5.6.3\\bin\\jmeter -n -t D:\\Autoaprendizaje\\DevopsUnir\\apache-jmeter-5.6.3\\bin\\P24-ApartadoB.jmx -f -l flask.jtl'
                perfReport sourceDataFiles: 'flask.jtl'
            }
            post {
                always {            
                    cleanWs()                    
                }
            }           
        }
    }
}
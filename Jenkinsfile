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
                git 'https://github.com/jdcr-dev/unir-helloworld'
                
                // Correccion respecto a la practica anterior donde le hacia en otro stage y podia tener problemas
                stash name: STASH_CALCULADORA, includes: '**'
            }
        }
        
        stage('Static') {
            steps {
                bat '''
                    flake8 --exit-zero --format=pylint app > flake8.out
                '''
                recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], qualityGates:[[threshold: 8, type: 'TOTAL', unstable: true], [threshold: 10, type:'TOTAL', unstable: true]]
            }
        }
        
        stage('Security') {
            steps {
                bat '''
                    bandit --exit-zero -r . -f custom -o bandit.out --severity-level medium --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                '''
                recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], qualityGates:[[threshold: 1, type: 'TOTAL', unstable: true], [threshold: 2, type:'TOTAL', unstable: true]]
            }
        }
        
        stage('Performance') {
            steps {
                bat 'D:\\Autoaprendizaje\\DevopsUnir\\apache-jmeter-5.6.3\\bin\\jmeter -n -t D:\\Autoaprendizaje\\DevopsUnir\\apache-jmeter-5.6.3\\bin\\P24.jmx -f -l flask.jtl'
                perfReport sourceDataFiles: 'flask.jtl'
            }
        }
        
        stage('Build') {
            steps {
                echo 'Eyyy, esto es Python. No hay que compilar nada!!!'
                echo WORKSPACE
                bat 'dir'
            }
        }
        
        stage('Start Flask') {
            steps {
                bat '''
                    set FLASK_APP=app/api.py
                    start flask run
                '''
            }
        }

        stage('Wait for Flask') {
            steps {
                script {
                    def retries = 0
                    def maxRetries = 3
                    def urlToCheck = 'http://localhost:5000'

                    // Esperamos que la aplicación este lista o que alcance la espera máxima que consideremos
                    while (retries < maxRetries) {           
                        def curlCommand = "curl -s -o NUL -w %%{http_code} ${urlToCheck}"                                                  
                        def httpResponse = bat(script: curlCommand, returnStdout: true).trim()                        

                        if (httpResponse.tokenize().last() == '200') {
                            echo "Info: Flask Arrancado"
                            break
                        } else {
                            echo "Warning: Esperando que Flask arranque"
                            sleep time: 5, unit: 'SECONDS'
                            retries++
                        }
                    }

                    if (retries == maxRetries) {
                        error "Timeout: La aplicación no arrancó pasados ${maxRetries * 5} segundos"
                    }
                }
            }
        }
        stage('Test'){
            parallel {
                stage('Unit') {
                    steps {                        
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {                            
                            bat '''                                
                                set PYTHONPATH=%WORKSPACE%
                                pytest --junitxml=result-unit.xml test/unit
                            '''
                            stash name: STASH_RESULTADOS_UNIT, includes: 'result-unit.xml'
                        }
                    }
                }
                    
                stage('Rest'){
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {                            
                            bat '''                                                                                                                    
                                set PYTHONPATH=%WORKSPACE%
                                pytest --junitxml=result-rest.xml test/rest
                            '''
                            stash name: STASH_RESULTADOS_REST, includes: 'result-rest.xml'
                        }
                    }
                }
            }
        }
        
        stage('Cobertura') {
            steps {
                bat '''
                coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest test\\unit
                    coverage xml
                '''
                catchError(buildResult:'UNSTABLE', stageResult: 'FAILURE') {
                    cobertura coberturaReportFile: 'coverage.xml', onlyStable: false, failUnstable: false, conditionalCoverageTargets: '10,10,10', lineCoverageTargets: '100,80,98'
                }
            }
        }
        
        stage('Results') {
            steps {
                unstash STASH_RESULTADOS_UNIT
                unstash STASH_RESULTADOS_REST
                
                junit 'result*.xml'
                echo 'FINISH'
            }
        }
    }
}
pipeline {
    agent {
        kubernetes {
            yamlFile 'jenkins/pod-templates/devops.yaml'
            defaultContainer 'ci'
        }
    }

    stages {

        stage('Debug') {
            steps {
                container('ci') {
                    sh '''
                        echo "Debug stage"
                        hostname
                        python --version
                        env | sort
                        ls -la
                    '''
                }
            }
        }

        stage('Unit Tests') {
            steps {
                container('ci') {
                  sh '''
                    echo "Running unit tests"
                    # This tells Python that the 'app' folder contains our packages
                    export PYTHONPATH=$PYTHONPATH:$(pwd)/app
                    pytest app/tests/test_app.py
                  '''
                }
            }
        }

        stage('Build') {
            steps {
                container('ci') {
                    sh '''
                        echo "Build validation"
                        python -m py_compile app/src/app.py
                    '''
                }
            }
        }

        stage('Terraform Validate') {
            steps {
                container('ci') {
                    sh '''
                        echo "Terraform validation"
                        cd terraform
                        terraform init
                        terraform validate
                    '''
                }
            }
        }

        stage('OPA Policy Check') {
            steps {
                container('ci') {
                    sh '''
                        echo "Running OPA policy checks"
                        opa eval \
                          --format pretty \
                          --data app/opa/terraform.rego \
                          --input terraform/main.tf \
                          "data.terraform.security"
                    '''
                }
            }
        }

        stage('Terraform Security') {
            steps {
                container('ci') {
                  sh '''
                    echo "Running Checkov"
                    # 1. Run offline
                    checkov -d terraform -o json --no-guide > checkov.json || true
                
                    # 2. Parse results safely
                    TOTAL=$(jq '.summary.total_checks' checkov.json)
                    FAILED=$(jq '.summary.failed' checkov.json)
                
                    # Default to 0 if null/empty
                    TOTAL=${TOTAL:-0}
                    FAILED=${FAILED:-0}

                    if [ "$TOTAL" -gt 0 ]; then
                      FAILURE_RATE=$(echo "scale=2; ($FAILED / $TOTAL) * 100" | bc)
                    else
                      FAILURE_RATE=0
                    fi

                    echo "Checkov failure rate: $FAILURE_RATE%"

                    # 3. Use bc for floating point comparison
                    if (( $(echo "$FAILURE_RATE > 10" | bc -l) )); then
                      echo "❌ Failure rate exceeds 10%"
                      exit 1
                    fi
                  '''
                }
            }
        }

        stage('Deploy.Run') {
            steps {
                container('ci') {
                sh '''
                  echo "Deploying and Running App"
                  # 1. Move into the 'app' directory so 'src' is visible
                  cd app
                
                  # 2. Set PYTHONPATH to the current directory
                  export PYTHONPATH=.
                
                  # 3. Run using the module flag (-m)
                  # Note: No '.py' extension here!
                  python3 -m src.app 3 5
                '''
                }
            }
        }
    }
}
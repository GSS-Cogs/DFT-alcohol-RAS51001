pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Clean') {
            steps {
                sh 'rm -rf out'
            }
        }
        stage('Transform') {
            agent {
                docker {
                    image 'cloudfluff/databaker'
                    reuseNode true
                }
            }
            steps {
                sh "jupyter-nbconvert --output-dir=out --ExecutePreprocessor.timeout=None --execute 'Estimated number of reported drink drive accidents and casualties in Great Britain 1979 - 2016.ipynb'"
                sh "jupyter-nbconvert --output-dir=out --ExecutePreprocessor.timeout=None --execute 'Reported road casualties in Great Britain, provisional estimates involving illegal alcohol levels.ipynb'"
            }
        }
        stage('Review') {
            steps {
                error "Needs review"
            }
        }
    }
    post {
        always {
            archiveArtifacts 'out/*'
        }
    }
}

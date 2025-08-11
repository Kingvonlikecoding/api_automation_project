pipeline {
    agent any
    
    tools {
        python 'Python3'  // 确保Jenkins中已配置Python环境
    }
    
    environment {
        ALLURE_RESULTS_DIR = 'allure-results'
        ALLURE_REPORT_DIR = 'allure-report'
    }
    
    triggers {
        pollSCM('H/15 * * * *')  // 每15分钟检查一次代码变更
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    // 安装项目依赖
                    bat 'pip install -r requirements.txt'
                    // 安装allure-commandline
                    bat 'pip install allure-commandline'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    try {
                        bat 'python -m pytest --alluredir=allure-results'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Test execution failed: ${e.message}")
                    }
                }
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                script {
                    // 生成Allure报告
                    bat 'allure generate ${ALLURE_RESULTS_DIR} -o ${ALLURE_REPORT_DIR} --clean'
                }
            }
        }
    }
    
    post {
        always {
            // 归档Allure报告
            archiveArtifacts artifacts: "${ALLURE_REPORT_DIR}/**"
            
            // 发送邮件通知
            emailext (
                subject: "${currentBuild.currentResult}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>构建状态: ${currentBuild.currentResult}</p>
                    <p>构建编号: ${env.BUILD_NUMBER}</p>
                    <p>构建详情: ${env.BUILD_URL}</p>
                    <p>Allure报告: ${env.BUILD_URL}artifact/${ALLURE_REPORT_DIR}/index.html</p>""",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                to: '${DEFAULT_RECIPIENTS}',  // 在Jenkins系统配置中设置默认收件人
                attachLog: true
            )
        }
        
        cleanup {
            // 清理工作空间
            cleanWs()
        }
    }
}

pipeline{
    agent any
    
    stages{
        stage ("Git Checkout"){
            steps{
                git url: "https://github.com/pushkarshajapurkar/two-tier-flask-app.git", branch: "master"
            }
        }
        stage ("Image Build"){
            steps{
                sh "docker build . -t two_tier_flask_app"
            }
        }
        stage ("Image Push To DockerHub"){
            steps{
                withCredentials([usernamePassword(credentialsId: "dockerHub", passwordVariable: "dockerHubPass", usernameVariable: "dockerHubUser")]){
                    sh "docker image tag two_tier_flask_app ${env.dockerHubUser}/two_tier_flask_app:latest"
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                    sh "docker push ${env.dockerHubUser}/two_tier_flask_app:latest"
                }
            }
        }
        stage ("Deploying the App"){
            steps{
                sh "docker-compose down && docker-compose up -d"
            }
        }
    }
}

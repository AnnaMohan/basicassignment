pipeline {
    agent any

    environment {
        APP_NAME = "application"
    }
    stages{
        stage('Clone Repository') {
            steps {
                script {
                    git branch: 'main', 
                    // credentialsId: 'your-credentials-id', 
                    url: 'https://github.com/AnnaMohan/basicassignment.git'
                }
            }
        }


        stage('Deploy to Server') {
            
            steps {
                sshagent(credentials: ['8d9ba472-7d7d-4851-b1b6-424eda51a4a6']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ec2-user@ec2-18-206-225-65.compute-1.amazonaws.com << 'EOF'
                        cd /home/ec2-user  # Change to your deployment directory if needed
                        python3 -m venv venv
                        source venv/bin/activate
                        #rm -rf basicassignment # instead remainign whole folder
                        pkill -f application.py # to kill the existing process to deploye new version of appln
                        sudo yum update -y
                        sudo yum install git -y
                        git clone https://github.com/AnnaMohan/basicassignment.git
                        cd ./basicassignment
                        echo $(pwd)
                        pip install -r requirements.txt
                        echo "****************************"
                        cat requirements.txt
                        echo "****************************"
                        echo $(pwd)
                        # export PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
                        # echo "Public IP: $PUBLIC_IP"
                        # export PORT=5000
                        # echo "PORT": $PORT
                        nohup python3 -u application.py >> flask.log 2>&1 & # appending logs to flask.log
                        #nohup python3 application.py > flask.log 2>&1 & # to store logs
                        #/dev/null 2>&1 & # to not to store logs 
                        #> std.out 2> std.err &
                        #disown #not sure why gpt suggested
                        exit #      to exit from ssh session so that pipeline will end.
                        #app.log 2>&1 &
                        #nohup python3 application.py 
                        #>/dev/null 2>&1 & 
                        EOF
                        
                    '''
                }
            }

        }
    }

    post {
        success {
            echo "Flask app deployed successfully!!"
        }
        failure {
            echo "Deployment failed!OOPS!!"
        }
    }
}

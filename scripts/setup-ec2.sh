# Setup EC2 to run sample python application
# Ref: https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-python3-boto3/
yum check-update
# install python3
sudo yum install python3 -y
python3 -m venv my_udacity_app/env
source ~/my_udacity_app/env/bin/activate
# upgrade pip
pip install pip --upgrade
# install python mysql driver
pip install mysql-connector-python




# import boto3
# client = boto3.client('sns')
#
# response = client.publish(TopicArn = "arn:aws:sns:us-east-1:396700303200:deviceStatus", Message="hello from aws", Subject = "aws sns")


from setupDB import UserDeviceDB
from flask import Flask, request, render_template
import boto3
# client = boto3.client('sns')



app = Flask(__name__, template_folder='../webserver/staticTemplates')
dbClient = UserDeviceDB("flow.db")

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/device-serial')
def deviceSerial():
    id = request.args.get('id')
    dbClient.update('d', [id, 'not-full'])
    #call alex's stuff
    print(id)
    return {"Status Code" : 200}



@app.route('/status', methods=['POST'])
def updateStatus():
    id = request.form.get('id')
    # get email from database using alex's code
    # alex makes query to get topicArn associated with this specific id.
    topicArn = "arn:aws:sns:us-east-1:396700303200:deviceStatus"

    response = client.publish(TopicArn = topicArn, Message="hello from aws", Subject = "aws sns")

    return "Sent Status Update"

@app.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    topicName = email.replace('@', '_').replace('.', '_')
    id = request.form.get('id')
    phoneNum = request.form.get('number')

    # call alex's code and see if email is valid and device id is valid

    response = client.create_topic(Name= topicName)
    topicArn = response.get('TopicArn')
    res = client.subscribe(TopicArn=topicArn, Protocol='email', Endpoint=email)
    # put data into database with alex's code

    return {'Status Code' : 200}








if __name__ == '__main__':

    # app.run(host='0.0.0.0')
    app.run()

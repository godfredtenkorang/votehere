from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'JesusIsLord'

@app.route("/", methods=["POST", "GET"])
def ussd_api():
    data = request.get_json()

    if data['USERID'] == 'gobrite':
        if data['MSGTYPE']:
            session['level'] = 'start'
            response = dict(USERID="gobrite", MSISDN="233248985021", MSG="Welcome to Gooey Vote.\nEnter Nominee Id", MSGTYPE=True)
        else:
            if 'level' in session:
                level = session['level']
                if level == 'start':
                    session['level'] = 'candidate'
                    session['candidate_id'] = data['USERDATA']

                    # select from the database the user with this id
                    name = "Kojo Men Sah"
                    response = dict(USERID="gobrite", MSISDN="233248985021", MSG=f"Confirm candidate\nName: {name}\n1) Confirm\n Cancel", MSGTYPE=True)
                elif level == 'candidate':
                    userdata = data['USERDATA']
                    if userdata == 1:
                        session['level'] = 'votes'
                        session['votes'] = userdata
                        response = dict(USERID="gobrite", MSISDN="233248985021", MSG="Enter the number of votes", MSGTYPE=True)
                    elif userdata == 2:
                        session.clear()
                        response = dict(USERID="gobrite", MSISDN="233248985021", MSG="You have cancelled", MSGTYPE=False)
                    else:
                        session.clear()
                        response = dict(USERID="gobrite", MSISDN="233248985021", MSG="You have entered an invalid data", MSGTYPE=False)
                elif level == 'votes':
                    votes = session['votes']
                    response = dict(USERID="gobrite", MSISDN="233248985021", MSG=f"You have entered {votes} votes", MSGTYPE=False)
                else:
                    response = dict(USERID="gobrite", MSISDN="233248985021", MSG="Welcome2to Jesus Christ of Nazareth",
                                    MSGTYPE=False)
            else:
                response = dict(USERID="gobrite", MSISDN="233248985021", MSG="You are not in a session", MSGTYPE=False)
    else:
        response = dict(USERID="gobrite", MSISDN="233248985021", MSG="you have entered a wrong value", MSGTYPE=False)

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)

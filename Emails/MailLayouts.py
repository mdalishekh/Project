# This module is specially made for sending mails to users for OTP verifications

# This function is responsible for sending mails to users for OTP verifications layout
def otp_mail_layout(user_first_name, OTP):
    otp_layout  = f'''
                 <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>OTP Email Template</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            width: 100%;
            max-width: 400px;
            margin: 0 auto; /* Centering the container */
            padding: 20px;
        }}
        .header {{
            background-color: #020c0d;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            border-radius: 4px;
        }}
        .content {{
            padding: 20px;
            text-align: center;
        }}
        .otp-container {{
            background-color: #020c0d;
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            margin: 20px auto;
            border-radius: 4px;
            width: 130px;
        }}
        .expiry-note {{
            font-size: 14px;
            color: #666666;
            margin-top: 20px;
        }}
        .footer {{
            font-size: 12px;
            color: #999999;
            text-align: center;
            padding: 10px;
            border-top: 1px solid #eeeeee;
        }}
    </style>
</head>
<body>
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; padding: 20px;">
        <tr>
            <td align="center">
                <div class="container">
                    <div class="header">Hi, {user_first_name}</div>
                    <div class="content">
                        <p>Your One Time Password is here below</p>
                        <div class="otp-container">{OTP}</div>
                        <p class="expiry-note">Please note this OTP will expire in 5 minutes</p>
                    </div>
                    <div class="footer">
                        This is an automated email. Please do not reply.
                    </div>
                </div>
            </td>
        </tr>
    </table>
</body>
</html>

'''
    return otp_layout


# This function is responsible to sending confirmation mail layout
def confirmation_mail_layout(user_first_name):
    confirmation_layout = f"""
                           <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmation Email</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-width: 400px;
            text-align: center;
        }}
        .header {{
            background-color: #020c0d;
            color: white;
            padding: 15px;
            font-size: 1.2em;
            font-family:  Geneva, Tahoma, sans-serif;
            border-radius: 8px 8px 0 0;
        }}
        .content {{
            margin: 20px 0;
        }}
        .created-account {{
            background-color: #020c0d;
            color: white;
            padding: 10px;
            font-size: 1em;
            font-family:  Geneva, Tahoma, sans-serif;
            border-radius: 4px;
            width: 80%;
            margin: 10px auto;
        }}
        .footer {{
            font-size: 0.9em;
            color: #777;
            margin-top: 20px;
        }}
        .footer-line {{
            border-top: 1px solid #ddd;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Confirmation Email</div>
        <div class="content">
            <p>Congratulations, {user_first_name} You have been successfully registered.</p>
            <div class="created-account">Your account has been created!</div>
            <p>Thank you for joining us. We're excited to have you on board.</p>
        </div>
        <div class="footer">
            <div class="footer-line"></div>
            <p>This is an automated email. Please do not reply.</p>
        </div>
    </div>
</body>
</html>

                           """
    return confirmation_layout
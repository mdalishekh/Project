# This module is specially made for sending mails to users for OTP verifications

# This function is responsible for sending mails to users for OTP verifications
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
                    <div class="header">Welcome {user_first_name}</div>
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

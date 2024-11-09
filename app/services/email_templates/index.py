def render_succed_email(dados):
    html_template = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">
    <head>
        <meta charset="UTF-8">
        <meta content="width=device-width, initial-scale=1" name="viewport">
        <meta name="x-apple-disable-message-reformatting">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta content="telephone=no" name="format-detection">
        <title>New Message 2</title>
        <!-- HTML and CSS content here -->
    </head>
    <body style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
        <div dir="ltr" class="es-wrapper-color" lang="en" style="background-color:#FAFAFA">
            <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" role="none" style="width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#FAFAFA">
                <tr>
                    <td valign="top" style="padding:0;Margin:0">
                        <table cellpadding="0" cellspacing="0" class="es-content" align="center" role="none" style="width:100%">
                            <tr>
                                <td align="center" style="padding:0;Margin:0">
                                    <table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" role="none" style="width:600px">
                                        <tr>
                                            <td align="left" style="padding-bottom:10px;padding-left:20px;padding-right:20px;padding-top:30px">
                                                <table cellpadding="0" cellspacing="0" width="100%" role="none">
                                                    <tr>
                                                        <td align="center" valign="top" style="width:560px">
                                                            <table cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                                                <tr>
                                                                    <td align="center" style="padding-top:10px;padding-bottom:10px;font-size:0px">
                                                                        <img src="https://em-content.zobj.net/source/apple/391/fire_1f525.png" alt="" style="display:block;border:0;outline:none;text-decoration:none" width="100" height="100">
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" class="es-m-txt-c" style="padding-bottom:10px">
                                                                        <h1 style="font-size:46px;font-weight:bold;color:#333333">Bem vindo a Firetest</h1>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" class="es-m-p0r es-m-p0l" style="padding-top:5px;padding-bottom:5px;padding-left:40px;padding-right:40px">
                                                                        <p style="line-height:21px;color:#333333;font-size:14px">We will keep you updated with the latest novelties, discounts, sales, new and seasonal collections, as well as events and news!</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="padding-top:10px;padding-bottom:10px;padding-left:20px;padding-right:20px">
                                                <table cellpadding="0" cellspacing="0" width="100%" role="none">
                                                    <tr>
                                                        <td align="center" valign="top" style="width:560px">
                                                            <table cellpadding="0" cellspacing="0" width="100%" style="border-left:2px dashed #cccccc;border-right:2px dashed #cccccc;border-top:2px dashed #cccccc;border-bottom:2px dashed #cccccc;border-radius:5px" role="presentation">
                                                                <tr>
                                                                    <td align="center" class="es-m-txt-c" style="padding-top:20px;padding-left:20px;padding-right:20px">
                                                                        <h2 style="font-size:26px;font-weight:bold;color:#333333">Email:</h2>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" class="es-m-txt-c" style="padding-top:10px;padding-bottom:20px;padding-left:20px;padding-right:20px">
                                                                        <h1 style="font-size:46px;font-weight:bold;color:#cc0000"><strong>{email}</strong></h1>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="padding-top:10px;padding-bottom:10px;padding-left:20px;padding-right:20px">
                                                <table cellpadding="0" cellspacing="0" width="100%" role="none">
                                                    <tr>
                                                        <td align="center" valign="top" style="width:560px">
                                                            <table cellpadding="0" cellspacing="0" width="100%" style="border-left:2px dashed #cccccc;border-right:2px dashed #cccccc;border-top:2px dashed #cccccc;border-bottom:2px dashed #cccccc;border-radius:5px" role="presentation">
                                                                <tr>
                                                                    <td align="center" class="es-m-txt-c" style="padding-top:20px;padding-left:20px;padding-right:20px">
                                                                        <h2 style="font-size:26px;font-weight:bold;color:#333333">Senha:</h2>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" class="es-m-txt-c" style="padding-top:10px;padding-bottom:20px;padding-left:20px;padding-right:20px">
                                                                        <h1 style="font-size:46px;font-weight:bold;color:#cc0000"><strong>{password}</strong></h1>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
    return html_template.format(email=dados['email'], password=dados['password'])


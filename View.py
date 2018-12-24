import webbrowser



def set_message(msg):
    f = open('helloworld.html', 'w')
    message = """<head></head>
        <body><p>AMK_MNA Web crawler!</p>
        <p>
        """ + msg + """
        </p>
        </body>
        </html>"""
    f.write(message)
    f.close()
def open_page():
    webbrowser.open_new_tab('helloworld.html')




from template import Template

if __name__ == '__main__':
    t = """
        <!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <meta http-equiv='X-UA-Compatible' content='ie=edge'>
            <title>Document</title>
        </head>
        <body>
            {# comments #}
            <p>Test</p>
        </body>
        </html>
    """

    template = Template(t)

    print(template.render())

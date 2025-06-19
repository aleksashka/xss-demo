import html
import time
import hashlib

from flask import Flask, request, make_response


app = Flask(__name__)

template_start = """
<html>
    <head>
        <title>XSS Demo</title>
    </head>
    <body>
        <h2>Очередной классный пост</h2>
        Интересный текст
        <hr>
        <h3>Комментарии:</h3>
"""

template_end = """
        <hr>
        <h3>Введите свой комментарий:</h3>
        <form method="post">
            <textarea name="message" rows="10" cols="80"></textarea><br>
            <button type="submit">Отправить</button>
        </form>
    </body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    global template_start, template_end
    html_content = template_start

    if request.method == "POST":
        user_text = request.form.get("message", "").strip()
    else:
        user_text = ""

    if user_text:
        html_content += user_text
    html_content += template_end

    response = make_response(html_content)
    if request.method == "GET":
        auth_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
        response.set_cookie("auth_id", auth_id)
        response.set_cookie("admin", "True")
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


"""
<script>
    alert(document.cookie);
</script>
"""


"""
Срочно отправьте этот текст на email: a@stex.kz
<div id="cookies"></div>
<script>
    document.getElementById("cookies").textContent = document.cookie;
</script>
"""


"""
<script>
    location.href="http://ip4.me";
</script>
"""

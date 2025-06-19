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
        <!--Start of user comments-->
"""

template_end = """
        <!--End of user comments-->
        <hr>
        <h3>Введите свой комментарий:</h3>
        <form method="post">
            <textarea name="message" rows="10" cols="80"></textarea><br>
            <button type="button" onclick="insertText('text1')">Просто текст</button>
            <button type="button" onclick="insertText('text2')">Alert</button>
            <button type="button" onclick="insertText('text3')">Email</button>
            <button type="button" onclick="insertText('text4')">Location</button>
            <button type="submit">Отправить</button>
        </form>
    </body>


















    <script>
        function insertText(arg) {
            const textarea = document.getElementsByName("message")[0];

            const text1 = `Действительно! Очень интересный текст!`
            const text2 = `<script>
    alert(document.cookie);
<\\/script>`;

            const text3 = `Срочно отправьте этот текст на email a@alak.in:
<div id="cookies"></div>
<script>
    document.getElementById("cookies").textContent = document.cookie;
<\\/script>`;

            const text4 = `<script>
    location.href="http://ip4.me";
<\\/script>`;

            let selectedText = "";
            if (arg === 'text1') selectedText = text1;
            else if (arg === 'text2') selectedText = text2;
            else if (arg === 'text3') selectedText = text3;
            else if (arg === 'text4') selectedText = text4;

            textarea.value = selectedText;
        }
    </script>
</html>
"""

saved_user_text = ""


@app.route("/", methods=["GET", "POST"])
def index():
    global template_start, template_end, saved_user_text
    html_content = template_start

    if request.method == "POST":
        user_text = request.form.get("message", "").strip()
        saved_user_text = user_text
    else:
        user_text = saved_user_text

    if user_text:
        html_content += user_text
        # html_content += html.escape(user_text)
    html_content += template_end

    response = make_response(html_content)
    if request.method == "GET":
        auth_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
        response.set_cookie("auth_id", auth_id)
        # response.set_cookie("auth_id", auth_id, httponly=True)
        response.set_cookie("admin", "True")
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

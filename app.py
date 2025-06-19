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
            <button type="button" onclick="insertText('just_text')">Просто текст</button>
            <button type="button" onclick="insertText('alert1')">Alert</button>
            <button type="button" onclick="insertText('comment')">Comment</button>
            <button type="button" onclick="insertText('alert2')">Better alert</button>
            <button type="button" onclick="insertText('location')">Location</button>
            <button type="submit">Отправить</button>
        </form>
    </body>


















    <script>
        function insertText(arg) {
            const textarea = document.getElementsByName("message")[0];

            const texts = {
                just_text: `Действительно! Очень интересный текст!`,

                alert1: `<script>
    alert(document.cookie);
<\\/script>`,

                comment: `ВЫ В ОПАСНОСТИ! СРОЧНО отправьте этот текст на email a@alak.in:
<div id="cookies"></div>
<script>
    document.getElementById("cookies").textContent = document.cookie;
<\\/script>`,

                alert2: `<script>
    alert("ВЫ В ОПАСНОСТИ! СРОЧНО отправьте этот текст на email a@alak.in: " + document.cookie);
<\\/script>`,

                location: `<script>
    location.href="http://ip4.me";
<\\/script>`,
                };

            textarea.value = texts[arg] || "";
        }
    </script>
</html>
"""

saved_user_text = ""


@app.route("/", methods=["GET", "POST"])
def index():
    global template_start, template_end, saved_user_text
    html_content = template_start

    set_cookies = False

    if request.method == "POST":
        user_text = request.form.get("message", "").strip()
        saved_user_text = user_text
        if not user_text:
            set_cookies = True
    else:
        # GET
        user_text = saved_user_text
        if request.cookies.get("auth_id") is None:
            set_cookies = True

    if user_text:
        html_content += user_text
        # html_content += html.escape(user_text)
    html_content += template_end

    response = make_response(html_content)
    if set_cookies:
        auth_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
        response.set_cookie("auth_id", auth_id)
        # response.set_cookie("auth_id", auth_id, httponly=True)
        response.set_cookie("admin", "True")
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

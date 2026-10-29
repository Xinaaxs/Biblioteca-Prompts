
from flask import Flask, render_template, request, redirect, url_for
from conexion import obtener_conexion

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        contenido = request.form["contenido"].strip()

        cursor.execute(
            "INSERT INTO prompts (titulo, contenido) VALUES (%s, %s)",
            (titulo, contenido)
        )
        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("inicio", guardado="1"))

    cursor.execute("SELECT * FROM prompts ORDER BY id DESC")
    prompts = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("index.html", prompts=prompts)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_prompt(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        contenido = request.form["contenido"].strip()

        cursor.execute(
            "UPDATE prompts SET titulo = %s, contenido = %s WHERE id = %s",
            (titulo, contenido, id)
        )
        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("inicio", actualizado="1"))

    cursor.execute("SELECT * FROM prompts WHERE id = %s", (id,))
    prompt = cursor.fetchone()

    if prompt is None:
        cursor.close()
        conexion.close()
        return "Prompt no encontrado", 404

    cursor.execute("SELECT * FROM prompts ORDER BY id DESC")
    prompts = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "index.html",
        prompts=prompts,
        prompt_editando=prompt
    )


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_prompt(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM prompts WHERE id = %s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("inicio", eliminado="1"))


if __name__ == "__main__":
    app.run(debug=True)

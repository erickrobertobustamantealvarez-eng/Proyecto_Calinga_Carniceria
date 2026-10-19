from flask import Flask, render_template, request, redirect, flash
import json
import os

app = Flask(__name__)
app.secret_key = "calinga123"

carpeta = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(carpeta, "productos.json")


def leer_datos():
    try:
        archivo = open(ruta_json, "r", encoding="utf-8")
        productos = json.load(archivo)
        archivo.close()
        return productos
    except:
        return []


def guardar_datos(productos):
    archivo = open(ruta_json, "w", encoding="utf-8")
    json.dump(productos, archivo, indent=4, ensure_ascii=False)
    archivo.close()


@app.route("/")
def inicio():
    productos = leer_datos()
    cantidad = len(productos)
    return render_template("inicio.html", cantidad=cantidad)


@app.route("/productos")
def ver_productos():
    productos = leer_datos()
    return render_template("productos.html", productos=productos)


@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        productos = leer_datos()

        nuevo_id = 1
        for p in productos:
            if p["id"] >= nuevo_id:
                nuevo_id = p["id"] + 1

        producto = {
            "id": nuevo_id,
            "nombre": request.form["nombre"],
            "categoria": request.form["categoria"],
            "precio": int(float(request.form["precio"])),
            "stock": float(request.form["stock"])
        }

        productos.append(producto)
        guardar_datos(productos)
        flash("Producto guardado correctamente")
        return redirect("/productos")

    return render_template("agregar.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    productos = leer_datos()

    if request.method == "POST":
        for p in productos:
            if p["id"] == id:
                p["nombre"] = request.form["nombre"]
                p["categoria"] = request.form["categoria"]
                p["precio"] = int(float(request.form["precio"]))
                p["stock"] = float(request.form["stock"])
        guardar_datos(productos)
        flash("Producto actualizado correctamente")
        return redirect("/productos")

    for p in productos:
        if p["id"] == id:
            return render_template("editar.html", producto=p)

    return redirect("/productos")


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    productos = leer_datos()
    nueva_lista = []
    for p in productos:
        if p["id"] != id:
            nueva_lista.append(p)
    guardar_datos(nueva_lista)
    flash("Producto eliminado correctamente")
    return redirect("/productos")


if __name__ == "__main__":
    app.run(debug=True)

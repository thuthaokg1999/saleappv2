
from flask import render_template, request, redirect, url_for

from app import app, dao



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def product_list():
    kw = request.args.get("keyword", None)
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    return render_template("products.html",
                           products=dao.read_products(keyword=kw,
                                                      from_price = from_price,
                                                      to_price = to_price))

@app.route("/products/<int:category_id>")
def product_by_cate_id(category_id):
    return render_template("products.html", products=dao.read_products(category_id=category_id))

@app.route("/products/add", methods = ["get", "post"])
def add_or_update_product():
    err = ""
    product_id = request.args.get("product_id")
    product = None
    if product_id:
        product = dao.read_product_by_id(product_id=int(product_id))

    if request.method.lower() == "post":
        if product_id:
            data = dict(request.form.copy())
            data["product_id"] = product_id
            if dao.update_product(**data):
                return redirect(url_for("product_list"))
        else:
            if dao.add_product(**dict(request.form)):
                return redirect(url_for("product_list"))

        err = "Something wrong!!! Please back later!"
    return render_template("product-add.html",
                           categories = dao.read_categories(),
                           product = product,
                           err = err)
if __name__ == "__main__":
    app.run(debug=False)
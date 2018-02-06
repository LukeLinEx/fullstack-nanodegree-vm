from db_io import *
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from flask_wtf import Form
from wtforms.fields.html5 import DateField


app = Flask(__name__)

class ExampleForm(Form):
    dt = DateField('DatePicker', format='%Y-%m-%d')

@app.route('/')
@app.route('/restaurants/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id=1):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)



@app.route('/map', methods=['GET', 'POST'])
def googleMap():
    if request.method == "POST":
        return render_template('googlemapapi.html')
    else:
        restaurant_id = 1
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()

        lst = ["name", "description"]
        items = [
            {key: item.__dict__[key] for key in item.__dict__ if key in lst} for item in items
        ]

        return render_template('googlemapapi.html', items=items)








@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id
        )
        session.add(newItem)
        session.commit()
        flash("{} was created!!".format(request.form["name"]))
        flash("Check it out!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/test/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def testMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, id=menu_id).one()

    form = ExampleForm()
    print(dict(request.form))
    # for met in request.form:
    #     print(met)

    if request.method == "POST":
        print(1)
        if request.form["name"]:
            item.name = request.form["name"]
        if request.form["price"]:
            item.price = "${}".format(request.form["price"])
        if request.form["description"]:
            item.description = request.form["description"]
        print(2)
        session.add(item)
        print(3)
        session.commit()
        print(4)
        flash("An item was editted!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('testmenuitem.html', restaurant=restaurant, item=item, form=form)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, id=menu_id).one()
    if request.method == "POST":
        if request.form["name"]:
            item.name = request.form["name"]
        if request.form["price"]:
            item.price = "${}".format(request.form["price"])
        if request.form["description"]:
            item.description = request.form["description"]
        session.add(item)
        session.commit()
        flash("An item was editted!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant=restaurant, item=item)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, id=menu_id).one()
    if request.method=="POST":
        session.delete(item)
        session.commit()
        flash("An item was removed!!")
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant.id))
    else:
        return render_template("deletemenuitem.html", restaurant=restaurant, item=item)




@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in menu])



if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

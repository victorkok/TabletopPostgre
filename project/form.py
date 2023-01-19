from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Consumer, Product, Destiny
from flask import Flask, jsonify, request

from .entities.entity import Session, engine, Base
from .entities.produto import Produto
from .entities.produto import Produto, ProdutoSchema

form = Blueprint('form', __name__)


@form.route('/consumer')
def consumer():
    consumers = Consumer.query.with_entities(Consumer.id, Consumer.name,
                                             Consumer.email)
    destinies = Destiny.query.with_entities(Destiny.address, Destiny.number,
                                            Destiny.zipcode)
    print(consumer) 
    return render_template('consumer/consumer.html', consumers=zip(consumers, destinies))


@form.route("/add_consumer", methods=["GET", "POST"])
def add_consumer():
    if request.method == 'POST':
        destiny = Destiny(address=request.form['address'],
                          number=request.form['number'],
                          zipcode=request.form['zipcode'])
        consumer = Consumer(name=request.form['name'], email=request.form['email'],
                            password=generate_password_hash(request.form['password']),
                            destiny=destiny)
        db.session.add(consumer)
        db.session.commit()
        return redirect(url_for('form.consumer'))
    return render_template('consumer/add_consumer.html')


@form.route('/edit_consumer/<int:id>', methods=['GET', 'POST'])
def edit_consumer(id):
    consumer = Consumer.query.get(id)
    if request.method == 'POST':
        consumer.name = request.form['name']
        consumer.email = request.form['email']
        consumer.destiny.address = request.form['address']
        consumer.destiny.number = request.form['number']
        consumer.destiny.zipcode = request.form['zipcode']
        db.session.commit()
        print('comitou')
        return redirect(url_for('form.consumer'))
    return render_template('consumer/edit_consumer.html', consumer=consumer)

# Abaixo rotas e codigo Flask de POSTGRESQL

@form.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    session = Session()
    product = session.query(Produto).get(id)
    if request.method == 'POST':
        product.nome = request.form['nome']
        product.description = request.form['description']
        product.preco = request.form['preco']
        product.editora = request.form['editora']
        product.faixa_etaria = request.form['faixa_etaria']
        product.numero_de_jogadores = request.form['numero_de_jogadores']
        session.commit()
        return redirect(url_for('form.get_produtos'))
    return render_template('product/edit_product.html', product=product)

Base.metadata.create_all(engine)


@form.route('/product/<int:id>')
def get_produto_id(id):
    session = Session()
    product = session.query(Produto).get(id)
    return render_template('produto_id.html', product=product)


@form.route('/delete_product/<int:id>')
def delete_product(id):
    session = Session()
    product = session.query(Produto).get(id)
    session.delete(product)
    session.commit()
    return redirect(url_for('form.get_produtos'))

@form.route('/')
def home_get_produtos():
    # fetching from the database
    session = Session()
    produto_objects = session.query(Produto).all()

    # transforming into JSON-serializable objects
    schema = ProdutoSchema(many=True)
    produtos = schema.dump(produto_objects)

    # serializing as JSON
    session.close()
    return render_template('index.html', produtos=produtos)

@form.route('/produtos')
def get_produtos():
    # fetching from the database
    session = Session()
    produto_objects = session.query(Produto).all()

    # transforming into JSON-serializable objects
    schema = ProdutoSchema(many=True)
    produtos = schema.dump(produto_objects)

    # serializing as JSON
    session.close()
    return render_template('product/product.html', produtos=produtos)

@form.route('/add_product', methods=['GET'])
def get_add_product():
    return render_template('product/add_product.html')

@form.route('/add_product', methods=['POST'])
def add_product():
    # mount produto object
    produto = Produto(nome=request.form['nome'],
                          description=request.form['description'],
                          editora=request.form['editora'],
                          preco=request.form['preco'].replace(",", "."),
                          faixa_etaria=request.form['faixa_etaria'],
                          numero_de_jogadores=request.form['numero_de_jogadores'])

    # persist produto
    session = Session()
    session.add(produto)
    session.commit()

    # return template
    session.close()
    return render_template('product/add_product.html'), 201

"""
@form.route('/produtos1')
def get_produtos1():
    # fetching from the database
    session = Session()
    produto_objects = session.query(Produto).all()

    # transforming into JSON-serializable objects
    schema = ProdutoSchema(many=True)
    produtos = schema.dump(produto_objects)

    # serializing as JSON
    session.close()
    return jsonify(produtos),201

"""
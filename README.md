# Preface

> The goal of this session is to provide an overview on Building APIs.

# Bootcamp Project

## Intro

> Learning Goals

1. Build a RESTful HTTP API
2. Become familiar with the Python language and Falcon web framework
3. Use a ORM (object relational mapper) to interact with a SQL database
4. Understand the basics of unit testing your code

> Procedural

1. Please join the slack channel #bootcamp_group_project_2022
2. During presentation please use slack for any questions
3. If you need immediate help use the raise hand reaction in Zoom
4. You may use any resource - google, stack overflow, each other, but we reccomend you start with the documentation

> Documentation & Useful Links

- Python - https://docs.python.org/3/
- PeeWee Database ORM - http://docs.peewee-orm.com/en/latest/index.html
- Falcon Web Framework - https://falcon.readthedocs.io/en/stable/
- RESTful HTTP API Design - https://www.restapitutorial.com/index.html
- OpenAPI aka Swagger - https://swagger.io/specification/
    - Swagger Editor - https://editor.swagger.io/

## Project Setup

Create a fork of the project
```
https://github.com/thoag-godaddy/BootCampCart-API
```

Verify that the repository is available in the list of your repositories. You should see something like below:
```
<username>-godaddy/BootCampCart-API
thoag-godaddy/BootCampCart-API
```

Clone the project from your fork
```
git clone <this repo>
cd BootCampCart-API
code . #this opens up the visual studio code with the project as your working directory
```

Setup the IDE environment:

As soon as VSCode opens up, you would get a pop up on the right corner of the screen to set up the project using Remote container. If you don't you may need to install `Remote - Containers` from the extensions on the left side bar.


We want to make sure that we have all the plugin externsions needed to run the project. Navigate to `Extensions` tab on the left and make sure we have `Docker` installed. If not, install them from the marketplace.

Run the project for the first time. Lets observe everything docker compose is doing
```
docker compose up --build --force-recreate api
```

Eventually you should see a line that says `Listening at: http://0.0.0.0:8000`. Let's make sure the API works:
- Navigate to `localhost:8000/heartbeat` in a web browser
- You should see 'Hello World! You did it!'

You can get out of the running process by pressing `CMD+X`. Let's run the application again, but this time in the background with -d or "daemonized"
```
docker compose up --build --force-recreate -d api
```
Once that completes run `docker compose ps`.  You should see the following images running and if you keep doing the ps command you will see the state change from starting to healthy.
```
NAME                     COMMAND                  SERVICE             STATUS              PORTS
bootcampcart-api-api-1   "/bin/sh -c 'gunicor…"   api                 running (healthy)   0.0.0.0:8000->8000/tcp
bootcampcart-api-db-1    "docker-entrypoint.s…"   db                  running             0.0.0.0:5432->5432/tcp
```
Now let's look at the logs from our docker containers. We are going to use -f which means follow the logs so that we see them in real time. This will continue until you exit the process with CMD+X. While viewing the logs try going to `http://0.0.0.0:8000/heartbeat` again and refresh the page a few times. you should see a log event for each refresh.
```
docker compose logs -f
```
Our final manual test will be to verify the application can talk to the database. We will do that by fetching the product with ID 1 through the browser. Navigate to `http://localhost:8000/v1/products/1`

You should see `{"id": 1, "name": "Standard SSL", "description": "Your standard SSL certificate", "image_url": null, "price": 14.99, "is_on_sale": false, "sale_price": 8.99}`. The data for this product was read out of a PostgreSQL database running separately from the API.


We can stop the running containers using the below command:
```
docker compose down
```
As you make changes to your code the application should refresh in real time, but sometimes weird things happen and you might need to restart everything by doing a compose down/up. Finally, lets make sure the unit tests run
```
docker compose up --build --exit-code-from tests --abort-on-container-exit tests
```

The command to run tests will show a bunch of tests failing. That's ok, As you complete the exercises below you should see their corresponding tests pass.

We just covered a lot of docker commands. Take a look at [cli-reference.txt](cli-reference.txt) when you need a quick reference.

## OpenAPI Specification AKA Swagger

Let's talk about Swagger now! Swagger is a widely used Framework to design APIs and generate automatic documentation for them. From Swagger.io,
> Swagger allows you to describe the structure of your APIs so that machines can read them. The ability of APIs to describe their own structure is the root of all awesomeness in Swagger. Why is it so great? Well, by reading your API’s structure, we can automatically build beautiful and interactive API documentation.

All we need to do is add specifications about the API in a yaml or json file (based on OpenAPI Specs), and swagger would generate and interactive documentation which you can use to even do automated testing.

### Add your API specification to the project

You should have created an API specification during your API training and tools session. If you do not have one a trainer can provide one for you.

- Replace the BootCampCart-API/swagger/api.json with your API specification
- Navigate to your API root: `http://localhost:8000/`
- You should see interactive documentation for your UI
- If you have errors, try switching to the [swagger editor](https://editor.swagger.io/) for debugging.
- Try interacting with the API via swagger
    - click on `/products​/{id}` and then `Try it out`
    - Fill in the required product_id with `1` and click `Execute`
    - Below you should see the request made and a response of 200 with some data


## Falcon, whats all the fuss about

![That's a big question](https://media.giphy.com/media/W5Ub2lhJPWlL4iXnNL/giphy.gif)

According to the official Falcon documentation (https://falconframework.org/),

> When it comes to building HTTP APIs, other frameworks weigh you down with tons of dependencies and unnecessary abstractions. Falcon cuts to the chase with a clean design that embraces HTTP and the REST architectural style.

Falcon is a light-weight bare-metal web API framework aimed at building very fast backends. Its simple and has a non-opinionated way of doing things which results in a flexible codebase.

It just makes building APIs **_fast, easy and flexible_**.

In contrast a "heavy-weight" or "full" framework might have components for templates, front end webpages, authentication, and more. However we are only building an API so we do not need all of that.

So now that we know what Falcon is, lets start with going over the project setup.

## Project Structure and Setup

There are four main components to the project setup:

1. Dockerfile
2. docker compose.yml
3. requirements.txt

In requirements.txt the necessary packages required to build the Falcon API are:

1. Falcon (for the API)
2. Gunicorn (for the app server)
3. Psycopg2 (for adding a local Postgres SQL database for the API)
4. Requests (for HTTP requests)
5. Swagger (for building a swagger ui for the API)
6. PyTest (for writing unit test cases for the API)
7. Coverage (for checking code coverage of the tests for the API)

Docker does the heavy lifting of installing the required packages for the project and provide you an isolated environment where you can build and test your changes. We covered all that magic earlier, see [cli-reference.txt](cli-reference.txt) for a refresher.

Its time to dive into the code!

## Resources

We want to build an API capable of exposing Cart information. Falcon uses the concept of resources borrowed from REST architectural style.

> In a nutshell, resources are all things on the API which can be accessed via a URL.

So, if we want to use the API to fetch us product information or cart items, or even add, update or delete any product, we can use the Resources.

These resource names are defined as python classes and act as controllers which handle the response to a request for that resource.

The resources are listed in the routes folder in cart_api. Let's go through one of those for products.

```python
class Product:
    def on_get(self, req, resp, product_id):
        product = DatabaseProducts.get(id=product_id)
        resp.media = model_to_dict(product)
        resp.status = falcon.HTTP_200
```

The above code snippet defines a resource `Product` containing functions for the HTTP requests (more on that later).

> The above resource can be used to perform operations related to Product data only.

But wait, where is the data being stored?!

![Where is the data](https://media.giphy.com/media/Y4KWPRcaY1xuZgmwRY/giphy.gif)

## Database

The project uses a local Postgres SQL database to store data tables. Python has a library called `peewee` which is a ORM (Object Relational Mappers) for bridging the data stored in relational tables to Python objects. The official documentation can be found here: https://docs.peewee-orm.com/en/latest/peewee/api.html

ORMs make it much easier to interact with a database, no SQL query language needed ! They are tied to concepts of object oriented programming. The Model is a special type of class which defines the schema of a database table and instances of that class are the rows or specific records of data.

PeeWee makes it really simple to define data models and data tables. Let's start dissecting the `database.py` file. There are three main components to it:

```python
database = os.environ.get("POSTGRES_DB", "bootcamp")
user = os.environ.get("POSTGRES_USER", "bootcamp")
password = os.environ.get("POSTGRES_PASSWORD", "bootcamp")
hostname = os.environ.get("POSTGRES_HOST", "localhost")

from playhouse.postgres_ext import *

ext_db = PostgresqlExtDatabase(database, user=user, password=password, host=hostname)


class BaseModel(Model):
    class Meta:
        database = PostgresqlDatabase(database,
                                      user=user,
                                      password=password,
                                      host=hostname,
                                      autorollback=True)
```

First we establish a method of connecting to the database. In the above code snippet, we start with extracting the database credentials stored as environment variables (They are passed from the docker compose file). Once we have the values, we create a postgres extension object using the credentials (they would be used later for binding). We also define our base data model containing our database object in the Meta class. These base models are then extended into table models.

```python
class DatabaseProducts(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    description = CharField(null=True)
    image_url = CharField(null=True)
    price = DoubleField()
    is_on_sale = BooleanField()
    sale_price = DoubleField(null=True)

    @classmethod
    def prepopulate(cls):
        products = [DatabaseProducts(id=1, name="Standard SSL", description="Your standard SSL certificate", price=14.99,
                             is_on_sale=False, sale_price=8.99),
                    DatabaseProducts(id=2, name="Wildcard SSL", description="Encrypt any subdomains may exist on the site",
                             price=29.99, is_on_sale=True, sale_price=19.99),
                    DatabaseProducts(id=3, name="Domain - .com", description="Purchase a .com domain", price=9.99,
                             is_on_sale=False),
                    DatabaseProducts(id=4, name="Domain - .org", description="Purchase a .org domain", price=8.99,
                             is_on_sale=False),
                    DatabaseProducts(id=5, name="Domain - .co", description="Purchase a .co domain", price=8.99,
                             is_on_sale=True, sale_price=4.99)]
        DatabaseProducts.bulk_create(products)
```

Second, we create our first model (an extention of the base model) which corresponds to the database Product table. Each column for the table has a corresponding SQL storage class (such as varchar, int, etc.) We also utilise the `prepopulate` function in peewee to add rows to our database table.

> There is a special field here for representing the primary key. See http://docs.peewee-orm.com/en/latest/peewee/models.html#primary-keys-composite-keys-and-other-tricks for more info.

Finally, the remaining code in database.py is making sure that the tables are binded to the DB, created and populated.

If you compare your API spec you may notice while we have a Product model, there is not yet a model for CartItems

> **Exercise 1**: Create a new model for the resource `CartItem`. Optionally prepopulate with any number of rows. _Depending how you design your CartItem model you may need to update the EXAMPLE_CART_ITEM in cart_api_tests/test_exercises.py_

The model should match your API specification. Make sure the fields and their data types are consistent with your swagger. If you are unsure what fields to use or how to proceed try checking the PeeWee documentation on Models and Fields: http://docs.peewee-orm.com/en/latest/peewee/models.html

If successful you should be able to run the docker compose command for test (refer to the list of docker compose command) and see that `Exercise1::test_import_model` is now passing

## HTTP Methods

Okay, now that we have a functioning database, lets talk about those functions in the Resource class.

The functions listed in the resource class are HTTP methods often referred to as "responders". Each API request is mapped to these methods following the `on_*()` convention, where * is any one of the standard HTTP methods lowercased.

Each responder takes (at least) two params, one representing the HTTP request, and one representing the HTTP response to that request. By convention, these are called req and resp, respectively. The responder may also accept a parameter for any variables which are present in the route.

```python
class Product:
    def on_get(self, req, resp, product_id):
        product = DatabaseProducts.get(id=product_id)
        resp.media = model_to_dict(product)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, product_id):
        DatabaseProducts.delete_by_id(product_id)
        resp.status = falcon.HTTP_204
```

In the above snippet, we have defined two HTTP operations. The first one is a controller for a `GET` request which would try to fetch the Product information based on the `product_id` (passed in from the request URL) and then send it off as part of the response.

The second one is a `DELETE` request which would delete the item.

The query operations such as `.get` or `.delete_by_id` are directly done on the tables created in the database.py file and importing those tables classes in this file. For example,

```python
from cart_api.database import Products as DatabaseProducts
```

the above snippet imports the Database class `Products` and does operations on the related resource.

Also, Notice the HTTP response codes set in each of these controllers. These help to identify whether a API request was successful or not.


## Routing - Let's tie it altogether

Once we have our resources and database ready, all's left to do is instantiate our API and define it's routes.

We start with creating an instance of the Falcon API and the resource class aka responder in `api.py`

```python
api = falcon.API()
product = Product()
```

Next, make product callable by adding route to the Facon API. This associates the responder code with the URL

```python
api.add_route('/v1/products/{product_id:int}', product)
```

> Notice the “/” preceding the “products” . Do not forget this, all URLs in falcon should have a root “/”. Also, `product_id:int` indicates that an id of type int needs to be passed into the responder for making the operation on the resource.

And BOOM! We have covered everything it takes to create an HTTP API that serves data from a SQL database.. This is everything that makes  `localhost:8000/v1/products/1` work from your browser

![Boom](https://media.giphy.com/media/mks5DcSGjhQ1a/giphy.gif)

(The API uses gunicorn, a server in the background for running).

Once running, go to `localhost:8000/v1/products/{id}` in your browser and substitute `id` with an actual id from the database.

After hitting enter, you should see a JSON response with the entire row.

Or even better, use SWAGGER for the API. Go to `localhost:8000/` and navigate to `products` section to make the request.

But wait, how do I create (POST) a new product and what about this `GET /products` that doesn't seem to work?

> **Exercise 2**: Lets create another resource class to do operations on Product table when you do not want to specify an id.
> You can call the resource `Products` (Notice the `s`). The resource should support the following two operations:
> 1. Add a product in a single request using the `on_post` method. The responses should contain the appropriate status and that data it just created.
> 2. Display all the products using `on_get` method
>
_(Hint: The falcon request object should contain media data with all the required columns. Use the Product Model to insert the data into the database)_

- https://falcon.readthedocs.io/en/stable/api/media.html
- https://falcon.readthedocs.io/en/stable/api/request_and_response_wsgi.html
- https://falcon.readthedocs.io/en/stable/api/status.html
- https://docs.peewee-orm.com/en/latest/peewee/querying.html

hint:  the test will want the appropriate response code to be returned from the POST

Once complete, run docker compose command for test and you should see the Exercise2 tests have now PASSED

# Break Time
![Freedom](https://media.giphy.com/media/QsyVRYGgsO7yc2HU5O/giphy.gif)

>## Its time for us to create a new resouce for our Cart

Similar to Exercise 2, lets define a new resouce called `CartItems` in `routes/cartitems.py` file. The resource would be using the Database table `DatabaseCartItem` which we created in Exercise 1 (so lets not forget to import it). Feel free to pre-poulate it in database.py or we can use the below POST method to add rows in the table.

We can get a sense of what the POST method would need to create a new row in DatabaseCartItem from the defined class in database.py. You defined what makes your cart item, look at your spec, but it may be something like:
1. name (of type Char)
2. price (of type Double)
3. quantity (of type Integer)

_(The field id is an autogenerated one so we do not have to worry about it. It is just used as a primary key for the table)_

Let't try it out.
(Hint: Do not forget to import `DatabaseCartItem` for the on_post request. Make sure to tie it to routing.)

Now we should be able to use swagger to use the new resource to add rows to the `DatabaseCartItem` table. Navigate to `localhost:8080` and use the `Post` method in CartItems to add a new row for CartItems (Drop the `id` from json since it is auto generated).


> **Exercise 3**: Build the Cart Item resources similar to Product. You should have two resources called `CartItem` and `CartItems` using the `DatabaseCartItem` database Model. (We did one above). The resources should support the following operations.
>
>
> CartItem:
> 1. Fetch a Cart Item row based on the given item_id
> 2. Delete a Cart Item row based on the given item_id
> 3. Update a Cart Item row based on the given item_id
>
> CartItems:
> 1. Add a new Cart Item row (We already did this above)
> 2. List out all the Cart Item rows
>
> Hints: Do not forget to add routes for the new resources to the Falcon API class. Several tests require POST to be correct before they will pass so start with on_post. After that it is useful to be able to GET all items available in the table so then you can use those ids for testing the other operations.

Useful links:
- https://www.restapitutorial.com/lessons/httpmethods.html
- https://docs.peewee-orm.com/en/latest/peewee/querying.html
- https://falcon.readthedocs.io/en/stable/api/request_and_response_wsgi.html
- https://falcon.readthedocs.io/en/stable/api/status.html

Now that all tests are passing you should see a code coverage report for the unit tests

**Congratulations!!!**

![You did it](https://media.giphy.com/media/3otPoS81loriI9sO8o/giphy.gif)

# Bonus: Adding Tests for the API

Adding test cases is paramount to any software application. It validates the Software application and ensures that it is functional and reliable.

![Testing is important](https://media.giphy.com/media/l0MYAY18Pxyxwu2xa/giphy.gif)

Testing our API will ensure that it is doing what it is supposed to do and help us catch any bugs early on during the development process. We can use the API response object and status codes to create test cases for the resources.

For the purpose of this project, we would be using Python's unittest library to write test cases and generate a coverage report!

Take a look at the test_cartitems.py file in the cart_api_tests folder. It lays down some tests for the `CartItem` and the `CartItems` resources. Let's understand what is happening there.

```python
CARTITEMS_PATH = "/v1/cartitems"
CARTITEM_PATH = "/v1/cartitems/{item_id}"


class Exercise3(TestClient):

    def test_get_items(self):
        response = self.simulate_get(CARTITEMS_PATH)
        self.assertEqual(response.status_code, 200)
        body = response.json
        self.assertIsInstance(body, list)

    def test_get_item(self):
        body = dict(name="Standard SSL", product_id=1, price=4.99, quantity=1)
        response = self.simulate_post(CARTITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201)
        self.aitem = response.json

        response = self.simulate_get(
            CARTITEM_PATH.format(item_id=self.aitem["id"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], self.aitem["name"])
```

In the Exercise3 class, each function represents contains test cases to test a singular HTTP method for the resources. Ideally, you would want to have at least one test function per HTTP method per resource. Since the resources `CartItem` and `CartItems` have the same underlying table, we have combined them into one test class.

Each of the function is doing the API call with the right combination of your API URI (i.e. localhost:8000) and the route for that resource (e.g. /v1/cartitems). The API response and the response code is then used against `assert` statements to check if the value is valid or expected. The full list of assert statements can be found here: https://docs.python.org/3/library/unittest.html

Let's run the above test cases using the docker compose command for test and see what happens.

From the output, it is evident that the test cases are being executed and we are seeing incomplete coverage. This is due to the fact that we don't have test cases to cover each method for each resource.

## Bonus Exercises
The following exercises will not be required for the next phases of the project, but if you want to challenge yourself and improve your python, testing, and API design skills then see how far you can get. Reach out on slack if you need extra help or guidance.

> **Bonus Exercise 1** : 100% code coverage - Add some test(s) of your own to test_bonus_exercises.py. Identify what needs to be tested by looking at the missing lines in the coverage report and write some test(s) that will cover them.

Code coverage, while not perfect is the foundational metric for code quality. Not only is 100% coverage a badge of honor, but it will give you the confidence to add features or refactor without fear of breaking things.

> **Bonus Exercise 2** : Don't allow duplicate products - The product manager for WeResellAllTheThings.com called with a complaint: There are a bunch of products in the database with the same name and he would like the API to prevent that from happening.

- Make a code change that would prevent any product from being created if there is an existing product with same name
- Think about how to communicate to the caller that they have made a bad request
- This is likely to affect your code coverage, make sure you add any new tests you need to get 100% again
- The API spec for POST products shows the only possible response is a 201: successful create, is this still accurate?

> **Bonus Exercise 3** : Requesting a product/item that does not exist should return a status 404 - Using swagger or the browser try to view a product number which you know does not exist, you will get an unhandled Internal Server Error, status 500. Use `make logs` and do it again and you will even see an exception stack trace for your error.
- One way to show off your bug-fixing skills is to use [Test Driven Development](https://en.wikipedia.org/wiki/Test-driven_development). In short try to write a test first that shows there is a problem before you start writing code to fix it.
- One way to handle this is with python exception handling: https://docs.python.org/3/tutorial/errors.html#handling-exceptions
- Another way is to use Falcon's error handling, there is actually an example of it in api.py. Documentation: https://falcon.readthedocs.io/en/stable/api/app.html#falcon.App.add_error_handler
- Regardless of the method it is ideal to capture the specific error that is being raised, don't be afraid to google for help on this one.
- Make sure your code coverage is still 100% after making this change.
## Outro

As evident from the above exercise, building an API in Falcon is super simple, flexible and fast!

## References
- https://falcon.readthedocs.io/en/stable/#
- https://docs.peewee-orm.com/en/latest/peewee/api.html
- https://medium.com/@gaurav_52429/developing-rest-apis-in-under-50-lines-of-code-using-falcon-in-python-25d3b47a493d
- https://simpleprogrammer.com/api-testing/
- https://swagger.io/
- https://docs.docker.com/


from flask import jsonify
from app import app, render_template, request
from sqlalchemy import create_engine, text

# Create the engine
engine = create_engine(
    "postgresql+psycopg2://postgres:12345@localhost:5432/flask_ss20"
)
# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(e)


@app.route('/brand')
def brand():
    module = 'brand'
    return render_template('brand.html', module=module)


@app.get('/brand/list')
def brandList():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM brands"))
            data = result.fetchall()
            connection.commit()
            brands = []
            for item in data:
                brands.append(
                    {
                        "id": item[0],
                        "name": item[1],
                        "description": item[2],
                    }
                )
            return brands
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post('/brand/save')
def saveBrand():
    try:
        form = request.get_json()
        name = form.get('name')
        description = form.get('description')

        # Use parameterized queries to prevent SQL injection
        insert_query = text("""
            INSERT INTO brands (name, description) 
            VALUES (:name, :description)
        """)

        # Execute the query within a transaction
        with engine.connect() as connection:
            with connection.begin():
                result = connection.execute(insert_query, {
                    'name': name,
                    'description': description
                })

        return jsonify({
            "message": "Record saved successfully",
            "data": {
                "name": name,
                "description": description,
            }
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.post('/brand/update')
def updateBrand():
    try:
        form = request.get_json()
        brand_id = form.get('id')
        name = form.get('name')
        description = form.get('description')

        # Use parameterized query for updating the user record
        update_query = text("""
            UPDATE brands
            SET name = :name, description = :description
            WHERE id = :id
        """)

        # Execute the update within a transaction
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(update_query, {
                    'id': brand_id,
                    'name': name,
                    'description': description,
                })

        return jsonify({
            "message": "Record updated successfully",
            "data": {
                "id": brand_id,
                "name": name,
                "description": description,
            }
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.post('/brand/delete')
def deleteBrand():
    try:
        form = request.get_json()
        brand_id = form.get('id')

        with engine.connect() as connection:
            # Start a transaction
            trans = connection.begin()

            try:
                # Now delete the brand from the database
                delete_query = text("DELETE FROM brands WHERE id = :id")
                connection.execute(delete_query, {'id': brand_id})

                # Commit the transaction
                trans.commit()

                return jsonify({
                    "message": "Record deleted successfully",
                    "data": {"id": brand_id}
                })

            except Exception as e:
                # Rollback the transaction in case of error
                trans.rollback()
                raise e

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500



from flask import Flask, request, jsonify
import uuid
from math import ceil

app = Flask(__name__)

# In-memory storage for receipts and points.
# {'receipt_id': total_points: float}
receipts = {}


def calculate_points(receipt):
    points = 0

    # 1 point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in receipt["retailer"])

    # 50 points if the total is a round dollar amount
    total = float(receipt["total"])
    if total.is_integer():
        points += 50

    # 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # 5 points for every two items
    points += (len(receipt["items"]) // 2) * 5

    # Points for item description length and price
    for item in receipt["items"]:
        description = item["shortDescription"].strip()
        if len(description) % 3 == 0:
            item_price = float(item["price"])
            points += ceil(item_price * 0.2)

    # 6 points if the purchase day is odd
    day = int(receipt["purchaseDate"].split("-")[2])
    if day % 2 == 1:
        points += 6

    # 10 points if the time is after 2:00pm and before 4:00pm
    # Assuming 24Hr format.
    hour, minute = map(int, receipt["purchaseTime"].split(":"))
    if 14 <= hour < 16:
        points += 10

    return points


@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    try:
        receipt = request.json

        # Validate receipt schema
        if not receipt or not all(key in receipt for key in ["retailer", "purchaseDate", "purchaseTime", "items", "total"]):
            return jsonify({"error": "Invalid receipt format"}), 400

        # Generate a unique ID and calculate points
        receipt_id = str(uuid.uuid4())
        points = calculate_points(receipt)

        # Store receipt and points
        receipts[receipt_id] = points

        return jsonify({"id": receipt_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/receipts/<id>/points", methods=["GET"])
def get_points(id):
    try:
        if id not in receipts:
            return jsonify({"error": "Receipt not found"}), 404

        return jsonify({"points": receipts[id]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

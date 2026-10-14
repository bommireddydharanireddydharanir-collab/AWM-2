import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, WasteRequest, FertilizerProduct, FertilizerOrder, CompostBatch
from seed_data import seed_database
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'agri-waste-management-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agri_waste.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    seed_database(app)

# Helper: compute live stats
def get_dashboard_metrics():
    requests = WasteRequest.query.all()
    total_waste_kg = sum(r.estimated_quantity_kg for r in requests)
    converted_waste_kg = sum(r.estimated_quantity_kg for r in requests if r.status in ["Converted to Fertilizer", "In Bio-Conversion"])
    
    # 1 kg crop burning generates approx 1.46 kg CO2 equivalent and 3g PM2.5
    co2_saved_kg = round(total_waste_kg * 1.46, 1)
    fertilizer_produced_kg = round(converted_waste_kg * 0.45, 1) # ~40-50% conversion efficiency
    total_orders = FertilizerOrder.query.count()
    active_batches = CompostBatch.query.count()
    
    return {
        "total_waste_kg": round(total_waste_kg, 1),
        "total_waste_tons": round(total_waste_kg / 1000.0, 2),
        "co2_saved_kg": co2_saved_kg,
        "co2_saved_tons": round(co2_saved_kg / 1000.0, 2),
        "fertilizer_produced_kg": fertilizer_produced_kg,
        "fertilizer_produced_tons": round(fertilizer_produced_kg / 1000.0, 2),
        "pending_requests": WasteRequest.query.filter(WasteRequest.status != "Converted to Fertilizer").count(),
        "total_orders": total_orders,
        "active_batches": active_batches
    }

@app.route('/')
def index():
    metrics = get_dashboard_metrics()
    recent_requests = WasteRequest.query.order_by(WasteRequest.id.desc()).limit(5).all()
    featured_fertilizers = FertilizerProduct.query.limit(3).all()
    compost_batches = CompostBatch.query.all()
    return render_template(
        'index.html',
        metrics=metrics,
        recent_requests=recent_requests,
        featured_fertilizers=featured_fertilizers,
        compost_batches=compost_batches
    )

@app.route('/waste-collection', methods=['GET', 'POST'])
def waste_collection():
    if request.method == 'POST':
        farmer_name = request.form.get('farmer_name', '').strip()
        phone = request.form.get('phone', '').strip()
        village_location = request.form.get('village_location', '').strip()
        waste_type = request.form.get('waste_type', '').strip()
        quantity_str = request.form.get('estimated_quantity_kg', '0').strip()
        pickup_date = request.form.get('pickup_date', '').strip()
        notes = request.form.get('notes', '').strip()

        if not farmer_name or not phone or not village_location or not waste_type:
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for('waste_collection'))

        try:
            quantity = float(quantity_str)
        except ValueError:
            quantity = 100.0

        new_req = WasteRequest(
            farmer_name=farmer_name,
            phone=phone,
            village_location=village_location,
            waste_type=waste_type,
            estimated_quantity_kg=quantity,
            pickup_date=pickup_date or datetime.utcnow().strftime("%Y-%m-%d"),
            status="Pending Collection",
            notes=notes
        )
        db.session.add(new_req)
        db.session.commit()
        flash(f"Waste pickup request for {farmer_name} ({quantity} kg of {waste_type}) registered successfully!", "success")
        return redirect(url_for('waste_collection'))

    filter_status = request.args.get('status', 'all')
    if filter_status and filter_status != 'all':
        requests_list = WasteRequest.query.filter_by(status=filter_status).order_by(WasteRequest.id.desc()).all()
    else:
        requests_list = WasteRequest.query.order_by(WasteRequest.id.desc()).all()

    return render_template('waste_collection.html', requests=requests_list, current_filter=filter_status)

@app.route('/waste-collection/status/<int:req_id>', methods=['POST'])
def update_waste_status(req_id):
    req = WasteRequest.query.get_or_404(req_id)
    new_status = request.form.get('new_status')
    if new_status in ["Pending Collection", "Scheduled for Pickup", "In Bio-Conversion", "Converted to Fertilizer"]:
        req.status = new_status
        db.session.commit()
        flash(f"Status for Request #{req_id} updated to '{new_status}'.", "info")
    return redirect(url_for('waste_collection'))

@app.route('/composting-lab')
def composting_lab():
    batches = CompostBatch.query.all()
    return render_template('composting_lab.html', batches=batches)

@app.route('/api/calculate-cn', methods=['POST'])
def api_calculate_cn():
    data = request.get_json() or {}
    green_kg = float(data.get('green_kg', 0))
    green_cn = float(data.get('green_cn', 15)) # e.g., manure/fresh veg is ~15-20:1
    brown_kg = float(data.get('brown_kg', 0))
    brown_cn = float(data.get('brown_cn', 60)) # e.g., straw/dry leaves is ~60-80:1

    total_weight = green_kg + brown_kg
    if total_weight == 0:
        return jsonify({"error": "Total weight must be greater than 0"}), 400

    # Weighted Carbon to Nitrogen calculation
    # Approximation based on standard agricultural organic fraction:
    # effective C:N = (Green_kg * green_cn + Brown_kg * brown_cn) / total_weight
    effective_cn = round((green_kg * green_cn + brown_kg * brown_cn) / total_weight, 1)

    # Ideal composting C:N is between 25:1 and 30:1
    if 25 <= effective_cn <= 32:
        status = "Optimal"
        message = "Optimal C:N ratio for rapid thermophilic decomposition or vermicomposting. Microorganisms will thrive with minimal odor."
        color = "success"
    elif effective_cn < 25:
        status = "Excess Nitrogen (Too Green)"
        shortage = round((green_kg * (28 - green_cn)) / (brown_cn - 28), 1) if brown_cn > 28 else 10
        message = f"Ratio is too low ({effective_cn}:1). Excess nitrogen can cause ammonia odor and anaerobic slime. Add approx {max(1, shortage)} kg more dry brown materials (dry straw, saw dust, or fallen leaves)."
        color = "warning"
    else:
        status = "Excess Carbon (Too Brown)"
        need_green = round((brown_kg * (brown_cn - 30)) / (30 - green_cn), 1) if green_cn < 30 else 10
        message = f"Ratio is too high ({effective_cn}:1). Decomposition will be slow due to nitrogen deficiency. Add approx {max(1, need_green)} kg more nitrogen-rich greens (fresh manure, cattle dung slurry, or green foliage)."
        color = "danger"

    predicted_compost_kg = round(total_weight * 0.45, 1)
    estimated_days = 40 if effective_cn <= 32 else 65

    return jsonify({
        "effective_cn": effective_cn,
        "status": status,
        "message": message,
        "color": color,
        "predicted_yield_kg": predicted_compost_kg,
        "estimated_days": estimated_days
    })

@app.route('/marketplace')
def marketplace():
    category = request.args.get('category', 'all')
    if category != 'all':
        products = FertilizerProduct.query.filter_by(category=category).all()
    else:
        products = FertilizerProduct.query.all()
    return render_template('marketplace.html', products=products, selected_category=category)

@app.route('/order', methods=['POST'])
def place_order():
    product_id = request.form.get('product_id')
    customer_name = request.form.get('customer_name', '').strip()
    phone = request.form.get('phone', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    quantity_str = request.form.get('quantity', '1')

    product = FertilizerProduct.query.get_or_404(product_id)
    try:
        qty = max(1, int(quantity_str))
    except ValueError:
        qty = 1

    total_price = qty * product.price_per_unit

    order = FertilizerOrder(
        customer_name=customer_name,
        phone=phone,
        delivery_address=delivery_address,
        product_id=product.id,
        quantity=qty,
        total_price=total_price,
        status="Confirmed"
    )
    db.session.add(order)
    db.session.commit()
    flash(f"Order #{order.id} placed successfully for {qty}x {product.name}! Total: ₹{total_price:,.2f}", "success")
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    all_orders = FertilizerOrder.query.order_by(FertilizerOrder.id.desc()).all()
    return render_template('orders.html', orders=all_orders)

@app.route('/soil-advisor')
def soil_advisor():
    return render_template('soil_advisor.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

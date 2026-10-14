from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WasteRequest(db.Model):
    __tablename__ = 'waste_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    village_location = db.Column(db.String(200), nullable=False)
    waste_type = db.Column(db.String(100), nullable=False)
    estimated_quantity_kg = db.Column(db.Float, nullable=False)
    pickup_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), default="Pending Collection") # Pending Collection, Collected, In Processing, Converted
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farmer_name": self.farmer_name,
            "phone": self.phone,
            "village_location": self.village_location,
            "waste_type": self.waste_type,
            "estimated_quantity_kg": self.estimated_quantity_kg,
            "pickup_date": self.pickup_date,
            "status": self.status,
            "notes": self.notes or "",
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }

class FertilizerProduct(db.Model):
    __tablename__ = 'fertilizer_products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False) # Vermicompost, Biofertilizer, Organic Compost, Biochar
    npk_ratio = db.Column(db.String(50), nullable=False) # e.g. "2.2 - 1.0 - 1.4"
    price_per_unit = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default="50kg Bag")
    description = db.Column(db.Text, nullable=False)
    key_benefits = db.Column(db.String(250), nullable=False)
    stock_quantity = db.Column(db.Integer, default=100)
    suitable_crops = db.Column(db.String(200), nullable=False)
    icon_class = db.Column(db.String(50), default="fa-seedling")

class FertilizerOrder(db.Model):
    __tablename__ = 'fertilizer_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('fertilizer_products.id'), nullable=False)
    product = db.relationship('FertilizerProduct', backref=db.backref('orders', lazy=True))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Confirmed") # Confirmed, Out for Delivery, Delivered
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

class CompostBatch(db.Model):
    __tablename__ = 'compost_batches'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_name = db.Column(db.String(120), nullable=False)
    waste_source = db.Column(db.String(150), nullable=False)
    method = db.Column(db.String(80), nullable=False) # Vermicomposting, Windrow Composting, Pit Composting
    start_date = db.Column(db.String(20), nullable=False)
    days_elapsed = db.Column(db.Integer, default=10)
    total_days = db.Column(db.Integer, default=45)
    cn_ratio = db.Column(db.String(20), default="30:1")
    temperature_c = db.Column(db.Float, default=42.0)
    moisture_pct = db.Column(db.Float, default=55.0)
    stage = db.Column(db.String(50), default="Thermophilic Stage")

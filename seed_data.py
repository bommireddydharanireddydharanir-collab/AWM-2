from models import db, WasteRequest, FertilizerProduct, CompostBatch, FertilizerOrder
from datetime import datetime

def seed_database(app):
    with app.app_context():
        # Check if products already exist
        if FertilizerProduct.query.count() == 0:
            products = [
                FertilizerProduct(
                    name="Organic Vermicompost Gold",
                    category="Vermicompost",
                    npk_ratio="2.5 - 1.2 - 1.5",
                    price_per_unit=380.0,
                    unit="40kg Bag",
                    description="Pure worm castings enriched with beneficial microbes, humic acids, and micronutrients. Produced by recycling paddy straw and cattle manure.",
                    key_benefits="Enhances soil aeration, improves moisture retention by 30%, and suppresses soil-borne diseases.",
                    stock_quantity=140,
                    suitable_crops="Vegetables, Paddy, Fruits, Flowering Plants",
                    icon_class="fa-worm"
                ),
                FertilizerProduct(
                    name="Enriched Biochar & Stubble Compost",
                    category="Compost",
                    npk_ratio="1.8 - 0.9 - 1.2",
                    price_per_unit=320.0,
                    unit="50kg Bag",
                    description="Thermal biochar mixed with decomposed wheat stubble and bagasse. Permanently sequesters carbon while creating porous microbial shelters in soil.",
                    key_benefits="Prevents nutrient leaching, regulates acidic/alkaline soils, locks carbon in soil for decades.",
                    stock_quantity=95,
                    suitable_crops="Wheat, Maize, Sugarcane, Cotton",
                    icon_class="fa-fire-flame-simple"
                ),
                FertilizerProduct(
                    name="Rhizo-Azoto Bio-Inoculant",
                    category="Biofertilizer",
                    npk_ratio="Microbial (N-Fixer & P-Solubilizer)",
                    price_per_unit=180.0,
                    unit="1kg Packet",
                    description="Contains live bacterial cultures of Azotobacter and Phosphate Solubilizing Bacteria (PSB) harvested from fermented agricultural biomass.",
                    key_benefits="Fixes atmospheric nitrogen up to 25-30 kg N/ha, reduces chemical urea need by 25%.",
                    stock_quantity=200,
                    suitable_crops="Pulses, Legumes, Oilseeds, Cereals",
                    icon_class="fa-bacterium"
                ),
                FertilizerProduct(
                    name="Concentrated Fermented Jeevamrutha",
                    category="Liquid Organic",
                    npk_ratio="Active Microbial Consortium",
                    price_per_unit=250.0,
                    unit="5 Litre Can",
                    description="Traditional bio-enhancer made from cow dung, urine, pulse flour, and virgin forest soil. Multiplies native soil microorganisms exponentially.",
                    key_benefits="Rapid foliar and soil root absorption, acts as natural plant vigor booster and mild pest repellent.",
                    stock_quantity=60,
                    suitable_crops="All horticulture crops, greenhouse farming, kitchen gardens",
                    icon_class="fa-bottle-droplet"
                ),
                FertilizerProduct(
                    name="Phospho-Compost (Rock Phosphate + Agro Waste)",
                    category="Compost",
                    npk_ratio="1.6 - 2.8 - 1.1",
                    price_per_unit=420.0,
                    unit="50kg Bag",
                    description="Natural rock phosphate co-composted with farmyard manure and dry crop residue, converting insoluble phosphorus into plant-ready form.",
                    key_benefits="Strong root system initiation, high flowering and fruiting efficiency without chemical superphosphate.",
                    stock_quantity=75,
                    suitable_crops="Paddy, Mustard, Groundnut, Tomato, Potato",
                    icon_class="fa-leaf"
                )
            ]
            db.session.bulk_save_objects(products)
            db.session.commit()

        if WasteRequest.query.count() == 0:
            sample_requests = [
                WasteRequest(
                    farmer_name="Ramesh Kumar",
                    phone="9876543210",
                    village_location="Rampur Village, Plot 14",
                    waste_type="Paddy Straw (Post-harvest)",
                    estimated_quantity_kg=2500,
                    pickup_date="2026-10-18",
                    status="Scheduled for Pickup",
                    notes="Residue dry and bundled. Ready for pickup near village main gate."
                ),
                WasteRequest(
                    farmer_name="Sita Devi",
                    phone="9812345678",
                    village_location="Green Valley Farm, Sector B",
                    waste_type="Sugarcane Bagasse & Leaves",
                    estimated_quantity_kg=1800,
                    pickup_date="2026-10-19",
                    status="In Bio-Conversion",
                    notes="High carbon content; routed to Composting Unit 2."
                ),
                WasteRequest(
                    farmer_name="Gurpreet Singh",
                    phone="9765432109",
                    village_location="Navpind, Field 3",
                    waste_type="Wheat Stubble",
                    estimated_quantity_kg=4200,
                    pickup_date="2026-10-15",
                    status="Converted to Fertilizer",
                    notes="Successfully processed into 1.6 tonnes of Organic Biochar Compost."
                ),
                WasteRequest(
                    farmer_name="Anil Gowda",
                    phone="9945123789",
                    village_location="Hassan Agro Cluster",
                    waste_type="Cattle Manure & Vegetable Residue",
                    estimated_quantity_kg=1200,
                    pickup_date="2026-10-21",
                    status="Pending Collection",
                    notes="Moist green waste suitable for vermicomposting pit 3."
                )
            ]
            db.session.bulk_save_objects(sample_requests)
            db.session.commit()

        if CompostBatch.query.count() == 0:
            batches = [
                CompostBatch(
                    batch_name="Vermicompost Pit #A1 - Eisenia Foetida",
                    waste_source="Cattle Manure (40%) + Paddy Straw (60%)",
                    method="Vermicomposting",
                    start_date="2026-09-20",
                    days_elapsed=24,
                    total_days=45,
                    cn_ratio="28:1",
                    temperature_c=26.5,
                    moisture_pct=62.0,
                    stage="Active Worm Feeding & Digestion"
                ),
                CompostBatch(
                    batch_name="Windrow Pile #B4 - Thermophilic",
                    waste_source="Sugarcane Bagasse + Green Forage",
                    method="Aerobic Windrow",
                    start_date="2026-10-02",
                    days_elapsed=12,
                    total_days=35,
                    cn_ratio="32:1",
                    temperature_c=58.2,
                    moisture_pct=54.0,
                    stage="Thermophilic Sanitization (Weed/Pathogen kill)"
                ),
                CompostBatch(
                    batch_name="Batch #C2 - Maturing Biochar Compost",
                    waste_source="Wheat Straw + Biochar + Rock Phosphate",
                    method="Phospho-Composting",
                    start_date="2026-09-01",
                    days_elapsed=43,
                    total_days=45,
                    cn_ratio="25:1",
                    temperature_c=31.0,
                    moisture_pct=48.0,
                    stage="Curing & Maturation (Near Harvest)"
                )
            ]
            db.session.bulk_save_objects(batches)
            db.session.commit()

"""
Seed the database with:
  - The two branches (Choondi, Tripunithura)
  - A default admin user (credentials from .env)
  - A few sample sofas so the catalog isn't empty on first run

Run with:  python -m app.seed
"""
from app.config import settings
from app.crud.branch import get_or_create_branch
from app.crud.product import add_product_images, create_product
from app.crud.user import get_user_by_username, create_admin_user
from app.database import Base, SessionLocal, engine
from app.schemas.product import ProductCreate


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # --- Branches ---
        choondi = get_or_create_branch(db, "Choondi")
        tripunithura = get_or_create_branch(db, "Tripunithura")
        print(f"Branches ready: {choondi.name} (id={choondi.id}), {tripunithura.name} (id={tripunithura.id})")

        # --- Default admin ---
        if not get_user_by_username(db, settings.DEFAULT_ADMIN_USERNAME):
            create_admin_user(
                db,
                username=settings.DEFAULT_ADMIN_USERNAME,
                password=settings.DEFAULT_ADMIN_PASSWORD,
                email=settings.DEFAULT_ADMIN_EMAIL,
            )
            print(f"Created default admin user: {settings.DEFAULT_ADMIN_USERNAME}")
        else:
            print("Default admin user already exists, skipping.")

        # --- Sample sofas (only if catalog is empty) ---
        from app.models.product import Product

        if db.query(Product).count() == 0:
            samples = [
                ProductCreate(
                    name="Milano 3-Seater Sofa",
                    price=34999,
                    description="A classic 3-seater sofa with a sturdy hardwood frame and plush cushioning.",
                    branch_id=choondi.id,
                    stock_count=2,
                    length_cm=210,
                    width_cm=90,
                    height_cm=85,
                    seating_capacity=3,
                    foam_thickness_cm=6,
                    foam_type="High Density Foam",
                    fabric_material="Velvet",
                    frame_material="Sheesham Wood",
                    color="Emerald Green",
                    warranty="2 Years",
                    available_colors=["Emerald Green", "Navy Blue", "Charcoal Grey"],
                ),
                ProductCreate(
                    name="Nordic L-Shape Sectional",
                    price=52999,
                    description="Spacious L-shaped sectional sofa, perfect for modern living rooms.",
                    branch_id=choondi.id,
                    stock_count=0,
                    length_cm=280,
                    width_cm=160,
                    height_cm=80,
                    seating_capacity=5,
                    foam_thickness_cm=8,
                    foam_type="Memory Foam",
                    fabric_material="Linen",
                    frame_material="Engineered Wood",
                    color="Beige",
                    warranty="3 Years",
                    available_colors=["Beige", "Light Grey"],
                ),
                ProductCreate(
                    name="Kochi Recliner Sofa",
                    price=45999,
                    description="Two-seater recliner sofa with premium leatherette upholstery.",
                    branch_id=tripunithura.id,
                    stock_count=4,
                    length_cm=180,
                    width_cm=95,
                    height_cm=100,
                    seating_capacity=2,
                    foam_thickness_cm=7,
                    foam_type="High Resilience Foam",
                    fabric_material="Leatherette",
                    frame_material="Solid Wood",
                    color="Tan Brown",
                    warranty="5 Years",
                    available_colors=["Tan Brown", "Black"],
                ),
                ProductCreate(
                    name="Coastal Compact Sofa",
                    price=27999,
                    description="A compact 2-seater ideal for small living spaces and apartments.",
                    branch_id=tripunithura.id,
                    stock_count=0,
                    length_cm=160,
                    width_cm=85,
                    height_cm=80,
                    seating_capacity=2,
                    foam_thickness_cm=5,
                    foam_type="High Density Foam",
                    fabric_material="Cotton Blend",
                    frame_material="Engineered Wood",
                    color="Mustard Yellow",
                    warranty="1 Year",
                    available_colors=["Mustard Yellow", "Teal"],
                ),
            ]
            for sample in samples:
                product = create_product(db, sample)
                # Placeholder image URLs (replace with real uploads via the admin panel).
                add_product_images(
                    db,
                    product,
                    [f"/static/uploads/placeholder-sofa-{(product.id % 3) + 1}.jpg"],
                )
            print(f"Seeded {len(samples)} sample sofas.")
        else:
            print("Products already exist, skipping sample sofa seeding.")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()

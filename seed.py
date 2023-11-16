from faker import Faker
import random
import requests
from datetime import datetime, timedelta

fake = Faker(["es_AR"])


def generate_material_name():
    materials = [
        "Steel",
        "Aluminum",
        "Copper",
        "Plastic",
        "Wood",
        "Glass",
        "Concrete",
        "Brick",
        "Stone",
        "Ceramic",
        "Rubber",
        "Leather",
        "Fabric",
        "Paper",
        "Cardboard",
        "Carbon fiber",
        "Fiberglass",
        "Graphene",
        "Kevlar",
        "Titanium",
        "Gold",
        "Silver",
        "Iron",
    ]
    return f"{random.choice(materials)}"


def generate_provider_name():
    return fake.company()


def generate_factory_name():
    return f"Fabrica {fake.company()}"


def generate_materials():
    materials = []
    for _ in range(10):
        materials.append(
            {
                "nombre": generate_material_name(),
            }
        )
    return materials


def generate_providers():
    providers = []
    for _ in range(10):
        providers.append(
            {
                "nombre": generate_provider_name(),
                "tipo_actor": random.choice(["Proveedor", "Reciclador"]),
                "ubicacion": fake.city(),
                "internacional": bool(random.getrandbits(1)),
            }
        )
    return providers


def generate_factories():
    factories = []
    for _ in range(10):
        factories.append(
            {
                "nombre": generate_factory_name(),
                "ubicacion": fake.city(),
                "internacional": True,
            }
        )
    return factories


def generate_materials_seed():
    materials = generate_materials()

    url = "http://45.55.121.156/api/proveedores/materiales/"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    for material in materials:
        payload = {
            "nombre": material["nombre"],
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.status_code)
        print(response.json())


def generate_factories_seed():
    factories = generate_factories()

    url = "http://45.55.121.156/api/proveedores/lugar-fabricacion/"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    for factory in factories:
        payload = {
            "nombre": factory["nombre"],
            "ubicacion": factory["ubicacion"],
            "internacional": factory["internacional"]
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.status_code)
        print(response.json())

def generate_providers_seed():
    providers = generate_providers()

    url = "http://45.55.121.156/api/proveedores/proveedores/"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    for provider in providers:
        payload = {
            "nombre": provider["nombre"],
            "tipo_actor": provider["tipo_actor"],
            "ubicacion": provider["ubicacion"],
            "internacional": provider["internacional"]
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.status_code)
        print(response.json())


# ...

def generate_material_provider():
    url_providers = "http://45.55.121.156/api/proveedores/proveedores/"
    url_materials = "http://45.55.121.156/api/proveedores/materiales/"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    providers_response = requests.get(url_providers, headers=headers)
    materials_response = requests.get(url_materials, headers=headers)

    if providers_response.status_code != 200 or materials_response.status_code != 200:
        print("Error: Could not retrieve providers or materials")
        return

    providers = providers_response.json()
    materials = materials_response.json()

    url = "http://45.55.121.156/api/proveedores/proveedores-materiales/"

    for material in materials:
        # randomly select a subset of providers for this material
        selected_providers = random.sample(providers, k=2)

        for provider in selected_providers:
            payload = {
                "actor": provider["id"],
                "material": material["id"],
                "cantidad_disponible": random.randint(1, 12)*10,
                "plazo_entrega_dias": random.randint(1, 30),
                "es_importado": random.choice([True, False])
            }
            print(payload)
            response = requests.post(url, json=payload, headers=headers)

            print(response.status_code)
            print(response.json())


def generate_factory_reservation():
    url_factories = "http://45.55.121.156/api/proveedores/lugar-fabricacion/"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    factories_response = requests.get(url_factories, headers=headers)

    if factories_response.status_code != 200:
        print("Error: Could not retrieve factories")
        return

    factories = factories_response.json()

    url = "http://45.55.121.156/api/proveedores/lugar-fabricacion-en-reserva/"

    for factory in factories:
        payload = {
            "telefono_reserva": fake.phone_number(),
            "fecha_final_disponible": (datetime.now() + timedelta(days=random.randint(365, 730))).strftime("%Y-%m-%d"),
            "lugar_de_fabricacion": factory["id"]
        }
        print(payload)
        response = requests.post(url, json=payload, headers=headers)
        print(response.status_code)
        print(response.json())

if __name__ == "__main__":
    generate_materials_seed()
    generate_factories_seed()
    generate_providers_seed()
    generate_material_provider()
    generate_factory_reservation()
"""Nice Classification (NCL 12-2023) — all 45 classes with canonical descriptions."""

from typing import Optional

NICE_CLASSES: dict[int, dict] = {
    1: {
        "title": "Chemicals",
        "description": "Chemicals for use in industry, science and photography; unprocessed artificial resins, unprocessed plastics; fire extinguishing and fire prevention compositions; tempering and soldering preparations; substances for tanning animal skins and hides; adhesives for use in industry; putties and other paste fillers; compost, manures, fertilizers; biological preparations for use in industry and science.",
        "examples": ["adhesives for industry", "fertilizers", "chemical reagents", "unprocessed resins"],
    },
    2: {
        "title": "Paints",
        "description": "Paints, varnishes, lacquers; preservatives against rust and against deterioration of wood; colorants, dyes; inks for printing, marking and engraving; raw natural resins; metals in foil and powder form for use in painting, decorating, printing and art.",
        "examples": ["paints", "varnishes", "dyes", "printing inks", "rust-proofing preparations"],
    },
    3: {
        "title": "Cosmetics and cleaning preparations",
        "description": "Non-medicated cosmetics and toiletry preparations; non-medicated dentifrices; perfumery, essential oils; bleaching preparations and other substances for laundry use; cleaning, polishing, scouring and abrasive preparations.",
        "examples": ["cosmetics", "perfumes", "soaps", "cleaning products", "toothpaste"],
    },
    4: {
        "title": "Lubricants and fuels",
        "description": "Industrial oils and greases, wax; lubricants; dust absorbing, wetting and binding compositions; fuels and illuminants; candles and wicks for lighting.",
        "examples": ["motor oil", "industrial lubricants", "fuel", "candles", "waxes"],
    },
    5: {
        "title": "Pharmaceuticals",
        "description": "Pharmaceuticals, medical and veterinary preparations; sanitary preparations for medical purposes; dietetic food and substances adapted for medical or veterinary use; food for babies; dietary supplements for humans and animals; plasters, materials for dressings; material for stopping teeth, dental wax; disinfectants; preparations for destroying vermin; fungicides, herbicides.",
        "examples": ["pharmaceuticals", "vitamins", "disinfectants", "dietary supplements", "medical dressings"],
    },
    6: {
        "title": "Metal goods",
        "description": "Common metals and their alloys, ores; metal materials for building and construction; transportable buildings of metal; non-electric cables and wires of common metal; small items of metal hardware; metal containers for storage or transport; safes.",
        "examples": ["metal pipes", "metal hardware", "metal containers", "locks", "safes"],
    },
    7: {
        "title": "Machinery",
        "description": "Machines, machine tools, power-operated tools; motors and engines; machine coupling and transmission components; agricultural implements other than hand-operated hand tools; incubators for eggs; automatic vending machines.",
        "examples": ["motors", "pumps", "compressors", "industrial machines", "power tools"],
    },
    8: {
        "title": "Hand tools",
        "description": "Hand tools and implements, hand-operated; cutlery; side arms, except firearms; razors.",
        "examples": ["cutlery", "hand tools", "knives", "scissors", "razors"],
    },
    9: {
        "title": "Electrical and scientific apparatus",
        "description": "Scientific, research, navigation, surveying, photographic, cinematographic, audiovisual, optical, weighing, measuring, signalling, detecting, testing, inspecting, life-saving and teaching apparatus and instruments; apparatus and instruments for conducting, switching, transforming, accumulating, regulating or controlling the distribution or use of electricity; apparatus and instruments for recording, transmitting, reproducing or processing sound, images or data; magnetic data carriers, recording discs; compact discs, DVDs and other digital recording media; mechanisms for coin-operated apparatus; cash registers, calculating machines, data processing equipment, computers; computer software; telecommunications apparatus and instruments.",
        "examples": ["computers", "software", "smartphones", "cameras", "medical devices", "sensors"],
    },
    10: {
        "title": "Medical apparatus",
        "description": "Surgical, medical, dental and veterinary apparatus and instruments; artificial limbs, eyes and teeth; orthopaedic articles; suturing materials; therapeutic and assistive devices adapted for persons with disabilities; massage apparatus; apparatus, devices and articles for nursing infants; sexual activity apparatus, devices and articles.",
        "examples": ["medical devices", "prosthetics", "surgical instruments", "wheelchairs", "dental apparatus"],
    },
    11: {
        "title": "Environmental control apparatus",
        "description": "Apparatus and installations for lighting, heating, cooling, steam generating, cooking, drying, ventilating, water supply and sanitary purposes.",
        "examples": ["air conditioners", "heating systems", "lighting fixtures", "water purifiers", "ovens"],
    },
    12: {
        "title": "Vehicles",
        "description": "Vehicles; apparatus for locomotion by land, air or water.",
        "examples": ["automobiles", "motorcycles", "bicycles", "aircraft", "boats", "electric vehicles"],
    },
    13: {
        "title": "Firearms",
        "description": "Firearms; ammunition and projectiles; explosives; fireworks.",
        "examples": ["firearms", "ammunition", "explosives", "fireworks"],
    },
    14: {
        "title": "Jewelry",
        "description": "Precious metals and their alloys; jewellery, precious and semi-precious stones; horological and chronometric instruments.",
        "examples": ["jewelry", "watches", "clocks", "precious metals", "gemstones"],
    },
    15: {
        "title": "Musical instruments",
        "description": "Musical instruments; music stands and holders for music; conductors' batons.",
        "examples": ["pianos", "guitars", "violins", "drums", "electronic instruments"],
    },
    16: {
        "title": "Paper goods and printed matter",
        "description": "Paper and cardboard; printed matter; bookbinding material; photographs; stationery and office requisites, except furniture; adhesives for stationery or household purposes; drawing materials and materials for artists; paintbrushes; instructional and teaching materials; plastic sheets, films and bags for wrapping and packaging; printers' type and clichés.",
        "examples": ["books", "magazines", "stationery", "office supplies", "printed publications"],
    },
    17: {
        "title": "Rubber goods",
        "description": "Unprocessed and semi-processed rubber, gutta-percha, gum, asbestos, mica and substitutes for all these materials; plastics and resins in extruded form for use in manufacture; packing, stopping and insulating materials; flexible pipes, tubes and hoses.",
        "examples": ["rubber gaskets", "insulating materials", "plastic tubes", "hoses", "seals"],
    },
    18: {
        "title": "Leather goods",
        "description": "Leather and imitations of leather; animal skins and hides; luggage and carrying bags; umbrellas and parasols; walking sticks; whips, harness and saddlery; collars, leashes and clothing for animals.",
        "examples": ["handbags", "wallets", "luggage", "backpacks", "leather goods"],
    },
    19: {
        "title": "Non-metallic building materials",
        "description": "Building materials, non-metallic; non-metallic rigid pipes for building; asphalt, pitch and bitumen; non-metallic transportable buildings; monuments, not of metal.",
        "examples": ["bricks", "cement", "glass for building", "non-metal pipes", "wood for building"],
    },
    20: {
        "title": "Furniture",
        "description": "Furniture, mirrors, picture frames; containers, not of metal, for storage or transport; unworked or semi-worked bone, horn, whalebone or mother-of-pearl; shells; meerschaum; yellow amber.",
        "examples": ["furniture", "mirrors", "picture frames", "wooden containers", "storage boxes"],
    },
    21: {
        "title": "Housewares and glass",
        "description": "Household or kitchen utensils and containers; cookware and tableware, except forks, knives and spoons; combs and sponges; brushes, except paintbrushes; brush-making materials; articles for cleaning purposes; unworked or semi-worked glass, except building glass; glassware, porcelain and earthenware.",
        "examples": ["kitchen utensils", "glassware", "cookware", "cleaning tools", "dishes"],
    },
    22: {
        "title": "Cordage and fibres",
        "description": "Ropes and string; nets; tents and tarpaulins; awnings of textile or synthetic materials; sails; sacks for the transport and storage of materials in bulk; padding and stuffing materials, except of paper or cardboard; raw fibrous textile materials and substitutes therefor.",
        "examples": ["ropes", "nets", "tarpaulins", "packing materials", "sails"],
    },
    23: {
        "title": "Yarns and threads",
        "description": "Yarns and threads for textile use.",
        "examples": ["yarns", "threads", "weaving thread", "sewing thread"],
    },
    24: {
        "title": "Fabrics",
        "description": "Textiles and substitutes for textiles; household linen; curtains of textile or plastic.",
        "examples": ["textiles", "bed linen", "towels", "curtains", "fabric"],
    },
    25: {
        "title": "Clothing",
        "description": "Clothing, footwear, headgear.",
        "examples": ["clothing", "shoes", "hats", "sportswear", "fashion accessories"],
    },
    26: {
        "title": "Fancy goods",
        "description": "Lace and embroidery, ribbons and braid; buttons, hooks and eyes, pins and needles; artificial flowers; hair decorations; false hair.",
        "examples": ["buttons", "ribbons", "lace", "embroidery", "hair accessories"],
    },
    27: {
        "title": "Floor coverings",
        "description": "Carpets, rugs, mats and matting, linoleum and other materials for covering existing floors; wall hangings, not of textile.",
        "examples": ["carpets", "rugs", "floor mats", "linoleum", "wall coverings"],
    },
    28: {
        "title": "Toys and sporting goods",
        "description": "Games, toys and playthings; video game apparatus; gymnastic and sporting articles; decorations for Christmas trees.",
        "examples": ["toys", "video games", "sports equipment", "board games", "fitness equipment"],
    },
    29: {
        "title": "Meats and processed foods",
        "description": "Meat, fish, poultry and game; meat extracts; preserved, frozen, dried and cooked fruits and vegetables; jellies, jams, compotes; eggs; milk, cheese, butter, yogurt and other milk products; oils and fats for food.",
        "examples": ["meat", "dairy products", "preserved vegetables", "frozen food", "cooking oils"],
    },
    30: {
        "title": "Staple foods",
        "description": "Coffee, tea, cocoa and artificial coffee; rice, pasta and noodles; tapioca and sago; flour and preparations made from cereals; bread, pastries and confectionery; chocolate; ice cream, sorbets and other edible ices; sugar, honey, treacle; yeast, baking-powder; salt, seasonings, spices, preserved herbs; vinegar, sauces and other condiments; ice.",
        "examples": ["coffee", "tea", "bakery products", "confectionery", "condiments", "spices"],
    },
    31: {
        "title": "Natural agricultural products",
        "description": "Raw and unprocessed agricultural, aquacultural, horticultural and forestry products; raw and unprocessed grains and seeds; fresh fruits and vegetables, fresh herbs; natural plants and flowers; bulbs, seedlings and seeds for planting; live animals; foodstuffs and beverages for animals; malt.",
        "examples": ["fresh fruits", "vegetables", "plants", "seeds", "live animals", "pet food"],
    },
    32: {
        "title": "Light beverages",
        "description": "Beers; non-alcoholic beverages; mineral and aerated waters; fruit beverages and fruit juices; syrups and other non-alcoholic preparations for making beverages.",
        "examples": ["beer", "soft drinks", "fruit juice", "mineral water", "energy drinks"],
    },
    33: {
        "title": "Wine and spirits",
        "description": "Alcoholic beverages, except beers; alcoholic preparations for making beverages.",
        "examples": ["wine", "spirits", "liqueurs", "whisky", "vodka"],
    },
    34: {
        "title": "Tobacco products",
        "description": "Tobacco and tobacco substitutes; cigarettes and cigars; electronic cigarettes and oral vaporizers for smokers; smokers' articles; matches.",
        "examples": ["cigarettes", "cigars", "tobacco", "e-cigarettes", "matches"],
    },
    35: {
        "title": "Advertising and business",
        "description": "Advertising; business management, organization and administration; office functions.",
        "examples": ["advertising services", "business consulting", "office administration", "market research", "recruitment"],
    },
    36: {
        "title": "Insurance and financial",
        "description": "Financial, monetary and banking services; insurance services; real estate affairs.",
        "examples": ["banking", "insurance", "investment services", "real estate", "financial consulting"],
    },
    37: {
        "title": "Building construction and repair",
        "description": "Construction services; installation and repair services; mining extraction, oil and gas drilling.",
        "examples": ["construction", "repair services", "installation", "maintenance", "plumbing"],
    },
    38: {
        "title": "Telecommunications",
        "description": "Telecommunications services.",
        "examples": ["internet services", "telephone services", "broadcasting", "messaging services", "VoIP"],
    },
    39: {
        "title": "Transportation and storage",
        "description": "Transport; packaging and storage of goods; travel arrangement.",
        "examples": ["shipping", "delivery services", "warehousing", "travel agencies", "logistics"],
    },
    40: {
        "title": "Treatment of materials",
        "description": "Treatment of materials; recycling of waste and trash; air purification and treatment of water; printing services; food and drink preservation.",
        "examples": ["manufacturing services", "printing", "recycling", "material processing", "food processing"],
    },
    41: {
        "title": "Education and entertainment",
        "description": "Education; providing of training; entertainment; sporting and cultural activities.",
        "examples": ["education", "training", "entertainment", "sports", "publishing", "online courses"],
    },
    42: {
        "title": "Scientific and technological services",
        "description": "Scientific and technological services and research and design relating thereto; industrial analysis, industrial research and industrial design services; quality control and authentication services; design and development of computer hardware and software.",
        "examples": ["software development", "IT services", "research", "cloud computing", "SaaS", "app development"],
    },
    43: {
        "title": "Food and drink services",
        "description": "Services for providing food and drink; temporary accommodation.",
        "examples": ["restaurants", "catering", "hotels", "food delivery", "coffee shops"],
    },
    44: {
        "title": "Medical and veterinary services",
        "description": "Medical services; veterinary services; hygienic and beauty care for human beings or animals; agriculture, aquaculture, horticulture and forestry services.",
        "examples": ["medical services", "veterinary care", "beauty salons", "dental services", "farming services"],
    },
    45: {
        "title": "Legal and security services",
        "description": "Legal services; security services for the physical protection of tangible property and individuals; personal and social services rendered by others to meet the needs of individuals.",
        "examples": ["legal services", "security services", "personal protection", "social services", "funeral services"],
    },
}


def get_all_classes() -> list[dict]:
    return [{"class_number": num, **data} for num, data in sorted(NICE_CLASSES.items())]


def get_class(number: int) -> Optional[dict]:
    if number not in NICE_CLASSES:
        return None
    return {"class_number": number, **NICE_CLASSES[number]}


def search_classes_by_keyword(keyword: str) -> list[dict]:
    keyword_lower = keyword.lower()
    results = []
    for num, data in NICE_CLASSES.items():
        text = (
            data["title"].lower()
            + " "
            + data["description"].lower()
            + " "
            + " ".join(data["examples"]).lower()
        )
        if keyword_lower in text:
            results.append({"class_number": num, **data})
    return results

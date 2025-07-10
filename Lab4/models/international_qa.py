def answer_french(question, context):
    """Answer questions in French using rule-based responses"""
    print("Processing French question...")

    # French answers for solar system questions
    french_answers = {
        "solar system": "Le système solaire est un système gravitationnel composé du Soleil et de huit planètes qui l'orbitent. Il comprend également des lunes, des astéroïdes et des comètes.",
        "planets": "Il y a huit planètes dans le système solaire: Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus et Neptune. Elles orbitent toutes autour du Soleil.",
        "sun": "Le Soleil est une étoile située au centre du système solaire. Il fournit la lumière et la chaleur à toutes les planètes.",
        "earth": "La Terre est la troisième planète du système solaire et la seule connue pour abriter la vie. Elle a une lune naturelle.",
        "mars": "Mars est connue comme la planète rouge. C'est la quatrième planète du système solaire.",
        "jupiter": "Jupiter est la plus grande planète du système solaire. C'est une géante gazeuse avec de nombreuses lunes.",
        "saturn": "Saturne est célèbre pour ses magnifiques anneaux. C'est une géante gazeuse.",
        "moon": "La Lune est le satellite naturel de la Terre. Elle orbite autour de notre planète."
    }

    # Find best match based on keywords in the question
    question_lower = question.lower()

    # Check for specific keywords
    if any(word in question_lower for word in ["solar system", "système solaire", "systeme solaire"]):
        return french_answers["solar system"]
    elif any(word in question_lower for word in ["planets", "planètes", "planetes", "planet"]):
        return french_answers["planets"]
    elif any(word in question_lower for word in ["sun", "soleil"]):
        return french_answers["sun"]
    elif any(word in question_lower for word in ["earth", "terre"]):
        return french_answers["earth"]
    elif any(word in question_lower for word in ["mars"]):
        return french_answers["mars"]
    elif any(word in question_lower for word in ["jupiter"]):
        return french_answers["jupiter"]
    elif any(word in question_lower for word in ["saturn", "saturne"]):
        return french_answers["saturn"]
    elif any(word in question_lower for word in ["moon", "lune"]):
        return french_answers["moon"]
    else:
        # Default answer about solar system
        return french_answers["solar system"]

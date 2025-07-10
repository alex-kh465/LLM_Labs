def answer_malayalam(question, context):
    """Answer questions in Malayalam using rule-based responses"""
    print("Processing Malayalam question...")

    # Malayalam answers for solar system questions
    malayalam_answers = {
        "solar system": "സൗരയൂഥം സൂര്യനും അതിനെ ചുറ്റി സഞ്ചരിക്കുന്ന എട്ട് ഗ്രഹങ്ങളും ഉൾപ്പെടുന്ന ഒരു സിസ്റ്റമാണ്. ഇത് ഗുരുത്വാകർഷണത്താൽ ബന്ധിപ്പിച്ചിരിക്കുന്നു.",
        "planets": "സൗരയൂഥത്തിൽ എട്ട് ഗ്രഹങ്ങളുണ്ട്: ബുധൻ, ശുക്രൻ, ഭൂമി, ചൊവ്വ, വ്യാഴം, ശനി, യുറാനസ്, നെപ്ട്യൂൺ. ഇവയെല്ലാം സൂര്യനെ ചുറ്റി സഞ്ചരിക്കുന്നു.",
        "sun": "സൂര്യൻ ഒരു നക്ഷത്രമാണ്. അത് സൗരയൂഥത്തിന്റെ കേന്ദ്രത്തിലാണ്. സൂര്യൻ എല്ലാ ഗ്രഹങ്ങൾക്കും പ്രകാശവും ചൂടും നൽകുന്നു.",
        "earth": "ഭൂമി സൗരയൂഥത്തിലെ മൂന്നാമത്തെ ഗ്രഹമാണ്. ഇത് ജീവൻ ഉള്ള ഏക ഗ്രഹമാണ്. ഭൂമിക്ക് ഒരു ചന്ദ്രനുണ്ട്.",
        "mars": "ചൊവ്വ ചുവന്ന ഗ്രഹം എന്നറിയപ്പെടുന്നു. ഇത് ഭൂമിയുടെ അടുത്തുള്ള ഗ്രഹമാണ്.",
        "jupiter": "വ്യാഴം സൗരയൂഥത്തിലെ ഏറ്റവും വലിയ ഗ്രഹമാണ്. ഇതിന് നിരവധി ചന്ദ്രന്മാരുണ്ട്.",
        "saturn": "ശനിക്ക് മനോഹരമായ വളയങ്ങളുണ്ട്. ഇത് വാതക ഗ്രഹമാണ്.",
        "moon": "ചന്ദ്രൻ ഭൂമിയുടെ പ്രകൃതിദത്ത ഉപഗ്രഹമാണ്. ഇത് ഭൂമിയെ ചുറ്റി സഞ്ചരിക്കുന്നു."
    }

    # Find best match based on keywords in the question
    question_lower = question.lower()

    # Check for specific keywords
    if any(word in question_lower for word in ["solar system", "സൗരയൂഥം"]):
        return malayalam_answers["solar system"]
    elif any(word in question_lower for word in ["planets", "ഗ്രഹങ്ങൾ", "planet"]):
        return malayalam_answers["planets"]
    elif any(word in question_lower for word in ["sun", "സൂര്യൻ"]):
        return malayalam_answers["sun"]
    elif any(word in question_lower for word in ["earth", "ഭൂമി"]):
        return malayalam_answers["earth"]
    elif any(word in question_lower for word in ["mars", "ചൊവ്വ"]):
        return malayalam_answers["mars"]
    elif any(word in question_lower for word in ["jupiter", "വ്യാഴം"]):
        return malayalam_answers["jupiter"]
    elif any(word in question_lower for word in ["saturn", "ശനി"]):
        return malayalam_answers["saturn"]
    elif any(word in question_lower for word in ["moon", "ചന്ദ്രൻ"]):
        return malayalam_answers["moon"]
    else:
        # Default answer about solar system
        return malayalam_answers["solar system"]

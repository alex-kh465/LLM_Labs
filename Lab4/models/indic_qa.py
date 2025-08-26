def answer_hindi(question, context):
    """Answer questions in Hindi using rule-based responses"""
    print("Processing Hindi question...")

    # Hindi answers for solar system related questions
    hindi_answers = {
        "solar system": "सौरमंडल सूर्य और उसके चारों ओर घूमने वाले आठ ग्रहों सहित एक प्रणाली है। यह गुरुत्वाकर्षण बल से एक साथ बंधा हुआ है।",
        "planets": "सौरमंडल में आठ ग्रह हैं: बुध, शुक्र, पृथ्वी, मंगल, बृहस्पति, शनि, यूरेनस और नेपच्यून। ये सभी सूर्य की परिक्रमा करते हैं।",
        "sun": "सूर्य एक तारा है जो सौरमंडल के केंद्र में स्थित है। यह सभी ग्रहों को प्रकाश और गर्मी प्रदान करता है।",
        "earth": "पृथ्वी सौरमंडल का तीसरा ग्रह है और यह एकमात्र ग्रह है जहाँ जीवन पाया जाता है। पृथ्वी का एक उपग्रह है जिसे चंद्रमा कहते हैं।",
        "mars": "मंगल को लाल ग्रह कहा जाता है। यह पृथ्वी के निकट का ग्रह है।",
        "jupiter": "बृहस्पति सौरमंडल का सबसे बड़ा ग्रह है और इसके कई चंद्रमा हैं।",
        "saturn": "शनि के चारों ओर सुंदर वलय हैं और यह एक गैस ग्रह है।",
        "moon": "चंद्रमा पृथ्वी का प्राकृतिक उपग्रह है और यह पृथ्वी की परिक्रमा करता है।"
    }

    # Normalize question text
    question_lower = question.lower()

    # Keyword-based matching
    if any(word in question_lower for word in ["solar system", "सौरमंडल"]):
        return hindi_answers["solar system"]
    elif any(word in question_lower for word in ["planets", "ग्रह", "ग्रहों", "planet"]):
        return hindi_answers["planets"]
    elif any(word in question_lower for word in ["sun", "सूर्य"]):
        return hindi_answers["sun"]
    elif any(word in question_lower for word in ["earth", "पृथ्वी"]):
        return hindi_answers["earth"]
    elif any(word in question_lower for word in ["mars", "मंगल"]):
        return hindi_answers["mars"]
    elif any(word in question_lower for word in ["jupiter", "बृहस्पति"]):
        return hindi_answers["jupiter"]
    elif any(word in question_lower for word in ["saturn", "शनि"]):
        return hindi_answers["saturn"]
    elif any(word in question_lower for word in ["moon", "चंद्रमा", "चाँद"]):
        return hindi_answers["moon"]
    else:
        # Default fallback answer
        return hindi_answers["solar system"]

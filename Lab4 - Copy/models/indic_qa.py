def answer_hindi(question, context):
    """Answer questions in Hindi using rule-based responses"""
    print("Processing Hindi question...")

    # Hindi answers for solar system questions
    hindi_answers = {
        "solar system": "सौरमंडल सूर्य और उसके चारों ओर घूमने वाले आठ ग्रहों का एक समूह है। यह गुरुत्वाकर्षण बल से जुड़ा हुआ है।",
        "planets": "सौरमंडल में आठ ग्रह हैं: बुध, शुक्र, पृथ्वी, मंगल, बृहस्पति, शनि, यूरेनस और नेपच्यून। ये सभी सूर्य की परिक्रमा करते हैं।",
        "sun": "सूर्य एक तारा है और यह सौरमंडल के केंद्र में स्थित है। सूर्य सभी ग्रहों को प्रकाश और ऊष्मा प्रदान करता है।",
        "earth": "पृथ्वी सौरमंडल का तीसरा ग्रह है। यह जीवन को समर्थन देने वाला एकमात्र ज्ञात ग्रह है। पृथ्वी का एक उपग्रह है जिसे चंद्रमा कहते हैं।",
        "mars": "मंगल को 'लाल ग्रह' के नाम से जाना जाता है। यह पृथ्वी के पड़ोसी ग्रहों में से एक है।",
        "jupiter": "बृहस्पति सौरमंडल का सबसे बड़ा ग्रह है। इसके कई चंद्रमा हैं।",
        "saturn": "शनि के चारों ओर सुंदर वलय (rings) हैं। यह एक गैस दानव ग्रह है।",
        "moon": "चंद्रमा पृथ्वी का प्राकृतिक उपग्रह है और यह पृथ्वी की परिक्रमा करता है।"
    }

    # Find best match based on keywords in the question
    question_lower = question.lower()

    # Check for specific keywords
    if any(word in question_lower for word in ["solar system", "सौरमंडल"]):
        return hindi_answers["solar system"]
    elif any(word in question_lower for word in ["planets", "ग्रह", "planet"]):
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
    elif any(word in question_lower for word in ["moon", "चंद्रमा"]):
        return hindi_answers["moon"]
    else:
        # Default answer about solar system
        return hindi_answers["solar system"]

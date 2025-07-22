class GemmaService:
    def generate_response(self, user_input: str) -> str:
        input_lower = user_input.lower()
        # Specific, pedagogical responses for demo
        if 'photosynthesis' in input_lower:
            return ("Photosynthesis is the process by which green plants use sunlight to make food from carbon dioxide and water. It produces oxygen as a byproduct. Would you like a diagram or a simple experiment?")
        if 'quadratic equation' in input_lower or 'solve 2x^2+5x+3=0' in input_lower:
            return ("To solve 2x²+5x+3=0, use the quadratic formula: x = [-b±√(b²-4ac)]/(2a). Here, a=2, b=5, c=3. The solutions are x = -1 and x = -1.5. Want to see the steps?")
        if 'atomic structure' in input_lower:
            return ("Atomic structure refers to how protons, neutrons, and electrons are arranged in an atom. The nucleus contains protons and neutrons, while electrons orbit around it. Need a diagram or more details?")
        if 'jamb english' in input_lower and 'synonym' in input_lower:
            return ("JAMB English Synonym Practice: What is the synonym of 'benevolent'? A) Kind B) Angry C) Small D) Quick. The answer is A) Kind. Want more questions?")
        if 'waec biology' in input_lower and 'respiration' in input_lower:
            return ("WAEC Biology Recap: Respiration is the process by which cells break down glucose to release energy. It can be aerobic (with oxygen) or anaerobic (without oxygen). Need a sample question?")
        if 'waec' in input_lower:
            return ("Preparing for WAEC? I can help with past questions, study tips, or topic explanations. What do you need help with?")
        if 'jamb' in input_lower:
            return ("JAMB prep is important! Would you like a practice question, syllabus overview, or advice on exam strategy?")
        if 'english grammar' in input_lower:
            return ("Let's improve your English grammar! Would you like a lesson, a quiz, or help with a specific grammar rule?")
        if 'biology' in input_lower:
            return ("Biology is fascinating! Do you want a concept explained, a diagram, or a practice question?")
        # General fallback
        return ("Great question! I'm here to help you learn. Please ask about any topic, exam, or subject, and I'll do my best to assist you with clear explanations and examples.")

// Predefined offline responses for demo
export const offlineAITutorResponses = [
  {
    match: /photosynthesis/i,
    response: "Photosynthesis is the process by which green plants use sunlight to make food from carbon dioxide and water. It produces oxygen as a byproduct. Would you like a diagram or a simple experiment?"
  },
  {
    match: /quadratic equation|2x\^2\+5x\+3=0/i,
    response: "To solve 2x²+5x+3=0, use the quadratic formula: x = [-b±√(b²-4ac)]/(2a). Here, a=2, b=5, c=3. The solutions are x = -1 and x = -1.5. Want to see the steps?"
  },
  {
    match: /atomic structure/i,
    response: "Atomic structure refers to how protons, neutrons, and electrons are arranged in an atom. The nucleus contains protons and neutrons, while electrons orbit around it. Need a diagram or more details?"
  },
  {
    match: /jamb english.*synonym/i,
    response: "JAMB English Synonym Practice: What is the synonym of 'benevolent'? A) Kind B) Angry C) Small D) Quick. The answer is A) Kind. Want more questions?"
  },
  {
    match: /waec biology.*respiration/i,
    response: "WAEC Biology Recap: Respiration is the process by which cells break down glucose to release energy. It can be aerobic (with oxygen) or anaerobic (without oxygen). Need a sample question?"
  },
  {
    match: /waec/i,
    response: "Preparing for WAEC? I can help with past questions, study tips, or topic explanations. What do you need help with?"
  },
  {
    match: /jamb/i,
    response: "JAMB prep is important! Would you like a practice question, syllabus overview, or advice on exam strategy?"
  },
  {
    match: /english grammar/i,
    response: "Let's improve your English grammar! Would you like a lesson, a quiz, or help with a specific grammar rule?"
  },
  {
    match: /biology/i,
    response: "Biology is fascinating! Do you want a concept explained, a diagram, or a practice question?"
  }
];

export const offlineFallback = "Great question! I'm here to help you learn. Please ask about any topic, exam, or subject, and I'll do my best to assist you with clear explanations and examples.";

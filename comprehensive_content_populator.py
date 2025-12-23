#!/usr/bin/env python3
"""
Comprehensive Content Population Script
Creates content for missing subjects and underrepresented topics
"""

import csv
import os
from datetime import datetime
import json

class ContentPopulator:
    """Populates content for missing subjects and underrepresented topics"""

    def __init__(self):
        self.templates_dir = "content_templates"
        self.content_dir = "content"
        os.makedirs(self.content_dir, exist_ok=True)

    def populate_missing_subjects(self):
        """Create comprehensive content for missing subjects"""

        subjects_content = {
            'English': self._get_english_content(),
            'Chemistry': self._get_chemistry_content(),
            'Biology': self._get_biology_content(),
            'Geography': self._get_geography_content(),
            'Economics': self._get_economics_content(),
            'History': self._get_history_content(),
            'Literature': self._get_literature_content(),
            'Computer Science': self._get_computer_science_content()
        }

        for subject, content_list in subjects_content.items():
            self._write_subject_content(subject, content_list)
            print(f"✅ Created {len(content_list)} content items for {subject}")

    def populate_underrepresented_topics(self):
        """Add content for underrepresented topics in existing subjects"""

        underrepresented_content = {
            'Mathematics': self._get_mathematics_additional_topics(),
            'Physics': self._get_physics_additional_topics(),
            'Chemistry': self._get_chemistry_additional_topics()
        }

        for subject, content_list in underrepresented_content.items():
            self._write_subject_content(subject, content_list, append=True)
            print(f"✅ Added {len(content_list)} additional topics for {subject}")

    def _write_subject_content(self, subject, content_list, append=False):
        """Write content to CSV file"""

        template_file = self._find_template_file(subject)
        if not template_file:
            print(f"⚠️  No template found for {subject}")
            return

        mode = 'a' if append else 'w'
        file_exists = os.path.exists(template_file) and append

        with open(template_file, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header only if creating new file
            if not file_exists:
                writer.writerow([
                    'title', 'subject', 'topic', 'subtopic', 'content_type', 'difficulty',
                    'exam_board', 'content', 'summary', 'learning_objectives', 'key_concepts',
                    'worked_examples', 'important_formulas', 'common_mistakes', 'practice_problems',
                    'exam_tips', 'estimated_read_time', 'prerequisites', 'related_questions',
                    'tags', 'author', 'references', 'multimedia_links', 'cultural_notes'
                ])

            # Write content rows
            for content_item in content_list:
                writer.writerow([
                    content_item.get('title', ''),
                    content_item.get('subject', subject),
                    content_item.get('topic', ''),
                    content_item.get('subtopic', ''),
                    content_item.get('content_type', 'study_guide'),
                    content_item.get('difficulty', 'intermediate'),
                    content_item.get('exam_board', 'WAEC'),
                    content_item.get('content', ''),
                    content_item.get('summary', ''),
                    content_item.get('learning_objectives', ''),
                    content_item.get('key_concepts', ''),
                    content_item.get('worked_examples', ''),
                    content_item.get('important_formulas', ''),
                    content_item.get('common_mistakes', ''),
                    content_item.get('practice_problems', ''),
                    content_item.get('exam_tips', ''),
                    content_item.get('estimated_read_time', '20'),
                    content_item.get('prerequisites', ''),
                    content_item.get('related_questions', ''),
                    content_item.get('tags', ''),
                    content_item.get('author', 'Content Generator'),
                    content_item.get('references', ''),
                    content_item.get('multimedia_links', ''),
                    content_item.get('cultural_notes', '')
                ])

    def _find_template_file(self, subject):
        """Find the most recent template file for a subject"""

        if not os.path.exists(self.templates_dir):
            return None

        subject_lower = subject.lower()
        template_files = [f for f in os.listdir(self.templates_dir)
                         if f.startswith(f'content_template_{subject_lower}') and f.endswith('.csv')]

        if not template_files:
            return None

        # Return the most recent file
        template_files.sort(reverse=True)
        return os.path.join(self.templates_dir, template_files[0])

    def _get_english_content(self):
        """Generate comprehensive English content"""

        return [
            {
                'title': 'English Language Comprehension Skills',
                'subject': 'English',
                'topic': 'Comprehension',
                'subtopic': 'Reading Skills',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# English Language Comprehension Skills

## Introduction
Comprehension skills are essential for understanding written texts and answering questions effectively in examinations.

## Types of Comprehension Questions

### Literal Comprehension
Understanding information directly stated in the text.

**Example:** If a passage states "The meeting starts at 3 PM", a literal question would ask "What time does the meeting start?"

### Inferential Comprehension
Reading between the lines to understand implied meanings.

**Example:** If a passage describes someone as "quiet and thoughtful", you might infer they are intelligent.

### Evaluative Comprehension
Making judgments about the text's content, language, and effectiveness.

**Example:** Assessing whether an argument is convincing or identifying bias.

## Reading Strategies

### Previewing
- Read the title and headings
- Look at illustrations or diagrams
- Read the first and last paragraphs
- Note key vocabulary

### Active Reading
- Highlight main ideas
- Underline key terms
- Write marginal notes
- Ask questions about the text

### Skimming and Scanning
- Skim for general understanding
- Scan for specific information

## Common Question Types

### Multiple Choice Questions
- Read the question first
- Eliminate obviously wrong answers
- Look for key words that match the text

### Short Answer Questions
- Answer directly and concisely
- Use complete sentences
- Support answers with evidence from text

### Summary Questions
- Identify main points only
- Use your own words
- Keep to specified word limit

## Practice Passage

**The Impact of Technology on Education**

Technology has revolutionized education in Nigeria. With the advent of computers and the internet, students now have access to vast amounts of information. Online learning platforms allow flexible study schedules, and digital textbooks reduce the cost of education. However, challenges remain, including unreliable electricity and limited internet access in rural areas.

Despite these obstacles, technology continues to transform Nigerian education. Mobile learning apps provide interactive lessons, and video conferencing enables remote teaching. As infrastructure improves, technology will play an even greater role in democratizing education across the country.

## Practice Questions

1. What is the main idea of the passage?
2. What challenges does the author mention regarding technology in Nigerian education?
3. What benefits of technology are discussed?
4. How does the author feel about the future of technology in education?

## Exam Tips
- Read questions carefully before reading the passage
- Manage your time effectively
- Practice with past WAEC questions
- Focus on understanding rather than memorization''',
                'summary': 'Comprehensive guide to developing comprehension skills for English language examinations',
                'learning_objectives': 'Identify different types of comprehension questions,Apply effective reading strategies,Answer comprehension questions accurately',
                'key_concepts': 'Literal comprehension,Inferential comprehension,Evaluative comprehension,Reading strategies',
                'worked_examples': 'Analysis of sample passage with different question types',
                'practice_problems': 'Practice questions based on sample passage',
                'exam_tips': 'Time management,Question analysis,Practice techniques',
                'estimated_read_time': '25',
                'prerequisites': 'Basic reading skills',
                'tags': 'english,comprehension,reading skills,waec',
                'cultural_notes': 'Focus on Nigerian education system and technology adoption challenges'
            },
            {
                'title': 'English Grammar: Tenses and Their Usage',
                'subject': 'English',
                'topic': 'Grammar',
                'subtopic': 'Tenses',
                'content_type': 'reference',
                'difficulty': 'intermediate',
                'content': '''# English Grammar: Tenses and Their Usage

## Introduction
Tenses show the time of an action or state. Understanding tenses is crucial for clear communication.

## Present Tenses

### Simple Present
**Form:** Base form (I eat, He eats)
**Usage:** Facts, habits, routines, timetables
**Example:** "I study English every day."

### Present Continuous
**Form:** am/is/are + verb-ing
**Usage:** Actions happening now, temporary situations
**Example:** "I am studying English now."

### Present Perfect
**Form:** have/has + past participle
**Usage:** Experiences, completed actions with present relevance
**Example:** "I have studied English for five years."

## Past Tenses

### Simple Past
**Form:** Past form (ate, went)
**Usage:** Completed actions at specific times
**Example:** "I studied English yesterday."

### Past Continuous
**Form:** was/were + verb-ing
**Usage:** Actions in progress at specific times
**Example:** "I was studying when you called."

### Past Perfect
**Form:** had + past participle
**Usage:** Actions completed before other past actions
**Example:** "I had studied before the exam."

## Future Tenses

### Simple Future
**Form:** will + base form
**Usage:** Predictions, spontaneous decisions
**Example:** "I will study tomorrow."

### Future Continuous
**Form:** will be + verb-ing
**Usage:** Actions in progress at future times
**Example:** "I will be studying at 8 PM tomorrow."

### Future Perfect
**Form:** will have + past participle
**Usage:** Completed actions by future times
**Example:** "I will have studied for two hours by then."

## Common Mistakes
- Using simple present for future events
- Confusing past simple with present perfect
- Incorrect auxiliary verbs
- Spelling errors in -ing forms

## Nigerian Context
In Nigerian English, present continuous is often used for future arrangements: "I am going to Lagos next week."

## Practice Exercises
1. Complete: "Every day, I _____ (go) to school."
2. Change: "I ate breakfast." → Present perfect
3. Correct: "I will have finish my homework."''',
                'summary': 'Complete reference guide to English tenses with Nigerian usage examples',
                'learning_objectives': 'Identify different English tenses,Use tenses correctly in sentences,Avoid common tense errors',
                'key_concepts': 'Present tenses,Past tenses,Future tenses,Tense forms and usage',
                'important_formulas': 'Tense formation rules and patterns',
                'practice_problems': 'Tense identification and correction exercises',
                'cultural_notes': 'Nigerian English tense usage patterns and common variations'
            }
        ]

    def _get_chemistry_content(self):
        """Generate comprehensive Chemistry content"""

        return [
            {
                'title': 'Organic Chemistry: Hydrocarbons',
                'subject': 'Chemistry',
                'topic': 'Organic Chemistry',
                'subtopic': 'Hydrocarbons',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Organic Chemistry: Hydrocarbons

## Introduction
Hydrocarbons are organic compounds containing only carbon and hydrogen atoms. They are the simplest organic compounds and form the basis of organic chemistry.

## Classification of Hydrocarbons

### Aliphatic Hydrocarbons
- **Alkanes**: Saturated hydrocarbons (CₙH₂ₙ₊₂)
- **Alkenes**: Unsaturated hydrocarbons with double bonds (CₙH₂ₙ)
- **Alkynes**: Unsaturated hydrocarbons with triple bonds (CₙH₂ₙ₋₂)

### Aromatic Hydrocarbons
- Contain benzene ring structure
- General formula: C₆H₆ for benzene
- Examples: Benzene, toluene, xylene

## Alkanes

### Properties
- Saturated (single bonds only)
- General formula: CₙH₂ₙ₊₂
- Non-polar molecules
- Insoluble in water, soluble in organic solvents

### Reactions
- **Combustion**: Complete burning in oxygen
  CH₄ + 2O₂ → CO₂ + 2H₂O

- **Substitution**: Reaction with halogens
  CH₄ + Cl₂ → CH₃Cl + HCl (in sunlight)

### Isomerism
- Structural isomers: Same molecular formula, different structures
- Example: Butane (C₄H₁₀) has 2 isomers

## Alkenes

### Properties
- Contain carbon-carbon double bonds
- General formula: CₙH₂ₙ
- More reactive than alkanes
- Undergo addition reactions

### Reactions
- **Addition of Hydrogen**: Hydrogenation
  CH₂=CH₂ + H₂ → CH₃-CH₃

- **Addition of Halogens**: Halogenation
  CH₂=CH₂ + Br₂ → CH₂Br-CH₂Br

- **Addition of Water**: Hydration
  CH₂=CH₂ + H₂O → CH₃-CH₂OH (requires acid catalyst)

## Alkynes

### Properties
- Contain carbon-carbon triple bonds
- General formula: CₙH₂ₙ₋₂
- More reactive than alkenes
- First member: Acetylene (C₂H₂)

### Reactions
- **Addition reactions**: Similar to alkenes but can add twice
- **Combustion**: Very exothermic
  2C₂H₂ + 5O₂ → 4CO₂ + 2H₂O

## Aromatic Hydrocarbons

### Benzene (C₆H₆)
- Special stability due to delocalized electrons
- Undergoes substitution rather than addition reactions
- Kekulé structure shows alternating double bonds

### Reactions of Benzene
- **Nitration**: C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O
- **Sulphonation**: C₆H₆ + H₂SO₄ → C₆H₅SO₃H + H₂O
- **Halogenation**: C₆H₆ + Cl₂ → C₆H₅Cl + HCl

## Nigerian Applications
- Petroleum refining in Port Harcourt and Lagos
- Natural gas processing
- Petrochemical industry
- Fuel production for transportation

## Laboratory Preparation
- Alkanes: Reduction of alkyl halides
- Alkenes: Dehydration of alcohols, dehydrohalogenation
- Alkynes: Action of water on carbides

## Common Mistakes
- Confusing general formulas
- Incorrect naming of isomers
- Forgetting reaction conditions
- Mixing up addition vs substitution reactions

## Practice Problems
1. Name the first four alkanes and give their formulas
2. Write the structural formula of ethene and ethyne
3. Explain why alkenes undergo addition reactions
4. Describe the laboratory preparation of ethene
5. What is the difference between aliphatic and aromatic hydrocarbons?''',
                'summary': 'Comprehensive guide to hydrocarbons covering alkanes, alkenes, alkynes, and aromatic compounds',
                'learning_objectives': 'Classify hydrocarbons,Understand properties and reactions,Apply knowledge to Nigerian petroleum industry',
                'key_concepts': 'Alkanes,Alkenes,Alkynes,Aromatic hydrocarbons,Hydrocarbon reactions',
                'important_formulas': 'General formulas: Alkanes CₙH₂ₙ₊₂, Alkenes CₙH₂ₙ, Alkynes CₙH₂ₙ₋₂',
                'worked_examples': 'Combustion reactions,Halogenation reactions,Hydrogenation reactions',
                'practice_problems': 'Hydrocarbon naming,Reaction prediction,Structural formulas',
                'cultural_notes': 'Nigerian petroleum industry applications and petrochemical significance'
            },
            {
                'title': 'Physical Chemistry: Chemical Kinetics',
                'subject': 'Chemistry',
                'topic': 'Physical Chemistry',
                'subtopic': 'Chemical Kinetics',
                'content_type': 'study_guide',
                'difficulty': 'advanced',
                'content': '''# Physical Chemistry: Chemical Kinetics

## Introduction
Chemical kinetics is the study of reaction rates and the factors that affect them. Understanding reaction rates is crucial for industrial processes and chemical analysis.

## Rate of Reaction
The rate of reaction is the change in concentration of reactants or products per unit time.

**Average Rate:** Total change over a period of time
**Instantaneous Rate:** Rate at a particular moment

### Units
- Rate = concentration/time
- Common units: mol dm⁻³ s⁻¹, mol L⁻¹ s⁻¹

## Factors Affecting Reaction Rates

### Concentration
- Rate ∝ [Reactants] for most reactions
- Rate = k[A]ⁿ[B]ᵐ (rate law)
- Order of reaction: n + m

### Temperature
- Rate doubles/triples for every 10°C rise (Rule of Thumb)
- Arrhenius equation: k = Ae^(-Ea/RT)
- Activation energy (Ea) determines temperature sensitivity

### Catalyst
- Increases reaction rate without being consumed
- Lowers activation energy
- Provides alternative reaction pathway

### Surface Area
- Larger surface area = faster reaction
- Important for heterogeneous reactions
- Particle size affects reaction rate

### Pressure
- Affects gaseous reactions
- Rate increases with pressure for reactions producing fewer gas molecules

## Order of Reaction

### Zero Order
- Rate = k (independent of concentration)
- Example: Decomposition on metal surfaces

### First Order
- Rate = k[A]
- Half-life constant: t½ = 0.693/k
- Examples: Radioactive decay, hydrolysis

### Second Order
- Rate = k[A]² or k[A][B]
- Half-life depends on initial concentration
- Examples: Alkaline hydrolysis of esters

## Rate Laws and Rate Constants

### Differential Rate Law
Expresses rate in terms of concentration derivatives

### Integrated Rate Law
Expresses concentration as function of time

### Zero Order: [A] = [A]₀ - kt
### First Order: ln[A] = ln[A]₀ - kt
### Second Order: 1/[A] = 1/[A]₀ + kt

## Activation Energy
- Minimum energy required for reaction
- Determined from Arrhenius plot: ln k vs 1/T
- Slope = -Ea/R

## Reaction Mechanisms
- Series of elementary steps
- Rate-determining step controls overall rate
- Molecularity vs order of reaction

## Nigerian Industrial Applications
- Petroleum refining reaction rates
- Cement manufacturing kinetics
- Food processing and preservation
- Pharmaceutical production timing
- Fertilizer manufacturing processes

## Experimental Methods
- Colorimetry for concentration measurement
- Gas collection for gaseous products
- Titration methods
- Conductivity measurements

## Common Mistakes
- Confusing order with molecularity
- Incorrect units for rate constants
- Misapplying integrated rate laws
- Forgetting temperature effects

## Practice Problems
1. For a first-order reaction, calculate half-life if k = 0.02 s⁻¹
2. Determine order of reaction from given rate data
3. Calculate activation energy from rate constants at two temperatures
4. Explain effect of catalyst on reaction rate
5. Derive integrated rate law for second-order reaction''',
                'summary': 'Comprehensive study of chemical kinetics including rates, orders, and mechanisms',
                'learning_objectives': 'Calculate reaction rates,Determine reaction orders,Understand factors affecting rates,Apply kinetics to industrial processes',
                'key_concepts': 'Reaction rates,Rate laws,Order of reaction,Activation energy,Reaction mechanisms',
                'important_formulas': 'Rate = k[A]ⁿ,Arrhenius equation: k = Ae^(-Ea/RT),Half-life equations',
                'worked_examples': 'Rate calculation,Order determination,Activation energy calculation',
                'practice_problems': 'Rate law problems,Half-life calculations,Mechanisms analysis',
                'cultural_notes': 'Applications in Nigerian petroleum, cement, and pharmaceutical industries'
            }
        ]

    def _get_biology_content(self):
        """Generate comprehensive Biology content"""

        return [
            {
                'title': 'Cell Biology: Structure and Function',
                'subject': 'Biology',
                'topic': 'Cell Biology',
                'subtopic': 'Cell Structure',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Cell Biology: Structure and Function

## Introduction
The cell is the basic unit of life. Understanding cell structure and function is fundamental to biology.

## Cell Theory
1. All living organisms are composed of cells
2. The cell is the basic unit of life
3. All cells arise from pre-existing cells

## Types of Cells

### Prokaryotic Cells
- No membrane-bound nucleus
- Smaller size (1-10 μm)
- Examples: Bacteria, Archaea
- Genetic material in nucleoid region

### Eukaryotic Cells
- Membrane-bound nucleus
- Larger size (10-100 μm)
- Examples: Plants, animals, fungi, protists
- Complex internal organization

## Cell Membrane (Plasma Membrane)

### Structure
- Phospholipid bilayer
- Proteins embedded in bilayer
- Cholesterol for fluidity
- Glycoproteins and glycolipids on surface

### Functions
- Selective permeability
- Cell recognition
- Cell signaling
- Protection

### Fluid Mosaic Model
- Membrane is fluid (components can move)
- Mosaic of different components
- Proposed by Singer and Nicolson

## Nucleus

### Structure
- Double membrane envelope
- Nuclear pores for communication
- Nucleolus (rRNA synthesis)
- Chromatin (DNA + proteins)

### Functions
- Control center of cell
- DNA replication and transcription
- Ribosome synthesis
- Cell division control

## Mitochondria

### Structure
- Double membrane
- Inner membrane forms cristae
- Matrix contains enzymes
- Own circular DNA

### Functions
- Cellular respiration
- ATP production
- Energy conversion
- Calcium storage

## Endoplasmic Reticulum (ER)

### Rough ER
- Ribosomes attached
- Protein synthesis and modification
- Membrane production

### Smooth ER
- No ribosomes
- Lipid synthesis
- Detoxification
- Calcium storage

## Golgi Apparatus
- Modifies and packages proteins
- Forms lysosomes
- Transports materials
- Produces secretory vesicles

## Lysosomes
- Contain hydrolytic enzymes
- Digest macromolecules
- Recycle cellular components
- Destroy pathogens

## Vacuoles
- Storage organelles
- Maintain turgor pressure (plants)
- Isolate harmful substances
- Store nutrients

## Cell Wall (Plants)
- Made of cellulose
- Provides structural support
- Protects against mechanical damage
- Prevents excessive water uptake

## Chloroplasts (Plants)
- Site of photosynthesis
- Contain chlorophyll
- Double membrane
- Thylakoids and stroma

## Comparison: Plant vs Animal Cells

| Feature | Plant Cell | Animal Cell |
|---------|------------|-------------|
| Cell Wall | Present | Absent |
| Chloroplasts | Present | Absent |
| Large Vacuole | Present | Small/absent |
| Centrioles | Absent | Present |
| Shape | Fixed | Irregular |

## Nigerian Context
- Malaria parasite affects red blood cells
- Agricultural research on plant cell structure
- Biotechnology applications in Lagos and Ibadan
- Traditional medicine uses plant cell components

## Microscopy
- Light microscope: 1000x magnification
- Electron microscope: 100,000x magnification
- Scanning vs Transmission electron microscopy

## Common Mistakes
- Confusing prokaryotic and eukaryotic cells
- Misidentifying organelles
- Forgetting plant-specific features
- Incorrect membrane structure description

## Practice Questions
1. Compare prokaryotic and eukaryotic cells
2. Describe the structure and function of mitochondria
3. Explain the fluid mosaic model
4. What are the differences between rough and smooth ER?
5. Why do plant cells have cell walls while animal cells do not?''',
                'summary': 'Comprehensive guide to cell structure and function covering organelles and cell types',
                'learning_objectives': 'Identify cell organelles,Compare cell types,Understand organelle functions,Apply knowledge to Nigerian biological research',
                'key_concepts': 'Cell theory,Prokaryotic cells,Eukaryotic cells,Cell organelles,Plant vs animal cells',
                'worked_examples': 'Cell structure identification,Organelle function analysis,Cell type comparison',
                'practice_problems': 'Organelle identification,Cell comparison,Function analysis',
                'cultural_notes': 'Malaria research,Plant biotechnology,Agricultural applications in Nigeria'
            },
            {
                'title': 'Ecology: Ecosystems and Interactions',
                'subject': 'Biology',
                'topic': 'Ecology',
                'subtopic': 'Ecosystems',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Ecology: Ecosystems and Interactions

## Introduction
Ecology is the study of organisms and their interactions with the environment. Ecosystems are communities of living organisms interacting with their physical environment.

## Levels of Ecological Organization

### Individual
- Single organism
- Physiological processes
- Behavioral adaptations

### Population
- Group of same species in area
- Population size and density
- Growth patterns

### Community
- All populations in area
- Interspecific interactions
- Species diversity

### Ecosystem
- Community + abiotic factors
- Energy flow and nutrient cycling
- Trophic levels

### Biosphere
- All ecosystems on Earth
- Global ecological processes

## Components of Ecosystem

### Biotic Components
- Producers (autotrophs)
- Consumers (heterotrophs)
- Decomposers (saprotrophs)

### Abiotic Components
- Light, temperature, water
- Soil, air, minerals
- Topography, climate

## Energy Flow in Ecosystems

### Food Chains
- Linear sequence of organisms
- Transfer of energy
- Trophic levels

### Food Webs
- Complex network of food chains
- More realistic representation
- Energy pathways

### Trophic Levels
1. **Producers**: Green plants, algae
2. **Primary Consumers**: Herbivores
3. **Secondary Consumers**: Carnivores
4. **Tertiary Consumers**: Top carnivores
5. **Decomposers**: Bacteria, fungi

## Ecological Pyramids

### Pyramid of Numbers
- Number of organisms at each level
- Usually pyramid-shaped
- Exceptions: Parasitic food chains

### Pyramid of Biomass
- Dry weight of organisms
- More accurate than numbers
- Always pyramid-shaped

### Pyramid of Energy
- Energy content at each level
- Always pyramid-shaped
- Shows energy loss (10% rule)

## Nutrient Cycling

### Carbon Cycle
- Photosynthesis and respiration
- Combustion and decomposition
- Oceanic absorption

### Nitrogen Cycle
- Nitrogen fixation
- Nitrification and denitrification
- Ammonification

### Water Cycle
- Evaporation and transpiration
- Condensation and precipitation
- Surface and groundwater flow

## Population Ecology

### Population Growth
- **Exponential Growth**: J-shaped curve
- **Logistic Growth**: S-shaped curve
- Carrying capacity

### Population Regulation
- Density-dependent factors
- Density-independent factors
- r and K strategists

## Nigerian Ecosystems

### Savanna Ecosystem
- Dominant in northern Nigeria
- Grasses, acacia trees
- Large herbivores (elephants, antelopes)
- Seasonal rainfall patterns

### Rainforest Ecosystem
- Niger Delta region
- High biodiversity
- Tropical climate
- Threatened by deforestation

### Freshwater Ecosystems
- Rivers: Niger, Benue, Cross River
- Lakes and wetlands
- Aquatic biodiversity
- Fishing industry importance

### Marine Ecosystems
- Atlantic coast
- Mangrove forests
- Coral reefs
- Fisheries and tourism

## Human Impact on Ecosystems

### Deforestation
- Loss of biodiversity
- Soil erosion
- Climate change contribution

### Pollution
- Water pollution in Niger Delta
- Air pollution in urban areas
- Plastic waste in oceans

### Overfishing
- Depletion of fish stocks
- Impact on coastal communities
- Need for sustainable practices

## Conservation Strategies

### Protected Areas
- National parks and reserves
- Biodiversity conservation
- Ecotourism development

### Sustainable Practices
- Agroforestry
- Sustainable fishing
- Waste management

### Environmental Education
- School programs
- Community awareness
- Policy development

## Common Mistakes
- Confusing food chains and food webs
- Misunderstanding energy flow
- Incorrect pyramid interpretations
- Forgetting Nigerian ecosystem examples

## Practice Questions
1. Explain the difference between a food chain and a food web
2. Describe the energy flow in an ecosystem
3. What are the main components of the nitrogen cycle?
4. Explain why ecological pyramids narrow towards the top
5. Describe a Nigerian ecosystem and its characteristics''',
                'summary': 'Comprehensive study of ecosystems, energy flow, nutrient cycling, and Nigerian ecological systems',
                'learning_objectives': 'Understand ecological organization,Explain energy flow and nutrient cycling,Analyze Nigerian ecosystems,Identify human impacts and conservation strategies',
                'key_concepts': 'Ecosystems,Energy flow,Nutrient cycling,Population ecology,Nigerian ecosystems',
                'worked_examples': 'Food web construction,Ecological pyramid analysis,Nutrient cycle diagrams',
                'practice_problems': 'Energy flow calculations,Ecosystem analysis,Nigerian conservation case studies',
                'cultural_notes': 'Nigerian savanna, rainforest, and marine ecosystems; impacts of oil industry and deforestation'
            }
        ]

    def _get_geography_content(self):
        """Generate comprehensive Geography content"""

        return [
            {
                'title': 'Physical Geography: Weather and Climate',
                'subject': 'Geography',
                'topic': 'Physical Geography',
                'subtopic': 'Weather and Climate',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Physical Geography: Weather and Climate

## Introduction
Weather and climate are fundamental concepts in geography. Weather is the atmospheric conditions at a specific time and place, while climate is the long-term average weather pattern.

## Elements of Weather

### Temperature
- Measure of hotness/coldness
- Measured in Celsius (°C) or Fahrenheit (°F)
- Controls evaporation and condensation
- Affects human comfort and activities

### Precipitation
- Water falling from atmosphere
- Types: Rain, snow, hail, sleet, dew
- Measured by rain gauge
- Essential for agriculture

### Humidity
- Amount of water vapor in air
- Relative humidity: Percentage of saturation
- Absolute humidity: Mass of water vapor per unit volume
- Affects comfort and weather patterns

### Wind
- Movement of air from high to low pressure
- Measured by anemometer
- Direction measured by wind vane
- Influences temperature and precipitation

### Atmospheric Pressure
- Weight of air above
- Measured in millibars (mb) or hectopascals (hPa)
- High pressure: Fair weather
- Low pressure: Stormy weather

## Weather Instruments

### Thermometer
- Measures temperature
- Mercury or alcohol based
- Maximum and minimum thermometers

### Barometer
- Measures atmospheric pressure
- Mercury or aneroid types
- Predicts weather changes

### Hygrometer
- Measures humidity
- Wet and dry bulb hygrometer
- Hair hygrometer

### Rain Gauge
- Measures precipitation
- Tipping bucket or funnel types
- Records rainfall amount

## Climate Classification

### Tropical Climate
- High temperatures year-round
- Heavy rainfall
- Located near equator
- Nigeria: Tropical rainforest and savanna

### Temperate Climate
- Four distinct seasons
- Moderate temperatures
- Adequate rainfall
- Found in middle latitudes

### Desert Climate
- Very low precipitation
- Extreme temperature variations
- Located in subtropical regions
- Nigeria: Northern parts (Sahara influence)

### Mediterranean Climate
- Hot, dry summers
- Mild, wet winters
- Found near large water bodies

## Nigerian Climate

### Tropical Rainforest Climate (South)
- Annual rainfall: 2000-3000mm
- Temperature: 25-32°C
- Double maxima rainfall
- High humidity and cloud cover

### Guinea Savanna Climate (Middle Belt)
- Annual rainfall: 1000-1500mm
- Temperature: 24-31°C
- Single rainfall maximum
- Longer dry season

### Sudan Savanna Climate (North)
- Annual rainfall: 500-1000mm
- Temperature: 25-35°C
- Short rainy season
- Long dry season

### Sahel Climate (Extreme North)
- Annual rainfall: <500mm
- Temperature: 20-40°C
- Very short rainy season
- Desertification prone

## Weather Forecasting

### Methods
- Satellite imagery
- Weather radar
- Weather balloons
- Computer models

### Nigerian Weather Services
- Nigerian Meteorological Agency (NIMET)
- Provides weather forecasts
- Issues warnings for severe weather
- Climate data collection

## Climate Change and Nigeria

### Impacts
- Rising temperatures
- Changing rainfall patterns
- Sea level rise (coastal areas)
- Increased extreme weather events

### Adaptation Strategies
- Improved irrigation systems
- Drought-resistant crops
- Climate-smart agriculture
- Coastal protection measures

## Common Mistakes
- Confusing weather and climate
- Incorrect temperature conversions
- Misunderstanding pressure systems
- Forgetting Nigerian climate variations

## Practice Questions
1. Explain the difference between weather and climate
2. Describe the main elements of weather
3. What weather instruments are used to measure temperature?
4. Describe the climate of your local area in Nigeria
5. How does climate change affect Nigeria?

## Fieldwork Activities
- Setting up a weather station
- Recording weather data over a week
- Analyzing weather maps
- Studying local climate patterns''',
                'summary': 'Comprehensive guide to weather elements, climate classification, and Nigerian weather patterns',
                'learning_objectives': 'Identify weather elements,Understand climate classification,Analyze Nigerian climate zones,Apply weather forecasting knowledge',
                'key_concepts': 'Weather elements,Climate classification,Nigerian climate zones,Weather instruments,Climate change',
                'worked_examples': 'Weather data analysis,Climate zone identification,Nigerian weather pattern studies',
                'practice_problems': 'Weather instrument usage,Climate data interpretation,Nigerian climate analysis',
                'cultural_notes': 'Nigerian Meteorological Agency,Climate change impacts on agriculture and coastal communities'
            }
        ]

    def _get_economics_content(self):
        """Generate comprehensive Economics content"""

        return [
            {
                'title': 'Microeconomics: Demand and Supply',
                'subject': 'Economics',
                'topic': 'Microeconomics',
                'subtopic': 'Demand and Supply',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Microeconomics: Demand and Supply

## Introduction
Demand and supply are fundamental concepts in economics. They determine prices and quantities in markets and explain how markets work.

## Theory of Demand

### Definition
Demand is the quantity of a good or service that consumers are willing and able to buy at various prices during a given period of time.

### Law of Demand
- Inverse relationship between price and quantity demanded
- As price increases, quantity demanded decreases (ceteris paribus)
- As price decreases, quantity demanded increases

### Demand Schedule
- Tabular representation of demand
- Shows quantity demanded at different prices

### Demand Curve
- Graphical representation of demand
- Downward sloping curve
- Shows inverse relationship

## Factors Affecting Demand

### Price of the Commodity
- Law of demand applies

### Income of Consumers
- **Normal Goods**: Demand increases with income
- **Inferior Goods**: Demand decreases with income

### Prices of Related Goods
- **Substitute Goods**: Price increase of one increases demand for the other
- **Complementary Goods**: Price increase of one decreases demand for the other

### Tastes and Preferences
- Changes in consumer preferences
- Advertising and marketing
- Cultural factors

### Number of Consumers
- Population growth
- Market size expansion

### Expectation of Future Prices
- If price expected to rise, current demand increases
- If price expected to fall, current demand decreases

## Theory of Supply

### Definition
Supply is the quantity of a good or service that producers are willing and able to offer for sale at various prices during a given period of time.

### Law of Supply
- Direct relationship between price and quantity supplied
- As price increases, quantity supplied increases
- As price decreases, quantity supplied decreases

### Supply Schedule
- Tabular representation of supply
- Shows quantity supplied at different prices

### Supply Curve
- Graphical representation of supply
- Upward sloping curve
- Shows direct relationship

## Factors Affecting Supply

### Price of the Commodity
- Law of supply applies

### Cost of Production
- Input prices (labor, raw materials)
- Technology improvements
- Taxes and subsidies

### Number of Producers
- Entry of new firms increases supply
- Exit of firms decreases supply

### Technology
- Technological improvements increase supply
- Reduce production costs

### Government Policies
- Taxes increase costs, decrease supply
- Subsidies decrease costs, increase supply

### Weather and Natural Conditions
- Important for agricultural products
- Natural disasters affect supply

## Market Equilibrium

### Definition
Equilibrium is the point where demand equals supply.

### Equilibrium Price
- Price at which quantity demanded = quantity supplied
- Also called market-clearing price

### Equilibrium Quantity
- Quantity bought and sold at equilibrium price

### Effects of Changes
- **Increase in Demand**: Price and quantity increase
- **Decrease in Demand**: Price and quantity decrease
- **Increase in Supply**: Price decreases, quantity increases
- **Decrease in Supply**: Price increases, quantity decreases

## Nigerian Economic Applications

### Agricultural Markets
- Cocoa, palm oil, cassava markets
- Seasonal supply variations
- Government intervention through marketing boards

### Petroleum Products
- PMS (petrol), diesel, kerosene
- Government subsidies and pricing
- Supply constraints and distribution

### Foreign Exchange Market
- Naira-dollar exchange rates
- Demand for imports, supply of exports
- Central Bank interventions

### Labor Market
- Supply of skilled labor
- Demand for various professions
- Wage determination

## Price Controls

### Price Ceiling
- Maximum price set by government
- Below equilibrium price
- Leads to shortages
- Examples: Rent controls, essential commodities

### Price Floor
- Minimum price set by government
- Above equilibrium price
- Leads to surpluses
- Examples: Minimum wage, agricultural products

## Elasticity

### Price Elasticity of Demand
- Measures responsiveness of quantity demanded to price changes
- Formula: %ΔQd / %ΔP

### Types
- **Elastic**: > 1
- **Inelastic**: < 1
- **Unit Elastic**: = 1

## Common Mistakes
- Confusing movements along vs shifts of curves
- Forgetting ceteris paribus assumption
- Misunderstanding equilibrium changes
- Incorrect elasticity calculations

## Practice Problems
1. Draw a demand curve and explain the law of demand
2. Explain factors that can cause a shift in the demand curve
3. What happens to equilibrium price and quantity when demand increases?
4. Calculate price elasticity of demand given: P=100→80, Q=200→300
5. Explain how price controls work in Nigerian markets

## Nigerian Case Studies
- Petroleum subsidy removal effects
- Cocoa price stabilization
- Rice import ban impacts
- Foreign exchange market reforms''',
                'summary': 'Comprehensive guide to demand and supply theory with Nigerian economic applications',
                'learning_objectives': 'Understand demand and supply laws,Analyze market equilibrium,Apply concepts to Nigerian markets,Explain government interventions',
                'key_concepts': 'Demand theory,Supply theory,Market equilibrium,Elasticity,Price controls',
                'important_formulas': 'Price elasticity = %ΔQ/%ΔP,Equilibrium: Qd = Qs',
                'worked_examples': 'Equilibrium analysis,Elasticity calculations,Nigerian market examples',
                'practice_problems': 'Curve analysis,Equilibrium changes,Elasticity problems,Nigerian case studies',
                'cultural_notes': 'Nigerian agricultural markets,Petroleum pricing,Foreign exchange management,Labor market dynamics'
            }
        ]

    def _get_history_content(self):
        """Generate comprehensive History content"""

        return [
            {
                'title': 'Nigerian History: Pre-Colonial Era',
                'subject': 'History',
                'topic': 'Nigerian History',
                'subtopic': 'Pre-Colonial Era',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Nigerian History: Pre-Colonial Era

## Introduction
Nigeria's pre-colonial history spans thousands of years, featuring diverse kingdoms, empires, and societies with rich cultural, political, and economic systems.

## Early Settlements and Societies

### Nok Culture (500 BC - 200 AD)
- Located in northern Nigeria
- Known for terracotta sculptures
- Iron working technology
- Agricultural society
- First evidence of organized society

### Igbo Ukwu Civilization (9th Century AD)
- Located in southeastern Nigeria
- Advanced bronze casting
- Complex burial practices
- Evidence of social stratification
- Trade connections with North Africa

## Major Kingdoms and Empires

### Kanem-Borno Empire (9th - 19th Century)
- Located in northeastern Nigeria
- Founded around Lake Chad
- Islamic influence from 11th century
- Military expansion under Dunama Dibbalemi
- Trade in salt, slaves, and horses
- Capital: Ngazargamu

### Oyo Empire (17th - 19th Century)
- Located in southwestern Nigeria
- Yoruba kingdom
- Centralized administration
- Cavalry-based military
- Trade with Europeans
- Alaafin (king) system

### Benin Kingdom (13th - 19th Century)
- Located in southern Nigeria
- Edo people
- Famous for bronze casting
- Centralized monarchy
- Trade with Portuguese
- Obas (kings) with extensive power

### Sokoto Caliphate (19th Century)
- Founded by Usman dan Fodio
- Islamic reform movement
- Covered northern Nigeria
- Administrative divisions (emirs)
- Islamic education system
- Trade networks

## Igbo Societies

### Decentralized Political System
- No centralized kingship
- Village-based governance
- Age-grade systems
- Democratic decision-making
- Title societies (Ozo, Nze)

### Economic Systems
- Agricultural economy
- Craft specialization
- Long-distance trade
- Market systems (Nkwo, Eke, Orie, Afor)
- Currency systems (manillas, cowries)

### Social Organization
- Extended family system
- Patrilineal descent
- Marriage customs
- Religious practices
- Art and cultural expressions

## Hausa-Fulani Societies

### City-States
- Kano, Katsina, Zazzau, Gobir
- Agricultural and trading centers
- Islamic scholarship
- Craft industries
- Market systems

### Political Systems
- Sarkin (king) system
- Council of elders
- Islamic legal system
- Administrative bureaucracy
- Military organization

## Southern Nigeria Societies

### Niger Delta Region
- Fishing and trading communities
- Canoe-based transportation
- Salt production
- Palm oil trade
- European contact from 15th century

### Yoruba Kingdoms
- Ife, Oyo, Benin, Ijebu
- Centralized monarchies
- Military expansion
- Trade networks
- Cultural achievements

## Economic Systems

### Agriculture
- Root crops (yam, cassava)
- Grain crops (millet, sorghum)
- Tree crops (oil palm, kolanut)
- Irrigation systems
- Seasonal farming

### Trade Networks
- Trans-Saharan trade
- Coastal trade
- Regional markets
- Currency systems
- Specialization and exchange

### Craft Industries
- Iron working
- Textile production
- Leather work
- Pottery and ceramics
- Wood carving

## Social and Cultural Systems

### Religion and Beliefs
- Indigenous religions
- Ancestor worship
- Nature spirits
- Divination practices
- Healing traditions

### Education Systems
- Apprenticeship training
- Oral traditions
- Islamic education (North)
- Initiation ceremonies
- Cultural preservation

### Art and Architecture
- Nok terracotta
- Benin bronzes
- Yoruba sculpture
- Hausa architecture
- Igbo masks and figures

## European Contact (15th - 19th Century)

### Portuguese Arrival (1472)
- First European contact
- Trade in gold, ivory, pepper
- Introduction of firearms
- Cultural exchange

### Atlantic Slave Trade (16th - 19th Century)
- Major impact on coastal societies
- Economic disruption
- Social changes
- Resistance movements

### Legitimate Trade (19th Century)
- Palm oil, palm kernels
- Groundnuts, cotton
- Timber, rubber
- Economic transformation

## Resistance to Colonialism

### Northern Resistance
- Sokoto Caliphate wars
- Mahdi movement
- Islamic reform movements
- Anti-colonial struggles

### Southern Resistance
- Ekumeku movement (Niger Delta)
- Aba Women's War (1929)
- Tax protests
- Cultural preservation

## Legacy and Continuity

### Cultural Preservation
- Traditional institutions
- Language maintenance
- Religious practices
- Art forms

### Modern Relevance
- Federal structure roots
- Regional diversity
- Cultural pluralism
- National identity formation

## Common Mistakes
- Oversimplifying complex societies
- Ignoring regional diversity
- Confusing kingdoms with modern states
- Underestimating technological achievements

## Practice Questions
1. Describe the major kingdoms in pre-colonial Nigeria
2. Explain the economic systems of pre-colonial societies
3. How did the slave trade affect Nigerian societies?
4. Compare the political systems of the Yoruba and Igbo
5. What evidence shows the technological advancement of pre-colonial Nigeria?

## Primary Sources
- Oral traditions
- Arabic manuscripts
- European travel accounts
- Archaeological evidence
- Linguistic studies''',
                'summary': 'Comprehensive study of pre-colonial Nigerian societies, kingdoms, and cultural achievements',
                'learning_objectives': 'Identify major Nigerian kingdoms,Understand pre-colonial economic systems,Analyze social and political organizations,Explain European contact effects',
                'key_concepts': 'Nigerian kingdoms,Pre-colonial societies,Economic systems,Social organization,European contact',
                'worked_examples': 'Kingdom analysis,Economic system comparison,Social structure studies',
                'practice_problems': 'Kingdom identification,Economic analysis,Societal comparison,European impact assessment',
                'cultural_notes': 'Diversity of Nigerian ethnic groups,Traditional institutions,Artistic achievements,Resistance to colonialism'
            }
        ]

    def _get_literature_content(self):
        """Generate comprehensive Literature content"""

        return [
            {
                'title': 'African Literature: Themes and Techniques',
                'subject': 'Literature',
                'topic': 'African Literature',
                'subtopic': 'Themes and Techniques',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# African Literature: Themes and Techniques

## Introduction
African literature encompasses diverse voices, languages, and traditions. It reflects the continent's history, cultures, and contemporary experiences.

## Historical Development

### Oral Literature
- Griots (West Africa) - storytellers and historians
- Proverbs, riddles, and folktales
- Epic narratives and praise poems
- Passed down through generations

### Colonial Period Literature
- Early African writers in European languages
- Themes of cultural conflict and identity
- Chinua Achebe, Wole Soyinka, Ngũgĩ wa Thiong'o
- Resistance to colonial narratives

### Post-Colonial Literature
- Independence and nation-building themes
- African diaspora literature
- Women's voices and perspectives
- Contemporary social issues

## Major Themes

### Identity and Cultural Conflict
- Clash between traditional and modern values
- Search for authentic African identity
- Hybrid cultural identities
- Language and expression issues

### Colonialism and Its Legacy
- Impact of European colonization
- Resistance and liberation struggles
- Post-colonial disillusionment
- Neo-colonialism critiques

### Social and Political Issues
- Corruption and governance
- Poverty and inequality
- Gender relations and patriarchy
- Environmental concerns

### Family and Community
- Extended family systems
- Generational conflicts
- Community obligations
- Urban-rural divides

### Spirituality and Tradition
- Indigenous belief systems
- Syncretism with Christianity/Islam
- Ancestor communication
- Mystical and supernatural elements

## Literary Techniques

### Oral Traditions in Written Form
- Call-and-response patterns
- Repetition and rhythm
- Proverbs and wise sayings
- Song and music integration

### Language and Style
- Code-switching and multilingualism
- Pidgin and creole usage
- African proverbs and imagery
- Oral narrative structures

### Symbolism and Imagery
- Nature symbolism
- Animal imagery
- Color symbolism
- Cultural metaphors

### Narrative Techniques
- Multiple perspectives
- Non-linear storytelling
- Magical realism
- Oral history integration

## Key Authors and Works

### Chinua Achebe (Nigeria)
- **Things Fall Apart** (1958)
- **Arrow of God** (1964)
- **Anthills of the Savannah** (1987)
- Themes: Cultural collision, colonialism, tradition vs modernity

### Wole Soyinka (Nigeria)
- **The Lion and the Jewel** (1959)
- **Death and the King's Horseman** (1975)
- Nobel Prize in Literature (1986)
- Themes: Cultural identity, political satire, Yoruba mythology

### Ngũgĩ wa Thiong'o (Kenya)
- **Weep Not, Child** (1964)
- **Petals of Blood** (1977)
- **Decolonising the Mind** (1986)
- Themes: Anti-colonial struggle, social justice, language politics

### Chimamanda Ngozi Adichie (Nigeria)
- **Half of a Yellow Sun** (2006)
- **Americanah** (2013)
- **We Should All Be Feminists** (2014)
- Themes: Gender, race, identity, Nigerian civil war

## Nigerian Literature Focus

### Early Nigerian Writers
- Amos Tutuola: Palm-wine Drinkard (1952)
- Cyprian Ekwensi: People of the City (1954)
- Chinua Achebe: First modern Nigerian novelist

### Contemporary Nigerian Authors
- Chimamanda Ngozi Adichie
- Wole Soyinka
- Ben Okri: The Famished Road (1991)
- Helon Habila: Waiting for an Angel (2002)

### Oral Literature Traditions
- Hausa: Katsina and Kano storytelling
- Yoruba: Ifá divination poetry
- Igbo: Folk tales and proverbs
- Efik: Leopard society narratives

## Literary Criticism and Analysis

### Approaches to African Literature
- Cultural nationalism
- Marxist criticism
- Feminist perspectives
- Postcolonial theory
- Orality-literacy continuum

### Themes Analysis
- Cultural conflict resolution
- Political allegory
- Social commentary
- Psychological realism
- Magical elements

## Language and Translation Issues

### Language Choices
- European languages vs indigenous languages
- Code-switching in narratives
- Pidgin and vernacular literature
- Translation challenges

### Ngũgĩ's Language Debate
- Writing in African languages
- Gikuyu novels
- Language and cultural identity
- Accessibility issues

## Contemporary Trends

### Afropolitan Literature
- Global African identities
- Transnational experiences
- Urban narratives
- Technology and modernity

### Women's Voices
- Gender inequality themes
- Female perspectives
- Body politics
- Intersectional identities

### Young Adult Literature
- Coming-of-age stories
- Educational themes
- Contemporary issues
- Accessible narratives

## Common Mistakes
- Treating African literature as monolithic
- Ignoring oral traditions
- Overemphasizing colonial influences
- Neglecting contemporary works

## Practice Activities
1. Compare oral and written African literature
2. Analyze themes in Things Fall Apart
3. Discuss language choices in African novels
4. Examine gender representations in African literature
5. Explore contemporary African literary trends

## Nigerian Literary Festivals
- Lagos International Poetry Festival
- Ake Arts and Book Festival
- Port Harcourt Book Festival
- Nigerian Writers Series

## Resources
- African Writers Trust
- Nigerian Academy of Letters
- Online literary journals
- University literature departments''',
                'summary': 'Comprehensive study of African literature with focus on Nigerian authors, themes, and literary techniques',
                'learning_objectives': 'Identify major African literary works,Analyze themes and techniques,Understand cultural contexts,Appreciate Nigerian literary contributions',
                'key_concepts': 'African literature themes,Oral traditions,Literary techniques,Nigerian authors,Postcolonial literature',
                'worked_examples': 'Literary analysis,Theme identification,Technique examination,Author comparisons',
                'practice_problems': 'Text analysis,Comparative studies,Theme exploration,Author research',
                'cultural_notes': 'Nigerian literary festivals,Oral storytelling traditions,African diaspora literature,Language debates'
            }
        ]

    def _get_computer_science_content(self):
        """Generate comprehensive Computer Science content"""

        return [
            {
                'title': 'Programming Fundamentals: Python Basics',
                'subject': 'Computer Science',
                'topic': 'Programming',
                'subtopic': 'Python Basics',
                'content_type': 'tutorial',
                'difficulty': 'intermediate',
                'content': '''# Programming Fundamentals: Python Basics

## Introduction
Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in web development, data science, automation, and more.

## Setting Up Python Environment

### Installation
- Download from python.org
- Use Anaconda for data science
- IDEs: VS Code, PyCharm, IDLE
- Package managers: pip, conda

### First Program
```python
print("Hello, World!")
```

## Basic Syntax

### Variables and Data Types

#### Variables
- Containers for storing data
- No declaration needed
- Dynamic typing

```python
name = "Alice"
age = 25
height = 5.7
is_student = True
```

#### Data Types
- **int**: Integer numbers
- **float**: Decimal numbers
- **str**: Text strings
- **bool**: True/False values
- **list**: Ordered collections
- **dict**: Key-value pairs

### Operators

#### Arithmetic Operators
```python
+  # Addition
-  # Subtraction
*  # Multiplication
/  # Division
// # Floor division
%  # Modulus
** # Exponentiation
```

#### Comparison Operators
```python
== # Equal to
!= # Not equal to
>  # Greater than
<  # Less than
>= # Greater than or equal to
<= # Less than or equal to
```

#### Logical Operators
```python
and # Logical AND
or  # Logical OR
not # Logical NOT
```

## Control Structures

### Conditional Statements

#### if Statement
```python
age = 18
if age >= 18:
    print("You are an adult")
```

#### if-else Statement
```python
age = 16
if age >= 18:
    print("You can vote")
else:
    print("You cannot vote yet")
```

#### if-elif-else Statement
```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

### Loops

#### for Loop
```python
# Iterate over a list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(fruit)

# Iterate over a range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4
```

#### while Loop
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

#### Loop Control
```python
# break - exit loop
for i in range(10):
    if i == 5:
        break
    print(i)

# continue - skip iteration
for i in range(5):
    if i == 2:
        continue
    print(i)
```

## Functions

### Defining Functions
```python
def greet(name):
    return f"Hello, {name}!"

# Calling functions
message = greet("Alice")
print(message)  # Hello, Alice!
```

### Parameters and Arguments
```python
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print(result)  # 8
```

### Default Parameters
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))           # Hello, Alice!
print(greet("Bob", "Hi"))       # Hi, Bob!
```

## Data Structures

### Lists
```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "orange"]

# Accessing elements
print(numbers[0])    # 1
print(fruits[-1])    # orange

# Modifying lists
fruits.append("grape")
fruits.insert(1, "mango")
fruits.remove("banana")

# List methods
len(fruits)          # length
fruits.sort()        # sort list
fruits.reverse()     # reverse list
```

### Dictionaries
```python
# Creating dictionaries
student = {
    "name": "Alice",
    "age": 20,
    "grade": "A"
}

# Accessing values
print(student["name"])    # Alice

# Modifying dictionaries
student["age"] = 21
student["major"] = "Computer Science"

# Dictionary methods
student.keys()       # get keys
student.values()     # get values
student.items()      # get key-value pairs
```

### Tuples
```python
# Creating tuples
coordinates = (10, 20)
colors = ("red", "green", "blue")

# Tuples are immutable
# coordinates[0] = 15  # This will cause an error
```

## File Handling

### Reading Files
```python
# Open and read a file
with open("example.txt", "r") as file:
    content = file.read()
    print(content)

# Read line by line
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())
```

### Writing Files
```python
# Write to a file
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is a test file.\n")

# Append to a file
with open("output.txt", "a") as file:
    file.write("This line will be appended.\n")
```

## Error Handling

### Try-Except Blocks
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

try:
    number = int("abc")
except ValueError:
    print("Invalid number format!")
```

### Multiple Exceptions
```python
try:
    # Some code that might raise exceptions
    result = int(input("Enter a number: "))
    division = 100 / result
except ValueError:
    print("Please enter a valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Nigerian Applications

### Educational Software
- Student management systems
- Online learning platforms
- Examination systems

### Business Automation
- Inventory management
- Sales tracking
- Financial calculations

### Data Analysis
- Census data processing
- Election result analysis
- Health statistics

### Web Development
- E-commerce platforms
- Government portals
- News websites

## Best Practices

### Code Style
- Use meaningful variable names
- Add comments for complex logic
- Follow PEP 8 style guide
- Use consistent indentation

### Error Prevention
- Validate user input
- Handle edge cases
- Use appropriate data types
- Test code thoroughly

### Efficiency
- Use built-in functions when possible
- Avoid unnecessary computations
- Use appropriate data structures
- Profile code performance

## Common Mistakes
- Indentation errors
- Case sensitivity issues
- Type conversion problems
- Infinite loops
- File handling without proper closing

## Practice Exercises

1. Write a program that calculates the average of three numbers
2. Create a list of Nigerian states and print them
3. Write a function that checks if a number is even or odd
4. Create a dictionary of student grades and calculate the class average
5. Write a program that reads a file and counts the number of words

## Resources
- Python Official Documentation
- Codecademy Python course
- freeCodeCamp Python tutorial
- Automate the Boring Stuff with Python (book)
- Python Nigeria community''',
                'summary': 'Comprehensive introduction to Python programming covering syntax, data structures, and Nigerian applications',
                'learning_objectives': 'Write basic Python programs,Understand data types and structures,Use control flow statements,Handle files and errors,Apply Python to Nigerian contexts',
                'key_concepts': 'Python syntax,Data types,Control structures,Functions,File handling,Nigerian applications',
                'worked_examples': 'Basic programs,Data structure operations,Function creation,File operations',
                'practice_problems': 'Programming exercises,Algorithm implementation,Real-world applications',
                'cultural_notes': 'Python usage in Nigerian education,business automation,government systems,tech community'
            }
        ]

    def _get_mathematics_additional_topics(self):
        """Generate additional Mathematics topics"""

        return [
            {
                'title': 'Mathematics: Geometry - Coordinate Geometry',
                'subject': 'Mathematics',
                'topic': 'Geometry',
                'subtopic': 'Coordinate Geometry',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Mathematics: Geometry - Coordinate Geometry

## Introduction
Coordinate geometry combines algebra and geometry to study geometric shapes using coordinate systems. It provides algebraic methods for geometric problems.

## Cartesian Coordinate System

### Coordinate Plane
- Two perpendicular number lines intersecting at origin (0,0)
- Horizontal axis: x-axis
- Vertical axis: y-axis
- Ordered pairs: (x, y)

### Quadrants
- Quadrant I: (+x, +y)
- Quadrant II: (-x, +y)
- Quadrant III: (-x, -y)
- Quadrant IV: (+x, -y)

## Distance Formula

### Formula
Distance between points P(x₁, y₁) and Q(x₂, y₂):
d = √[(x₂ - x₁)² + (y₂ - y₁)²]

### Applications
- Finding lengths of line segments
- Proving geometric properties
- Navigation and mapping

### Examples
Distance between (2, 3) and (5, 7):
d = √[(5-2)² + (7-3)²] = √[9 + 16] = √25 = 5

## Midpoint Formula

### Formula
Midpoint of P(x₁, y₁) and Q(x₂, y₂):
M = ((x₁ + x₂)/2, (y₁ + y₂)/2)

### Applications
- Finding centers of line segments
- Dividing lines in ratios
- Constructing geometric figures

### Example
Midpoint of (1, 2) and (7, 10):
M = ((1+7)/2, (2+10)/2) = (4, 6)

## Section Formula

### Internal Division
Point dividing line segment in ratio m:n from P to Q:
x = (nx₁ + mx₂)/(m + n)
y = (ny₁ + my₂)/(m + n)

### External Division
Point dividing line segment externally in ratio m:n:
x = (nx₁ - mx₂)/(m - n)
y = (ny₁ - my₂)/(m - n)

## Straight Lines

### Equation of a Line

#### Slope-Intercept Form
y = mx + c
- m: slope (gradient)
- c: y-intercept

#### General Form
ax + by + c = 0

#### Two-Point Form
y - y₁ = m(x - x₁)
where m = (y₂ - y₁)/(x₂ - x₁)

### Slope of a Line

#### Formula
m = (y₂ - y₁)/(x₂ - x₁)

#### Special Cases
- Horizontal line: slope = 0
- Vertical line: slope = undefined
- Parallel lines: equal slopes
- Perpendicular lines: slopes are negative reciprocals

### Angle Between Lines
If slopes are m₁ and m₂, then:
tanθ = |(m₂ - m₁)/(1 + m₁m₂)|

## Circles

### Equation of a Circle
Center (h, k), radius r:
(x - h)² + (y - k)² = r²

### Standard Forms
- Center at origin: x² + y² = r²
- General form: x² + y² + dx + ey + f = 0

### Circle Properties
- Circumference: 2πr
- Area: πr²
- Tangent lines: perpendicular to radius
- Chord properties

## Conic Sections

### Parabola
- Equation: y² = 4ax (focus at (a, 0))
- Directrix: x = -a
- Vertex: (0, 0)
- Focal length: a

### Ellipse
- Equation: x²/a² + y²/b² = 1
- Foci: (±c, 0) where c² = a² - b²
- Major/minor axes: 2a, 2b
- Eccentricity: c/a < 1

### Hyperbola
- Equation: x²/a² - y²/b² = 1
- Foci: (±c, 0) where c² = a² + b²
- Transverse axis: 2a
- Conjugate axis: 2b
- Eccentricity: c/a > 1

## Applications in Nigeria

### Surveying and Mapping
- Land surveying using coordinate geometry
- GPS coordinate systems
- Urban planning and development

### Architecture and Construction
- Building design and layout
- Road and bridge construction
- Structural engineering calculations

### Navigation
- Geographic coordinate systems
- Map projections
- Distance and direction calculations

### Computer Graphics
- 2D and 3D modeling
- Animation and gaming
- Computer-aided design (CAD)

## Common Mistakes
- Incorrect coordinate ordering
- Sign errors in formulas
- Confusion between distance and midpoint
- Wrong slope calculations
- Misunderstanding perpendicular lines

## Practice Problems
1. Find distance between (3, 4) and (7, 1)
2. Find midpoint of (2, 5) and (8, 11)
3. Find equation of line through (1, 2) with slope 3
4. Find equation of circle with center (2, 3) and radius 5
5. Determine if lines 2x + 3y = 5 and 3x - 2y = 7 are perpendicular

## WAEC Applications
- Coordinate geometry problems
- Circle theorems applications
- Straight line graphs
- Locus problems
- Construction problems''',
                'summary': 'Comprehensive guide to coordinate geometry including lines, circles, and conic sections',
                'learning_objectives': 'Apply distance and midpoint formulas,Find equations of lines and circles,Understand conic sections,Use coordinate geometry in problem solving',
                'key_concepts': 'Coordinate systems,Distance formula,Midpoint formula,Straight lines,Circles,Conic sections',
                'important_formulas': 'Distance: √[(x₂-x₁)²+(y₂-y₁)²],Midpoint: ((x₁+x₂)/2,(y₁+y₂)/2),Line: y=mx+c',
                'worked_examples': 'Distance calculations,Line equations,Circle equations,Conic section problems',
                'practice_problems': 'Coordinate geometry exercises,WAEC-style problems,Application problems',
                'cultural_notes': 'Nigerian surveying applications,Architecture in Nigerian cities,Computer graphics in Nigerian tech industry'
            },
            {
                'title': 'Mathematics: Calculus - Differentiation',
                'subject': 'Mathematics',
                'topic': 'Calculus',
                'subtopic': 'Differentiation',
                'content_type': 'study_guide',
                'difficulty': 'advanced',
                'content': '''# Mathematics: Calculus - Differentiation

## Introduction
Calculus is the mathematical study of change. Differentiation deals with rates of change and slopes of curves. It has applications in physics, engineering, economics, and many other fields.

## Limits and Continuity

### Concept of Limit
The limit of f(x) as x approaches a is L if f(x) gets arbitrarily close to L as x gets close to a.

lim(x→a) f(x) = L

### Continuity
A function f(x) is continuous at x = a if:
1. f(a) exists
2. lim(x→a) f(x) exists
3. lim(x→a) f(x) = f(a)

### Types of Discontinuity
- Removable discontinuity
- Jump discontinuity
- Infinite discontinuity

## Derivative Definition

### Average Rate of Change
For function f(x), average rate of change over [x, x+Δx]:
(f(x+Δx) - f(x))/Δx

### Instantaneous Rate of Change
lim(Δx→0) [f(x+Δx) - f(x)]/Δx

### Derivative Notation
- f'(x) or dy/dx
- d/dx[f(x)]

## Basic Differentiation Rules

### Power Rule
d/dx[xⁿ] = nxⁿ⁻¹

### Constant Rule
d/dx[c] = 0

### Constant Multiple Rule
d/dx[cf(x)] = c f'(x)

### Sum Rule
d/dx[f(x) + g(x)] = f'(x) + g'(x)

### Difference Rule
d/dx[f(x) - g(x)] = f'(x) - g'(x)

### Product Rule
d/dx[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)

### Quotient Rule
d/dx[f(x)/g(x)] = [f'(x)g(x) - f(x)g'(x)]/[g(x)]²

### Chain Rule
d/dx[f(g(x))] = f'(g(x)) * g'(x)

## Derivatives of Trigonometric Functions

### Basic Trigonometric Derivatives
- d/dx[sin x] = cos x
- d/dx[cos x] = -sin x
- d/dx[tan x] = sec² x
- d/dx[cot x] = -cosec² x
- d/dx[sec x] = sec x tan x
- d/dx[cosec x] = -cosec x cot x

## Derivatives of Exponential and Logarithmic Functions

### Exponential Functions
- d/dx[eˣ] = eˣ
- d/dx[aˣ] = aˣ ln a

### Logarithmic Functions
- d/dx[ln x] = 1/x
- d/dx[logₐ x] = 1/(x ln a)

## Higher Order Derivatives

### Second Derivative
f''(x) = d/dx[f'(x)]

### Third Derivative
f\'\'\'(x) = d/dx[f\'\'(x)]

### Notation
- f'(x), f''(x), f\'\'\'(x)
- d2y/dx2, d3y/dx3

## Applications of Differentiation

### Rate of Change Problems
- Velocity: dx/dt
- Acceleration: d2x/dt2
- Marginal cost: dC/dx
- Marginal revenue: dR/dx

### Tangents and Normals
- Slope of tangent: f'(a)
- Equation of tangent: y - f(a) = f'(a)(x - a)
- Normal is perpendicular to tangent

### Maximum and Minimum Values

#### Critical Points
Points where f'(x) = 0 or undefined

#### Second Derivative Test
- If f''(c) > 0: local minimum
- If f''(c) < 0: local maximum
- If f''(c) = 0: inconclusive

### Increasing and Decreasing Functions
- Increasing: f'(x) > 0
- Decreasing: f'(x) < 0
- Constant: f'(x) = 0

## Optimization Problems

### Steps for Optimization
1. Identify variables and constraints
2. Write equation in terms of one variable
3. Find critical points
4. Test critical points and endpoints
5. Verify solution

### Examples
- Maximum area with fixed perimeter
- Minimum cost for given volume
- Optimal production levels

## Nigerian Applications

### Economics
- Profit maximization: dπ/dx = 0
- Cost minimization
- Elasticity calculations
- Marginal analysis

### Engineering
- Velocity and acceleration calculations
- Structural optimization
- Electrical circuit analysis
- Mechanical system design

### Physics
- Motion analysis
- Force and energy relationships
- Wave and oscillation problems
- Heat transfer calculations

### Agriculture
- Optimal crop yields
- Fertilizer application rates
- Irrigation system design
- Pest control optimization

## Common Mistakes
- Incorrect application of product/quotient rules
- Chain rule errors
- Sign errors in trigonometric derivatives
- Confusion between maximum and minimum
- Forgetting domain restrictions

## Practice Problems
1. Differentiate: y = x³ + 2x² - 5x + 3
2. Find d/dx[sin(x² + 1)]
3. Use product rule: y = (x² + 1)(x³ - 2)
4. Find equation of tangent to y = x² at x = 2
5. Find maximum area of rectangle with perimeter 20m
6. A particle moves with s = t³ - 6t² + 9t. Find velocity and acceleration

## WAEC Applications
- Rate of change problems
- Tangent and normal calculations
- Maximum/minimum applications
- Motion problems
- Optimization in real-world contexts''',
                'summary': 'Comprehensive guide to differentiation including rules, applications, and optimization',
                'learning_objectives': 'Apply differentiation rules,Solve rate of change problems,Find maximum and minimum values,Use differentiation in optimization,Apply calculus to Nigerian contexts',
                'key_concepts': 'Limits and continuity,Derivative rules,Applications of differentiation,Optimization problems,Higher order derivatives',
                'important_formulas': 'Power rule: d/dx[xⁿ]=nxⁿ⁻¹,Product rule,Chain rule,Second derivative test',
                'worked_examples': 'Basic differentiation,Rate problems,Optimization examples,Motion analysis',
                'practice_problems': 'Differentiation exercises,Application problems,WAEC-style questions,Nigerian context problems',
                'cultural_notes': 'Economic optimization in Nigerian businesses,Agricultural applications,Engineering calculations,Physics applications in Nigerian education'
            },
            {
                'title': 'Mathematics: Statistics - Probability',
                'subject': 'Mathematics',
                'topic': 'Statistics',
                'subtopic': 'Probability',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Mathematics: Statistics - Probability

## Introduction
Probability is the study of chance and uncertainty. It quantifies the likelihood of events occurring and is essential for decision-making in uncertain situations.

## Basic Concepts

### Experiment
A process that produces an outcome. Examples:
- Tossing a coin
- Rolling a die
- Drawing cards from a deck

### Sample Space
Set of all possible outcomes. Denoted by S.

### Event
Subset of the sample space. Can be:
- Simple event: Single outcome
- Compound event: Multiple outcomes
- Impossible event: Empty set
- Certain event: Entire sample space

## Classical Probability

### Definition
P(E) = Number of favorable outcomes / Total number of possible outcomes

### Assumptions
- All outcomes equally likely
- Finite number of outcomes
- Outcomes mutually exclusive

### Examples
- Coin toss: P(Heads) = 1/2
- Die roll: P(6) = 1/6
- Card draw: P(King) = 4/52 = 1/13

## Addition Rule

### For Mutually Exclusive Events
P(A ∪ B) = P(A) + P(B)

### For Non-Mutually Exclusive Events
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)

### Complementary Events
P(A') = 1 - P(A)

## Multiplication Rule

### Independent Events
P(A ∩ B) = P(A) * P(B)

### Dependent Events
P(A ∩ B) = P(A) * P(B|A)

### Conditional Probability
P(B|A) = P(A ∩ B) / P(A)

## Tree Diagrams
Visual representation of multi-stage experiments showing:
- Branches for choices
- Probabilities on branches
- Outcomes at endpoints

## Permutations and Combinations

### Permutations
Arrangements of objects where order matters.

### Formula
ⁿPᵣ = n! / (n-r)!

### Combinations
Selections of objects where order doesn't matter.

### Formula
ⁿCᵣ = n! / (r!(n-r)!)

## Binomial Probability

### Conditions
- Fixed number of trials (n)
- Each trial has 2 outcomes (success/failure)
- Constant probability of success (p)
- Independent trials

### Formula
P(X = r) = ⁿCᵣ pʳ (1-p)ⁿ⁻ʳ

### Mean and Variance
- Mean: μ = np
- Variance: σ² = np(1-p)

## Normal Distribution

### Properties
- Bell-shaped curve
- Symmetric about mean
- Total area under curve = 1
- Defined by mean (μ) and standard deviation (σ)

### Standard Normal Distribution
- Mean = 0, Standard deviation = 1
- Z-scores: z = (x - μ)/σ

### Applications
- Heights and weights
- Test scores
- Measurement errors
- Quality control

## Nigerian Applications

### Agriculture
- Crop yield predictions
- Weather forecasting
- Pest control effectiveness
- Harvest timing decisions

### Health
- Disease outbreak probabilities
- Vaccine effectiveness
- Epidemiological studies
- Health insurance calculations

### Business and Finance
- Stock market predictions
- Insurance risk assessment
- Investment decisions
- Market research analysis

### Education
- Examination success rates
- Student performance predictions
- Admission probability calculations
- Learning outcome assessments

### Sports
- Match outcome predictions
- Player performance analysis
- Betting odds calculations
- Tournament probability modeling

## Common Mistakes
- Confusing permutations and combinations
- Incorrect application of addition/multiplication rules
- Forgetting conditional probability formula
- Misinterpreting independent vs dependent events
- Incorrect binomial probability calculations

## Practice Problems
1. A bag contains 5 red and 3 blue balls. Find P(drawing red ball)
2. Two dice are rolled. Find P(sum = 7)
3. A coin is tossed 3 times. Find P(exactly 2 heads)
4. In a class of 30 students, 18 passed Math, 20 passed English, 12 passed both. Find P(passed at least one)
5. Calculate probability of drawing 3 aces from a deck of 52 cards

## WAEC Applications
- Probability calculations
- Statistical analysis
- Decision making under uncertainty
- Risk assessment problems
- Real-world application problems

## Data Collection Methods
- Surveys and questionnaires
- Experiments and observations
- Sampling techniques
- Census vs sample surveys

## Statistical Measures
- Mean, median, mode
- Range, variance, standard deviation
- Quartiles and percentiles
- Correlation and regression

## Hypothesis Testing
- Null and alternative hypotheses
- Level of significance
- p-values and critical values
- Type I and Type II errors

## Confidence Intervals
- Estimation of population parameters
- Margin of error calculations
- Sample size determination
- Interpretation of results''',
                'summary': 'Comprehensive guide to probability theory including basic concepts, distributions, and Nigerian applications',
                'learning_objectives': 'Calculate basic probabilities,Apply addition and multiplication rules,Use permutations and combinations,Solve binomial probability problems,Apply probability to Nigerian contexts',
                'key_concepts': 'Sample space and events,Probability rules,Permutations and combinations,Binomial distribution,Normal distribution',
                'important_formulas': 'P(E)=n(E)/n(S),Binomial: P(X=r)=ⁿCᵣ pʳ qⁿ⁻ʳ,Normal distribution z-scores',
                'worked_examples': 'Basic probability calculations,Tree diagram problems,Binomial distribution examples,Normal distribution applications',
                'practice_problems': 'Probability exercises,WAEC-style problems,Nigerian context applications,Statistical analysis problems',
                'cultural_notes': 'Agricultural probability applications,Nigerian lottery systems,Sports betting analysis,Health probability studies,Election probability calculations'
            }
        ]

    def _get_physics_additional_topics(self):
        """Generate additional Physics topics"""

        return [
            {
                'title': 'Physics: Mechanics - Energy and Power',
                'subject': 'Physics',
                'topic': 'Mechanics',
                'subtopic': 'Energy and Power',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Physics: Mechanics - Energy and Power

## Introduction
Energy is the capacity to do work. Power is the rate at which work is done or energy is transferred. Understanding energy conservation is fundamental to physics.

## Forms of Energy

### Kinetic Energy
Energy possessed by a body due to its motion.

**Formula:** KE = ½mv²
- m: mass (kg)
- v: velocity (m/s)
- Unit: Joule (J)

### Potential Energy
Energy stored in a body due to its position or state.

#### Gravitational Potential Energy
**Formula:** PE = mgh
- m: mass (kg)
- g: acceleration due to gravity (9.8 m/s²)
- h: height (m)
- Unit: Joule (J)

#### Elastic Potential Energy
**Formula:** PE = ½kx²
- k: spring constant (N/m)
- x: extension/compression (m)

### Mechanical Energy
Total energy possessed by a system.

**Formula:** ME = KE + PE

## Conservation of Mechanical Energy

### Principle
In the absence of non-conservative forces (like friction), mechanical energy remains constant.

**Equation:** KE₁ + PE₁ = KE₂ + PE₂

### Applications
- Free fall problems
- Pendulum motion
- Roller coasters
- Projectile motion

## Work-Energy Theorem

### Definition
Work done by all forces acting on a body equals change in kinetic energy.

**Equation:** W_net = ΔKE = KE₂ - KE₁

### Work Done by a Force
**Formula:** W = F * d * cosθ
- F: force (N)
- d: displacement (m)
- θ: angle between force and displacement
- Unit: Joule (J)

## Power

### Definition
Rate of doing work or transferring energy.

**Formula:** P = W/t
- W: work done (J)
- t: time (s)
- Unit: Watt (W)

### Alternative Formula
P = F * v
- F: force (N)
- v: velocity (m/s)

## Efficiency

### Definition
Ratio of useful energy output to total energy input.

**Formula:** Efficiency = (Useful energy output / Total energy input) * 100%

### Mechanical Advantage
Ratio of load to effort in machines.

## Energy Conversion

### Examples
- Electrical → Mechanical: Electric motor
- Mechanical → Electrical: Generator
- Chemical → Electrical: Battery
- Light → Electrical: Solar panel
- Heat → Mechanical: Steam engine

## Nigerian Energy Applications

### Hydroelectric Power
- Kainji Dam, Jebba Dam, Shiroro Dam
- Clean energy production
- Flood control and irrigation

### Thermal Power Plants
- Egbin Power Plant (coal/gas)
- Afam Power Plant (gas)
- Electricity generation for industries

### Renewable Energy
- Solar power installations
- Wind energy potential
- Biomass from agricultural waste
- Mini-hydro projects

### Petroleum Industry
- Oil exploration and production
- Refining processes
- Energy export economy

### Transportation
- Automobile fuel efficiency
- Public transportation systems
- Aviation fuel consumption
- Railway electrification

## Energy Crisis in Nigeria

### Challenges
- Inadequate power generation
- Transmission losses
- Distribution inefficiencies
- Fuel importation dependence

### Solutions
- Renewable energy development
- Energy conservation programs
- Improved infrastructure
- Alternative energy sources

## Conservation of Energy

### First Law of Thermodynamics
Energy cannot be created or destroyed, only converted from one form to another.

**Equation:** ΔU = Q - W
- ΔU: change in internal energy
- Q: heat added to system
- W: work done by system

## Elastic and Inelastic Collisions

### Elastic Collision
Kinetic energy conserved
- Momentum conserved
- KE conserved

### Inelastic Collision
Kinetic energy not conserved
- Momentum conserved
- Some KE converted to other forms

## Common Mistakes
- Confusing work and power
- Incorrect sign conventions for work
- Forgetting potential energy reference point
- Misapplying conservation laws
- Wrong units in calculations

## Practice Problems
1. A 2kg mass is thrown vertically with speed 10m/s. Find maximum height reached
2. A spring with k=100N/m is compressed by 0.2m. Find elastic potential energy
3. Calculate work done in lifting 50kg mass to height 5m
4. A 1000kg car accelerates from rest to 20m/s in 10s. Find average power
5. Find efficiency of a machine that does 800J work with 2000J energy input

## WAEC Applications
- Energy conservation problems
- Work and power calculations
- Efficiency problems
- Nigerian energy context questions
- Real-world application problems

## Laboratory Activities
- Verification of conservation of energy
- Measurement of spring constants
- Power output calculations
- Efficiency determinations
- Energy conversion demonstrations''',
                'summary': 'Comprehensive guide to energy forms, conservation laws, power, and Nigerian energy applications',
                'learning_objectives': 'Identify different forms of energy,Apply conservation of energy,Calculate work and power,Understand energy conversion,Analyze Nigerian energy systems',
                'key_concepts': 'Kinetic energy,Potential energy,Conservation laws,Work-energy theorem,Power,Efficiency',
                'important_formulas': 'KE=1/2mv²,PE=mgh,W=Fdcosθ,P=W/t,Efficiency=output/input*100%',
                'worked_examples': 'Energy conservation problems,Work calculations,Power problems,Efficiency calculations',
                'practice_problems': 'Energy conversion exercises,WAEC-style problems,Nigerian energy applications,Conservation law problems',
                'cultural_notes': 'Nigerian hydroelectric dams,Petroleum industry,Energy crisis solutions,Renewable energy development,Transportation energy use'
            },
            {
                'title': 'Physics: Electricity - Circuits and Components',
                'subject': 'Physics',
                'topic': 'Electricity',
                'subtopic': 'Circuits and Components',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Physics: Electricity - Circuits and Components

## Introduction
Electricity involves the flow of electric charge through conductors. Electric circuits are pathways for electric current, consisting of various components that control and utilize electrical energy.

## Basic Electric Quantities

### Electric Current
Rate of flow of electric charge.

**Formula:** I = Q/t
- I: current (A)
- Q: charge (C)
- t: time (s)

### Potential Difference (Voltage)
Work done per unit charge.

**Formula:** V = W/Q
- V: voltage (V)
- W: work (J)
- Q: charge (C)

### Resistance
Opposition to current flow.

**Formula:** R = V/I (Ohm's Law)
- R: resistance (Ω)
- V: voltage (V)
- I: current (A)

## Ohm's Law
Current through a conductor is directly proportional to voltage and inversely proportional to resistance.

**Equation:** V = IR

## Electric Power

### Definition
Rate of electrical energy transfer.

**Formula:** P = VI
- P: power (W)
- V: voltage (V)
- I: current (A)

### Alternative Formulas
P = I²R
P = V²/R

### Electrical Energy
**Formula:** E = Pt = VIt
- E: energy (J)
- P: power (W)
- t: time (s)

## Resistors in Series

### Total Resistance
R_total = R₁ + R₂ + R₃ + ...

### Current
Same through all resistors: I_total = I₁ = I₂ = I₃

### Voltage Division
V_total = V₁ + V₂ + V₃ + ...

## Resistors in Parallel

### Total Resistance
1/R_total = 1/R₁ + 1/R₂ + 1/R₃ + ...

### Current Division
I_total = I₁ + I₂ + I₃ + ...

### Voltage
Same across all resistors: V_total = V₁ = V₂ = V₃

## Electrical Components

### Fixed Resistor
- Constant resistance value
- Color coding for identification
- Power rating specifications

### Variable Resistor (Rheostat)
- Adjustable resistance
- Used in volume controls, dimmer switches
- Sliding contact mechanism

### Thermistor
- Resistance changes with temperature
- NTC: Negative Temperature Coefficient
- PTC: Positive Temperature Coefficient

### Light Dependent Resistor (LDR)
- Resistance decreases with light intensity
- Used in automatic lighting systems
- Semiconductor material

## Capacitors

### Definition
Device that stores electrical charge.

### Capacitance
**Formula:** C = Q/V
- C: capacitance (F)
- Q: charge (C)
- V: voltage (V)

### Energy Stored
**Formula:** E = ½CV² = ½QV = Q²/2C

### Capacitors in Series
1/C_total = 1/C₁ + 1/C₂ + 1/C₃ + ...

### Capacitors in Parallel
C_total = C₁ + C₂ + C₃ + ...

## Electromotive Force (EMF)

### Definition
Energy supplied per unit charge by a source.

### Internal Resistance
- Opposition within the source
- Reduces terminal voltage
- V_terminal = EMF - Ir

## Meters and Measurements

### Ammeter
- Measures current
- Connected in series
- Low resistance

### Voltmeter
- Measures voltage
- Connected in parallel
- High resistance

### Multimeter
- Measures voltage, current, resistance
- Digital and analog types
- Various ranges

## Nigerian Electrical Applications

### Power Generation and Distribution
- National grid system
- Power Holding Company of Nigeria (PHCN)
- Rural electrification projects
- Solar home systems

### Telecommunications
- Telephone networks
- Mobile communication systems
- Internet infrastructure
- Satellite communications

### Transportation
- Electric trains (Lagos-Ibadan rail)
- Automobile electrical systems
- Aviation electronics
- Marine electrical systems

### Industrial Applications
- Manufacturing processes
- Oil and gas industry
- Mining operations
- Construction equipment

### Domestic Applications
- Household appliances
- Lighting systems
- Security systems
- Entertainment electronics

## Electrical Safety

### Hazards
- Electric shock
- Electrical fires
- Equipment damage
- Data loss

### Safety Measures
- Proper earthing
- Circuit breakers and fuses
- Insulated tools
- Regular maintenance

## Common Mistakes
- Incorrect series/parallel calculations
- Wrong meter connections
- Ignoring internal resistance
- Unit conversion errors
- Power rating violations

## Practice Problems
1. Calculate current through 10Ω resistor with 5V applied
2. Find total resistance of 2Ω, 3Ω, 4Ω in series
3. Calculate total resistance of 2Ω, 3Ω, 4Ω in parallel
4. A 100W bulb operates at 220V. Find current and resistance
5. Calculate energy consumed by 2000W heater in 1 hour

## WAEC Applications
- Circuit calculations
- Component identification
- Power and energy problems
- Nigerian electrical systems
- Safety and applications

## Laboratory Activities
- Verification of Ohm's law
- Series and parallel circuits
- Power measurements
- Component testing
- Safety demonstrations''',
                'summary': 'Comprehensive guide to electric circuits, components, power calculations, and Nigerian applications',
                'learning_objectives': 'Apply Ohm\'s law,Analyze series and parallel circuits,Calculate electrical power and energy,Understand electrical components,Apply knowledge to Nigerian electrical systems',
                'key_concepts': 'Ohm\'s law,Circuit analysis,Electrical power,Resistors and capacitors,Electrical safety',
                'important_formulas': 'V=IR,P=VI,E=Pt,R_series=R1+R2,R_parallel=1/R1+1/R2',
                'worked_examples': 'Circuit calculations,Power problems,Energy consumption,Component analysis',
                'practice_problems': 'Circuit design problems,WAEC-style calculations,Nigerian electrical applications,Safety problems',
                'cultural_notes': 'Nigerian power distribution,Telecommunications industry,Electrical safety in Nigeria,Industrial applications,Rural electrification'
            },
            {
                'title': 'Physics: Optics - Light and Lenses',
                'subject': 'Physics',
                'topic': 'Optics',
                'subtopic': 'Light and Lenses',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Physics: Optics - Light and Lenses

## Introduction
Optics is the study of light and its interactions with matter. Lenses are transparent materials that refract light to form images. Understanding lenses is crucial for cameras, microscopes, telescopes, and human vision.

## Nature of Light

### Wave Theory
- Light as electromagnetic waves
- Speed in vacuum: 3 * 10^8 m/s
- Wavelength and frequency relationship: c = fλ

### Particle Theory
- Light as photons
- Energy of photon: E = hf
- h = 6.63 * 10^-34 J s (Planck's constant)

### Dual Nature
Light exhibits both wave and particle properties depending on the situation.

## Refraction

### Definition
Bending of light when passing from one medium to another.

### Snell's Law
n₁ sin i = n₂ sin r
- n₁, n₂: refractive indices
- i: angle of incidence
- r: angle of refraction

### Refractive Index
n = c/v = sin i / sin r
- c: speed in vacuum
- v: speed in medium

## Lenses

### Types of Lenses

#### Convex (Converging) Lens
- Thicker in middle
- Converges light rays
- Forms real images
- Used in cameras, microscopes

#### Concave (Diverging) Lens
- Thinner in middle
- Diverges light rays
- Forms virtual images
- Used in spectacles for myopia

### Lens Terminology

#### Optical Center (O)
Point through which light passes undeviated

#### Principal Axis
Line joining centers of curvature

#### Focal Point (F)
Point where parallel rays converge (convex) or appear to diverge (concave)

#### Focal Length (f)
Distance between optical center and focal point

#### Object Distance (u)
Distance from object to optical center (negative for real objects)

#### Image Distance (v)
Distance from image to optical center (negative for real images)

## Lens Formula

### Formula
1/v - 1/u = 1/f

### Magnification
m = h_i/h_o = v/u
- h_i: image height
- h_o: object height

### Power of Lens
P = 1/f (in meters)
- Unit: Dioptre (D)
- Convex lens: positive power
- Concave lens: negative power

## Ray Diagrams

### Convex Lens

#### Object at Infinity
- Parallel rays → converge at F
- Image: real, inverted, diminished at F

#### Object beyond 2F
- Image: real, inverted, diminished between F and 2F

#### Object at 2F
- Image: real, inverted, same size at 2F

#### Object between F and 2F
- Image: real, inverted, magnified beyond 2F

#### Object at F
- Image: at infinity

#### Object between F and O
- Image: virtual, erect, magnified on same side

### Concave Lens
- Always forms virtual, erect, diminished images
- Image between F and O on same side as object

## Lens Defects

### Spherical Aberration
- Different parts of lens have different focal lengths
- Corrected by using lens stops or aspheric lenses

### Chromatic Aberration
- Different wavelengths refracted differently
- Corrected by achromatic lenses (combination of convex and concave)

## Applications of Lenses

### Human Eye
- Cornea and lens focus light on retina
- Accommodation: changing focal length
- Near point and far point
- Defects: myopia, hyperopia, presbyopia

### Corrective Lenses
- Myopia: concave lenses
- Hyperopia: convex lenses
- Astigmatism: cylindrical lenses

### Optical Instruments

#### Microscope
- Objective and eyepiece lenses
- Magnification: M = m_o * m_e
- Total magnification up to 1000x

#### Telescope
- Objective and eyepiece lenses
- Types: refracting, reflecting
- Magnification: M = f_o/f_e

#### Camera
- Convex lens forms real, inverted image on film/sensor
- Aperture controls light, shutter controls time
- Zoom lenses change focal length

## Nigerian Applications

### Healthcare
- Spectacles and contact lenses
- Ophthalmic equipment
- Diagnostic instruments
- Surgical microscopes

### Education
- Laboratory microscopes
- Projectors and overhead projectors
- Telescopes for astronomy
- Photographic equipment

### Industry
- Quality control microscopes
- Machine vision systems
- Laser cutting and welding
- Optical fiber communications

### Research
- Scientific research equipment
- Medical research instruments
- Environmental monitoring
- Material analysis

## Light Phenomena

### Total Internal Reflection
- Occurs when light travels from denser to rarer medium
- Critical angle: sin C = n₂/n₁
- Applications: optical fibers, diamonds, mirages

### Optical Fibers
- Total internal reflection for signal transmission
- Used in telecommunications
- Internet and cable TV
- Medical endoscopes

## Common Mistakes
- Incorrect sign conventions for lenses
- Confusion between convex and concave lenses
- Wrong ray diagram constructions
- Magnification formula errors
- Power calculation mistakes

## Practice Problems
1. A convex lens has focal length 20cm. Find image distance for object 30cm away
2. Calculate magnification for lens with u = -15cm, v = -10cm
3. Find power of lens with focal length -25cm
4. Draw ray diagram for object between F and 2F of convex lens
5. Explain why concave lens always forms virtual images

## WAEC Applications
- Lens formula problems
- Ray diagram questions
- Magnification calculations
- Power of lens problems
- Optical instrument applications

## Laboratory Activities
- Determination of focal length
- Lens formula verification
- Microscope magnification
- Telescope construction
- Eye defect corrections''',
                'summary': 'Comprehensive guide to light, refraction, lenses, and optical instruments with Nigerian applications',
                'learning_objectives': 'Understand light refraction,Apply lens formula,Draw ray diagrams,Analyze optical instruments,Apply optics to Nigerian contexts',
                'key_concepts': 'Refraction,Lens types,Lens formula,Optical instruments,Light phenomena',
                'important_formulas': 'Lens formula: 1/v - 1/u = 1/f,Magnification: m = v/u,Power: P = 1/f',
                'worked_examples': 'Lens calculations,Ray diagrams,Magnification problems,Power calculations',
                'practice_problems': 'Lens formula exercises,WAEC-style problems,Optical instrument analysis,Nigerian application problems',
                'cultural_notes': 'Healthcare optics in Nigeria,Educational equipment,Telecommunications industry,Research applications,Traditional optical practices'
            },
            {
                'title': 'Physics: Thermodynamics - Heat and Temperature',
                'subject': 'Physics',
                'topic': 'Thermodynamics',
                'subtopic': 'Heat and Temperature',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'content': '''# Physics: Thermodynamics - Heat and Temperature

## Introduction
Thermodynamics is the study of heat, work, and energy transfer. It deals with the relationships between heat, work, and other forms of energy. Understanding thermodynamics is essential for engines, refrigerators, and many industrial processes.

## Temperature and Heat

### Temperature
Measure of hotness or coldness of a body.

### Heat
Energy transferred due to temperature difference.

### Units
- Temperature: Celsius (°C), Kelvin (K), Fahrenheit (°F)
- Heat: Joule (J), calorie (cal)
- 1 cal = 4.184 J

### Temperature Conversion
- °C to K: T(K) = T(°C) + 273
- °F to °C: T(°C) = (T(°F) - 32) * 5/9

## Thermal Expansion

### Linear Expansion
**Formula:** ΔL = L₀ α ΔT
- ΔL: change in length
- L₀: original length
- α: linear expansion coefficient
- ΔT: temperature change

### Area Expansion
**Formula:** ΔA = A₀ β ΔT
- β = 2α (for most materials)

### Volume Expansion
**Formula:** ΔV = V₀ γ ΔT
- γ = 3α (for most materials)

### Applications
- Bimetallic strips in thermostats
- Railway tracks expansion joints
- Glassware in laboratories

## Heat Transfer

### Conduction
Transfer of heat through direct contact.

**Formula:** Q = (kAΔT)/d * t
- k: thermal conductivity
- A: area
- ΔT: temperature difference
- d: thickness
- t: time

### Convection
Transfer of heat by movement of fluid.

#### Natural Convection
Due to density differences (hot air rises)

#### Forced Convection
Due to external force (fans, pumps)

### Radiation
Transfer of heat by electromagnetic waves.

**Formula:** Q = σAT⁴
- σ: Stefan-Boltzmann constant (5.67 * 10^-8 W/m²K⁴)
- A: surface area
- T: absolute temperature

## Specific Heat Capacity

### Definition
Heat required to raise temperature of 1kg substance by 1K.

**Formula:** Q = mcΔT
- Q: heat energy (J)
- m: mass (kg)
- c: specific heat capacity (J/kgK)
- ΔT: temperature change (K)

### Water Equivalent
Mass of water that would absorb same heat as the substance.

## Latent Heat

### Latent Heat of Fusion
Heat required to change 1kg solid to liquid at melting point.

### Latent Heat of Vaporization
Heat required to change 1kg liquid to vapor at boiling point.

**Formula:** Q = mL
- L: latent heat (J/kg)

## First Law of Thermodynamics

### Statement
Energy cannot be created or destroyed, only converted from one form to another.

**Equation:** ΔU = Q - W
- ΔU: change in internal energy
- Q: heat added to system
- W: work done by system

### Sign Conventions
- Q positive: heat added to system
- Q negative: heat removed from system
- W positive: work done by system
- W negative: work done on system

## Heat Engines

### Efficiency
Ratio of work output to heat input.

**Formula:** η = W/Q₁ = 1 - (Q₂/Q₁)
- W: work done
- Q₁: heat input
- Q₂: heat rejected

### Carnot Engine
Theoretical maximum efficiency.

**Formula:** η = 1 - (T₂/T₁)
- T₁: hot reservoir temperature
- T₂: cold reservoir temperature

## Refrigerators and Heat Pumps

### Coefficient of Performance (COP)
**Formula:** COP = Q₂/W = T₂/(T₁ - T₂)
- Q₂: heat extracted from cold reservoir
- W: work input
- T₁, T₂: temperatures

## Nigerian Applications

### Petroleum Industry
- Oil refining processes
- Heat exchangers in refineries
- Pipeline temperature control
- Storage tank insulation

### Agriculture
- Food preservation and refrigeration
- Greenhouse temperature control
- Crop drying processes
- Cold storage facilities

### Manufacturing
- Metal working and forging
- Plastic molding processes
- Textile dyeing and finishing
- Cement production

### Domestic Applications
- Cooking and food preparation
- Water heating systems
- Air conditioning
- Refrigeration appliances

### Power Generation
- Thermal power plants
- Geothermal energy exploration
- Solar thermal systems
- Waste heat recovery

## Climate and Weather

### Greenhouse Effect
- Atmospheric heat trapping
- Global warming implications
- Nigerian climate patterns
- Desertification in northern Nigeria

### Urban Heat Islands
- Temperature differences in cities
- Lagos heat island effect
- Urban planning considerations

## Common Mistakes
- Confusing heat and temperature
- Wrong sign conventions in thermodynamics
- Incorrect unit conversions
- Misunderstanding heat transfer mechanisms
- Wrong efficiency calculations

## Practice Problems
1. Convert 25°C to Kelvin and Fahrenheit
2. Calculate change in length of 2m steel rod heated from 20°C to 50°C (α = 1.2 * 10^-5/K)
3. Find heat required to raise temperature of 2kg water from 20°C to 100°C
4. Calculate latent heat when 5kg ice at 0°C changes to water at 0°C (L = 3.34 * 10^5 J/kg)
5. Find efficiency of engine with Q₁ = 1000J, Q₂ = 600J

## WAEC Applications
- Heat transfer problems
- Specific heat calculations
- Latent heat problems
- Thermodynamic efficiency
- Nigerian climate applications

## Laboratory Activities
- Specific heat determination
- Thermal expansion measurements
- Heat transfer demonstrations
- Calorimetry experiments
- Engine efficiency calculations''',
                'summary': 'Comprehensive guide to thermodynamics, heat transfer, thermal expansion, and Nigerian energy applications',
                'learning_objectives': 'Distinguish heat and temperature,Calculate thermal expansion,Understand heat transfer mechanisms,Apply first law of thermodynamics,Analyze Nigerian energy systems',
                'key_concepts': 'Temperature and heat,Thermal expansion,Heat transfer,Thermodynamics,Heat engines',
                'important_formulas': 'Q=mcΔT,ΔL=L₀αΔT,η=1-(Q₂/Q₁),ΔU=Q-W',
                'worked_examples': 'Heat calculations,Expansion problems,Thermodynamic cycles,Efficiency calculations',
                'practice_problems': 'Heat transfer exercises,WAEC-style problems,Nigerian application problems,Thermodynamic analysis',
                'cultural_notes': 'Nigerian petroleum refining,Agricultural heat applications,Manufacturing processes,Domestic energy use,Climate change impacts'
            }
        ]

    def _get_chemistry_additional_topics(self):
        """Generate additional Chemistry topics"""

        return [
            {
                'title': 'Chemistry: Physical Chemistry - Chemical Kinetics',
                'subject': 'Chemistry',
                'topic': 'Physical Chemistry',
                'subtopic': 'Chemical Kinetics',
                'content_type': 'study_guide',
                'difficulty': 'advanced',
                'content': '''# Chemistry: Physical Chemistry - Chemical Kinetics

## Introduction
Chemical kinetics is the study of reaction rates and the factors that affect them. Understanding reaction rates is crucial for industrial processes and chemical analysis.

## Rate of Reaction
The rate of reaction is the change in concentration of reactants or products per unit time.

**Average Rate:** Total change over a period of time
**Instantaneous Rate:** Rate at a particular moment

### Units
- Rate = concentration/time
- Common units: mol dm⁻³ s⁻¹, mol L⁻¹ s⁻¹

## Factors Affecting Reaction Rates

### Concentration
- Rate ∝ [Reactants] for most reactions
- Rate = k[A]ⁿ[B]ᵐ (rate law)
- Order of reaction: n + m

### Temperature
- Rate doubles/triples for every 10°C rise (Rule of Thumb)
- Arrhenius equation: k = Ae^(-Ea/RT)
- Activation energy (Ea) determines temperature sensitivity

### Catalyst
- Increases reaction rate without being consumed
- Lowers activation energy
- Provides alternative reaction pathway

### Surface Area
- Larger surface area = faster reaction
- Important for heterogeneous reactions
- Particle size affects reaction rate

### Pressure
- Affects gaseous reactions
- Rate increases with pressure for reactions producing fewer gas molecules

## Order of Reaction

### Zero Order
- Rate = k (independent of concentration)
- Example: Decomposition on metal surfaces

### First Order
- Rate = k[A]
- Half-life constant: t½ = 0.693/k
- Examples: Radioactive decay, hydrolysis

### Second Order
- Rate = k[A]² or k[A][B]
- Half-life depends on initial concentration
- Examples: Alkaline hydrolysis of esters

## Rate Laws and Rate Constants

### Differential Rate Law
Expresses rate in terms of concentration derivatives

### Integrated Rate Law
Expresses concentration as function of time

### Zero Order: [A] = [A]₀ - kt
### First Order: ln[A] = ln[A]₀ - kt
### Second Order: 1/[A] = 1/[A]₀ + kt

## Activation Energy
- Minimum energy required for reaction
- Determined from Arrhenius plot: ln k vs 1/T
- Slope = -Ea/R

## Reaction Mechanisms
- Series of elementary steps
- Rate-determining step controls overall rate
- Molecularity vs order of reaction

## Nigerian Industrial Applications
- Petroleum refining reaction rates
- Cement manufacturing kinetics
- Food processing and preservation
- Pharmaceutical production timing
- Fertilizer manufacturing processes

## Experimental Methods
- Colorimetry for concentration measurement
- Gas collection for gaseous products
- Titration methods
- Conductivity measurements

## Common Mistakes
- Confusing order with molecularity
- Incorrect units for rate constants
- Misapplying integrated rate laws
- Forgetting temperature effects

## Practice Problems
1. For a first-order reaction, calculate half-life if k = 0.02 s⁻¹
2. Determine order of reaction from given rate data
3. Calculate activation energy from rate constants at two temperatures
4. Explain effect of catalyst on reaction rate
5. Derive integrated rate law for second-order reaction''',
                'summary': 'Comprehensive study of chemical kinetics including rates, orders, and mechanisms',
                'learning_objectives': 'Calculate reaction rates,Determine reaction orders,Understand factors affecting rates,Apply kinetics to industrial processes',
                'key_concepts': 'Reaction rates,Rate laws,Order of reaction,Activation energy,Reaction mechanisms',
                'important_formulas': 'Rate = k[A]ⁿ,Arrhenius equation: k = Ae^(-Ea/RT),Half-life equations',
                'worked_examples': 'Rate calculation,Order determination,Activation energy calculation',
                'practice_problems': 'Rate law problems,Half-life calculations,Mechanisms analysis',
                'cultural_notes': 'Applications in Nigerian petroleum, cement, and pharmaceutical industries'
            },
            {
                'title': 'Chemistry: Biochemistry - Enzymes and Metabolism',
                'subject': 'Chemistry',
                'topic': 'Biochemistry',
                'subtopic': 'Enzymes and Metabolism',
                'content_type': 'study_guide',
                'difficulty': 'advanced',
                'content': '''# Chemistry: Biochemistry - Enzymes and Metabolism

## Introduction
Biochemistry is the study of chemical processes in living organisms. Enzymes are biological catalysts that speed up metabolic reactions. Understanding enzymes and metabolism is crucial for medicine, agriculture, and biotechnology.

## Enzymes

### Definition
Proteins that act as biological catalysts, speeding up chemical reactions without being consumed.

### Characteristics
- Highly specific
- Work under mild conditions
- Can be regulated
- Recycled in reactions

### Enzyme-Substrate Complex
- Lock and key model (Emil Fischer)
- Induced fit model (Daniel Koshland)
- Active site: region where substrate binds

## Factors Affecting Enzyme Activity

### Temperature
- Optimum temperature (usually 35-40°C for human enzymes)
- Denaturation at high temperatures
- Q₁₀ rule: Rate doubles for every 10°C rise

### pH
- Optimum pH varies by enzyme
- Pepsin: pH 2 (stomach)
- Amylase: pH 7 (neutral)
- Extreme pH causes denaturation

### Substrate Concentration
- Rate increases with substrate concentration
- V_max: maximum rate when enzyme saturated
- Michaelis-Menten equation: v = V_max[S]/(K_m + [S])

### Enzyme Concentration
- Rate proportional to enzyme concentration
- Excess substrate required

### Inhibitors
- Competitive inhibitors: compete with substrate
- Non-competitive inhibitors: bind to allosteric site
- Irreversible inhibitors: permanently inactivate

## Enzyme Classification

### By Function
- Oxidoreductases: redox reactions
- Transferases: group transfers
- Hydrolases: hydrolysis reactions
- Lyases: bond cleavage
- Isomerases: isomerization
- Ligases: bond formation

### By Source
- Intracellular enzymes
- Extracellular enzymes
- Digestive enzymes

## Metabolism

### Definition
Sum of all chemical reactions in living organisms.

### Catabolism
- Breakdown of complex molecules
- Energy releasing
- Examples: glycolysis, Krebs cycle

### Anabolism
- Synthesis of complex molecules
- Energy requiring
- Examples: protein synthesis, photosynthesis

## Glycolysis

### Location
Cytoplasm of cells

### Process
- Converts glucose to pyruvate
- Anaerobic process
- Net gain: 2 ATP, 2 NADH
- Occurs in all living cells

### Steps
1. Phosphorylation of glucose
2. Isomerization to fructose-6-phosphate
3. Phosphorylation to fructose-1,6-bisphosphate
4. Cleavage to DHAP and G3P
5. Isomerization and oxidation
6. Substrate-level phosphorylation

## Krebs Cycle (Citric Acid Cycle)

### Location
Mitochondrial matrix

### Process
- Complete oxidation of acetyl-CoA
- Produces CO₂, NADH, FADH₂, ATP
- Amphibolic pathway

### Key Reactions
- Condensation with oxaloacetate
- Isomerizations and decarboxylations
- Substrate-level phosphorylation
- Regeneration of oxaloacetate

## Electron Transport Chain

### Location
Inner mitochondrial membrane

### Process
- NADH and FADH₂ oxidation
- Proton gradient formation
- ATP synthesis (oxidative phosphorylation)

### Components
- Complex I-IV: electron carriers
- ATP synthase: ATP production
- Cytochromes and iron-sulfur proteins

## Photosynthesis

### Light Reactions
- Occur in thylakoid membranes
- Light energy → ATP + NADPH
- Water splitting and oxygen evolution

### Dark Reactions (Calvin Cycle)
- Occur in stroma
- CO₂ fixation and carbohydrate synthesis
- Requires ATP and NADPH

## Nigerian Applications

### Agriculture
- Enzyme use in food processing
- Biofertilizers and biopesticides
- Crop improvement through biotechnology
- Post-harvest technology

### Medicine
- Enzyme therapy for diseases
- Diagnostic enzymes
- Drug metabolism studies
- Vaccine production

### Industry
- Brewing and fermentation
- Textile processing
- Detergent enzymes
- Waste treatment

### Food Technology
- Cheese and yogurt production
- Baking industry
- Fruit juice clarification
- Meat tenderization

## Biotechnology Applications

### Genetic Engineering
- Enzyme production through recombinant DNA
- Protein engineering
- Metabolic pathway modification

### Industrial Enzymes
- Amylase in starch hydrolysis
- Protease in detergent formulations
- Lipase in fat processing
- Cellulase in textile industry

## Common Mistakes
- Confusing competitive and non-competitive inhibition
- Incorrect glycolysis ATP accounting
- Misunderstanding enzyme specificity
- Wrong metabolic pathway sequences

## Practice Problems
1. Explain lock and key vs induced fit models
2. Calculate enzyme efficiency at different temperatures
3. Describe glycolysis steps and energy yield
4. Explain Krebs cycle role in metabolism
5. Compare photosynthesis light and dark reactions

## WAEC Applications
- Enzyme inhibition mechanisms
- Metabolic pathway questions
- Biochemical reaction calculations
- Nigerian agricultural applications
- Industrial biotechnology''',
                'summary': 'Comprehensive study of enzymes, metabolic pathways, and biochemical processes',
                'learning_objectives': 'Understand enzyme function and regulation,Explain metabolic pathways,Analyze biochemical processes,Apply biochemistry to Nigerian industries',
                'key_concepts': 'Enzymes,Metabolism,Glycolysis,Krebs cycle,Photosynthesis',
                'important_formulas': 'Michaelis-Menten: v = V_max[S]/(K_m + [S]),Enzyme kinetics',
                'worked_examples': 'Enzyme kinetics,Glycolysis calculations,Metabolic pathway analysis',
                'practice_problems': 'Enzyme problems,Metabolic pathway questions,WAEC-style biochemistry',
                'cultural_notes': 'Nigerian brewing industry,Food processing,Medical applications,Agricultural biotechnology'
            }
        ]

def main():
    """Main function to populate content"""

    populator = ContentPopulator()

    print("🚀 Starting comprehensive content population...")
    print("=" * 60)

    # Populate missing subjects
    print("📚 Populating missing subjects...")
    populator.populate_missing_subjects()

    # Populate underrepresented topics
    print("🔧 Adding underrepresented topics...")
    populator.populate_underrepresented_topics()

    print("✅ Content population completed!")
    print("📊 Run 'python content_dashboard.py --display-dashboard' to see updated statistics")

if __name__ == "__main__":
    main()
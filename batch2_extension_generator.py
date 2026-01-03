#!/usr/bin/env python3
"""
Complete Batch 2 - Generate remaining 3 lessons
Chemistry: Acids, Bases and Salts
Biology: Nutrition in Plants
Biology: Nutrition in Animals
"""

import json
from datetime import datetime
from pathlib import Path

def generate_chemistry_acids_bases():
    """Generate Chemistry: Acids, Bases and Salts lesson"""
    return {
        "id": "chem_acids_bases_salts_advanced",
        "title": "Acids, Bases and Salts: From Lagos Battery Market to Badagry Salt",
        "subject": "Chemistry",
        "topic": "Acids, Bases and Salts",
        "difficulty": "intermediate",
        "exam_weight": "very_high",
        "read_time_minutes": 25,
        "created_at": datetime.now().isoformat(),
        "learning_objectives": [
            "Identify properties of acids, bases, and salts",
            "Understand pH scale and neutralization reactions",
            "Prepare salts using different methods",
            "Apply knowledge to Nigerian industries (batteries, soap, salt production)",
            "Solve WAEC-style acid-base problems"
        ],
        "prerequisites": ["Chemical reactions", "Chemical equations", "Basic chemistry"],
        "content": """
# Acids, Bases and Salts: Chemistry in Nigerian Daily Life

## Introduction
Every day, Nigerians interact with acids, bases, and salts: car battery acid in Lagos markets (₦5,000), lime for building construction, Badagry salt production, soap making in Kano, and antacids for treating ulcers. Understanding these substances connects chemistry to Nigerian industries and daily life.

## Part 1: Properties of Acids

### Common Nigerian Acids
- **Car battery acid** (sulfuric acid, H₂SO₄) - Lagos battery markets
- **Vinegar** (acetic acid, CH₃COOH) - Nigerian cooking
- **Citrus fruits** (citric acid) - Oranges, lemons
- **Stomach acid** (hydrochloric acid, HCl) - Digestion

### Acid Properties
1. Sour taste (citrus fruits)
2. Turn blue litmus paper red
3. pH < 7
4. React with metals to produce hydrogen gas
5. React with carbonates to produce CO₂
6. Neutralize bases

### Worked Example 1: Car Battery Acid Reaction
A mechanic in Lagos adds zinc metal to dilute sulfuric acid from a battery.

**Reaction**: Zn + H₂SO₄ → ZnSO₄ + H₂

**Observation**: Bubbles of hydrogen gas, zinc dissolves

**Test**: Light a splint near gas → 'pop' sound confirms H₂

**Nigerian Context**: This reaction shows why battery terminals corrode over time and need cleaning/replacement (common issue in Nigerian vehicles).

## Part 2: Properties of Bases

### Common Nigerian Bases
- **Lime** (calcium hydroxide, Ca(OH)₂) - Building construction
- **Caustic soda** (sodium hydroxide, NaOH) - Soap making
- **Wood ash** (potassium hydroxide, KOH) - Traditional soap
- **Ammonia** (NH₃) - Cleaning products

### Base Properties
1. Bitter taste (caution: do not taste!)
2. Turn red litmus paper blue
3. pH > 7
4. Feel slippery/soapy
5. Neutralize acids

### Worked Example 2: Soap Making in Kano
Traditional soap makers mix palm oil with wood ash extract (contains KOH).

**Reaction**: Palm oil + KOH → Soap + Glycerol

**Process**:
1. Burn palm fronds to get ash
2. Dissolve ash in water (extracts KOH)
3. Filter solution
4. Heat with palm oil for 2-3 hours
5. Add salt to separate soap
6. Mold and dry

**Economics**: 10 liters palm oil (₦15,000) + ash (free) → 50 bars soap (₦20,000 revenue) = ₦5,000 profit

**Nigerian Industry**: This traditional method is still used alongside modern factories in northern Nigeria.

## Part 3: The pH Scale

### Understanding pH
- pH = power of Hydrogen
- Scale: 0 to 14
- pH 7 = Neutral (pure water)
- pH < 7 = Acidic
- pH > 7 = Basic/Alkaline

### Nigerian Examples
| Substance | pH | Category |
|-----------|----|----|
| Car battery acid | 1-2 | Strong acid |
| Vinegar (Nigerian cooking) | 2-3 | Weak acid |
| Orange juice | 3-4 | Weak acid |
| Rain water (Lagos) | 5-6 | Slightly acidic |
| Pure water | 7 | Neutral |
| Blood | 7.4 | Slightly alkaline |
| Antacid (for ulcers) | 9-10 | Base |
| Lime water (construction) | 12-13 | Strong base |
| Caustic soda (soap making) | 14 | Strong base |

### Worked Example 3: Treating Ulcers with Antacids
A patient with stomach acid (pH 2) takes an antacid tablet containing Mg(OH)₂.

**Problem**: Explain how antacid works.

**Solution**:
- Stomach acid: HCl (pH 2, excess acid causes pain)
- Antacid: Mg(OH)₂ (base)
- **Neutralization**: 2HCl + Mg(OH)₂ → MgCl₂ + 2H₂O
- Result: Acid neutralized, pH rises to ~5-6, pain relieved

**Nigerian Market**: Antacids cost ₦500-2,000 per pack, common in pharmacies nationwide.

## Part 4: Neutralization Reactions

### General Equation
**Acid + Base → Salt + Water**

### Worked Example 4: Lime in Construction (Abuja)
Construction workers mix lime Ca(OH)₂ with CO₂ from air for cement hardening.

**Reaction**: Ca(OH)₂ + CO₂ → CaCO₃ + H₂O

**Process**:
- Lime paste applied to walls
- CO₂ from air slowly reacts
- Forms hard calcium carbonate (limestone)
- Takes weeks to fully harden

**Economics**: 50kg bag lime ₦3,000, covers 20m² of wall

**Nigerian Construction**: Essential for plastering in building projects across Nigeria.

## Part 5: Preparation of Salts

### Method 1: Acid + Metal
**HCl + Zn → ZnCl₂ + H₂**

### Method 2: Acid + Metal Oxide
**H₂SO₄ + CuO → CuSO₄ + H₂O**

### Method 3: Acid + Metal Carbonate
**2HCl + CaCO₃ → CaCl₂ + H₂O + CO₂**

### Method 4: Acid + Base (Neutralization)
**HNO₃ + NaOH → NaNO₃ + H₂O**

### Worked Example 5: Badagry Salt Production
At Badagry salt flats (Lagos State), seawater is evaporated to produce table salt (NaCl).

**Process**:
1. Seawater pumped into shallow ponds
2. Sun evaporates water over 2-3 weeks
3. Salt crystals form (NaCl concentration increases)
4. Harvest and wash salt
5. Dry and package

**Yield**: 1000 liters seawater → 30 kg salt (3% concentration)

**Economics**: 
- Production cost: ₦30/kg (evaporation, labor)
- Selling price: ₦50/kg wholesale
- Annual production: 5,000+ tonnes in Badagry

**Nigerian Industry**: Badagry salt industry employs thousands, supplies Lagos markets.

### Worked Example 6: Preparing Zinc Chloride in Lab
A student prepares zinc chloride salt from zinc metal and hydrochloric acid.

**Procedure**:
1. Add excess zinc granules to dilute HCl
2. Reaction: Zn + 2HCl → ZnCl₂ + H₂↑
3. Filter to remove unreacted zinc
4. Evaporate filtrate to crystallization point
5. Cool to form ZnCl₂ crystals
6. Dry between filter papers

**Safety**: Wear goggles, acid is corrosive

**WAEC Practical**: Common exam question format

## Part 6: Nigerian Industries Using Acids, Bases, Salts

### Battery Industry (Lagos)
- Lead-acid batteries use H₂SO₄
- Market: Alaba International Market
- Price: ₦5,000-25,000 per battery
- Recycling: Old batteries bought for ₦1,500

### Soap Manufacturing (Kano)
- Traditional: Wood ash (KOH) + palm oil
- Modern: Caustic soda (NaOH) + various oils
- Annual production: 100,000+ tonnes
- Employs: 50,000+ workers

### Salt Production (Badagry)
- Seawater evaporation
- Annual yield: 5,000+ tonnes
- Supplies: Lagos markets
- Price: ₦50-80/kg wholesale

### Construction (Nationwide)
- Lime (Ca(OH)₂) for plastering
- Cement neutralization
- Annual consumption: 500,000+ tonnes
- Price: ₦3,000 per 50kg bag

## WAEC Exam Tips

1. **Memorize neutralization equation**: Acid + Base → Salt + Water
2. **pH scale**: Know which substances are acidic/basic
3. **Litmus tests**: Blue → red (acid), Red → blue (base)
4. **Salt preparation methods**: Choose correct method for given salt
5. **Balance equations**: Always balance chemical equations
6. **Safety**: Mention safety precautions in practicals
7. **Show all steps**: WAEC awards method marks

## Practice Problems

**Problem 1**: A Nigerian farmer notices his soil pH is 5 (too acidic for crops). What can he add to neutralize it?

**Problem 2**: Calculate mass of salt formed when 100ml of 1M HCl reacts with excess NaOH. (Hint: HCl + NaOH → NaCl + H₂O, find moles first)

**Problem 3**: Describe how to prepare copper(II) sulfate crystals from copper oxide and dilute sulfuric acid.

**Problem 4**: A Lagos mechanic mixes 500ml of 2M H₂SO₄ with 500ml of 2M NaOH. What is the final pH? Is it safe to touch?

## Key Formulas Summary

- **Neutralization**: Acid + Base → Salt + Water
- **Acid + Metal**: Acid + Metal → Salt + Hydrogen
- **Acid + Carbonate**: Acid + Carbonate → Salt + Water + CO₂
- **pH**: pH = -log[H⁺]

## Nigerian Context Importance

Understanding acids, bases, and salts is essential for:
- **Battery maintenance** - Car mechanics
- **Construction** - Building workers
- **Agriculture** - Soil pH management
- **Health** - Treating ulcers, understanding digestion
- **Industry** - Soap making, salt production, food processing
- **Environment** - Acid rain effects, water treatment

This knowledge connects classroom chemistry to real Nigerian livelihoods and industries!
""",
        "diagrams": ["chem_acids_bases_salts_ph_scale.png", "chem_acids_bases_salts_neutralization.png"],
        "tags": ["acids", "bases", "salts", "pH scale", "neutralization", "WAEC", "very high priority", "Badagry salt", "batteries", "soap making", "construction"],
        "nigerian_context": "Lagos battery market (₦5,000), Badagry salt production (5,000 tonnes/year), Kano soap making (traditional + modern), lime construction (₦3,000/50kg), antacids for ulcers, car battery maintenance, building plastering",
        "summary": "Comprehensive acids, bases, and salts lesson covering properties, pH scale, neutralization, and salt preparation. Nigerian contexts: Lagos car batteries, Badagry salt flats (30kg from 1000L seawater), Kano soap making (₦5,000 profit/batch), construction lime, antacids. Includes 6 worked examples with Nigerian applications.",
        "views": 0,
        "likes": 0,
        "status": "published"
    }

def generate_plant_nutrition():
    """Generate Biology: Nutrition in Plants lesson"""
    return {
        "id": "bio_nutrition_plants_advanced",
        "title": "Nutrition in Plants: From Photosynthesis to Nigerian Farms",
        "subject": "Biology",
        "topic": "Nutrition in Plants",
        "difficulty": "intermediate",
        "exam_weight": "very_high",
        "read_time_minutes": 26,
        "created_at": datetime.now().isoformat(),
        "learning_objectives": [
            "Explain photosynthesis process and factors affecting it",
            "Understand mineral nutrition in plants",
            "Identify nutrient deficiency symptoms",
            "Apply knowledge to Nigerian agriculture (cassava, yam, cocoa, maize)",
            "Solve WAEC-style plant nutrition problems"
        ],
        "prerequisites": ["Cell structure", "Plant structure", "Basic chemistry"],
        "content": """
# Nutrition in Plants: Feeding Nigeria's Farms

## Introduction
Nigeria feeds 220 million people through agriculture. From cassava farms in Benue to cocoa plantations in Ondo, from yam cultivation in Enugu to maize fields in Kaduna—all depend on plant nutrition. Understanding photosynthesis and mineral requirements is essential for Nigerian food security.

## Part 1: Photosynthesis - The Foundation

### The Process
**6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂**
(Carbon dioxide + Water → Glucose + Oxygen)

### Requirements
1. **Chlorophyll** - Green pigment in chloroplasts
2. **Light energy** - From sunlight
3. **Carbon dioxide** - From air (0.04%)
4. **Water** - From soil via roots

### Products
1. **Glucose** - Used for energy, growth, storage
2. **Oxygen** - Released to atmosphere

### Worked Example 1: Cassava Photosynthesis (Benue State)
A cassava farm in Benue has 10,000 plants. Each plant has ~200 leaves averaging 400 cm² per leaf.

**Calculate total photosynthetic surface area**.

**Solution**:
- Leaves per plant = 200
- Total plants = 10,000
- Total leaves = 200 × 10,000 = 2,000,000 leaves
- Area per leaf = 400 cm² = 0.04 m²
- Total area = 2,000,000 × 0.04 = 80,000 m²
- **Total area = 8 hectares of photosynthetic surface**

**Nigerian Context**: Large surface area explains why cassava is efficient at producing tubers (40-50 tonnes/hectare possible with good fertilizer).

## Part 2: Factors Affecting Photosynthesis

### 1. Light Intensity
- **Too low**: Slow photosynthesis (cloudy days, rainy season)
- **Optimal**: Bright sunlight (Nigerian dry season)
- **Too high**: No further increase (light saturation)

### Nigerian Example: Cocoa Under Shade
In Ondo State, cocoa trees grow under taller trees (plantain, kola).

**Why?** Young cocoa needs 50-70% shade:
- Prevents excessive light damage
- Reduces water loss
- Optimal photosynthesis at moderate light
- Mature cocoa tolerates more light

**Economics**: Shade trees = ₦50,000 investment, but increase cocoa yield by 30%

### 2. Carbon Dioxide Concentration
- Normal air: 0.04% CO₂
- Optimal: 0.1% CO₂ (2.5× normal)
- Limiting factor in closed spaces

### 3. Temperature
- **Too low** (<10°C): Enzymes inactive (not common in Nigeria)
- **Optimal**: 25-35°C (Nigerian average)
- **Too high** (>40°C): Enzymes denature, stomata close

### Worked Example 2: Maize Growth in Kaduna
In Kaduna, maize grows in two seasons:

**Dry season irrigation**:
- Temperature: 30-35°C (optimal)
- Light: High intensity (clear skies)
- Water: Supplemented by irrigation
- Growth: 3-4 months, 6-8 tonnes/hectare

**Rainy season**:
- Temperature: 25-30°C (good)
- Light: Reduced (cloudy days)
- Water: Abundant
- Growth: 4-5 months, 4-6 tonnes/hectare

**Analysis**: Dry season yields more despite needing irrigation because of higher light intensity and temperature.

### 4. Water Availability
- Required for photosynthesis
- Maintains turgor pressure
- Transport medium for nutrients
- Cooling (transpiration)

## Part 3: Mineral Nutrition

### Macronutrients (Needed in Large Amounts)

#### Nitrogen (N)
- **Function**: Protein synthesis, chlorophyll, amino acids
- **Deficiency**: Yellow older leaves, stunted growth
- **Nigerian source**: Urea (46% N), NPK fertilizer
- **Cost**: ₦15,000 per 50kg NPK 20-10-10

#### Phosphorus (P)
- **Function**: DNA, RNA, ATP (energy), root development
- **Deficiency**: Dark green/purple leaves, poor root growth
- **Nigerian source**: Single superphosphate, NPK
- **Application**: Important for yam, cassava root formation

#### Potassium (K)
- **Function**: Enzyme activation, stomata operation, disease resistance
- **Deficiency**: Yellow leaf edges, weak stems
- **Nigerian source**: Muriate of potash, NPK fertilizer

### Micronutrients (Needed in Small Amounts)
- Iron (Fe) - Chlorophyll synthesis
- Magnesium (Mg) - Center of chlorophyll molecule
- Calcium (Ca) - Cell wall formation
- Sulfur (S) - Protein synthesis

### Worked Example 3: NPK Fertilizer Application (Benue Cassava Farm)
A farmer applies NPK 20-10-10 at 300 kg/hectare on 5 hectares.

**Calculate nutrients applied:**

**Solution**:
- Total NPK = 300 kg/ha × 5 ha = 1,500 kg
- **Nitrogen**: 20% of 1,500 = 300 kg pure N
- **Phosphorus**: 10% of 1,500 = 150 kg pure P₂O₅
- **Potassium**: 10% of 1,500 = 150 kg pure K₂O

**Cost**: 1,500 kg ÷ 50 kg/bag = 30 bags
30 bags × ₦15,000 = **₦450,000 total fertilizer cost**

**Expected yield increase**: 
- Without fertilizer: 15 tonnes/ha
- With fertilizer: 30-40 tonnes/ha
- Extra yield: 15-25 tonnes/ha × 5 ha = 75-125 tonnes
- @ ₦50,000/tonne = ₦3.75-6.25M revenue
- **Profit after fertilizer**: ₦3.3-5.8M

**ROI**: 733-1289% return on fertilizer investment!

## Part 4: Nutrient Deficiency in Nigerian Crops

### Nitrogen Deficiency (Most Common)
**Symptoms**:
- Yellowing of older leaves (chlorosis)
- Stunted growth
- Thin, weak stems

**Nigerian crops affected**: Maize, rice, vegetables

**Solution**: Apply urea (46% N) at 100-200 kg/ha or NPK

**Prevention**: Regular fertilizer application, crop rotation with legumes (beans, cowpea)

### Phosphorus Deficiency
**Symptoms**:
- Dark green or purple leaves
- Poor root development
- Delayed maturity

**Nigerian crops affected**: Yam, cassava, sweet potato

**Solution**: Single superphosphate at planting

### Iron Deficiency (Chlorosis)
**Symptoms**:
- Yellow young leaves (veins stay green)
- Interveinal chlorosis

**Nigerian crops affected**: Citrus, vegetables in alkaline soils

**Solution**: Foliar spray of iron chelate, adjust soil pH

### Worked Example 4: Diagnosing Maize Deficiency (Kaduna)
A farmer notices his maize has:
- Yellow older leaves
- Thin, weak stems  
- Slow growth despite adequate water

**Diagnosis**: Nitrogen deficiency

**Treatment**:
1. Apply urea (46% N) at 150 kg/hectare
2. Or NPK 20-10-10 at 200 kg/hectare
3. Split application: Half at 3 weeks, half at 6 weeks
4. Expect improvement in 1-2 weeks

**Cost**: Urea 150kg @ ₦20,000/50kg = ₦60,000/hectare

## Part 5: Transport in Plants

### Xylem (Water & Minerals Up)
- Dead cells forming tubes
- Transport from roots to leaves
- Driven by transpiration pull
- Contains dissolved minerals (N, P, K, etc.)

### Phloem (Sugars/Food Down)
- Living cells (sieve tubes)
- Transport sugars from leaves to storage organs
- Bidirectional flow
- Active transport (requires energy)

### Worked Example 5: Water Uptake in Palm Trees (Southeast Nigeria)
An oil palm tree in Imo State transpires 40 liters of water daily during dry season.

**Calculate weekly water requirement:**

**Solution**:
- Daily: 40 liters
- Weekly: 40 × 7 = 280 liters = 280 kg water
- Annual: 40 × 365 = 14,600 liters ≈ 14.6 tonnes

**Implication**: This water carries dissolved NPK nutrients from soil to leaves. Without adequate soil moisture, nutrient uptake is impaired even with fertilizer application.

**Nigerian farming practice**: Mulching around palm base conserves soil moisture, reduces transpiration losses.

## Part 6: Nigerian Agricultural Applications

### Cassava Farming (40 million tonnes/year)
- Main producing states: Benue, Cross River, Delta
- NPK requirement: 300-400 kg/ha (20-10-10)
- Yield: 15-40 tonnes/ha depending on fertilizer
- Market price: ₦50,000/tonne (₦750,000-2M/ha revenue)

### Yam Cultivation (47 million tonnes/year - world's largest)
- Main states: Benue, Taraba, Enugu, Niger
- High P requirement for tuber development
- NPK 12-12-17 at 300 kg/ha
- Yield: 15-30 tonnes/ha
- Price: ₦200-300/kg (₦3-9M/ha revenue)

### Cocoa Production (250,000+ tonnes/year)
- Main states: Ondo, Cross River, Osun, Edo
- Shade requirements (50-70% for young trees)
- NPK 15-15-15 at 200 kg/ha
- Yield: 400-800 kg/ha dried beans
- Export price: ₦1,500-2,000/kg

### Maize Farming (11 million tonnes/year)
- Main states: Kaduna, Kano, Niger, Taraba
- N requirement very high (urea 200-300 kg/ha)
- Yield: 4-8 tonnes/ha
- Price: ₦200/kg (₦800,000-1.6M/ha)

## WAEC Exam Tips

1. **Photosynthesis equation**: Memorize word and chemical equations
2. **Limiting factors**: Understand light, CO₂, temperature, water
3. **Deficiency symptoms**: Yellow older leaves = N, Purple = P, Yellow edges = K
4. **Practical skills**: Test for starch (iodine), test for CO₂ (limewater)
5. **Nigerian examples**: Use local crops in answers (cassava, yam, maize)
6. **Show calculations**: NPK percentages, fertilizer quantities
7. **Draw diagrams**: Chloroplast structure, leaf cross-section

## Practice Problems

**Problem 1**: A 10-hectare cassava farm requires NPK 20-10-10 at 300 kg/ha. Calculate:
(a) Total fertilizer needed (kg)
(b) Number of 50kg bags
(c) Total cost @ ₦15,000/bag
(d) Pure nitrogen applied

**Problem 2**: Describe three factors that limit photosynthesis in Nigerian cocoa farms and how farmers overcome each.

**Problem 3**: A maize farmer notices yellow older leaves and stunted growth. Diagnose the deficiency and recommend treatment with calculations.

## Key Equations Summary

- **Photosynthesis**: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂
- **NPK Calculation**: (% N/100) × Total fertilizer = Pure N
- **Fertilizer Cost**: (Total kg ÷ 50 kg/bag) × ₦15,000/bag

## Nigerian Context Importance

Plant nutrition knowledge is critical for:
- **Food security** - Feeding 220M+ population
- **Farmer income** - 70% of rural livelihoods
- **Export earnings** - Cocoa, cashew, sesame
- **Industrial raw materials** - Cassava (starch), palm oil
- **Environmental sustainability** - Proper fertilizer use
- **Career opportunities** - Agronomy, agribusiness

Understanding photosynthesis and mineral nutrition empowers Nigerian farmers to increase yields, improve incomes, and ensure food security!
""",
        "diagrams": ["bio_nutrition_plants_photosynthesis.png", "bio_nutrition_plants_deficiencies.png"],
        "tags": ["photosynthesis", "plant nutrition", "fertilizer", "NPK", "cassava", "yam", "cocoa", "maize", "WAEC", "very high priority", "Nigerian agriculture"],
        "nigerian_context": "Cassava farming Benue (40M tonnes/year), yam cultivation (world's largest 47M tonnes), cocoa Ondo (250k tonnes), maize Kaduna (11M tonnes), NPK fertilizer (₦15,000/50kg), nutrient deficiencies, palm oil Southeast, farmer economics",
        "summary": "Plant nutrition lesson covering photosynthesis (6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂), limiting factors, mineral requirements (NPK), deficiency symptoms, and transport. Nigerian agriculture focus: Cassava 40M tonnes/year, yam 47M tonnes (world's largest), cocoa Ondo, maize Kaduna. Includes fertilizer economics: ₦450k investment → ₦3.3-5.8M profit (733-1289% ROI).",
        "views": 0,
        "likes": 0,
        "status": "published"
    }

def generate_animal_nutrition():
    """Generate Biology: Nutrition in Animals lesson"""
    return {
        "id": "bio_nutrition_animals_advanced",
        "title": "Nutrition in Animals: From Nigerian Foods to Human Digestion",
        "subject": "Biology",
        "topic": "Nutrition in Animals",
        "difficulty": "intermediate",
        "exam_weight": "very_high",
        "read_time_minutes": 27,
        "created_at": datetime.now().isoformat(),
        "learning_objectives": [
            "Identify classes of food and their functions",
            "Understand human digestive system",
            "Explain digestion and absorption processes",
            "Perform food tests for nutrients",
            "Apply knowledge to Nigerian diet and nutrition"
        ],
        "prerequisites": ["Cell structure", "Human anatomy", "Basic chemistry"],
        "content": """
# Nutrition in Animals: Understanding the Nigerian Diet

## Introduction
Nigeria's rich culinary tradition—Jollof rice, Egusi soup, Pounded yam, Suya, Moi-moi—provides the nutrients our bodies need. Understanding nutrition helps explain why a balanced Nigerian diet includes these foods and how our digestive system processes them.

## Part 1: Classes of Food

### 1. Carbohydrates (Energy Foods)
**Function**: Provide energy (1g = 4 kcal)

**Nigerian sources**:
- **Rice** (Jollof rice) - 80% carbohydrate
- **Yam** (Pounded yam, boiled yam) - 28% carbohydrate
- **Cassava** (Garri, fufu) - 38% carbohydrate
- **Maize** (Corn, pap/ogi) - 75% carbohydrate
- **Plantain** (Dodo, boiled) - 32% carbohydrate

**Types**:
- **Simple sugars**: Glucose, fructose (fruits, honey)
- **Complex starches**: Rice, yam, cassava

**Daily requirement**: 300-400g (60% of total energy)

### 2. Proteins (Body-building Foods)
**Function**: Growth, repair, enzymes, antibodies (1g = 4 kcal)

**Nigerian sources**:
- **Beans** (Moi-moi, Akara) - 22% protein
- **Fish** (Tilapia, catfish, stockfish) - 20-25% protein
- **Meat** (Beef, goat, chicken, suya) - 20-25% protein
- **Eggs** - 13% protein
- **Groundnuts** - 25% protein
- **Soy beans** - 36% protein

**Types**:
- **Complete proteins**: Meat, fish, eggs (contain all essential amino acids)
- **Incomplete proteins**: Beans, nuts (lack some amino acids)

**Daily requirement**: 50-70g for adults

### 3. Fats and Oils (Energy Storage)
**Function**: Energy storage, insulation, vitamin absorption (1g = 9 kcal - highest energy)

**Nigerian sources**:
- **Palm oil** (Red oil) - Used in soups, stews
- **Groundnut oil** - For frying
- **Coconut oil** - Traditional cooking
- **Butter/margarine** - Bread, baking
- **Fish oil** (from oily fish)

**Daily requirement**: 50-70g (25-30% of total energy)

### 4. Vitamins (Regulatory/Protective)
**Function**: Regulate body processes, prevent diseases

**Key vitamins in Nigerian diet**:
- **Vitamin A**: Palm oil (red color = carotene), carrots, green vegetables
  - Deficiency: Night blindness, dry skin
- **Vitamin C**: Oranges, tomatoes, peppers
  - Deficiency: Scurvy (bleeding gums)
- **Vitamin D**: Fish, eggs, sunshine (Nigeria has plenty!)
  - Deficiency: Rickets (soft bones in children)
- **Vitamin B complex**: Yam, rice, beans, meat
  - Deficiency: Beriberi, anemia

### 5. Minerals (Regulatory/Structural)
**Function**: Bones, teeth, blood, enzymes

**Key minerals**:
- **Calcium**: Milk, fish (bones), vegetables
  - Function: Strong bones and teeth
- **Iron**: Meat, beans, green vegetables
  - Function: Hemoglobin (carries oxygen)
  - Deficiency: Anemia (common in Nigeria)
- **Iodine**: Iodized salt, fish
  - Function: Thyroid hormone
  - Deficiency: Goiter (swollen neck)

### 6. Water
**Function**: Transport, temperature regulation, chemical reactions

**Daily requirement**: 2-3 liters (8-10 glasses)

**Nigerian context**: Pure water sachets (₦10 each), boreholes, treated tap water

### 7. Fiber (Roughage)
**Function**: Aids digestion, prevents constipation

**Nigerian sources**: Vegetables, fruits, whole grains, beans

## Part 2: Balanced Diet - The Nigerian Approach

### Traditional 6-3-1 Method
Nigerian nutritionists recommend:
- **6 portions**: Carbohydrates (Rice, yam, garri, etc.)
- **3 portions**: Proteins (Fish, meat, beans)
- **1 portion**: Vegetables/fruits

### Sample Balanced Nigerian Meals

#### Breakfast (₦500-800)
- Bread + Akara + Pap
- OR Boiled yam + egg sauce
- OR Plantain + beans

#### Lunch/Dinner (₦1,200-2,000)
- **Main**: Jollof rice with chicken/fish
- **Soup option**: Egusi soup + pounded yam + beef
- **Swallow option**: Eba + vegetable soup + fish
- **Side**: Salad, fruit

**Daily cost for balanced diet in Lagos**: ₦1,500-2,500

### Worked Example 1: Calculating Daily Nutrition Needs
A 70kg adult male in Lagos needs:
- Energy: 2,500 kcal/day
- Protein: 56g/day (0.8g per kg body weight)
- Fat: 70g/day

**Sample menu**:
- **Breakfast**: Bread (200 kcal) + Akara (150 kcal) + Pap (100 kcal) = 450 kcal, 12g protein
- **Lunch**: Jollof rice (400 kcal) + Chicken (200 kcal) + Salad (50 kcal) = 650 kcal, 25g protein
- **Dinner**: Pounded yam (500 kcal) + Egusi soup (300 kcal) + Fish (150 kcal) = 950 kcal, 30g protein
- **Snacks**: Fruits, nuts (400 kcal), 8g protein

**Total**: 2,450 kcal, 75g protein ✅ **Meets requirements**

## Part 3: Human Digestive System

### Organs and Functions

#### 1. Mouth (Oral Cavity)
**Process**: Mechanical digestion (chewing), chemical digestion (saliva)
- **Teeth**: Break food into smaller pieces
- **Saliva**: Contains amylase enzyme
- **Reaction**: Starch → Maltose (sugar)

**Nigerian example**: Chewing pounded yam requires strong molars; saliva begins breaking down starch immediately.

#### 2. Esophagus (Food Pipe)
**Process**: Peristalsis (wave-like muscle contractions push food down)
- Length: ~25 cm
- Time: 10-15 seconds for food to reach stomach

#### 3. Stomach
**Process**: Mechanical churning + chemical digestion
- **Gastric juice**: Contains HCl (pH 2) + pepsin enzyme
- **Reaction**: Proteins → Peptides
- **Time**: Food stays 2-4 hours

**Nigerian example**: After eating suya (protein), pepsin breaks down meat proteins. Acidic environment kills bacteria.

#### 4. Small Intestine (6-7 meters long)
**Three parts**: Duodenum, Jejunum, Ileum

**Duodenum** (first 25cm):
- **Bile** (from liver): Emulsifies fats
- **Pancreatic juice**: Contains lipase, amylase, trypsin
- **Reactions**:
  - Fats → Fatty acids + Glycerol (lipase)
  - Starch → Maltose → Glucose (amylase)
  - Proteins → Amino acids (trypsin)

**Jejunum & Ileum**:
- **Absorption**: Nutrients absorbed through villi into bloodstream
- **Surface area**: Increased by millions of villi (finger-like projections)

**Nigerian example**: After eating Egusi soup (high fat content), bile emulsifies the palm oil into tiny droplets, then lipase breaks them down for absorption.

#### 5. Large Intestine (Colon)
**Process**: Water reabsorption, formation of feces
- Length: 1.5 meters
- **Time**: 12-24 hours
- **Absorption**: Water, vitamins

**Nigerian context**: Adequate fiber (from vegetables) prevents constipation by retaining water in colon.

#### 6. Rectum and Anus
**Process**: Storage and elimination of feces (egestion)

### Worked Example 2: Digestion Timeline for Nigerian Meal
A person eats Jollof rice + chicken at 2:00 PM.

**Timeline**:
- **2:00 PM**: Mouth - Chewing, saliva begins starch digestion
- **2:01 PM**: Swallowing, esophagus transport (15 seconds)
- **2:01-6:00 PM**: Stomach - Protein digestion (4 hours)
- **6:00-8:00 PM**: Small intestine - Complete digestion and absorption (2 hours)
- **8:00 PM-10:00 AM** (next day): Large intestine - Water absorption (14 hours)
- **10:00 AM**: Egestion (feces)

**Total time**: Mouth to anus = ~20 hours

## Part 4: Absorption and Assimilation

### Villi Structure (Small Intestine)
- **Shape**: Finger-like projections
- **Function**: Increase surface area for absorption
- **Structure**:
  - Thin wall (one cell thick)
  - Rich blood supply (capillaries)
  - Lacteal (for fat absorption)

### What Gets Absorbed Where

**Small intestine**:
- Glucose → Blood → Liver → Body cells
- Amino acids → Blood → Liver → Body cells
- Fatty acids + Glycerol → Lymph → Blood
- Vitamins, minerals → Blood

**Large intestine**:
- Water → Blood
- Vitamins (K, B12 produced by bacteria) → Blood

### Assimilation
Nutrients used by body cells:
- **Glucose**: Respiration for energy (or stored as glycogen)
- **Amino acids**: Build new proteins (muscles, enzymes)
- **Fatty acids**: Energy storage (or cell membranes)

## Part 5: Food Tests (WAEC Practicals)

### Test for Starch (Iodine Test)
- **Reagent**: Iodine solution (brown)
- **Positive result**: Blue-black color
- **Nigerian foods**: Yam, cassava, rice, maize

**Procedure**:
1. Grind food sample
2. Add 2-3 drops iodine solution
3. Observe color change

### Test for Reducing Sugars (Benedict's Test)
- **Reagent**: Benedict's solution (blue)
- **Method**: Heat in water bath
- **Positive result**: Green → Yellow → Orange → Brick-red (depending on sugar concentration)
- **Nigerian foods**: Fruits, honey

### Test for Proteins (Biuret Test)
- **Reagents**: NaOH + Copper sulfate
- **Positive result**: Purple/violet color
- **Nigerian foods**: Beans, fish, meat, eggs

### Test for Fats (Grease Spot Test)
- **Method**: Rub food on filter paper, hold against light
- **Positive result**: Translucent (greasy) spot
- **Nigerian foods**: Palm oil, groundnut oil, butter

### Worked Example 3: Testing Nigerian Foods
A student tests four foods: Garri, groundnut, orange juice, fish.

**Results**:
| Food | Iodine | Benedict's | Biuret | Grease Spot |
|------|--------|------------|--------|-------------|
| Garri | Blue-black | Negative | Negative | Negative |
| Groundnut | Negative | Negative | Purple | Translucent |
| Orange juice | Negative | Orange | Negative | Negative |
| Fish | Negative | Negative | Purple | Slight translucent |

**Conclusion**:
- Garri: Rich in starch
- Groundnut: Contains protein and fat
- Orange juice: Contains reducing sugars (fructose, glucose)
- Fish: Contains protein and some fat

## Part 6: Malnutrition in Nigerian Context

### Protein-Energy Malnutrition

#### Kwashiorkor
**Cause**: Severe protein deficiency (child weaned to starchy diet)
**Symptoms**:
- Swollen belly (fluid retention)
- Thin limbs
- Skin lesions
- Hair discoloration (orange/red)

**Nigerian context**: Common in rural areas where children eat mostly garri/pap with little protein

**Prevention**: Include beans, fish, eggs in children's diet

#### Marasmus
**Cause**: Severe calorie and protein deficiency
**Symptoms**:
- Extreme thinness
- Wrinkled skin
- No fat or muscle

**Prevention**: Adequate food quantity and quality

### Vitamin Deficiencies

#### Vitamin A Deficiency
**Symptoms**: Night blindness, dry eyes
**Nigerian prevention**: Red palm oil (rich in carotene), carrots

#### Vitamin C Deficiency (Scurvy)
**Symptoms**: Bleeding gums, slow wound healing
**Nigerian prevention**: Oranges (₦50-100 each), tomatoes, peppers

#### Iron Deficiency (Anemia)
**Symptoms**: Fatigue, pale skin, dizziness
**Common in**: Pregnant women, children
**Nigerian prevention**: Red meat, beans, green vegetables, iron supplements

## WAEC Exam Tips

1. **Food classes**: Memorize all 7 classes and Nigerian examples
2. **Digestive system**: Draw and label diagram accurately
3. **Enzymes**: Know where each enzyme works (amylase, pepsin, lipase, trypsin)
4. **Food tests**: Learn all 4 tests, reagents, and results
5. **Balanced diet**: Use Nigerian foods in explanations
6. **Deficiency diseases**: Link to symptoms and prevention
7. **Show calculations**: Energy content, daily requirements

## Practice Problems

**Problem 1**: Plan a balanced Nigerian meal for a family of 4 with ₦5,000 budget. Include all food classes and calculate portions.

**Problem 2**: Explain how Egusi soup provides a balanced meal. Identify carbohydrates, proteins, fats, vitamins, and minerals present.

**Problem 3**: A student performs food tests on groundnut. Predict results for iodine test, Benedict's test, Biuret test, and grease spot test. Explain your reasoning.

**Problem 4**: Calculate daily calorie needs for a 60kg woman and design a Nigerian meal plan to meet this requirement.

## Key Equations Summary

- **Energy content**: Carbohydrates = 4 kcal/g, Proteins = 4 kcal/g, Fats = 9 kcal/g
- **Protein requirement**: 0.8g per kg body weight
- **Daily water**: 2-3 liters (8-10 glasses)
- **BMI**: Weight (kg) ÷ Height² (m²)

## Nigerian Context Importance

Understanding nutrition is essential for:
- **Personal health** - Preventing malnutrition and obesity
- **Family planning** - Feeding children and pregnant women properly
- **Economic decision** - Smart food budgeting (₦1,500-2,500/day)
- **Disease prevention** - Avoiding kwashiorkor, anemia, scurvy
- **Academic success** - Proper brain function requires balanced diet
- **Career paths** - Nutritionists, dietitians, food scientists

Nigeria's rich food diversity provides all necessary nutrients when properly combined!
""",
        "diagrams": ["bio_nutrition_animals_digestive_system.png", "bio_nutrition_animals_food_tests.png"],
        "tags": ["nutrition", "digestive system", "food tests", "balanced diet", "malnutrition", "WAEC", "very high priority", "Nigerian foods", "Jollof rice", "proteins", "carbohydrates"],
        "nigerian_context": "Jollof rice, Egusi soup, Pounded yam, Suya, Moi-moi, Akara, Nigerian balanced diet (6-3-1 method), daily food cost (₦1,500-2,500 Lagos), kwashiorkor prevention, food tests on Nigerian foods (garri, groundnut, fish), palm oil vitamin A, anemia in pregnant women",
        "summary": "Animal nutrition lesson covering 7 food classes, balanced Nigerian diet (₦1,500-2,500/day Lagos), human digestive system (mouth to anus 20-hour timeline), absorption via villi, food tests (iodine, Benedict's, Biuret, grease spot), and malnutrition (kwashiorkor, marasmus). Nigerian foods featured: Jollof rice, Egusi soup, Pounded yam, beans, fish. Includes meal planning and economic calculations.",
        "views": 0,
        "likes": 0,
        "status": "published"
    }

def complete_batch2():
    """Generate and save all 3 remaining lessons"""
    print("=" * 70)
    print("COMPLETING BATCH 2 - FINAL 3 LESSONS")
    print("=" * 70)
    
    lessons = []
    
    print("\n[1/3] Generating Chemistry: Acids, Bases and Salts...")
    lessons.append(generate_chemistry_acids_bases())
    print("   ✅ Complete (25 min read)")
    
    print("\n[2/3] Generating Biology: Nutrition in Plants...")
    lessons.append(generate_plant_nutrition())
    print("   ✅ Complete (26 min read)")
    
    print("\n[3/3] Generating Biology: Nutrition in Animals...")
    lessons.append(generate_animal_nutrition())
    print("   ✅ Complete (27 min read)")
    
    # Save to batch2_extension.json
    output_path = Path("generated_content/batch2_extension.json")
    
    with open(output_path, "w") as f:
        json.dump({
            "metadata": {
                "version": "2.1",
                "total_items": 3,
                "generator": "Batch2Extension",
                "generated_date": datetime.now().isoformat(),
                "total_read_time_minutes": sum(l["read_time_minutes"] for l in lessons),
                "exam_board": "WAEC"
            },
            "content": lessons
        }, f, indent=2)
    
    print(f"\n💾 Saved to: {output_path}")
    print("\n" + "=" * 70)
    print("BATCH 2 COMPLETE - 5 LESSONS TOTAL")
    print("=" * 70)
    print(f"\n📚 Total lessons: 5 (2 earlier + 3 now)")
    print(f"📊 Total read time: ~138 minutes")
    print(f"✅ Coverage: Trigonometry, Work/Energy, Acids/Bases, Plant Nutrition, Animal Nutrition")
    print("\nNext: Deploy to Wave 3 platform (run batch2_content_deployer.py)")

if __name__ == "__main__":
    complete_batch2()

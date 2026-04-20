
import { useMemo, useState } from "react";

function App() {
const [activeTab, setActiveTab] = useState(null);
    const [language, setLanguage] = useState("en");

  const translations = {
    en: {
      appName: "Skincare AI",
      productDetails: "Product Details",
productNameLabel: "Name",
category: "Category",
      score: "Score",
      unnamedProduct: "Unnamed Product",

noBrand: "No Brand",
source: "Source",
localDataset: "Local Dataset",
externalPreview: "External Preview",
nameBasedFallback: "Name-Based Fallback",
      ingredients: "Ingredients",
ingredientsPlaceholder: "Example: Retinol, Niacinamide, Hyaluronic Acid",
checkIngredients: "Check Ingredients",
      enterProductNameAlert: "Please enter a product name.",
      routineTitle: "Build My Routine",
      productNotFoundExternalPreview: "Product not found in local dataset. Displaying external-source preview.",
productNotFoundNameFallback: "Product not found in local dataset or external preview list. Showing name-based fallback only.",
routineSubtitle: "Create a customized skincare routine based on your skin type and main concern.",
mainConcern: "Main Concern",
selectMainConcern: "Select main concern",
buildMyRoutine: "Build My Routine",
selectedProfile: "Selected Profile",
concern: "Concern",
morningRoutine: "Morning Routine",
nightRoutine: "Night Routine",
suggestedProducts: "Suggested Products",
orderOfUse: "Order of Use",
aiNotes: "AI Notes",
oily: "Oily",
dry: "Dry",
combination: "Combination",
sensitive: "Sensitive",
acne: "Acne",
dryness: "Dryness",
pigmentation: "Pigmentation",
generalCare: "General Care",
      productLabel: "Product",
      ingredientCheckerTitle: "Ingredient Checker",
ingredientCheckerSubtitle: "Enter ingredients separated by commas to review ingredient-to-ingredient logic, caution, conflicts, synergy, notes, and strength.",
      history: "History",
      welcome: "Welcome to Skincare AI",
      subtitle: "Analyze your skincare products intelligently ✨",
      interaction: "Interaction",
      productAnalyzer: "Product Analyzer",
      ingredientChecker: "Ingredient Checker",
      routine: "Routine",
      interactionTitle: "Interaction Analysis",
interactionSubtitle: "Add your skincare products and check if they work well together.",
productName: "Product Name",
brand: "Brand",
addProduct: "+ Add Product",
skinType: "Skin Type",
selectSkinType: "Select skin type",
analyze: "Analyze My Products",
alertEnter2Products: "Please enter at least 2 products.",
alertSelectSkinType: "Please select a skin type.",
productAnalyzerTitle: "Product Analyzer",
productAnalyzerSubtitle: "Enter a product name and brand to preview category, full ingredients, active ingredients, suitability, warnings, and product details.",
analyzeProduct: "Analyze Product",  
enterProductName: "Enter product name",  
enterBrandName: "Enter brand name",  
conflict: "Conflict",
caution: "Caution",
safe: "Safe",
skinTypeLabel: "Skin Type",
products: "Products",


interactionConflictSummary: "These products may strongly conflict and could irritate the skin when used together.",
interactionConflictWhy1: "Retinol combined with strong exfoliating ingredients can increase irritation.",
interactionConflictWhy2: "This combination may weaken the skin barrier, especially for sensitive users.",
interactionConflictRec1: "Avoid using these products in the same routine.",
interactionConflictRec2: "Use one product in the morning and the other at night only if appropriate.",
interactionConflictRec3: "Start slowly and patch test first.",

interactionCautionSummary: "Some ingredients may cause irritation when combined. Use with caution.",
interactionCautionWhy1: "Some active ingredients may be too strong when layered together.",
interactionCautionWhy2: "Skin irritation depends on concentration, formulation, and skin type.",
interactionCautionRec1: "Use the products at different times of day.",
interactionCautionRec2: "Do not introduce all active products at once.",
interactionCautionRec3: "Monitor your skin for irritation or dryness.",

interactionSafeSummary: "These products appear generally compatible in this preview analysis.",
interactionSafeWhy1: "No strong conflict was detected in this simplified compatibility logic.",
interactionSafeWhy2: "The selected products seem more suitable to be used in the same overall routine.",
interactionSafeRec1: "Apply products in a gentle order from light to heavy texture.",
interactionSafeRec2: "Keep monitoring your skin response over time.",
interactionSafeRec3: "Use sunscreen in daytime routines when needed.", 
fallbackSourceNotes: "Fallback Source Notes",
whyThisResult: "Why this result",
recommendations: "Recommendations",     
},
    ar: {
      appName: "ذكاء العناية بالبشرة",
      productLabel: "المنتج",
      productDetails: "تفاصيل المنتج",
productNameLabel: "الاسم",
category: "الفئة",
      ingredients: "المكوّنات",
      unnamedProduct: "منتج غير مسمّى",
noBrand: "من دون ماركة",
source: "المصدر",
localDataset: "قاعدة البيانات المحلية",
externalPreview: "معاينة خارجية",
nameBasedFallback: "نتيجة تقريبية بالاسم",
ingredientsPlaceholder: "مثال: ريتينول، نياسيناميد، حمض الهيالورونيك",
checkIngredients: "فحص المكوّنات",
      enterProductNameAlert: "يرجى إدخال اسم المنتج.",
      history: "السجل",
      welcome: "مرحبًا بك في Skincare AI",
      subtitle: "حلّل منتجات العناية بالبشرة بذكاء ✨",
      interaction: "التفاعل",
      productAnalyzer: "تحليل المنتج",
      ingredientCheckerTitle: "فحص المكوّنات",
ingredientCheckerSubtitle: "أدخلي المكوّنات مفصولة بفواصل لتحليل التفاعل بينها، والتحذيرات، والتعارض، والتوافق، والملاحظات.",
      ingredientChecker: "فحص المكوّنات",
      routine: "الروتين",
     productNotFoundExternalPreview: "المنتج غير موجود في قاعدة البيانات المحلية. يتم عرض معاينة من مصدر خارجي.",
productNotFoundNameFallback: "المنتج غير موجود في قاعدة البيانات المحلية ولا في قائمة المعاينة الخارجية. يتم عرض نتيجة تقريبية بالاعتماد على الاسم فقط.", 
      score: "النتيجة",
      interactionTitle: "تحليل التفاعل",
     skinTypeLabel: "نوع البشرة",
products: "المنتجات",
routineTitle: "بناء الروتين",
routineSubtitle: "أنشئي روتين عناية مخصصًا حسب نوع بشرتك والمشكلة الأساسية.",
mainConcern: "المشكلة الأساسية",
selectMainConcern: "اختاري المشكلة الأساسية",
buildMyRoutine: "بناء الروتين",
selectedProfile: "الملف المختار",
concern: "المشكلة",
morningRoutine: "روتين الصباح",
nightRoutine: "روتين المساء",
suggestedProducts: "المنتجات المقترحة",
orderOfUse: "ترتيب الاستخدام",
aiNotes: "ملاحظات الذكاء الاصطناعي",
oily: "دهنية",
dry: "جافة",
combination: "مختلطة",
sensitive: "حساسة",
acne: "حب الشباب",
dryness: "الجفاف",
pigmentation: "التصبغات",
generalCare: "عناية عامة",

interactionSubtitle: "أضيفي منتجاتك وشوفي إذا بيتوافقوا مع بعض.",
productName: "اسم المنتج",
brand: "الماركة",
addProduct: "+ إضافة منتج",
skinType: "نوع البشرة",
selectSkinType: "اختاري نوع البشرة",
analyze: "تحليل المنتجات",
alertEnter2Products: "الرجاء إدخال منتجين على الأقل.",
alertSelectSkinType: "الرجاء اختيار نوع البشرة.",
productAnalyzerTitle: "تحليل المنتج",
productAnalyzerSubtitle: "أدخلي اسم المنتج والماركة لعرض الفئة والمكونات الكاملة والمكونات الفعالة ومدى المناسبة والتحذيرات والتفاصيل.",
analyzeProduct: "تحليل المنتج",
enterProductName: "أدخلي اسم المنتج",
enterBrandName: "أدخلي اسم الماركة",
conflict: "تعارض",
caution: "حذر",
safe: "آمن",

interactionConflictSummary: "قد تتعارض هذه المنتجات بشكل قوي وقد تسبب تهيّجًا عند استخدامها معًا.",
interactionConflictWhy1: "دمج الريتينول مع مكوّنات التقشير القوية قد يزيد التهيّج.",
interactionConflictWhy2: "هذا المزيج قد يضعف حاجز البشرة، خصوصًا للبشرة الحساسة.",
interactionConflictRec1: "تجنّبي استخدام هذه المنتجات في نفس الروتين.",
interactionConflictRec2: "يمكن استخدام أحدها صباحًا والآخر ليلًا إذا كان ذلك مناسبًا.",
interactionConflictRec3: "ابدئي تدريجيًا وجرّبي اختبار حساسية أولًا.",

interactionCautionSummary: "بعض المكوّنات قد تسبب تهيّجًا عند دمجها. استخدميها بحذر.",
interactionCautionWhy1: "بعض المواد الفعالة قد تكون قوية جدًا عند استخدامها معًا.",
interactionCautionWhy2: "التهيّج يعتمد على التركيز والتركيبة ونوع البشرة.",
interactionCautionRec1: "استخدمي المنتجات في أوقات مختلفة من اليوم.",
interactionCautionRec2: "لا تدخلي كل المواد الفعالة مرة واحدة.",
interactionCautionRec3: "راقبي بشرتك لأي تهيّج أو جفاف.",

interactionSafeSummary: "تبدو هذه المنتجات متوافقة بشكل عام في هذا التحليل المبدئي.",
interactionSafeWhy1: "لم يتم اكتشاف تعارض قوي في منطق التوافق المبسّط الحالي.",
interactionSafeWhy2: "تبدو المنتجات المختارة أنسب للاستخدام ضمن نفس الروتين بشكل عام.",
interactionSafeRec1: "طبّقي المنتجات بترتيب لطيف من الأخف إلى الأثقل.",
interactionSafeRec2: "استمرّي بمراقبة استجابة بشرتك مع الوقت.",
interactionSafeRec3: "استخدمي واقي الشمس في الروتين النهاري عند الحاجة.",
fallbackSourceNotes: "ملاحظات المصدر البديل",
whyThisResult: "سبب هذه النتيجة",
recommendations: "التوصيات",
    },
    fr: {
      appName: "Skincare AI",
      productLabel: "Produit",
      productDetails: "Détails du produit",
productNameLabel: "Nom",
category: "Catégorie",
      enterProductNameAlert: "Veuillez entrer le nom du produit.",
      score: "Score",
      unnamedProduct: "Produit sans nom",
noBrand: "Sans marque",
source: "Source",
localDataset: "Base de données locale",
externalPreview: "Aperçu externe",
nameBasedFallback: "Résultat approximatif par nom",
      history: "Historique",
      welcome: "Bienvenue sur Skincare AI",
      subtitle: "Analysez vos produits de soin intelligemment ✨",
      interaction: "Interaction",
      productAnalyzer: "Analyseur de produit",
      ingredientChecker: "Vérificateur d’ingrédients",
      routine: "Routine",
      productNotFoundExternalPreview: "Produit introuvable dans la base locale. Affichage d’un aperçu à partir d’une source externe.",
productNotFoundNameFallback: "Produit introuvable dans la base locale ou la liste d’aperçu externe. Affichage d’un résultat approximatif basé uniquement sur le nom.",
      interactionTitle: "Analyse des interactions",
      ingredients: "Ingrédients",
ingredientsPlaceholder: "Exemple : Rétinol, Niacinamide, Acide Hyaluronique",
checkIngredients: "Vérifier les ingrédients",
      skinTypeLabel: "Type de peau",
products: "Produits",
ingredientCheckerTitle: "Vérificateur d’ingrédients",
ingredientCheckerSubtitle: "Entrez les ingrédients séparés par des virgules pour analyser les interactions, précautions, conflits, synergies et notes.",

interactionSubtitle: "Ajoutez vos produits et vérifiez s’ils fonctionnent bien ensemble.",
productName: "Nom du produit",
brand: "Marque",
addProduct: "+ Ajouter un produit",
routineTitle: "Créer ma routine",
routineSubtitle: "Créez une routine de soin personnalisée selon votre type de peau et votre préoccupation principale.",
mainConcern: "Préoccupation principale",
selectMainConcern: "Sélectionnez la préoccupation principale",
buildMyRoutine: "Créer ma routine",
selectedProfile: "Profil sélectionné",
concern: "Préoccupation",
morningRoutine: "Routine du matin",
nightRoutine: "Routine du soir",
suggestedProducts: "Produits suggérés",
orderOfUse: "Ordre d’utilisation",
aiNotes: "Notes IA",
oily: "Grasse",
dry: "Sèche",
combination: "Mixte",
sensitive: "Sensible",
acne: "Acné",
dryness: "Sécheresse",
pigmentation: "Pigmentation",
generalCare: "Soin général",
skinType: "Type de peau",
selectSkinType: "Sélectionnez le type de peau",
analyze: "Analyser mes produits",
alertEnter2Products: "Veuillez entrer au moins 2 produits.",
alertSelectSkinType: "Veuillez sélectionner un type de peau.",
productAnalyzerTitle: "Analyseur de produit",
productAnalyzerSubtitle: "Entrez le nom du produit et la marque pour afficher la catégorie, les ingrédients, les actifs, la compatibilité, les avertissements et les détails.",
analyzeProduct: "Analyser le produit",
enterProductName: "Entrez le nom du produit",
enterBrandName: "Entrez le nom de la marque",
conflict: "Conflit",
caution: "Prudence",
safe: "Sûr",

interactionConflictSummary: "Ces produits peuvent fortement entrer en conflit et irriter la peau lorsqu’ils sont utilisés ensemble.",
interactionConflictWhy1: "Le rétinol combiné à des exfoliants puissants peut augmenter l’irritation.",
interactionConflictWhy2: "Cette combinaison peut affaiblir la barrière cutanée, surtout pour les peaux sensibles.",
interactionConflictRec1: "Évitez d’utiliser ces produits dans la même routine.",
interactionConflictRec2: "Utilisez l’un le matin et l’autre le soir seulement si cela convient.",
interactionConflictRec3: "Commencez lentement et faites un test cutané d’abord.",

interactionCautionSummary: "Certains ingrédients peuvent provoquer une irritation lorsqu’ils sont combinés. À utiliser avec prudence.",
interactionCautionWhy1: "Certains actifs peuvent être trop forts lorsqu’ils sont superposés.",
interactionCautionWhy2: "L’irritation dépend de la concentration, de la formule et du type de peau.",
interactionCautionRec1: "Utilisez les produits à des moments différents de la journée.",
interactionCautionRec2: "N’introduisez pas tous les actifs en même temps.",
interactionCautionRec3: "Surveillez votre peau pour détecter irritation ou sécheresse.",

interactionSafeSummary: "Ces produits semblent généralement compatibles dans cette analyse préliminaire.",
interactionSafeWhy1: "Aucun conflit fort n’a été détecté dans cette logique simplifiée de compatibilité.",
interactionSafeWhy2: "Les produits sélectionnés semblent plus adaptés à une utilisation dans la même routine globale.",
interactionSafeRec1: "Appliquez les produits dans un ordre doux du plus léger au plus riche.",
interactionSafeRec2: "Continuez à surveiller la réaction de votre peau au fil du temps.",
interactionSafeRec3: "Utilisez un écran solaire dans la routine de jour si nécessaire.",
fallbackSourceNotes: "Notes sur la source de remplacement",
whyThisResult: "Pourquoi ce résultat",
recommendations: "Recommandations",
    },
  };

  const t = translations[language];

  const [products, setProducts] = useState([
    { name: "", brand: "" },
    { name: "", brand: "" },
  ]);

  const [skinType, setSkinType] = useState("");
  const [analysisResult, setAnalysisResult] = useState(null);

  const [singleProduct, setSingleProduct] = useState({
    name: "",
    brand: "",
  });
  const [productAnalysisResult, setProductAnalysisResult] = useState(null);

  const [ingredientInput, setIngredientInput] = useState("");
  const [ingredientCheckerResult, setIngredientCheckerResult] = useState(null);

  const [routineSkinType, setRoutineSkinType] = useState("");
  const [routineConcern, setRoutineConcern] = useState("");
  const [routineResult, setRoutineResult] = useState(null);

  const ingredientLibrary = useMemo(
    () => ({
      retinol: {
        label: "Retinol",
        aliases: ["retinol", "retinal", "retinyl", "retinoid"],
        category: "Active / Renewal",
        purpose: "Supports skin renewal and helps with acne, texture, and fine lines.",
        strength: "High",
        cautionLevel: "High caution",
        optimalPH:
          "Not strongly pH-dependent in the same way as acids, but needs careful routine pairing.",
        goodWith: ["Niacinamide", "Ceramides", "Hyaluronic Acid", "Peptides"],
        avoidWith: ["AHA", "BHA", "Benzoyl Peroxide"],
        notes: [
          "Can be irritating when combined with strong exfoliating acids.",
          "Best introduced slowly, especially for dry or sensitive skin.",
          "Usually preferred in night routines.",
        ],
      },
      vitamin_c: {
        label: "Vitamin C",
        aliases: [
          "vitamin c",
          "ascorbic acid",
          "ethyl ascorbic",
          "sodium ascorbyl phosphate",
        ],
        category: "Brightening / Antioxidant",
        purpose: "Helps brighten the skin and supports antioxidant protection.",
        strength: "Medium to High",
        cautionLevel: "Moderate caution",
        optimalPH: "Often works best in acidic formulas depending on the form used.",
        goodWith: ["Sunscreen", "Ferulic Acid", "Vitamin E", "Hyaluronic Acid"],
        avoidWith: [
          "Retinol in the same routine for sensitive users",
          "Too many strong acids",
        ],
        notes: [
          "Some skin types tolerate it very well, while sensitive skin may react depending on formula strength.",
          "Very useful in morning routines when paired with sunscreen.",
        ],
      },
      niacinamide: {
        label: "Niacinamide",
        aliases: ["niacinamide", "nicotinamide"],
        category: "Barrier / Balancing",
        purpose:
          "Helps support the barrier, balance oil, and improve overall skin appearance.",
        strength: "Low to Medium",
        cautionLevel: "Low caution",
        optimalPH: "Generally flexible and easy to combine in many routines.",
        goodWith: ["Hyaluronic Acid", "Ceramides", "Retinol", "Peptides"],
        avoidWith: ["No major hard conflict in this simplified checker"],
        notes: [
          "Usually one of the easiest actives to combine.",
          "High percentages may still irritate some users.",
        ],
      },
      aha: {
        label: "AHA",
        aliases: ["aha", "glycolic acid", "lactic acid", "mandelic acid"],
        category: "Exfoliant",
        purpose: "Helps with surface exfoliation, texture, and dullness.",
        strength: "Medium to High",
        cautionLevel: "High caution",
        optimalPH: "Usually most active in lower-pH formulas.",
        goodWith: ["Hydrating products", "Ceramides", "Gentle moisturizers"],
        avoidWith: ["Retinol", "Benzoyl Peroxide", "Too many strong actives together"],
        notes: [
          "Overuse can weaken the barrier.",
          "Sensitive skin may need reduced frequency.",
        ],
      },
      bha: {
        label: "BHA / Salicylic Acid",
        aliases: ["bha", "salicylic acid", "salicylic"],
        category: "Exfoliant / Acne",
        purpose:
          "Helps unclog pores and is commonly used for acne-prone or oily skin.",
        strength: "Medium",
        cautionLevel: "Moderate to high caution",
        optimalPH: "Typically performs best in acidic formulas.",
        goodWith: ["Niacinamide", "Hydrating support", "Oil-control routines"],
        avoidWith: ["Retinol in the same routine", "Too many exfoliants"],
        notes: [
          "Can be very useful for acne-prone skin.",
          "Still needs caution when layered with other strong actives.",
        ],
      },
      benzoyl_peroxide: {
        label: "Benzoyl Peroxide",
        aliases: ["benzoyl peroxide", "benzoyl"],
        category: "Acne Treatment",
        purpose: "Targets acne-causing bacteria and active breakouts.",
        strength: "High",
        cautionLevel: "High caution",
        optimalPH: "Formula-dependent; focus more on tolerance and pairing caution.",
        goodWith: ["Gentle cleanser", "Moisturizer", "Barrier-support products"],
        avoidWith: ["Retinol", "Too many drying actives"],
        notes: [
          "Can be drying and irritating.",
          "Often better to keep the rest of the routine simple.",
        ],
      },
      hyaluronic_acid: {
        label: "Hyaluronic Acid",
        aliases: ["hyaluronic acid", "sodium hyaluronate", "ha"],
        category: "Hydration",
        purpose: "Supports hydration and helps reduce dryness.",
        strength: "Low",
        cautionLevel: "Low caution",
        optimalPH: "Very flexible in routines.",
        goodWith: ["Retinol", "Vitamin C", "Niacinamide", "Ceramides", "Peptides"],
        avoidWith: ["No major hard conflict in this simplified checker"],
        notes: [
          "Very easy to place into most routines.",
          "Useful as a support ingredient rather than a conflict ingredient.",
        ],
      },
      ceramides: {
        label: "Ceramides",
        aliases: ["ceramide", "ceramides"],
        category: "Barrier Support",
        purpose: "Supports the skin barrier and helps reduce dryness or irritation.",
        strength: "Low",
        cautionLevel: "Low caution",
        optimalPH: "Flexible.",
        goodWith: ["Retinol", "AHA", "BHA", "Niacinamide", "Hyaluronic Acid"],
        avoidWith: ["No major hard conflict in this simplified checker"],
        notes: [
          "Helpful as a support ingredient around stronger actives.",
          "Often a good pairing when irritation risk exists.",
        ],
      },
      peptides: {
        label: "Peptides",
        aliases: ["peptide", "peptides", "matrixyl", "copper peptide"],
        category: "Support / Anti-aging",
        purpose:
          "Supports skin condition and is often used in barrier or anti-aging routines.",
        strength: "Low to Medium",
        cautionLevel: "Low caution",
        optimalPH: "Generally flexible, though exact formulas matter.",
        goodWith: ["Niacinamide", "Hyaluronic Acid", "Ceramides"],
        avoidWith: [
          "Too many strong exfoliants in the same routine if skin is reactive",
        ],
        notes: [
          "Usually acts as a support ingredient rather than a major conflict driver.",
          "Final formula still matters.",
        ],
      },
    }),
    []
  );

  const productDatabase = useMemo(
    () => [
      {
        name: "Retinol Night Serum",
        brand: "GlowLab",
        category: "Serum",
        concern: ["acne", "texture", "fine lines"],
        skinTypes: ["Oily", "Combination", "Normal"],
        ingredients: [
          "Retinol",
          "Glycerin",
          "Hyaluronic Acid",
          "Ceramides",
          "Panthenol",
        ],
        activeIngredients: ["Retinol"],
        warnings: [
          "May cause dryness or irritation.",
          "Avoid combining with strong acids in the same routine.",
          "Use sunscreen during daytime.",
        ],
        image: "https://via.placeholder.com/260x180?text=Retinol+Serum",
      },
      {
        name: "Vitamin C Bright Serum",
        brand: "LumiSkin",
        category: "Serum",
        concern: ["pigmentation", "dullness"],
        skinTypes: ["Dry", "Combination", "Oily", "Normal"],
        ingredients: ["Vitamin C", "Ferulic Acid", "Vitamin E", "Glycerin"],
        activeIngredients: ["Vitamin C"],
        warnings: [
          "Sensitive skin may need gradual introduction.",
          "Do not overload the same routine with many strong actives.",
        ],
        image: "https://via.placeholder.com/260x180?text=Vitamin+C+Serum",
      },
      {
        name: "Barrier Repair Cream",
        brand: "CalmDerma",
        category: "Moisturizer",
        concern: ["dryness", "barrier", "sensitivity"],
        skinTypes: ["Dry", "Sensitive", "Combination", "Normal"],
        ingredients: [
          "Ceramides",
          "Cholesterol",
          "Fatty Acids",
          "Glycerin",
          "Panthenol",
        ],
        activeIngredients: ["Ceramides"],
        warnings: ["No major ingredient warning detected in this simplified dataset preview."],
        image: "https://via.placeholder.com/260x180?text=Barrier+Cream",
      },
      {
        name: "Salicylic Clear Cleanser",
        brand: "PureBalance",
        category: "Cleanser",
        concern: ["acne", "oiliness", "pores"],
        skinTypes: ["Oily", "Combination"],
        ingredients: ["Salicylic Acid", "Glycerin", "Aloe Vera", "Betaine"],
        activeIngredients: ["Salicylic Acid"],
        warnings: [
          "Can feel drying if the rest of the routine is too harsh.",
          "Avoid too many exfoliating steps in the same routine.",
        ],
        image: "https://via.placeholder.com/260x180?text=Salicylic+Cleanser",
      },
      {
        name: "Hydrating HA Essence",
        brand: "AquaBloom",
        category: "Essence",
        concern: ["dryness", "dehydration"],
        skinTypes: ["Dry", "Sensitive", "Combination", "Oily", "Normal"],
        ingredients: ["Hyaluronic Acid", "Glycerin", "Panthenol", "Allantoin"],
        activeIngredients: ["Hyaluronic Acid"],
        warnings: ["No major hard warning detected in this simplified dataset preview."],
        image: "https://via.placeholder.com/260x180?text=Hydrating+Essence",
      },
    ],
    []
  );

  const externalProductDatabase = useMemo(
    () => [
      {
        name: "Effaclar Serum",
        brand: "La Roche-Posay",
        category: "Serum",
        concern: ["acne", "pores", "texture"],
        skinTypes: ["Oily", "Combination"],
        ingredients: ["Salicylic Acid", "Niacinamide", "Glycolic Acid", "LHA"],
        activeIngredients: ["Salicylic Acid", "Niacinamide", "Glycolic Acid"],
        warnings: [
          "External-source preview only.",
          "Contains multiple active ingredients and may be strong for sensitive skin.",
        ],
        image: "https://via.placeholder.com/260x180?text=External+Effaclar+Serum",
      },
      {
        name: "CeraVe Resurfacing Retinol Serum",
        brand: "CeraVe",
        category: "Serum",
        concern: ["acne marks", "texture", "post-blemish care"],
        skinTypes: ["Oily", "Combination", "Normal"],
        ingredients: ["Retinol", "Niacinamide", "Ceramides", "Licorice Root Extract"],
        activeIngredients: ["Retinol", "Niacinamide"],
        warnings: [
          "External-source preview only.",
          "Retinol products need gradual introduction and sunscreen support.",
        ],
        image: "https://via.placeholder.com/260x180?text=External+Retinol+Serum",
      },
      {
        name: "The Ordinary Niacinamide 10% + Zinc 1%",
        brand: "The Ordinary",
        category: "Serum",
        concern: ["oiliness", "blemishes", "pores"],
        skinTypes: ["Oily", "Combination", "Normal"],
        ingredients: ["Niacinamide", "Zinc PCA", "Tamarindus Indica Seed Gum"],
        activeIngredients: ["Niacinamide", "Zinc PCA"],
        warnings: [
          "External-source preview only.",
          "Some users may feel irritation with high niacinamide percentages.",
        ],
        image: "https://via.placeholder.com/260x180?text=External+Niacinamide",
      },
      {
        name: "SkinCeuticals C E Ferulic",
        brand: "SkinCeuticals",
        category: "Serum",
        concern: ["dullness", "pigmentation", "antioxidant support"],
        skinTypes: ["Normal", "Dry", "Combination"],
        ingredients: ["Vitamin C", "Vitamin E", "Ferulic Acid"],
        activeIngredients: ["Vitamin C", "Ferulic Acid", "Vitamin E"],
        warnings: [
          "External-source preview only.",
          "Vitamin C formulas may be irritating for very sensitive skin.",
        ],
        image: "https://via.placeholder.com/260x180?text=External+Vitamin+C",
      },
    ],
    []
  );

  const addProduct = () => {
    setProducts([...products, { name: "", brand: "" }]);
  };

  const handleProductChange = (index, field, value) => {
    const updatedProducts = [...products];
    updatedProducts[index][field] = value;
    setProducts(updatedProducts);
  };

  const detectIngredientObjectsFromList = (ingredients) => {
    const normalized = ingredients.map((item) => item.toLowerCase());

    return Object.values(ingredientLibrary).filter((entry) =>
      entry.aliases.some((alias) =>
        normalized.some((ing) => ing.includes(alias.toLowerCase()))
      )
    );
  };

  const inferCategoryFromText = (text) => {
    if (text.includes("cleanser")) return "Cleanser";
    if (text.includes("cream") || text.includes("moisturizer")) return "Moisturizer";
    if (text.includes("serum")) return "Serum";
    if (text.includes("essence")) return "Essence";
    return "Unknown Category";
  };

  const inferIngredientsFromText = (text) => {
    const detected = [];
    if (text.includes("retinol")) detected.push("Retinol");
    if (text.includes("vitamin c")) detected.push("Vitamin C");
    if (text.includes("niacinamide")) detected.push("Niacinamide");
    if (text.includes("salicylic")) detected.push("Salicylic Acid");
    if (text.includes("glycolic")) detected.push("Glycolic Acid");
    if (text.includes("lactic")) detected.push("Lactic Acid");
    if (text.includes("hyaluronic")) detected.push("Hyaluronic Acid");
    if (text.includes("ceramide")) detected.push("Ceramides");
    if (text.includes("benzoyl")) detected.push("Benzoyl Peroxide");
    return detected;
  };

  const normalizeProductForSearch = (product) =>
    `${product.name} ${product.brand}`.trim().toLowerCase();

  const searchProductInSource = (name, brand, sourceArray) => {
    const searchedName = name.trim().toLowerCase();
    const searchedBrand = brand.trim().toLowerCase();

    return sourceArray.find((item) => {
      const itemText = `${item.name} ${item.brand}`.toLowerCase();
      const nameMatch =
        item.name.toLowerCase().includes(searchedName) ||
        searchedName.includes(item.name.toLowerCase()) ||
        itemText.includes(searchedName);
      const brandMatch = searchedBrand
        ? item.brand.toLowerCase().includes(searchedBrand) ||
          searchedBrand.includes(item.brand.toLowerCase())
        : true;
      return nameMatch && brandMatch;
    });
  };

  const searchProductWithFallback = (name, brand = "") => {
    const localProduct = searchProductInSource(name, brand, productDatabase);
    if (localProduct) {
      return {
        found: true,
        source: "local",
        product: localProduct,
      };
    }

    const externalProduct = searchProductInSource(name, brand, externalProductDatabase);
    if (externalProduct) {
      return {
        found: true,
        source: "external",
        product: externalProduct,
        message: t.productNotFoundExternalPreview,
      };
    }

    const text = `${name} ${brand}`.trim().toLowerCase();
    const inferredIngredients = inferIngredientsFromText(text);

    return {
      found: false,
      source: "name-based",
      message: t.productNotFoundNameFallback,
      product: {
        name: name || "Unnamed Product",
        brand: brand || "No Brand",
        category: inferCategoryFromText(text),
        concern: ["Will be stronger when connected to real backend search"],
        skinTypes: ["Final suitability should come from dataset or API"],
        ingredients:
          inferredIngredients.length > 0
            ? inferredIngredients
            : ["Exact ingredient list not available"],
        activeIngredients:
          inferredIngredients.length > 0
            ? inferredIngredients
            : ["No clear active ingredient detected from name alone"],
        warnings: [
          "This is only a name-based fallback.",
          "Do not rely on this as the final product truth.",
        ],
        image: "https://via.placeholder.com/260x180?text=Fallback+Preview",
      },
    };
  };

  const buildInteractionAnalysis = (resolvedProducts, selectedSkinType) => {
    const allText = resolvedProducts
      .map((entry) => normalizeProductForSearch(entry.product || entry))
      .join(" ");

    let result;

    if (
      allText.includes("retinol") &&
      (allText.includes("aha") ||
        allText.includes("bha") ||
        allText.includes("salicylic") ||
        allText.includes("benzoyl") ||
        allText.includes("glycolic"))
    ) {
result = {
  status: t.conflict,
  icon: "❌",
  score: 35,
  summary: t.interactionConflictSummary,
  why: [
    t.interactionConflictWhy1,
    t.interactionConflictWhy2,
  ],
  recommendations: [
    t.interactionConflictRec1,
    t.interactionConflictRec2,
    t.interactionConflictRec3,
  ],
  bg: "#FFF1F1",
  border: "#F5B5B5",
  titleColor: "#C62828",
  badgeBg: "#FFD6D6",
  badgeColor: "#9F1D1D",
  sectionBg: "#FFE7E7",
};
} else if (
  (allText.includes("retinol") && allText.includes("vitamin c")) ||
  (allText.includes("niacinamide") && allText.includes("vitamin c"))
) {
  result = {
    status: t.caution,
    icon: "⚠️",
    score: 72,
    summary: t.interactionCautionSummary,
    why: [
      t.interactionCautionWhy1,
      t.interactionCautionWhy2,
    ],
    recommendations: [
      t.interactionCautionRec1,
      t.interactionCautionRec2,
      t.interactionCautionRec3,
    ],
    bg: "#FFF9E6",
    border: "#FFD580",
    titleColor: "#C77D00",
    badgeBg: "#FFE8B3",
    badgeColor: "#8A5A00",
    sectionBg: "#FFF3CC",
  };
} else {
  result = {
    status: t.safe,
    icon: "✅",
    score: 91,
    summary: t.interactionSafeSummary,
    why: [
      t.interactionSafeWhy1,
      t.interactionSafeWhy2,
    ],
    recommendations: [
      t.interactionSafeRec1,
      t.interactionSafeRec2,
      t.interactionSafeRec3,
    ],
    bg: "#EEFBEF",
    border: "#A7E3AE",
    titleColor: "#2E7D32",
    badgeBg: "#D6F5D9",
    badgeColor: "#1F5C24",
    sectionBg: "#DFF6E2",
  };
}

const sourceNotes = resolvedProducts
  .filter((entry) => entry.source !== "local")
  .map(
    (entry) =>
      `${entry.product.name} — ${
        entry.source === "external"
          ? t.externalPreview
          : t.nameBasedFallback
      }`
  );

    return {
      ...result,
      products: resolvedProducts,
      skinType: selectedSkinType,
      sourceNotes,
    };
  };

  const handleAnalyze = () => {
    const filledProducts = products.filter(
      (product) => product.name.trim() !== "" || product.brand.trim() !== ""
    );

    if (filledProducts.length < 2) {
      alert(t.alertEnter2Products);
      return;
    }

    if (!skinType) {
      alert(t.alertSelectSkinType);
      return;
    }

    const resolvedProducts = filledProducts.map((item) =>
      searchProductWithFallback(item.name, item.brand)
    );

    const result = buildInteractionAnalysis(resolvedProducts, skinType);
    setAnalysisResult(result);
  };

  const handleSingleProductChange = (field, value) => {
    setSingleProduct((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSingleProductAnalyze = () => {
    if (!singleProduct.name.trim()) {
       alert(t.enterProductNameAlert);
      return;
    }

    const searchResult = searchProductWithFallback(singleProduct.name, singleProduct.brand);
    const matchedProduct = searchResult.product;
    const detectedActiveObjects = detectIngredientObjectsFromList(
      matchedProduct.ingredients || []
    );
    const warnings = [...(matchedProduct.warnings || [])];

    if (
      (matchedProduct.ingredients || []).some((ing) =>
        ing.toLowerCase().includes("retinol")
      )
    ) {
      warnings.push("Be careful with AHA/BHA or benzoyl peroxide in the same routine.");
    }

    setProductAnalysisResult({
      status:
        searchResult.source === "local"
          ? "Dataset-Based Product Analyzer"
          : searchResult.source === "external"
          ? "External-Source Product Analyzer"
          : "Name-Based Product Analyzer",
      icon:
        searchResult.source === "local"
          ? "🧴"
          : searchResult.source === "external"
          ? "🌐"
          : "🔎",
      source: searchResult.source,
      sourceMessage:
        searchResult.source === "local"
          ? "Matched from the local dataset."
          : searchResult.message,
      summary:
        searchResult.source === "local"
          ? "This product was matched from the current local dataset and its details are displayed below."
          : searchResult.source === "external"
          ? "This product was not found locally, so an external-source preview was used as fallback."
          : "No exact local or external preview match was found, so this result uses name-based fallback only.",
      product: matchedProduct,
      category: matchedProduct.category,
      concern: matchedProduct.concern,
      skinTypes: matchedProduct.skinTypes,
      ingredients: matchedProduct.ingredients,
      activeIngredients: matchedProduct.activeIngredients,
      detectedIngredientObjects: detectedActiveObjects,
      warnings,
      image: matchedProduct.image,
      bg:
        searchResult.source === "local"
          ? "#F3F0FF"
          : searchResult.source === "external"
          ? "#EAF4FF"
          : "#FFF9E6",
      border:
        searchResult.source === "local"
          ? "#D7CCFF"
          : searchResult.source === "external"
          ? "#B9D8FF"
          : "#FFD580",
      titleColor:
        searchResult.source === "local"
          ? "#6C63FF"
          : searchResult.source === "external"
          ? "#1565C0"
          : "#C77D00",
      sectionBg:
        searchResult.source === "local"
          ? "#F7F4FF"
          : searchResult.source === "external"
          ? "#F1F8FF"
          : "#FFF3CC",
    });
  };

  const parseIngredientInput = (value) => {
    return value
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
  };

  const findIngredientMatches = (items) => {
    return items.map((typedIngredient) => {
      const lower = typedIngredient.toLowerCase();

      const matched = Object.values(ingredientLibrary).find((entry) =>
        entry.aliases.some((alias) => lower.includes(alias.toLowerCase()))
      );

      return {
        typed: typedIngredient,
        matched: matched || null,
      };
    });
  };

  const buildPairInsights = (matchedEntries) => {
    const matchedObjects = matchedEntries.map((entry) => entry.matched).filter(Boolean);

    const labels = matchedObjects.map((item) => item.label);
    const joinedText = labels.join(" | ").toLowerCase();

    const synergies = [];
    const conflicts = [];
    const developerNotes = [];

    if (
      joinedText.includes("retinol") &&
      (joinedText.includes("aha") ||
        joinedText.includes("bha") ||
        joinedText.includes("salicylic"))
    ) {
      conflicts.push("Retinol with AHA/BHA can be too strong in the same routine.");
      developerNotes.push("Recommended separation: different nights or slower introduction.");
    }

    if (joinedText.includes("retinol") && joinedText.includes("benzoyl peroxide")) {
      conflicts.push("Retinol with benzoyl peroxide may increase irritation and dryness.");
      developerNotes.push("Keep the routine simple and avoid stacking multiple strong treatments.");
    }

    if (joinedText.includes("vitamin c") && joinedText.includes("retinol")) {
      conflicts.push(
        "Vitamin C with retinol is not always impossible, but may be irritating for some users in the same routine."
      );
      developerNotes.push("Often easier to separate by time of day or alternate usage.");
    }

    if (joinedText.includes("niacinamide") && joinedText.includes("hyaluronic acid")) {
      synergies.push("Niacinamide + Hyaluronic Acid is a supportive and generally easy combination.");
    }

    if (joinedText.includes("retinol") && joinedText.includes("ceramides")) {
      synergies.push("Ceramides can support the barrier around retinol use.");
    }

    if (joinedText.includes("retinol") && joinedText.includes("hyaluronic acid")) {
      synergies.push("Hyaluronic Acid can add hydration support around retinol routines.");
    }

    if (joinedText.includes("vitamin c") && joinedText.includes("sunscreen")) {
      synergies.push("Vitamin C is commonly supportive in morning antioxidant routines with sunscreen.");
    }

    if (synergies.length === 0 && conflicts.length === 0) {
      developerNotes.push(
        "No strong direct conflict or strong synergy was detected in the current simplified ingredient logic."
      );
    }

    return { synergies, conflicts, developerNotes };
  };

  const handleIngredientCheck = () => {
    const parsedIngredients = parseIngredientInput(ingredientInput);

    if (parsedIngredients.length === 0) {
      alert("Please enter at least one ingredient.");
      return;
    }

    const matchedEntries = findIngredientMatches(parsedIngredients);
    const foundCount = matchedEntries.filter((entry) => entry.matched).length;

    const pairInsights = buildPairInsights(matchedEntries);

    const strengths = matchedEntries
      .filter((entry) => entry.matched)
      .map((entry) => `${entry.matched.label}: ${entry.matched.strength}`);

    const cautionFlags = matchedEntries
      .filter((entry) => entry.matched)
      .map((entry) => `${entry.matched.label}: ${entry.matched.cautionLevel}`);

    const notes = matchedEntries.flatMap((entry) =>
      entry.matched
        ? [`${entry.matched.label}: ${entry.matched.notes.join(" ")}`]
        : [`${entry.typed}: Not found in the current simplified ingredient library.`]
    );

    const optimalPH = matchedEntries
      .filter((entry) => entry.matched)
      .map((entry) => `${entry.matched.label}: ${entry.matched.optimalPH}`);

    setIngredientCheckerResult({
      typedIngredients: parsedIngredients,
      matchedEntries,
      foundCount,
      synergies: pairInsights.synergies,
      conflicts: pairInsights.conflicts,
      developerNotes: pairInsights.developerNotes,
      strengths,
      cautionFlags,
      notes,
      optimalPH,
      bg: pairInsights.conflicts.length > 0 ? "#FFF1F1" : "#EEFBEF",
      border: pairInsights.conflicts.length > 0 ? "#F5B5B5" : "#A7E3AE",
      titleColor: pairInsights.conflicts.length > 0 ? "#C62828" : "#2E7D32",
sectionBg: pairInsights.conflicts.length > 0 ? "#FFE7E7" : "#EDF9F0",
      status:
        pairInsights.conflicts.length > 0
          ? "Ingredient Caution"
          : pairInsights.synergies.length > 0
          ? "Ingredient Match Review"
          : "Ingredient Logic Review",
      icon:
        pairInsights.conflicts.length > 0
          ? "⚠️"
          : pairInsights.synergies.length > 0
          ? "🧪"
          : "📋",
    });
  };

  const handleRoutineBuild = () => {
    if (!routineSkinType) {
      alert("Please select your skin type.");
      return;
    }

    if (!routineConcern) {
      alert("Please select your main concern.");
      return;
    }

    let result;

    if (routineConcern === "acne") {
      result = {
        title: "Acne-Focused Routine",
        summary:
          "This routine is designed to help manage breakouts while keeping the skin barrier supported.",
        morningRoutine: [
          "Gentle Cleanser",
          "Niacinamide Serum",
          "Lightweight Moisturizer",
          "Oil-free Sunscreen",
        ],
        nightRoutine: [
          "Gentle Cleanser",
          "Treatment Product (such as salicylic acid or retinol depending on tolerance)",
          "Barrier-support Moisturizer",
        ],
        suggestedProducts: [
          "Gentle cleanser for acne-prone skin",
          "Niacinamide serum",
          "Non-comedogenic moisturizer",
          "Broad-spectrum sunscreen",
        ],
        usageOrder: [
          "Cleanser",
          "Treatment/Serum",
          "Moisturizer",
          "Sunscreen in the morning only",
        ],
        aiNotes: [
          "Do not introduce multiple strong actives at once.",
          "If irritation appears, reduce frequency of treatment products.",
          "Hydration and barrier support are still important even for oily or acne-prone skin.",
        ],
        bg: "#EEFBEF",
        border: "#A7E3AE",
        titleColor: "#2E7D32",
        sectionBg: "#DFF6E2",
      };
    } else if (routineConcern === "dryness") {
      result = {
        title: "Hydration & Barrier Routine",
        summary:
          "This routine is designed to reduce dryness and support the skin barrier.",
        morningRoutine: [
          "Hydrating Cleanser",
          "Hyaluronic Acid Serum",
          "Rich Moisturizer",
          "Sunscreen",
        ],
        nightRoutine: [
          "Hydrating Cleanser",
          "Barrier-support Serum or Essence",
          "Rich Moisturizer or Night Cream",
        ],
        suggestedProducts: [
          "Hydrating cleanser",
          "Hyaluronic acid serum",
          "Ceramide moisturizer",
          "Gentle sunscreen",
        ],
        usageOrder: [
          "Cleanser",
          "Hydrating serum",
          "Moisturizer",
          "Sunscreen in the morning only",
        ],
        aiNotes: [
          "Avoid over-exfoliating while the skin is dry.",
          "Barrier-support ingredients like ceramides and glycerin are useful.",
          "Consistency matters more than using too many products.",
        ],
        bg: "#F3F0FF",
        border: "#D7CCFF",
        titleColor: "#6C63FF",
        sectionBg: "#F7F4FF",
      };
    } else if (routineConcern === "pigmentation") {
      result = {
        title: "Brightening Routine",
        summary:
          "This routine is designed to help with dullness and uneven tone while keeping irritation controlled.",
        morningRoutine: [
          "Gentle Cleanser",
          "Vitamin C Serum",
          "Moisturizer",
          "Sunscreen",
        ],
        nightRoutine: [
          "Gentle Cleanser",
          "Brightening or renewal-focused treatment",
          "Moisturizer",
        ],
        suggestedProducts: [
          "Vitamin C serum",
          "Gentle moisturizer",
          "Daily sunscreen",
          "Night treatment for skin renewal",
        ],
        usageOrder: [
          "Cleanser",
          "Treatment/Serum",
          "Moisturizer",
          "Sunscreen in the morning only",
        ],
        aiNotes: [
          "Sunscreen is essential in any pigmentation-focused routine.",
          "Do not over-layer strong brightening actives if your skin is sensitive.",
          "Results usually need time and consistency.",
        ],
bg: "#FBF4FF",
border: "#E2CFF8",
titleColor: "#8A63D2",
sectionBg: "#F6EEFF",
      };
    } else {
      result = {
        title: "General Balanced Routine",
        summary:
          "This routine is designed as a simple starting structure for everyday skin support.",
        morningRoutine: ["Gentle Cleanser", "Light Serum", "Moisturizer", "Sunscreen"],
        nightRoutine: ["Gentle Cleanser", "Targeted Serum if needed", "Moisturizer"],
        suggestedProducts: [
          "Gentle cleanser",
          "Basic serum",
          "Daily moisturizer",
          "Broad-spectrum sunscreen",
        ],
        usageOrder: ["Cleanser", "Serum", "Moisturizer", "Sunscreen in the morning only"],
        aiNotes: [
          "A simple routine is often better than an overloaded one.",
          "Adjust product strength based on your skin tolerance.",
          "Later, this tab can become much stronger when connected to the backend dataset.",
        ],
        bg: "#EEFBEF",
        border: "#A7E3AE",
        titleColor: "#2E7D32",
        sectionBg: "#DFF6E2",
      };
    }

    setRoutineResult({
      ...result,
      skinType: routineSkinType,
      concern: routineConcern,
    });
  };

const tabStyle = (tab) => ({
  padding: "10px 20px",
  borderRadius: "30px",
  border: activeTab === tab ? "none" : "1px solid #e0e0e0",
  cursor: "pointer",
  background:
    activeTab === tab
      ? "linear-gradient(135deg, #6C63FF, #8E85FF)"
      : "white",
  color: activeTab === tab ? "white" : "#555",
  fontWeight: "500",
  boxShadow:
    activeTab === tab
      ? "0 4px 12px rgba(108,99,255,0.3)"
      : "0 2px 6px rgba(0,0,0,0.05)",
  transform: activeTab === tab ? "scale(1.05)" : "scale(1)",
  transition: "all 0.25s ease",
});

const productCardStyle = {
  background: "white",
  border: "1px solid #eee",
  borderRadius: "18px",
  padding: "22px",
  marginBottom: "18px",
  boxShadow: "0 6px 18px rgba(0,0,0,0.06)",
  transition: "all 0.25s ease",
};

const inputStyle = {
  width: "100%",
  padding: "14px 16px",
  borderRadius: "14px",
  border: "1px solid #dcd6ff",
  marginTop: "8px",
  boxSizing: "border-box",
  background: "#ffffff",
  fontSize: "15px",
  outline: "none",
  boxShadow: "inset 0 1px 2px rgba(0,0,0,0.03)",
};
const detailLabelStyle = {
  fontSize: "13px",
  color: "#7C7698",
  marginBottom: "8px",
  fontWeight: "600",
  letterSpacing: "0.2px",
  textTransform: "uppercase",
};

const detailValueStyle = {
  fontWeight: "600",
  color: "#2F2A45",
  fontSize: "20px",
  lineHeight: "1.4",
};

const detailItemStyle = {
  minWidth: 0,
};
const infoBlockStyle = (bg) => ({
  background: bg,
  borderRadius: "14px",
  padding: "16px",
  marginBottom: "18px",
  border: "1px solid rgba(0,0,0,0.04)",
});
  

  return (
  <div
  dir={language === "ar" ? "rtl" : "ltr"}
  style={{
    fontFamily: "Arial, sans-serif",
    background: "#fafafa",
    minHeight: "100vh",
    textAlign: language === "ar" ? "right" : "left",
  }}
>
    
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "20px 40px",
          background: "white",
          boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
        }}
      >
        <h2 style={{ margin: 0 }}>{t.appName}</h2>

        <div>
<select
  value={language}
  onChange={(e) => setLanguage(e.target.value)}
  style={{
    padding: "8px",
    borderRadius: "8px",
    border: "1px solid #ddd",
  }}
>
  <option value="en">English</option>
  <option value="ar">العربية</option>
  <option value="fr">Français</option>
</select>

          <button
            style={{
              marginLeft: "10px",
              padding: "8px 12px",
              borderRadius: "8px",
              border: "none",
              background: "#6C63FF",
              color: "white",
              cursor: "pointer",
            }}
          >
           {t.history}
          </button>
        </div>
      </div>

<div
 style={{
  position: "relative",
backgroundImage:
  activeTab === "interaction"
    ? "url('/images/4.png')"
    : activeTab === "product"
    ? "url('/images/5.png')"
    : "url('/images/1.jpg')",
 backgroundSize:
  activeTab === "interaction" || activeTab === "product"
    ? "contain"
    : "cover",
  backgroundPosition: "center 70%", // 👈 نزلنا الصورة
 backgroundRepeat: activeTab === "interaction" ? "no-repeat" : "no-repeat",
  height: "360px", // 👈 زودنا الطول شوي
  width: "100%",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  textAlign: "center",
  borderRadius: "0 0 28px 28px",
  overflow: "hidden",
  marginBottom: "16px",
}}
>
  <div
    style={{
      position: "absolute",
      inset: 0,
 background:
  activeTab === "interaction" || activeTab === "product"
    ? "transparent"
    : "linear-gradient(135deg, rgba(0,0,0,0.6), rgba(108,99,255,0.4))",
    }}
  />

<div
  style={{
    position: "relative",
    zIndex: 1,
    maxWidth: "700px",
    display:
  activeTab === "interaction" || activeTab === "product"
    ? "none"
    : "block",
  }}
>
    <h1
      style={{
       fontSize: "42px",
fontWeight: "700",
letterSpacing: "0.5px", 
        color: "white",
        marginBottom: "10px",
      }}
    >
      {t.welcome}
    </h1>

    <p
      style={{
        color: "white",
        fontSize: "18px",
opacity: 0.9,
        margin: 0,
      }}
    >
      {t.subtitle}
    </p>
  </div>
</div>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "12px",
          marginBottom: "40px",
          flexWrap: "wrap",
        }}
      >
<button style={tabStyle("interaction")} onClick={() => setActiveTab("interaction")}>
  {t.interaction}
</button>

<button style={tabStyle("product")} onClick={() => setActiveTab("product")}>
  {t.productAnalyzer}
</button>

<button style={tabStyle("ingredient")} onClick={() => setActiveTab("ingredient")}>
  {t.ingredientChecker}
</button>

<button style={tabStyle("routine")} onClick={() => setActiveTab("routine")}>
  {t.routine}
</button>
      </div>

      <div style={{ maxWidth: "900px", margin: "0 auto", padding: "0 20px 60px" }}>
        {activeTab === "interaction" && (
          <div
            style={{
             background: "linear-gradient(145deg, #ffffff, #f3f0ff)",
borderRadius: "24px",
padding: "32px",
boxShadow: "0 10px 30px rgba(108,99,255,0.12)",
border: "1px solid rgba(108,99,255,0.15)",
backdropFilter: "blur(6px)",
            }}
          >
<h2 style={{ 
  textAlign: "center", 
  marginBottom: "10px",
  fontSize: "26px",
  fontWeight: "700",
  background: "linear-gradient(135deg, #6C63FF, #8E85FF)",
  WebkitBackgroundClip: "text",
  WebkitTextFillColor: "transparent"
}}>
  ✨ {t.interactionTitle}
</h2>

<p style={{ 
  textAlign: "center", 
  color: "#777", 
  marginBottom: "35px",
  fontSize: "16px"
}}>
  {t.interactionSubtitle}
</p>

            {products.map((product, index) => (
              <div key={index} style={productCardStyle}>
                <h3 style={{ marginTop: 0, marginBottom: "16px", textAlign: "center" }}>
                  {t.productLabel} {index + 1}
                </h3>

                <div style={{ marginBottom: "14px" }}>
                  <label
  style={{
    fontWeight: "600",
    display: "block",
    marginBottom: "6px",
    color: "#4B4563",
    fontSize: "15px",
  }}
>
                    {t.productName}
                  </label>
                  <input
                    type="text"
                    placeholder={t.enterProductName}
                    style={inputStyle}
                    value={product.name}
                    onChange={(e) => handleProductChange(index, "name", e.target.value)}
                  />
                </div>

                <div>
                 <label
  style={{
    fontWeight: "600",
    display: "block",
    marginBottom: "6px",
    color: "#4B4563",
    fontSize: "15px",
  }}
>
                    {t.brand}
                  </label>
                  <input
                    type="text"
                    placeholder={t.enterBrandName}
                    style={inputStyle}
                    value={product.brand}
                    onChange={(e) => handleProductChange(index, "brand", e.target.value)}
                  />
                </div>
              </div>
            ))}

            <div style={{ textAlign: "center", marginBottom: "25px" }}>
              <button
                onClick={addProduct}
                style={{
                  padding: "10px 18px",
                  borderRadius: "12px",
                  border: "1px dashed #6C63FF",
                  background: "#F5F4FF",
                  color: "#6C63FF",
                  fontWeight: "bold",
                  cursor: "pointer",
                }}
              >
                {t.addProduct}
              </button>
            </div>

            <div style={{ marginBottom: "25px" }}>
              <label
                style={{
                  display: "block",
                  marginBottom: "8px",
                  fontWeight: "bold",
                }}
              >
                {t.skinType}
              </label>
              <select
                value={skinType}
                onChange={(e) => setSkinType(e.target.value)}
                style={{
                  width: "100%",
                  padding: "12px",
                  borderRadius: "10px",
                  border: "1px solid #ddd",
                }}
              >
                <option value="">{t.selectSkinType}</option>
               <option value="Oily">{t.oily}</option>
<option value="Dry">{t.dry}</option>
<option value="Combination">{t.combination}</option>
<option value="Sensitive">{t.sensitive}</option>
              </select>
            </div>

            <div style={{ textAlign: "center", marginBottom: "40px" }}>
<button
  onClick={handleAnalyze}
  onMouseEnter={(e) => {
    e.target.style.transform = "translateY(-2px)";
  }}
  onMouseLeave={(e) => {
    e.target.style.transform = "translateY(0)";
  }}
  style={{
    padding: "14px 26px",
    borderRadius: "14px",
    border: "none",
    background: "linear-gradient(135deg, #6C63FF, #8E85FF)",
    color: "white",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
    boxShadow: "0 6px 18px rgba(108,99,255,0.35)",
    transition: "all 0.25s ease",
  }}
>
  {t.analyze}
</button>
            </div>

{analysisResult && (
  <div
    style={{
      background: "linear-gradient(180deg, rgba(255,255,255,0.95), rgba(248,246,255,0.95))",
      border: `2px solid ${analysisResult.border}`,
      borderRadius: "24px",
      padding: "28px",
      textAlign: language === "ar" ? "right" : "left",
boxShadow:
  analysisResult.status === t.conflict
    ? "0 12px 30px rgba(255, 0, 0, 0.15)"
    : analysisResult.status === t.caution
    ? "0 12px 30px rgba(245, 166, 35, 0.18)"
    : "0 12px 30px rgba(46, 204, 113, 0.18)",
overflow: "hidden",
    }}
  >
    <img
  src="/images/4.png"
  alt="Interaction result visual"
  style={{
    width: "100%",
    maxHeight: "220px",
    objectFit: "contain",
    borderRadius: "16px",
    marginBottom: "18px",
    background: "rgba(255,255,255,0.55)",
    border: "1px solid rgba(108,99,255,0.08)",
    padding: "8px",
  }}
/>
   <div
  style={{
    height: "4px",
    width: "100%",
    background:
      analysisResult.status === t.conflict
        ? "linear-gradient(90deg, #ff4d4d, #ff9999)"
        : analysisResult.status === t.caution
        ? "linear-gradient(90deg, #f5a623, #fbd786)"
        : "linear-gradient(90deg, #2ecc71, #a8e6cf)",
    borderTopLeftRadius: "24px",
    borderTopRightRadius: "24px",
    marginBottom: "12px",
  }}
/>
<div
  style={{
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "12px",
    flexWrap: "wrap",
    marginBottom: "20px",
    paddingBottom: "16px",
    borderBottom: "1px solid rgba(108,99,255,0.12)",
  }}
>
<h3
  style={{
    margin: 0,
    color: analysisResult.titleColor,
    fontSize: "24px",
    fontWeight: "700",
    letterSpacing: "0.2px",
  }}
>
                    {analysisResult.icon} {analysisResult.status}
                  </h3>

<div
  style={{
    background: analysisResult.badgeBg,
    color: analysisResult.badgeColor,
    padding: "10px 16px",
    borderRadius: "999px",
    fontWeight: "700",
    fontSize: "14px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.05)",
  }}
>
                    {t.score}: {analysisResult.score}/100
                  </div>
                </div>

<p
  style={{
    color: "#4B4563",
    lineHeight: "1.8",
    marginTop: 0,
    marginBottom: "22px",
    fontSize: "16px",
  }}
>
                  {analysisResult.summary}
                </p>

<div
  style={{
    marginBottom: "22px",
    color: "#333",
    background: "rgba(108,99,255,0.06)",
    padding: "12px 14px",
    borderRadius: "14px",
    fontSize: "15px",
  }}
>
  <strong>{t.skinTypeLabel}:</strong> {analysisResult.skinType}
</div>

                <div style={{ marginBottom: "18px" }}>
                  <strong style={{ color: "#333" }}>{t.products}</strong>
                  <div style={{ marginTop: "10px" }}>
                    {analysisResult.products.map((entry, index) => (
                      <div
                        key={index}
                        style={{
  marginBottom: "10px",
  color: "#444",
  padding: "12px 14px",
  background: "rgba(108,99,255,0.05)",
  borderRadius: "14px",
  border: "1px solid rgba(108,99,255,0.08)",
}}
                      >
                        <div>
  {entry.product.name || t.unnamedProduct} — {entry.product.brand || t.noBrand}
</div>
<div style={{ fontSize: "13px", marginTop: "4px" }}>
  {t.source}: {entry.source === "local" ? t.localDataset : entry.source === "external" ? t.externalPreview : t.nameBasedFallback}
</div>
                      </div>
                    ))}
                  </div>
                </div>

                {analysisResult.sourceNotes.length > 0 && (
                  <div
                    style={{
                      background: "#F8F4E8",
                      borderRadius: "14px",
                      padding: "16px",
                      marginBottom: "14px",
                    }}
                  >
                    <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                      {t.fallbackSourceNotes}
                    </strong>
                    {analysisResult.sourceNotes.map((item, index) => (
                     <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.8" }}>
                        • {item}
                      </div>
                    ))}
                  </div>
                )}

                <div
                  style={{
background: "rgba(255,255,255,0.72)",
borderRadius: "18px",
padding: "18px",
border: "1px solid rgba(108,99,255,0.10)",
boxShadow: "0 4px 10px rgba(0,0,0,0.03)",
                    marginBottom: "14px",
                  }}
                >
                 <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                    {t.whyThisResult}
                  </strong>

                  {analysisResult.why.map((item, index) => (
                    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                      • {item}
                    </div>
                  ))}
                </div>

                <div
                  style={{
                    background: analysisResult.sectionBg,
                    borderRadius: "14px",
                    padding: "16px",
                  }}
                >
                  <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                    {t.recommendations}
                  </strong>

                  {analysisResult.recommendations.map((item, index) => (
                    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                      • {item}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === "product" && (
          <div
            style={{
background: "linear-gradient(145deg, #ffffff, #f3f0ff)",
borderRadius: "24px",
padding: "32px",
boxShadow: "0 10px 30px rgba(108,99,255,0.12)",
border: "1px solid rgba(108,99,255,0.15)",
backdropFilter: "blur(6px)",
            }}
          >
            <h2
  style={{
    textAlign: "center",
    marginBottom: "10px",
    fontSize: "26px",
    fontWeight: "700",
    background: "linear-gradient(135deg, #6C63FF, #8E85FF)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  }}
>
  🧴 {t.productAnalyzerTitle}
</h2>

            <p
  style={{
    textAlign: "center",
    color: "#777",
    marginBottom: "35px",
    fontSize: "16px",
    lineHeight: "1.7",
    maxWidth: "720px",
    marginInline: "auto",
  }}
>
  {t.productAnalyzerSubtitle}
</p>

            <div style={productCardStyle}>
              <div style={{ marginBottom: "14px" }}>
                <label
  style={{
    fontWeight: "600",
    display: "block",
    marginBottom: "6px",
    color: "#4B4563",
    fontSize: "15px",
  }}
>
                  {t.productName}
                </label>
                <input
                  type="text"
                 placeholder={t.enterProductName}
                  style={inputStyle}
                  value={singleProduct.name}
                  onChange={(e) => handleSingleProductChange("name", e.target.value)}
                />
              </div>

              <div>
                <label
  style={{
    fontWeight: "600",
    display: "block",
    marginBottom: "6px",
    color: "#4B4563",
    fontSize: "15px",
  }}
>
                  {t.brand}
                </label>
                <input
                  type="text"
                  placeholder={t.enterBrandName}
                  style={inputStyle}
                  value={singleProduct.brand}
                  onChange={(e) => handleSingleProductChange("brand", e.target.value)}
                />
              </div>
            </div>

            <div style={{ textAlign: "center", marginBottom: "40px" }}>
<button
  onClick={handleSingleProductAnalyze}
  onMouseEnter={(e) => {
    e.target.style.transform = "translateY(-2px)";
  }}
  onMouseLeave={(e) => {
    e.target.style.transform = "translateY(0)";
  }}
  style={{
    padding: "14px 26px",
    borderRadius: "14px",
    border: "none",
    background: "linear-gradient(135deg, #6C63FF, #8E85FF)",
    color: "white",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
    boxShadow: "0 6px 18px rgba(108,99,255,0.35)",
    transition: "all 0.25s ease",
  }}
>
  {t.analyzeProduct}
</button>
            </div>

{productAnalysisResult && (
  <div
    style={{
      background: "linear-gradient(180deg, rgba(255,255,255,0.95), rgba(248,246,255,0.95))",
      border: "1px solid rgba(108,99,255,0.15)",
      borderRadius: "24px",
      padding: "28px",
      textAlign: language === "ar" ? "right" : "left",
      boxShadow: "0 12px 30px rgba(108,99,255,0.12)",
      marginTop: "30px",
    }}
  >
    <img
  src="/images/6.png"
  alt="Product analysis visual"
  style={{
    width: "100%",
    maxHeight: "220px",
    objectFit: "contain",
    borderRadius: "16px",
    marginBottom: "18px",
    background: "rgba(255,255,255,0.6)",
    padding: "8px",
    border: "1px solid rgba(0,0,0,0.05)",
  }}
/>
                <div style={{ marginBottom: "16px" }}>
<h3
  style={{
    margin: 0,
    color: "#6C63FF",
    fontSize: "24px",
    fontWeight: "700",
    letterSpacing: "0.2px",
  }}
>
                    {productAnalysisResult.icon} {productAnalysisResult.status}
                  </h3>
                </div>

                <p
                  style={{
                    color: "#444",
                    lineHeight: "1.7",
                    marginTop: 0,
                    marginBottom: "12px",
                  }}
                >
                  {productAnalysisResult.summary}
                </p>

<div
  style={{
    marginBottom: "20px",
    background: "rgba(108,99,255,0.06)",
    padding: "12px 14px",
    borderRadius: "14px",
    fontSize: "14px",
    color: "#444",
    border: "1px solid rgba(108,99,255,0.08)",
  }}
>
  <strong>{t.source}:</strong>{" "}
  {productAnalysisResult.source === "local"
    ? t.localDataset
    : productAnalysisResult.source === "external"
    ? t.externalPreview
    : t.nameBasedFallback}

  <div style={{ marginTop: "6px", color: "#666", lineHeight: "1.6" }}>
    {productAnalysisResult.sourceMessage}
  </div>
</div>

<div style={{ marginBottom: "18px" }}>
  <div style={infoBlockStyle(productAnalysisResult.sectionBg)}>
    <strong
      style={{
        display: "block",
        marginBottom: "16px",
        color: "#2F2A45",
        fontSize: "18px",
        fontWeight: "700",
      }}
    >
      {t.productDetails || "Product Details"}
    </strong>

    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "12px 20px",
      }}
    >
      <div>
       <div style={{ 
  fontSize: "14px",
  color: "#6A6485",
  marginBottom: "6px",
  fontWeight: "500",
  letterSpacing: "0.2px"
}}>
         {t.productNameLabel || "Name"}
        </div>
       <div style={{ 
  fontWeight: "600",
  color: "#2F2A45",
  fontSize: "15px",
  lineHeight: "1.5"
}}>
          {productAnalysisResult.product.name || "Unnamed Product"}
        </div>
      </div>

      <div>
       <div style={{ 
  fontSize: "14px",
  color: "#6A6485",
  marginBottom: "6px",
  fontWeight: "500",
  letterSpacing: "0.2px"
}}>
         {t.brand || "Brand"}
        </div>
       <div style={{ 
  fontWeight: "600",
  color: "#2F2A45",
  fontSize: "15px",
  lineHeight: "1.5"
}}>
          {productAnalysisResult.product.brand || "No Brand"}
        </div>
      </div>

      <div>
       <div style={{ 
  fontSize: "14px",
  color: "#6A6485",
  marginBottom: "6px",
  fontWeight: "500",
  letterSpacing: "0.2px"
}}>
        {t.category || "Category"}
        </div>
       <div style={{ 
  fontWeight: "600",
  color: "#2F2A45",
  fontSize: "15px",
  lineHeight: "1.5"
}}>
          {productAnalysisResult.category}
        </div>
      </div>

      <div>
      <div style={{ 
  fontSize: "14px",
  color: "#6A6485",
  marginBottom: "6px",
  fontWeight: "500",
  letterSpacing: "0.2px"
}}>
        {t.concern || "Concerns"}
        </div>
       <div style={{ 
  fontWeight: "600",
  color: "#2F2A45",
  fontSize: "15px",
  lineHeight: "1.5"
}}>
          {productAnalysisResult.concern.join(", ")}
        </div>
      </div>
    </div>
  </div>
</div>

<div style={infoBlockStyle(productAnalysisResult.sectionBg)}>
  <strong
    style={{
      display: "block",
      marginBottom: "12px",
      color: "#3F3A5B",
      fontSize: "14px",
    }}
  >
    Suitable Skin Types
  </strong>

  <div
    style={{
      display: "flex",
      flexWrap: "wrap",
      gap: "10px",
    }}
  >
    {productAnalysisResult.skinTypes.map((item, index) => (
      <div
        key={index}
        style={{
          padding: "8px 14px",
          borderRadius: "999px",
          background: "rgba(108,99,255,0.08)",
          border: "1px solid rgba(108,99,255,0.12)",
          color: "#4B4563",
          fontSize: "14px",
          fontWeight: "600",
        }}
      >
        {item}
      </div>
    ))}
  </div>
</div>

                <div style={infoBlockStyle(productAnalysisResult.sectionBg)}>
                  <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                    Full Ingredients
                  </strong>
                  {productAnalysisResult.ingredients.map((item, index) => (
                    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                      • {item}
                    </div>
                  ))}
                </div>

                <div style={infoBlockStyle(productAnalysisResult.sectionBg)}>
                 <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                    Active Ingredients
                  </strong>
                  {productAnalysisResult.activeIngredients.map((item, index) => (
                    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                      • {item}
                    </div>
                  ))}
                </div>

                <div style={infoBlockStyle(productAnalysisResult.sectionBg)}>
                  <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                    Ingredient-Based Notes
                  </strong>
                  {productAnalysisResult.detectedIngredientObjects.length > 0 ? (
                    productAnalysisResult.detectedIngredientObjects.map((item, index) => (
                      <div key={index} style={{ marginBottom: "10px", color: "#444", lineHeight: "1.7" }}>
                        • <strong>{item.label}</strong>: {item.purpose}
                      </div>
                    ))
                  ) : (
                    <div style={{ color: "#444" }}>
                      • No detailed ingredient logic could be extracted from the current preview.
                    </div>
                  )}
                </div>

                <div style={infoBlockStyle(productAnalysisResult.sectionBg)}>
                  <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                    Warnings Based on Ingredients
                  </strong>
                  {productAnalysisResult.warnings.map((item, index) => (
                    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                      • {item}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === "ingredient" && (
          <div
            style={{
background: "linear-gradient(145deg, #ffffff, #f3f0ff)",
borderRadius: "24px",
padding: "32px",
boxShadow: "0 10px 30px rgba(108,99,255,0.12)",
border: "1px solid rgba(108,99,255,0.15)",
backdropFilter: "blur(6px)",
            }}
          >
<h2
  style={{
    textAlign: "center",
    marginBottom: "10px",
    fontSize: "26px",
    fontWeight: "700",
    background: "linear-gradient(135deg, #6C63FF, #8E85FF)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  }}
>
  🧪 {t.ingredientCheckerTitle}
</h2>

<p
  style={{
    textAlign: "center",
    color: "#777",
    marginBottom: "35px",
    fontSize: "16px",
    lineHeight: "1.7",
    maxWidth: "720px",
    marginInline: "auto",
  }}
>
  {t.ingredientCheckerSubtitle}
</p>

<div style={productCardStyle}>
  <label
    style={{
      fontWeight: "600",
      display: "block",
      marginBottom: "10px",
      color: "#4B4563",
      fontSize: "14px",
    }}
  >
    {t.ingredients}
  </label>

  <textarea
    placeholder={t.ingredientsPlaceholder}
    style={{
      ...inputStyle,
      minHeight: "140px",
      resize: "vertical",
      lineHeight: "1.6",
      padding: "16px",
      borderRadius: "16px",
      border: "1px solid #d6d0ff",
      background: "#fff",
    }}
    value={ingredientInput}
    onChange={(e) => setIngredientInput(e.target.value)}
  />
</div>

            <div style={{ textAlign: "center", marginBottom: "40px" }}>
<button
  onClick={handleIngredientCheck}
  onMouseEnter={(e) => {
    e.target.style.transform = "translateY(-2px)";
  }}
  onMouseLeave={(e) => {
    e.target.style.transform = "translateY(0)";
  }}
  style={{
    padding: "14px 26px",
    borderRadius: "14px",
    border: "none",
    background: "linear-gradient(135deg, #6C63FF, #8E85FF)",
    color: "white",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
    boxShadow: "0 6px 18px rgba(108,99,255,0.35)",
    transition: "all 0.25s ease",
  }}
>
  {t.checkIngredients}
</button>
            </div>

            {ingredientCheckerResult && (
              <div
                style={{
                  background: ingredientCheckerResult.bg,
                  border: `1px solid ${ingredientCheckerResult.border}`,
                  borderRadius: "18px",
                  padding: "24px",
                  textAlign: "left",
                }}
              >
                <img
  src="/images/7.png"
  alt="Ingredient checker visual"
  style={{
    width: "100%",
    maxHeight: "220px",
    objectFit: "contain",
    borderRadius: "16px",
    marginBottom: "18px",
    background: "rgba(255,255,255,0.6)",
    padding: "8px",
    border: "1px solid rgba(0,0,0,0.05)",
  }}
/>
                <div style={{ marginBottom: "16px" }}>
<h3
  style={{
    margin: 0,
    color: ingredientCheckerResult.titleColor,
    fontSize: "24px",
    fontWeight: "700",
    letterSpacing: "0.2px",
  }}
>
  {ingredientCheckerResult.icon} {ingredientCheckerResult.status}
</h3>
<div
  style={{
    height: "4px",
    width: "60px",
    background: ingredientCheckerResult.titleColor,
    borderRadius: "4px",
    marginTop: "10px",
  }}
/>
                </div>
<div style={{ marginBottom: "18px" }}>
  <strong style={{ color: "#333" }}>Entered Ingredients</strong>
  <div style={{ marginTop: "10px" }}>
    {ingredientCheckerResult.typedIngredients.map((item, index) => (
      <div
        key={index}
        style={{
          marginBottom: "8px",
          color: "#444",
          padding: "10px 12px",
          background: "rgba(255,255,255,0.6)",
          borderRadius: "10px",
          border: "1px solid rgba(0,0,0,0.05)",
        }}
      >
        {item}
      </div>
    ))}
  </div>
</div>

                <div style={infoBlockStyle(ingredientCheckerResult.sectionBg)}>
<strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#312B4A",
    fontSize: "14px",
  }}
>
  Recognized Ingredient Logic
</strong>
                  {ingredientCheckerResult.matchedEntries.map((entry, index) => (
                    <div key={index} style={{ marginBottom: "10px", color: "#444", lineHeight: "1.6" }}>
                      • <strong>{entry.typed}</strong>: {entry.matched ? entry.matched.label : "Not found in the current simplified library"}
                    </div>
                  ))}
                </div>

                <div style={infoBlockStyle(ingredientCheckerResult.sectionBg)}>
                  <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#2E7D32",
    fontSize: "14px",
  }}
>
  Synergy / What Works Well Together
</strong>
                 {ingredientCheckerResult.synergies.length > 0 ? (
  ingredientCheckerResult.synergies.map((item, index) => (
    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.8" }}>
      • {item}
    </div>
  ))
) : (
  <div style={{ color: "#444" }}>• No strong synergy detected in this simplified logic.</div>
)}
                </div>

                <div style={infoBlockStyle(ingredientCheckerResult.sectionBg)}>
                 <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#C62828",
    fontSize: "14px",
  }}
>
  Direct Conflict / What Should Not Be Mixed
</strong>
                 {ingredientCheckerResult.conflicts.length > 0 ? (
  ingredientCheckerResult.conflicts.map((item, index) => (
    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.8" }}>
      • {item}
    </div>
  ))
) : (
  <div style={{ color: "#444" }}>• No strong direct conflict detected in this simplified logic.</div>
)}
                </div>

                <div style={infoBlockStyle(ingredientCheckerResult.sectionBg)}>
                 <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#6A6485",
    fontSize: "14px",
  }}
>
  Strength / Intensity
</strong>
                  {ingredientCheckerResult.strengths.length > 0 ? (
                    ingredientCheckerResult.strengths.map((item, index) => (
                      <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                        • {item}
                      </div>
                    ))
                  ) : (
                    <div style={{ color: "#444" }}>• No strength data available for the entered items.</div>
                  )}
                </div>

                <div style={infoBlockStyle(ingredientCheckerResult.sectionBg)}>
                 <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#6A6485",
    fontSize: "14px",
  }}
>
  Caution Flags
</strong>
                  {ingredientCheckerResult.cautionFlags.length > 0 ? (
                    ingredientCheckerResult.cautionFlags.map((item, index) => (
                      <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                        • {item}
                      </div>
                    ))
                  ) : (
                    <div style={{ color: "#444" }}>• No caution data available for the entered items.</div>
                  )}
                </div>

                <div style={infoBlockStyle(ingredientCheckerResult.sectionBg)}>
                  <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                    Optimal pH / Formula Notes
                  </strong>
                  {ingredientCheckerResult.optimalPH.length > 0 ? (
                    ingredientCheckerResult.optimalPH.map((item, index) => (
                      <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                        • {item}
                      </div>
                    ))
                  ) : (
                    <div style={{ color: "#444" }}>• No pH-related note available for the entered items.</div>
                  )}
                </div>

                <div style={infoBlockStyle(ingredientCheckerResult.sectionBg)}>
                 <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                    Developer Notes
                  </strong>
                  {ingredientCheckerResult.developerNotes.map((item, index) => (
                    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                      • {item}
                    </div>
                  ))}
                </div>

                <div style={infoBlockStyle(ingredientCheckerResult.sectionBg)}>
                 <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#3F3A5B",
    fontSize: "14px",
  }}
>
                    Extra Notes Per Ingredient
                  </strong>
                  {ingredientCheckerResult.notes.map((item, index) => (
                    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
                      • {item}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

       {activeTab === "routine" && (
  <div
    style={{
background: "linear-gradient(145deg, #ffffff, #f3f0ff)",
borderRadius: "24px",
padding: "32px",
boxShadow: "0 10px 30px rgba(108,99,255,0.12)",
border: "1px solid rgba(108,99,255,0.15)",
backdropFilter: "blur(6px)",
    }}
  >
<h2
  style={{
    textAlign: "center",
    marginBottom: "10px",
    fontSize: "26px",
    fontWeight: "700",
    background: "linear-gradient(135deg, #6C63FF, #8E85FF)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  }}
>
  📅 {t.routineTitle}
</h2>

<p
  style={{
    textAlign: "center",
    color: "#777",
    marginBottom: "35px",
    fontSize: "16px",
    lineHeight: "1.7",
    maxWidth: "720px",
    marginInline: "auto",
  }}
>
  {t.routineSubtitle}
</p>

    <div style={productCardStyle}>
      <div style={{ marginBottom: "18px" }}>
        <label
  style={{
    fontWeight: "600",
    display: "block",
    marginBottom: "6px",
    color: "#4B4563",
    fontSize: "14px",
  }}
>
          {t.skinType}
        </label>
        <select
          value={routineSkinType}
          onChange={(e) => setRoutineSkinType(e.target.value)}
          style={inputStyle}
        >
          <option value="">{t.selectSkinType}</option>
          <option value="Oily">{t.oily}</option>
          <option value="Dry">{t.dry}</option>
          <option value="Combination">{t.combination}</option>
          <option value="Sensitive">{t.sensitive}</option>
        </select>
      </div>

      <div>
        <label
  style={{
    fontWeight: "600",
    display: "block",
    marginBottom: "6px",
    color: "#4B4563",
    fontSize: "14px",
  }}
>
          {t.mainConcern}
        </label>
        <select
          value={routineConcern}
          onChange={(e) => setRoutineConcern(e.target.value)}
          style={inputStyle}
        >
          <option value="">{t.selectMainConcern}</option>
          <option value="acne">{t.acne}</option>
          <option value="dryness">{t.dryness}</option>
          <option value="pigmentation">{t.pigmentation}</option>
          <option value="general">{t.generalCare}</option>
        </select>
      </div>
    </div>

    <div style={{ textAlign: "center", marginBottom: "40px" }}>
<button
  onClick={handleRoutineBuild}
  onMouseEnter={(e) => {
    e.target.style.transform = "translateY(-2px)";
  }}
  onMouseLeave={(e) => {
    e.target.style.transform = "translateY(0)";
  }}
  style={{
    padding: "14px 26px",
    borderRadius: "14px",
    border: "none",
    background: "linear-gradient(135deg, #6C63FF, #8E85FF)",
    color: "white",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
    boxShadow: "0 6px 18px rgba(108,99,255,0.35)",
    transition: "all 0.25s ease",
  }}
>
  {t.buildMyRoutine}
</button>
    </div>

    {routineResult && (
      <div
        style={{
          background: routineResult.bg,
          border: `1px solid ${routineResult.border}`,
          borderRadius: "18px",
          padding: "24px",
          textAlign: language === "ar" ? "right" : "left",
        }}
      >
        <img
  src="/images/2.png"
  alt="Routine visual"
  style={{
    width: "100%",
    maxHeight: "220px",
    objectFit: "contain",
    borderRadius: "16px",
    marginBottom: "18px",
    background: "rgba(255,255,255,0.6)",
    padding: "8px",
    border: "1px solid rgba(0,0,0,0.05)",
  }}
/>
        <div style={{ marginBottom: "16px" }}>
<h3
  style={{
    margin: 0,
    color: routineResult.titleColor,
    fontSize: "24px",
    fontWeight: "700",
    letterSpacing: "0.2px",
  }}

>
  ✨ {routineResult.title}
</h3>
        </div>
        
<p
  style={{
    color: "#444",
    lineHeight: "1.7",
    marginTop: 0,
    marginBottom: "18px",
  }}
>
  {routineResult.summary}
</p>

<div
  style={{
    height: "4px",
    width: "60px",
    background: routineResult.titleColor,
    borderRadius: "4px",
    marginTop: "-4px",
    marginBottom: "18px",
  }}
/>

        <div style={{ marginBottom: "18px" }}>
          <strong style={{ color: "#333" }}>{t.selectedProfile}</strong>
          <div
            style={{
              marginTop: "10px",
              color: "#444",
              background: "rgba(255,255,255,0.65)",
borderRadius: "12px",
padding: "12px 14px",
border: "1px solid rgba(0,0,0,0.05)",
fontSize: "14px",
lineHeight: "1.6",
            }}
          >
            {t.skinTypeLabel}: {routineResult.skinType} — {t.concern}: {routineResult.concern}
          </div>
        </div>

<div
  style={{
    ...infoBlockStyle(routineResult.sectionBg),
    border: "1px solid rgba(0,0,0,0.06)",
    boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
    padding: "18px",
  }}
>
  <strong
    style={{
      display: "block",
      marginBottom: "14px",
      color: "#2F2A45",
      fontSize: "15px",
      fontWeight: "700",
    }}
  >
    {t.morningRoutine}
  </strong>

  {routineResult.morningRoutine.map((item, index) => (
    <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
      {index + 1}. {item}
    </div>
  ))}
</div>

        <div
  style={{
    ...infoBlockStyle(routineResult.sectionBg),
    border: "1px solid rgba(0,0,0,0.06)",
    boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
    padding: "18px",
  }}
>
 <strong
  style={{
    display: "block",
    marginBottom: "14px",
    color: "#2F2A45",
    fontSize: "15px",
    fontWeight: "700",
  }}
>
            {t.nightRoutine}
          </strong>

          {routineResult.nightRoutine.map((item, index) => (
            <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
              {index + 1}. {item}
            </div>
          ))}
        </div>

        <div
  style={{
    ...infoBlockStyle(routineResult.sectionBg),
    border: "1px solid rgba(0,0,0,0.06)",
    boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
    padding: "18px",
  }}
>
          <strong
  style={{
    display: "block",
    marginBottom: "12px",
  color: "#6A6485",
fontSize: "14px",
  }}
>
            {t.suggestedProducts}
          </strong>

          {routineResult.suggestedProducts.map((item, index) => (
            <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
              • {item}
            </div>
          ))}
        </div>

        <div style={infoBlockStyle(routineResult.sectionBg)}>
          <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#6A6485",
    fontSize: "14px",
  }}
>
            {t.orderOfUse}
          </strong>

          {routineResult.usageOrder.map((item, index) => (
            <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
              {index + 1}. {item}
            </div>
          ))}
        </div>

        <div style={infoBlockStyle(routineResult.sectionBg)}>
          <strong
  style={{
    display: "block",
    marginBottom: "12px",
    color: "#6A6485",
    fontSize: "14px",
  }}
>
            {t.aiNotes}
          </strong>

          {routineResult.aiNotes.map((item, index) => (
            <div key={index} style={{ marginBottom: "8px", color: "#444", lineHeight: "1.6" }}>
              • {item}
            </div>
          ))}
        </div>
      </div>
    )}
  </div>
)}
      </div>
    </div>
  );
}

export default App;
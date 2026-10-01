"""
Seed data generator containing ~260 realistic, detailed reviews across 4 distinct categories:
Products, Restaurants, Movies, and Mobile Apps.
"""

CATEGORIES_DATA = [
    {
        "name": "Products",
        "slug": "products",
        "description": "Consumer electronics, gadgets, home hardware, and smart appliances.",
        "icon": "package"
    },
    {
        "name": "Restaurants",
        "slug": "restaurants",
        "description": "Culinary dining, fine dining, bistros, cafes, and street food.",
        "icon": "utensils"
    },
    {
        "name": "Movies",
        "slug": "movies",
        "description": "Theatrical releases, indie films, streaming cinema, and documentaries.",
        "icon": "film"
    },
    {
        "name": "Mobile Apps",
        "slug": "mobile-apps",
        "description": "iOS and Android apps spanning productivity, finance, health, and utilities.",
        "icon": "smartphone"
    }
]

USERS_DATA = [
    {"username": "alex_tech", "email": "alex.chen@example.com"},
    {"username": "sarah_foodie", "email": "sarah.m@example.com"},
    {"username": "cinephile_dan", "email": "daniel.k@example.com"},
    {"username": "emily_dev", "email": "emily.watson@example.com"},
    {"username": "marcus_reviews", "email": "marcus.v@example.com"},
    {"username": "priya_patel", "email": "priya.p@example.com"},
    {"username": "jordan_b", "email": "jordan.blake@example.com"},
    {"username": "elena_g", "email": "elena.g@example.com"},
    {"username": "liam_audio", "email": "liam.audio@example.com"},
    {"username": "chloe_taste", "email": "chloe.t@example.com"},
    {"username": "david_movies", "email": "david.ross@example.com"},
    {"username": "zack_app_tester", "email": "zack.tester@example.com"},
    {"username": "hannah_design", "email": "hannah.d@example.com"},
    {"username": "robert_c", "email": "robert.clark@example.com"},
    {"username": "sophia_w", "email": "sophia.w@example.com"}
]

# Raw templates per category to generate realistic reviews with variable dates and ratings
PRODUCTS_RAW = [
    # Positive
    ("Sony WH-1000XM5", "Unrivaled noise cancellation and comfort", "The active noise cancellation on these headphones is absolute wizardry on flights and train commutes. Soundstage is wide, battery life easily hits 30 hours, and the microphone clarity in Zoom calls is noticeably improved over the XM4. Best travel gear I own.", 5, 42, "2024-01-05"),
    ("Keychron Q1 Pro", "Outstanding tactile typing feel", "CNC aluminum chassis with pre-lubed mechanical switches makes typing an absolute joy. Heavy build quality prevents any desk slip, and the wireless bluetooth seamlessly switches between my MacBook and Windows workstation.", 5, 29, "2024-01-12"),
    ("Logitech MX Master 3S", "The undisputed productivity mouse king", "The MagSpeed electromagnetic scroll wheel and ergonomic thumb rest eliminate all wrist fatigue during long coding sessions. The silent clicks are satisfying and ideal for open plan offices.", 5, 35, "2024-01-18"),
    ("Dell UltraSharp U2723QE", "Flawless IPS Black contrast and color accuracy", "Color calibration straight out of the box was spot on for graphic design. The USB-C hub with 90W power delivery charges my laptop with a single clean cable. Deep blacks and crystal sharp 4K text.", 5, 19, "2024-01-25"),
    ("Kindle Paperwhite 11th Gen", "Best reading gadget ever made", "Warm light adjustment makes night reading effortless on the eyes. The battery literally lasts for weeks on a single charge. Waterproof design is perfect for beach trips and baths.", 5, 51, "2024-02-02"),
    ("Anker 737 Power Bank", "Incredible 140W fast charging speeds", "Charges my 16-inch MacBook Pro at maximum speed while also topping up my phone. The dynamic smart digital display showing wattage output and estimated charge time is immensely helpful.", 5, 16, "2024-02-10"),
    ("Breville Barista Touch", "Cafe quality espresso at home", "The automated steam wand produces silky microfoam effortlessly. Grinder settings are accurate and intuitive touchscreen guides make pulling a rich double shot foolproof.", 5, 38, "2024-02-15"),
    ("Dyson V15 Detect", "Astounding suction power and laser visibility", "The green laser reveals microscopic dust on hardwood floors that traditional vacuums completely miss. Suction adjusts automatically based on dirt levels. Worth every dollar.", 5, 27, "2024-02-22"),
    ("Apple Watch Ultra 2", "Incredible outdoor battery and screen brightness", "The 3000 nit display is fully readable in blazing direct sunlight. Dual-frequency GPS track mapping is insanely accurate on mountain trail runs, and the titanium casing is virtually indestructible.", 5, 33, "2024-03-01"),
    ("Steam Deck OLED", "The premier handheld PC gaming experience", "The OLED panel delivers phenomenal contrast, HDR pop, and vibrant colors. Fan noise is nearly inaudible compared to the original LCD model, and the 90Hz refresh rate makes gameplay ultra smooth.", 5, 64, "2024-03-08"),
    
    # Moderate / Neutral
    ("Bose QuietComfort Ultra", "Great sound and comfort, but software glitches", "The spatial audio immersion is wonderful and ear cushions are plush. However, the companion iOS app frequently loses connection and requires re-pairing. Decent hardware plagued by clunky software.", 3, 14, "2024-01-08"),
    ("Samsung Galaxy S24 Ultra", "Powerhouse performance hampered by anti-glare grain", "Snapdragon performance and camera zoom are extraordinary. However, in low brightness environments, the anti-reflective glass exhibits a slight grain effect. A premium device with subtle quirks.", 3, 21, "2024-01-20"),
    ("Ninja Air Fryer Pro", "Fast cooking, but takes up too much counter space", "Crisps french fries and chicken tenders evenly without excessive oil. The basket is easy to clean, but the exterior footprint is bulky for small studio kitchens.", 3, 9, "2024-02-04"),
    ("Fitbit Charge 6", "Solid fitness tracking, missing third-party sync", "Step counting and continuous heart rate tracking are reliable. Google Maps integration is convenient, but the mandatory Google account migration broke several older social features.", 3, 11, "2024-02-18"),
    ("Razer BlackShark V2", "Crisp gaming audio, mediocre microphone build", "Directional positional audio in competitive shooters is crisp and accurate. The volume potentiometer feels somewhat loose after four months of usage.", 3, 7, "2024-03-05"),

    # Negative
    ("SmartHome Thermostat X", "Unreliable WiFi connection and persistent sensor drops", "Constantly disconnects from the home network every three days, causing the HVAC system to default to uncomfortable temperatures. Customer support offered zero meaningful troubleshooting assistance.", 1, 48, "2024-01-14"),
    ("HyperGlide Gaming Mouse", "Terrible double-clicking issue within weeks", "Both the left switch and the scroll wheel developed severe double-click stutter after barely a month. Build feels cheap and plastic creaks under normal grip pressure.", 1, 31, "2024-01-27"),
    ("EcoClean Robot Vacuum", "Gets stuck everywhere and app mapping is broken", "The vacuum gets stranded on standard low-pile area rugs and loses its stored room maps repeatedly. It spends more time crying for help with error beeps than actually vacuuming.", 1, 57, "2024-02-12"),
    ("Aura Glow Smart Lamp", "Flickers violently and Bluetooth setup failed", "The companion application refuses to discover the lamp over Bluetooth on modern Android phones. When plugged in, the LED driver makes an annoying high-pitched buzzing whine.", 1, 24, "2024-02-28"),
    ("UltraSlim Wireless Charger", "Overheats phone and charges at an agonizing crawl", "Instead of fast charging, it triggered the phone's thermal safety shutdown within twenty minutes. Unsafe design and completely fails to deliver advertised wattage.", 1, 39, "2024-03-14"),

    # Additional Realistic Reviews
    ("Sony WH-1000XM5", "Great audio fidelity but earcups get warm", "Sound quality is remarkably well-balanced, but during long three hour video editing sessions my ears get noticeably warm. ANC remains the best in class.", 4, 18, "2024-01-16"),
    ("Keychron Q1 Pro", "Sturdy keyboard, south-facing LEDs take getting used to", "Typing resonance is solid and heavy. The keycaps have clear lettering, though south-facing LEDs mean shine-through legends are dim in dark rooms.", 4, 12, "2024-01-30"),
    ("Dell UltraSharp U2723QE", "Occasional wake-from-sleep delay on Mac", "Superb panel clarity and vivid sRGB coverage. Only drawback is a 4-second delay when waking up from M2 Mac sleep mode over Thunderbolt.", 4, 8, "2024-02-08"),
    ("Breville Barista Touch", "Steep price tag but durable espresso maker", "Takes a bit of practice to dial in the grind size for freshly roasted beans, but once dialed, the crema is thick and flavorful.", 4, 23, "2024-02-25"),
    ("Logitech MX Master 3S", "A bit large for petite hands", "Feature-rich and smooth gesture controls, but my partner finds it too bulky for smaller hand sizes. Exceptional battery lifespan however.", 4, 15, "2024-03-10"),
    ("SmartHome Thermostat X", "Mediocre scheduling interface", "The energy savings reports are neat, but programming custom weekly heating schedules is unnecessarily convoluted on the small touchscreen.", 2, 19, "2024-01-22"),
    ("HyperGlide Gaming Mouse", "Lightweight but sensor skips on cloth pads", "The PTFE feet glide effortlessly, but the optical sensor occasionally skips pixels during fast flick shots in FPS games.", 2, 14, "2024-02-14"),
    ("Ninja Air Fryer Pro", "Fan is louder than expected", "Food tastes great and cooks in half the oven time, but the cooling fan is quite noisy and stays on for several minutes after cooking.", 3, 6, "2024-03-02"),
    ("Kindle Paperwhite 11th Gen", "Page turns are responsive and crisp", "Text looks identical to printed book paper. The flush front screen is sleek and dust-resistant. Cannot imagine traveling without it.", 5, 28, "2024-01-10"),
    ("Dyson V15 Detect", "Battery drains quickly in Boost mode", "Standard suction is more than sufficient for everyday floors. Boost mode cleans carpets thoroughly but cuts battery life to roughly 12 minutes.", 4, 17, "2024-02-20"),
    ("Anker 737 Power Bank", "Bulky for coat pockets but charges laptops like a champ", "It is quite heavy to carry around in a jacket, but keeping it inside a backpack completely eliminates low-battery anxiety on full working days.", 4, 22, "2024-03-12"),
    ("Apple Watch Ultra 2", "Way too bulky under dress shirt cuffs", "Rugged outdoor capabilities are unmatched, but the massive 49mm casing makes buttoning tight formal shirt cuffs difficult.", 3, 10, "2024-01-28"),
    ("Steam Deck OLED", "Battery life improvement is night and day", "Playing demanding indie games and AAA titles with deep inky blacks and vivid colors is a joy. The updated WiFi 6E chip downloads games twice as fast.", 5, 45, "2024-02-16"),
    ("Aura Glow Smart Lamp", "Colors are nice when it finally connects", "The ambient sunrise alarm feature is gentle and pleasant. However, getting the initial WiFi handshake took five frustrating factory resets.", 2, 8, "2024-03-04"),
    ("UltraSlim Wireless Charger", "Disappointing charging radius", "If the smartphone is even half an inch off dead center, charging stops completely and the notification LED flashes red.", 2, 16, "2024-01-19"),
    ("Bose QuietComfort Ultra", "Supremely comfortable on marathon flights", "The headphone weight distribution is exceptional. Zero ear clamp pressure even after a 10-hour flight across the Atlantic.", 5, 34, "2024-02-06"),
    ("Samsung Galaxy S24 Ultra", "The flat display is a massive improvement", "Finally eliminating the curved glass edges makes using the S-Pen so much better. Battery easily lasts 1.5 days of heavy mixed usage.", 5, 29, "2024-02-24"),
    ("EcoClean Robot Vacuum", "Consistently misses baseboards and corners", "Navigates open living rooms decently, but fails to reach perimeter baseboards and the spinning edge brush throws crumbs outward instead of vacuuming them.", 2, 13, "2024-03-15"),
    ("Fitbit Charge 6", "Accurate sleep score and silent vibration alarm", "The sleep stage breakdown correlates well with how rested I feel. The gentle haptic wrist alarm wakes me up without waking my spouse.", 4, 20, "2024-01-24"),
    ("Razer BlackShark V2", "Solid budget headset for competitive gaming", "The passive noise isolation from the memory foam cushions blocks room fans effectively. Audio EQ presets in Synapse are convenient.", 4, 11, "2024-02-11"),
    ("MacBook Air M3", "Silent powerhouse with all-day battery endurance", "Editing 4K ProRes videos without hearing a single fan hiss is pure magic. The midnight finish looks gorgeous and finger-print resistance is notably improved.", 5, 58, "2024-01-14"),
    ("AirPods Pro 2 USB-C", "Adaptive audio transparency is unmatched", "The seamless blend between active noise cancellation and transparency when someone speaks to you in the office works reliably without needing to take out the earbuds.", 5, 47, "2024-02-03"),
    ("LG C3 OLED 55-inch", "Incredible gaming specs with 4K 120Hz and G-Sync", "Instantaneous pixel response times and perfect black levels elevate console gaming. WebOS interface is snappy, though initial picture settings needed calibration.", 5, 39, "2024-02-19"),
    ("Herman Miller Aeron Chair", "Ergonomic savior for chronic lumbar back pain", "After eight hour work days my lower back has stopped aching completely. The Pellicle mesh keeps you cool and posture naturally upright. Lifetime investment.", 5, 61, "2024-03-01"),
    ("Garmin Forerunner 265", "Vibrant AMOLED screen and marathon training readiness", "Training readiness metrics helped me avoid overtraining injuries. Physical buttons make lap timing simple with sweaty workout gloves.", 5, 32, "2024-03-11"),
    ("Ninja Creami Deluxe", "Fun ice cream maker, but deafening blender roar", "Produces decadent protein ice cream and fruit sorbets with silky smooth texture. However, the churning motor sounds like an industrial jet engine.", 3, 25, "2024-01-21"),
    ("Asus ROG Ally Z1 Extreme", "Great screen and ergonomics, battery disappears", "Handles modern PC games smoothly at 1080p, but high wattage mode drains the battery within 50 minutes. Requires tethering to a heavy power brick.", 3, 21, "2024-02-14"),
    ("Sony A7 IV Mirrorless", "Autofocus tracking is black magic, menu is dense", "Eye-tracking autofocus locks onto moving subjects instantly. Menus are packed with endless nested settings that require hours to configure.", 4, 19, "2024-03-04"),
    ("Shure SM7B Vocal Mic", "Warm broadcast vocal tone, needs high preamp gain", "Legendary microphone for podcasts and vocal recording. Keep in mind you will definitely need a Cloudlifter or high-gain audio interface to power it.", 4, 37, "2024-01-31"),
    ("SoundPulse Bluetooth Speaker", "Muffled bass and distorted sound above 60% volume", "Sound quality is hollow and muddy. Turning the volume past halfway introduces severe harsh distortion on high frequencies. Complete letdown.", 1, 41, "2024-02-23"),
    ("RapidCharge 65W GaN Plug", "Sparks in wall outlet and stopped working after 3 weeks", "Plugged it into a standard living room outlet and saw a visible electrical spark. The USB-C port died completely and will not charge anything.", 1, 52, "2024-03-08")
]

RESTAURANTS_RAW = [
    # Positive
    ("Osteria Francescana", "A transcendent culinary journey through Italian heritage", "Every course was a masterclass in balance and storytelling. The five ages of Parmigiano Reggiano exhibited extraordinary texture variance. Wine pairing from the head sommelier was flawless.", 5, 62, "2024-01-04"),
    ("Ichiran Ramen Shibuya", "Rich tonkotsu broth with perfectly customized noodle firmness", "The private solo dining booth allows complete focus on the meal. The rich pork bone broth was decadent without being greasy, and the signature red spicy sauce provided an invigorating kick.", 5, 44, "2024-01-11"),
    ("Blue Fin Sushi Lounge", "Melt in your mouth Otoro and exquisite omakase", "Chef Hiroshi presented 14 courses of seasonal fish flown directly from Toyosu market. The akami tuna marinated in soy and the seared Hokkaido scallop with yuzu were unforgettable.", 5, 37, "2024-01-17"),
    ("The Rustic Hearth Bistro", "Wood-fired perfection with local farm-to-table produce", "The roasted bone marrow with sourdough toast and the dry-aged ribeye steak were seared to absolute perfection. Cozy ambiance with a roaring fireplace and attentive waitstaff.", 5, 29, "2024-01-26"),
    ("Taqueria Los Compadres", "Authentic street tacos packed with explosive flavors", "Hands down the best al pastor and carne asada in town. Hand-pressed corn tortillas, freshly charred pineapple, and a salsa verde with the perfect level of cilantro and habanero heat.", 5, 53, "2024-02-03"),
    ("Le Petite Croissant", "Flakiest buttery croissants outside of Paris", "The almond croissant had a rich, creamy frangipane filling with toasted slivered almonds on top. Pair it with their velvety double espresso for an ideal breakfast.", 5, 31, "2024-02-09"),
    ("Golden Dragon Dumpling House", "Steaming soup dumplings bursting with savory broth", "The pork and crab xiao long bao are masterfully crafted with thin delicate skins that do not tear. The scallion pancakes were crispy, golden, and completely non-greasy.", 5, 40, "2024-02-17"),
    ("Smokey Bones BBQ", "Tender brisket with deep smoky bark", "The brisket had a gorgeous pink smoke ring and pulled apart with a fork. The sweet vinegar coleslaw cut the richness beautifully. Outstanding craft beer selection on tap.", 5, 26, "2024-02-23"),
    ("Truffle & Basil", "Handmade pasta and fragrant black truffle cream sauce", "The tagliolini with shaved black truffles was pure luxury on a plate. Warm, crusty focaccia bread served with Sicilian olive oil set an inviting tone for dinner.", 5, 35, "2024-03-03"),
    ("Sweet Green Salads", "Fresh crisp greens and vibrant seasonal grain bowls", "The harvest bowl with roasted sweet potatoes, warm wild rice, and creamy balsamic vinaigrette is my go-to lunch. Clean, nutritious, and consistently fresh ingredients.", 5, 18, "2024-03-09"),

    # Neutral / Mixed
    ("Ichiran Ramen Shibuya", "Delicious broth, but two hour queue in the rain", "The ramen itself is comforting and delicious, but standing outside in an unmanaged queue for over 90 minutes slightly dampened the overall dining experience.", 3, 22, "2024-01-09"),
    ("The Rustic Hearth Bistro", "Hearty food, but acoustically deafening on weekends", "Steak and cocktails were delicious, but the industrial dining room acoustic design made holding a normal conversation across the table nearly impossible without shouting.", 3, 14, "2024-01-23"),
    ("Blue Fin Sushi Lounge", "Exquisite sushi marred by rushed course pacing", "Fish quality was unquestionably pristine, but the servers brought out three courses simultaneously instead of pacing them out. At this price tier, service should feel relaxed.", 3, 17, "2024-02-07"),
    ("Sweet Green Salads", "Good food, but portion sizes are shrinking", "Tastes great and feels healthy, but the bowl was only three-quarters full today despite charging over sixteen dollars. Quality remains high, value is slipping.", 3, 13, "2024-02-19"),
    ("Smokey Bones BBQ", "Great ribs, lukewarm mac and cheese", "The smoked baby back ribs were tender and smoky, but our side orders of cornbread and mac and cheese arrived lukewarm and dry.", 3, 8, "2024-03-06"),

    # Negative
    ("Pasta Pronto Express", "Cold rubbery noodles drowned in watery sauce", "The fettuccine was severely overcooked and clumped together in an oily pool. The chicken was dry, unseasoned, and rubbery. Avoid this tourist trap at all costs.", 1, 55, "2024-01-13"),
    ("Ocean Catch Seafood Grill", "Fishy smelling oysters and terribly sluggish service", "Our party waited forty-five minutes just for water glasses. When the raw oysters finally arrived, they smelled rancid and off-putting. Two of our friends suffered food poisoning.", 1, 68, "2024-01-29"),
    ("Burger Joint Deluxe", "Soggy buns, lukewarm patties, and indifferent staff", "The burger was a greasy mess that disintegrated the moment it was picked up. Fries were cold and soggy, and the cashier seemed annoyed that we dared to ask for napkins.", 1, 37, "2024-02-13"),
    ("Spice Palace Indian Diner", "Bland curries with tough meat and burnt naan", "The butter chicken lacked any depth of spice and tasted like plain tomato paste with sugar. The garlic naan arrived blackened and charred bitter on the underside.", 1, 41, "2024-02-27"),
    ("Cafe Bonjour Corner", "Overpriced stale pastries and rude management", "The chocolate croissant was dry as cardboard and clearly leftover from the previous morning. When we politely mentioned this to the manager, she rolled her eyes and refused a refund.", 1, 33, "2024-03-13"),

    # Additional Reviews
    ("Osteria Francescana", "Artful presentation and courteous staff", "Intimate setting with attentive service. Every dish looks like modern art, although the portions are strictly minimalist as expected for avant-garde dining.", 4, 15, "2024-01-15"),
    ("Taqueria Los Compadres", "Flavorful tacos, limited indoor seating", "Food is consistently ten out of ten. Only downside is there are only three small metal tables inside, so be prepared to eat in your car during lunch rush.", 4, 21, "2024-01-31"),
    ("Le Petite Croissant", "Best sourdough baguettes in the neighborhood", "Crisp crust with an airy, chewy crumb. Sells out rapidly by 10 AM on Saturday mornings, so set your alarm early.", 4, 19, "2024-02-11"),
    ("Golden Dragon Dumpling House", "Incredible chili oil wontons", "The spicy chili vinaigrette on the steamed pork wontons has the ideal balance of garlic, vinegar, and Sichuan peppercorn tingle.", 5, 27, "2024-02-21"),
    ("Truffle & Basil", "Romantic atmosphere and great cocktail list", "Dimly lit tables, soft jazz, and an inventive rosemary gin fizz cocktail make this a top-tier date night restaurant.", 4, 16, "2024-03-07"),
    ("Pasta Pronto Express", "Uncooked garlic overpowering everything", "They threw raw minced garlic into the marinara sauce without sauteing it first. Left a harsh burning aftertaste the entire evening.", 2, 11, "2024-01-21"),
    ("Ocean Catch Seafood Grill", "Overcooked dry salmon", "The grilled salmon filet was cooked past well-done until completely dried out and chalky. Tartar sauce was the only thing giving it moisture.", 2, 18, "2024-02-05"),
    ("Burger Joint Deluxe", "Decent milkshake, mediocre fries", "The salted caramel thick shake was tasty, but the fries were completely unsalted and limp.", 2, 7, "2024-02-26"),
    ("Spice Palace Indian Diner", "Biryani was okay, raita tasted sour", "Rice grains were well separated and aromatic, but the yogurt raita side was spoiled and tasted distinctly sour.", 2, 14, "2024-03-11"),
    ("Cafe Bonjour Corner", "Coffee is decent, seating is cramped", "The flat white was properly extracted, but tables are packed so tightly together you are virtually sharing a conversation with neighboring strangers.", 3, 9, "2024-01-18"),
    ("Ichiran Ramen Shibuya", "Consistently hits the spot late at night", "Being open 24 hours makes this a life-saver after late night flights. The matcha pudding dessert is surprisingly refreshing.", 5, 30, "2024-02-01"),
    ("The Rustic Hearth Bistro", "Outstanding roasted duck breast", "Crispy rendered skin and succulent medium-rare meat paired with cherry port wine reduction. Server was knowledgeable about local winery vintages.", 5, 24, "2024-02-15"),
    ("Blue Fin Sushi Lounge", "Fresh uni with nori crisps", "Sea urchin from Santa Barbara was sweet, creamy, and briny. Rice temperature was warm and seasoned with traditional red vinegar.", 5, 22, "2024-03-01"),
    ("Sweet Green Salads", "Fast and healthy meal prep option", "Order ahead via their mobile app and your bowl is ready on the pickup shelf within five minutes. Great for busy professionals.", 4, 12, "2024-03-10"),
    ("Smokey Bones BBQ", "Pulled pork sandwich was stacked high", "Generous portion of smoked pork shoulder drizzled with tangy Carolina mustard sauce on a toasted brioche bun.", 4, 15, "2024-01-27"),
    ("Osteria Francescana", "Memory of a Mortadella sandwich was divine", "Elevating street food flavors into fine dining foam and gnocco fritto. Creative, thought-provoking, and delicious.", 5, 36, "2024-02-10"),
    ("Taqueria Los Compadres", "Salsa bar is top notch", "Four varieties of house-made salsas ranging from mild avocado crema to fire-roasted habanero. Pickled carrots and radishes are always fresh.", 5, 25, "2024-02-24"),
    ("Burger Joint Deluxe", "Way too greasy and heavy", "Felt sick an hour after eating the double bacon stack. The grease soaked completely through two paper wrappers.", 1, 29, "2024-03-04"),
    ("Ocean Catch Seafood Grill", "Manager argued over defective crab claws", "Crab claws were dry and hollow. Instead of apologizing, the floor manager argued that this is normal seasonality. Appalling attitude.", 1, 44, "2024-03-16"),
    ("Le Petite Croissant", "Pain au chocolat with real dark chocolate batons", "Laminated layers shattered in buttery shards with every bite. Authentic French bakery mastery in every pastry.", 5, 33, "2024-01-25"),
    ("Dishoom Covent Garden", "Black Daal and bacon naan roll are legendary", "The twenty-four hour simmered black daal has unbelievable velvet richness. The chai tea is spiced perfectly and refills keep coming with warmth.", 5, 62, "2024-02-12"),
    ("Joe's Pizza Greenwich Village", "The quintessential New York thin crust slice", "Crisp bottom with zero sag, tangy sweet tomato sauce, and gooey whole milk mozzarella. Cheap, blistering hot, and iconic.", 5, 54, "2024-02-28"),
    ("Din Tai Fung", "Consistency of soup dumplings across continents is shocking", "Every single xiao long bao has exactly 18 delicate folds. The spicy cucumber salad and pork chop fried rice are equally exquisite.", 5, 48, "2024-03-05"),
    ("Momofuku Noodle Bar", "Pork belly buns are pillow soft perfection", "Hoisin sauce with quick-pickled cucumber and meltingly tender pork belly. Pork ramen broth is deeply savory and hearty.", 5, 39, "2024-01-14"),
    ("Tartine Bakery", "Country sourdough bread with an incredible caramelized crust", "The sourdough loaf is an artisan masterpiece. Morning buns with citrus orange zest and cinnamon are worth the long Sunday line.", 5, 41, "2024-02-08"),
    ("Shake Shack", "ShackBurger is dependable, crinkle fries are mediocre", "The smashed beef patty with Martin's potato roll and ShackSauce always hits the spot. Crinkle cut fries still feel somewhat frozen and bland.", 3, 19, "2024-02-21"),
    ("Waffle King Diner", "Sticky tables and watered down maple syrup", "The server ignored us for twenty minutes while chatting in the corner. The waffle was gummy, served with cold butter that refused to melt.", 1, 38, "2024-03-12"),
    ("Curry House Express", "Oily butter chicken and stale basmati rice", "The oil was separated on top of the curry container in a yellow puddle. Chicken pieces were tough and chewy.", 1, 29, "2024-01-28"),
    ("Sizzling Fajita Cantina", "Tasteless guacamole made with unripe avocados", "Guacamole was hard, flavorless, and devoid of lime juice or salt. The fajita skillet arrived lukewarm without any sizzle.", 2, 21, "2024-02-17"),
    ("Green Garden Veggie Cafe", "Creative plant-based dishes with vibrant herbs", "The cashew mac and cheese and jackfruit carnitas tacos tasted amazingly satisfying. Freshly pressed ginger turmeric juice was revitalizing.", 5, 27, "2024-03-02")
]

MOVIES_RAW = [
    # Positive
    ("Oppenheimer", "A towering biographical achievement in cinematic tension", "Christopher Nolan crafts an intense psychological study of consequence. Cillian Murphy delivers the performance of a lifetime, and Ludwig Göransson's propulsive score keeps your heart racing throughout the three-hour runtime.", 5, 78, "2024-01-03"),
    ("Dune: Part Two", "A monumental sci-fi spectacle with staggering scale", "Denis Villeneuve has created a modern science fiction landmark. The audio design of the sandworm riding sequences will rattle your chest in IMAX, and Greig Fraser's cinematography is hypnotic and majestic.", 5, 84, "2024-01-15"),
    ("Spider-Man: Across the Spider-Verse", "Revolutionary visual animation and emotional depth", "Every frame is an explosion of distinct artistic styles, from watercolor brushstrokes to punk rock collage. The relationship between Miles and Gwen is genuine and deeply poignant.", 5, 65, "2024-01-28"),
    ("Past Lives", "A quiet, devastatingly beautiful meditation on love and fate", "Celine Song's debut feature is gentle, nuanced, and emotionally devastating. The concept of In-Yun anchors an understated story of modern immigrant connection and bittersweet what-ifs.", 5, 49, "2024-02-05"),
    ("The Batman", "A gritty, rain-drenched detective noir masterpiece", "Robert Pattinson brings raw vulnerability and brooding intensity to the Dark Knight. Gotham feels like a living, corrupt metropolis straight out of David Fincher's Se7en.", 5, 57, "2024-02-14"),
    ("Anatomy of a Fall", "Electrifying courtroom drama dissecting truth and marriage", "Sandra Hüller's multilingual performance is utterly magnetic. The script keeps you perpetually questioning the boundary between objective truth and subjective narrative fabrication.", 5, 38, "2024-02-22"),
    ("Poor Things", "Audacious, hilarious, and visually breathtaking feminist fable", "Emma Stone gives a fearless comedic and dramatic performance as Bella Baxter. The surreal production design and warped wide-angle lenses create an unforgettable whimsical wonderland.", 5, 41, "2024-03-02"),
    ("Killers of the Flower Moon", "An unsparing and essential chronicle of systemic betrayal", "Martin Scorsese examines American history with unflinching moral gravity. Lily Gladstone commands every frame with quiet, powerful dignity.", 5, 50, "2024-03-09"),
    ("Barbie", "A vibrant, razor-sharp existential comedy with genuine heart", "Greta Gerwig manages to deliver both a technicolor spectacle and a resonant cultural critique. Ryan Gosling's comedic commitment as Ken stole every single scene.", 5, 59, "2024-03-15"),
    ("Mission Impossible: Dead Reckoning", "Relentless, breathtaking practical action choreography", "Tom Cruise and Christopher McQuarrie deliver pure adrenaline. The runaway steam train climax and Rome car chase sequence demonstrate why practical stunt work is superior to green screen.", 5, 46, "2024-01-10"),

    # Neutral / Mixed
    ("The Marvels", "Fun chemistry between leads hampered by chaotic pacing", "Iman Vellani's Kamala Khan brings infectious charm and joy, and the body-swapping fight choreography has clever moments. However, the villain is forgettable and the third act feels rushed.", 3, 25, "2024-01-19"),
    ("Napoleon", "Stunning battle sequences undermined by disjointed narrative", "The battle of Austerlitz is a triumph of military scale and visual staging. Yet the historical drama between Napoleon and Josephine feels cold, fragmented, and strangely unengaging.", 3, 31, "2024-02-02"),
    ("Wonka", "Sweet musical charm, slightly overly saccharine", "Timothée Chalamet is charming and energetic in the role, and Hugh Grant as an Oompa Loompa is hilarious. However, the songs feel somewhat forgettable compared to the 1971 classic.", 3, 19, "2024-02-18"),
    ("Rebel Moon - Part One", "Impressive visual worldbuilding dragged down by slow motion", "Zack Snyder creates fascinating costume designs and sci-fi aesthetic, but nearly every action shot is drowned in excessive slow motion, and character dialogue is largely exposition.", 3, 28, "2024-03-05"),
    ("Argylle", "Entertaining twists that overstay their welcome", "The first hour is a delightful spy caper with Sam Rockwell shining in action scenes. By twist number five in the final act, the plot collapses under its own absurdity.", 3, 16, "2024-03-12"),

    # Negative
    ("Madame Web", "A bewildering catastrophe of wooden acting and lazy CGI", "One of the most bafflingly incompetent comic book adaptations in modern memory. The ADR dubbing is painfully obvious, dialogue sounds written by early AI, and there is zero superhero action.", 1, 89, "2024-01-24"),
    ("The Exorcist: Believer", "A soulless cash grab stripping away the original dread", "Disrespects William Friedkin's horror classic by trading psychological terror and religious tension for cheap jump scares and hollow nostalgia bait.", 1, 62, "2024-02-08"),
    ("Expend4bles", "Abysmal green screen effects and geriatric action tropes", "Terrible low-budget digital blood, muddy lighting, and incomprehensible quick-cut editing. The franchise has completely run out of gas and creativity.", 1, 47, "2024-02-24"),
    ("Winnie the Pooh: Blood and Honey", "Unwatchable amateur exploitation with zero horror payoff", "Taking advantage of public domain copyright to produce a dark, incompetent slasher film. Terrible sound mixing, dreadful acting, and completely devoid of suspense.", 1, 53, "2024-03-06"),
    ("Ghostbusters: Frozen Empire", "Overstuffed nostalgia assembly line with too many characters", "With twelve main characters fighting for screen time, nobody gets an actual emotional arc. The spooky villain is defeated within five minutes of finally showing up.", 2, 34, "2024-03-17"),

    # Additional Reviews
    ("Oppenheimer", "Third act courtroom hearing dragged slightly", "The Trinity test sequence is cinema history, but the lengthy security clearance trial in cramped rooms lost some of the narrative momentum towards the final hour.", 4, 26, "2024-01-12"),
    ("Dune: Part Two", "Javier Bardem provides great comedic grounding", "Stilgar's devout belief in Paul brings surprising humor to a heavy political tragedy. The sound mixing in theater was thunderous.", 5, 33, "2024-01-22"),
    ("Spider-Man: Across the Spider-Verse", "Cliffhanger ending was frustrating in the theater", "Brilliant animation, but the sudden 'To Be Continued' title card felt jarring after over two hours of intense emotional buildup.", 4, 29, "2024-02-06"),
    ("Past Lives", "The silence between dialogue speaks volumes", "Subtle gazes and awkward body language convey more emotional heartbreak than monologue ever could. Beautiful cinematography.", 5, 21, "2024-02-16"),
    ("The Batman", "A bit long at three hours, but beautifully stylized", "Could easily have trimmed twenty minutes from the third act flood sequence, but the Batmobile ignition scene alone makes it worth seeing on a big screen.", 4, 30, "2024-02-28"),
    ("Madame Web", "Hilariously bad dialogue worth watching for laughs", "Line delivery like 'He was in the Amazon with my mom' had our entire theater erupting in laughter. Inadvertently the funniest comedy of the year.", 2, 42, "2024-01-30"),
    ("Poor Things", "Mark Ruffalo's performance is legendary", "Ruffalo's aristocratic temper tantrums and comedic timing complement Emma Stone's uninhibited journey of discovery perfectly.", 5, 25, "2024-02-12"),
    ("Barbie", "Production design deserves every Oscar", "Building real physical life-size Barbie dream houses without digital sets paid off tremendously. The costume design is iconic.", 5, 36, "2024-02-26"),
    ("The Marvels", "The cat scene was hilarious", "Shortest runtime in Marvel history is a blessing and a curse. Fun character interactions, but the emotional stakes felt nonexistent.", 3, 14, "2024-03-08"),
    ("Napoleon", "Costumes and set pieces were phenomenal", "Visually lavish representation of the French empire, even if the screenplay paints the titular character in a bizarrely pathetic light.", 3, 18, "2024-01-17"),
    ("Anatomy of a Fall", "The dog acting deserves special recognition", "Messi the border collie delivers an astonishing dramatic performance. The courtroom testimony scenes felt uncomfortably authentic.", 5, 27, "2024-02-01"),
    ("Killers of the Flower Moon", "Devastating historical chronicle", "Three and a half hours fly by because every performance is grounded in horrifying reality. Robert De Niro plays a terrifyingly calm sociopath.", 5, 31, "2024-02-15"),
    ("Wonka", "Heartwarming family movie for the holidays", "Exceeded expectations with its whimsical tone and colorful production. Hugh Grant steals every scene he enters.", 4, 20, "2024-02-27"),
    ("The Exorcist: Believer", "Boring characters and reliance on loud noises", "Failed to build any atmospheric tension. The demon makeup looked synthetic and unconvincing compared to the 1973 original.", 1, 35, "2024-03-10"),
    ("Rebel Moon - Part One", "Felt like a montage of other sci-fi movies", "Borrows heavily from Seven Samurai, Star Wars, and Warhammer without infusing a distinct personality of its own.", 2, 23, "2024-01-26"),
    ("Mission Impossible: Dead Reckoning", "Hayley Atwell is a fantastic addition to the team", "Grace brings an unpredictable pickpocket dynamic that contrasts wonderfully with Ethan Hunt's calculated precision.", 5, 32, "2024-02-09"),
    ("Ghostbusters: Frozen Empire", "Fun for kids, repetitive for longtime fans", "Nostalgic callbacks to Slimer and the Stay Puft Marshmallow men, but the new ice villain lacked screen time and menace.", 3, 15, "2024-02-23"),
    ("Argylle", "Horrible CGI cat took me out of the movie", "The digital green screen on the cat backpack looked worse than video games from ten years ago. Disappointing from Matthew Vaughn.", 2, 22, "2024-03-04"),
    ("Expend4bles", "Stallone is barely in it", "Promoted as a team reunion, but Sylvester Stallone disappears after fifteen minutes. Cheap fight choreography and uninspired sets.", 1, 30, "2024-03-14"),
    ("Winnie the Pooh: Blood and Honey", "Cheap cash grab devoid of talent", "Lighting is so pitch black you cannot even see what is happening on screen half the time. Total waste of cinema bandwidth.", 1, 41, "2024-01-08"),
    ("Interstellar", "Hans Zimmer score and emotional black hole voyage", "A modern sci-fi triumph. The docking scene with Hans Zimmer's pipe organ score remains one of the most thrilling cinematic sequences ever constructed.", 5, 76, "2024-01-11"),
    ("Everything Everywhere All At Once", "Mind-bending multiverse family drama with absurd humor", "Masterfully balances hot dog fingers and philosophical nihilism with deeply touching mother-daughter healing. Ke Huy Quan was mesmerizing.", 5, 68, "2024-01-29"),
    ("Parasite", "Impeccable social satire with razor sharp tonal shifts", "Bong Joon-ho crafts an architectural thriller where every camera movement and staircase symbol communicates social class divide. Perfection.", 5, 81, "2024-02-10"),
    ("The Creator", "Brilliant visual effects on modest budget, formulaic script", "Looks better than movies with triple the budget, showcasing photorealistic cybernetics. Sadly the emotional father-child plot feels like recycled tropes.", 3, 24, "2024-02-20"),
    ("Fast X", "Defies all physics laws, Jason Momoa having a blast", "Complete cartoon silliness with muscle cars driving down exploding dams. Momoa is deliciously unhinged even if the movie is mindless drivel.", 2, 33, "2024-03-07"),
    ("Morbius", "Boring vampire origin story with muddy action scenes", "Suffers from murky blue-tinted CGI smoke and disjointed editing. Not even Matt Smith's energetic dancing could rescue this tedious narrative.", 1, 58, "2024-03-15")
]

MOBILE_APPS_RAW = [
    # Positive
    ("Notion Workspace", "The ultimate all-in-one productivity and notes hub", "The relational database tables, markdown support, and nested subpages replaced four different disconnected apps for me. Sync across iOS, iPadOS, and Web is instantaneous and reliable.", 5, 54, "2024-01-06"),
    ("Duolingo", "Addictive gamified language learning that actually works", "The streak system, bite-sized lessons, and quirky widget animations keep me coming back every single day. Completed my 300-day Spanish streak and can now comfortably read basic news articles.", 5, 67, "2024-01-16"),
    ("Spotify Music & Podcasts", "Unbeatable music discovery algorithms and Daylist", "The Discover Weekly and Daylist playlists introduce me to incredible indie artists every week. Spotify Connect integration lets me hand off audio seamlessly between my phone, smart TV, and car.", 5, 73, "2024-01-27"),
    ("Habitify Tracker", "Clean minimalist habit tracking with insightful charts", "No bloated social features or annoying ads. Just clean check-ins, beautiful Apple Health integration, and insightful completion rate statistics that motivate consistent daily routines.", 5, 33, "2024-02-04"),
    ("Pocket Casts", "The gold standard podcast player with silence trimming", "The smart speed variable playback and silence trimming save hours of listening time every month. Volume boost normalizes quiet hosts effortlessly. Essential daily app.", 5, 41, "2024-02-13"),
    ("Revolut Banking", "Seamless foreign exchange rates and instant virtual cards", "Using Revolut while traveling abroad saved me hundreds in hidden bank FX fees. Disposable single-use virtual cards provide complete peace of mind when buying from unfamiliar websites.", 5, 52, "2024-02-21"),
    ("Strava Running & Cycling", "Unmatched athletic community and segment leaderboards", "Competing for local hill climb segments pushes my weekend cycling sessions to another level. The GPS route recording and heatmaps are pinpoint accurate.", 5, 60, "2024-03-01"),
    ("Headspace Meditation", "Gentle mindfulness guides that reduced my sleep anxiety", "Andy Puddicombe's calming voice and the sleepcast ambient stories transformed my insomnia. The SOS 3-minute breathing exercises are a lifesaver during stressful workdays.", 5, 39, "2024-03-07"),
    ("MyFitnessPal", "Massive verified food database makes calorie tracking effortless", "Barcode scanner works on virtually every grocery item. Macros breakdown and nutrient tracking helped me drop fifteen pounds over four months of clean eating.", 5, 48, "2024-03-14"),
    ("Todoist", "Natural language parsing makes task entry lightning fast", "Typing 'Submit quarterly report every second Tuesday at 4pm' automatically creates recurring reminders with zero manual date picker clicking. The best task manager on the market.", 5, 45, "2024-01-09"),

    # Neutral / Mixed
    ("Notion Workspace", "Powerful desktop experience, sluggish mobile startup", "I love Notion for organizing my life, but the mobile app takes four to five seconds to load on older iPhones. When you want to jot down a quick quick thought, the delay is irritating.", 3, 27, "2024-01-21"),
    ("Duolingo", "Gamification has become aggressively pushy with energy hearts", "The lesson structure is still fun, but running out of 'hearts' and being locked out of practicing unless you pay for Super or watch 30-second mobile game ads ruins the flow.", 3, 34, "2024-02-09"),
    ("Spotify Music & Podcasts", "Great music, but podcasts clutter the home feed", "I wish there was an option to completely hide podcasts and audiobooks. My home screen is crowded with algorithmic recommendations I have zero interest in listening to.", 3, 29, "2024-02-25"),
    ("MyFitnessPal", "Paywalling the barcode scanner was a greedy move", "The barcode scanner was a free core feature for eight years before they locked it behind a steep monthly premium subscription. The app works, but corporate greed is showing.", 3, 38, "2024-03-03"),
    ("Strava Running & Cycling", "Great community, recent price hikes were unjustified", "Subscription cost increased significantly without adding substantial new features. Free tier continues to lose basic segment analysis tools.", 3, 23, "2024-03-11"),

    # Negative
    ("QuickBudget Pro", "Constant sync crashes and corrupt account balances", "After the latest update, the app deleted six months of categorized expense transactions. It continuously fails to sync with Chase bank and customer support auto-closes tickets.", 1, 64, "2024-01-14"),
    ("FitPulse Workout Timer", "Plagued with predatory pop-up subscription traps", "You cannot even click a simple interval timer button without a full-screen $79.99/year subscription modal blocking the screen. Canceling the free trial requires jumping through ridiculous hoops.", 1, 71, "2024-01-30"),
    ("SleepCycle Sleep Tracker", "Drains 50% battery overnight and inaccurate microphone data", "My phone was burning hot on my bedside nightstand. Woke up to a completely drained battery and the app falsely recorded me snoring when the room was empty.", 1, 44, "2024-02-15"),
    ("TaskFlow Planner", "Lost all my project notes after an unprompted logout", "Updated overnight and forced a logout. Upon logging back in, all my synchronized tasks and reminders were completely erased. Inexcusable bug for a productivity tool.", 1, 56, "2024-02-28"),
    ("EasyRecipe Meal Planner", "Full of intrusive unskippable video ads", "Takes twenty seconds of loud casino game ads just to view a grocery ingredients list. The UI freezes constantly and recipes fail to cache offline.", 1, 49, "2024-03-16"),

    # Additional Reviews
    ("Notion Workspace", "Database formulas 2.0 are game changers", "Writing rollups and conditional formulas in project trackers feels like writing lightweight code. Extremely versatile.", 5, 26, "2024-01-18"),
    ("Duolingo", "Leaderboard leagues add friendly competition", "Climbing up to the Diamond League was surprisingly thrilling. Keeps me practicing every evening before bed.", 4, 21, "2024-02-01"),
    ("Pocket Casts", "Sync between phone and Mac desktop is flawless", "Listened halfway through an episode on my commute, opened my laptop at work and it resumed down to the exact second.", 5, 30, "2024-02-17"),
    ("Revolut Banking", "Split bill feature with friends is effortless", "Splitting dinner tabs and sending payment request links to contacts who do not even use Revolut is so convenient.", 5, 25, "2024-03-05"),
    ("Habitify Tracker", "Home screen widgets are clean and motivating", "The iOS interactive lock screen widget allows checking off morning hydration without unlocking the phone.", 5, 19, "2024-01-25"),
    ("QuickBudget Pro", "Bank API integration repeatedly disconnects", "Have to re-authenticate two-factor SMS codes every single day. Completely defeats the purpose of automated budgeting.", 2, 28, "2024-02-10"),
    ("FitPulse Workout Timer", "Annoying audio cues that mute my background music", "Every time the timer beeps for a rest interval, it cuts off my Spotify music completely instead of ducking the volume.", 2, 17, "2024-02-22"),
    ("Headspace Meditation", "Great content, but pricey annual subscription", "The meditation courses for stress and focus are top quality, but eighty dollars a year feels steep for students on a budget.", 4, 15, "2024-03-08"),
    ("Todoist", "Keyboard shortcuts on desktop are incredible", "Pressing 'Q' from anywhere opens the quick add modal. Syncs instantly to the mobile app notifications.", 5, 32, "2024-01-13"),
    ("SleepCycle Sleep Tracker", "Alarm works well, premium analytics are unnecessary", "The smart wake window is gentle and works as advertised. Most of the paid premium sleep trend charts are just gimmicks though.", 3, 12, "2024-01-31"),
    ("EasyRecipe Meal Planner", "Decent recipes buried under messy layout", "The actual food recipes are delicious, but finding them requires navigating through three tiers of intrusive banners.", 2, 16, "2024-02-14"),
    ("TaskFlow Planner", "Notifications are delayed by hours", "Reminders scheduled for 9:00 AM consistently fire at 2:00 PM in the afternoon. Completely defeats the purpose of an alert system.", 1, 33, "2024-02-27"),
    ("Spotify Music & Podcasts", "Audio quality is good enough, UI needs simplification", "Very broad music catalog, but the mobile navigation tabs change every few months with confusing redesigns.", 4, 22, "2024-03-12"),
    ("Duolingo", "Repetitive exercises after unit 10", "Sentences start feeling mechanical and unnatural in later units. Still decent for vocabulary retention.", 3, 14, "2024-01-11"),
    ("Strava Running & Cycling", "Beacon live tracking gives safety peace of mind", "My family can see my live location during long 40-mile solo bike rides in the hills. Wonderful safety feature.", 5, 28, "2024-01-29"),
    ("MyFitnessPal", "Step tracking sync with Apple Health is buggy", "Frequently doubles the active calorie burn if both Apple Watch and iPhone step counting are active.", 2, 24, "2024-02-12"),
    ("Revolut Banking", "Customer support chat takes hours to reply", "App is brilliant when everything works, but when a foreign merchant card charge pending transaction got stuck, live chat took 6 hours to respond.", 3, 18, "2024-02-26"),
    ("Notion Workspace", "Offline mode is still severely lacking", "If you are on an airplane without WiFi, opening an un-cached document is impossible. Truly needs a robust offline cache.", 3, 31, "2024-03-09"),
    ("QuickBudget Pro", "Dark mode is poorly contrasted", "Gray text on dark gray background makes reading small monetary cents nearly unreadable in low light.", 2, 15, "2024-01-23"),
    ("Habitify Tracker", "Privacy policy is clear and honest", "Appreciate that they do not sell user habit data or telemetry to third-party ad brokers.", 5, 20, "2024-02-07"),
    ("Obsidian Notes", "Local markdown files provide unmatched data ownership", "Having pure markdown files on my local storage that I control gives total freedom. Community canvas and graph view plugins are extraordinary.", 5, 59, "2024-01-17"),
    ("Linear Project Management", "Lightning fast issue tracking and keyboard shortcuts", "Takes microseconds to switch views, create tickets, and assign subtasks. Built for developers who hate sluggish Jira interfaces.", 5, 44, "2024-02-04"),
    ("Canva Graphic Design", "Makes social media marketing graphics effortless", "Thousands of templates and automatic background removal tools save hours. Exporting high-res PNGs directly to Instagram is seamless.", 5, 36, "2024-02-23"),
    ("CryptoVault Wallet", "Terrible update wiped biometric FaceID login", "Version 4.2 broke FaceID authentication entirely, leaving users stranded unless they entered 24-word recovery seeds. Buggy release.", 1, 63, "2024-03-03"),
    ("RideNow Taxi Booking", "Surge pricing triples during sudden rainstorms", "Fares spiked from fifteen to fifty dollars instantly during a light five-minute drizzle. Drivers routinely cancel bookings to fish for surges.", 1, 47, "2024-03-13"),
]

def get_raw_seed_data():
    return {
        "products": PRODUCTS_RAW,
        "restaurants": RESTAURANTS_RAW,
        "movies": MOVIES_RAW,
        "mobile-apps": MOBILE_APPS_RAW
    }

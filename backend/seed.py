"""
Database Seeder Script:
Populates SQLite database with categories, users, reviews, and computed VADER sentiment scores.
"""
import random
import os
import sys

# Ensure backend package can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    init_db, get_db, get_or_create_user, insert_review, insert_sentiment_score, count_reviews
)
from nlp import analyze_sentiment
from seed_data import CATEGORIES_DATA, USERS_DATA, get_raw_seed_data

def run_seed(force: bool = False):
    print("Initializing SQLite database tables...")
    init_db()
    
    current_count = count_reviews()
    if current_count > 0 and not force:
        print(f"Database already contains {current_count} reviews. Skipping seed (pass force=True to re-seed).")
        return current_count

    print("Seeding users...")
    user_ids = []
    for user_info in USERS_DATA:
        uid = get_or_create_user(user_info["username"], user_info["email"])
        user_ids.append(uid)

    print("Seeding categories...")
    category_map = {}
    with get_db() as conn:
        cursor = conn.cursor()
        for cat in CATEGORIES_DATA:
            cursor.execute(
                """
                INSERT OR IGNORE INTO categories (name, slug, description, icon)
                VALUES (?, ?, ?, ?);
                """,
                (cat["name"], cat["slug"], cat["description"], cat["icon"])
            )
            # Retrieve category id
            row = cursor.execute("SELECT id FROM categories WHERE slug = ?;", (cat["slug"],)).fetchone()
            category_map[cat["slug"]] = row["id"]

    print("Seeding reviews and calculating VADER sentiment scores...")
    raw_data = get_raw_seed_data()
    total_seeded = 0

    # If force, clear old reviews
    if force:
        with get_db() as conn:
            conn.execute("DELETE FROM sentiment_scores;")
            conn.execute("DELETE FROM reviews;")

    for cat_slug, review_list in raw_data.items():
        cat_id = category_map[cat_slug]
        for item in review_list:
            item_name, title, text, rating, helpful_count, created_date = item
            
            # Pick a deterministic or random user
            user_id = random.choice(user_ids)
            
            # Format realistic ISO timestamp
            created_at = f"{created_date} 14:30:00"
            
            review_id = insert_review(
                category_id=cat_id,
                user_id=user_id,
                item_name=item_name,
                title=title,
                text=text,
                rating=rating,
                helpful_count=helpful_count,
                created_at=created_at
            )
            
            # Analyze sentiment with VADER
            sentiment_res = analyze_sentiment(f"{title}. {text}")
            
            insert_sentiment_score(
                review_id=review_id,
                sentiment_label=sentiment_res["label"],
                compound_score=sentiment_res["compound"],
                pos_score=sentiment_res["pos"],
                neu_score=sentiment_res["neu"],
                neg_score=sentiment_res["neg"],
                analyzed_at=created_at
            )
            total_seeded += 1

        # Additional variety reviews per category to guarantee ~65 reviews per vertical
        extra_items = {
            "products": [
                ("Apple AirPods Max", "Exquisite audio and build, but carry case is ridiculous", "The aluminum cups and mesh headband feel truly luxurious. Sound is balanced with crisp separation, but the included smart case offers zero real drop protection.", 4, 26, "2024-01-07"),
                ("Samsung Galaxy Watch 6", "Smooth WearOS with detailed sleep tracking", "The physical rotating bezel is back and feels satisfying. Battery life requires charging every 36 hours, but health metrics are top notch.", 4, 15, "2024-01-26"),
                ("Logitech MX Mechanical", "Crisp low profile tactile typing", "Pairing switches between three machines with dedicated easy-switch keys works instantaneously. Battery lasts over a month with backlight turned down.", 5, 23, "2024-02-13"),
                ("Razer DeathAdder V3 Pro", "Ergonomic esports mouse with optical switches", "Superb hand palm support and zero latency wireless connection. Smooth skates and zero click latency.", 5, 31, "2024-02-27"),
                ("Anker Nano Power Bank", "Built-in foldable lightning connector is super convenient", "Small enough to fit in a watch pocket. Great emergency juice for long days out around town.", 4, 12, "2024-03-09"),
                ("CheapTech USB Hub", "Overheated and fried my flash drive", "Plugged in two standard thumb drives and within ten minutes the aluminum casing was burning hot. Disconnected immediately.", 1, 46, "2024-03-14"),
                ("Bose SoundLink Flex", "Punchy portable bass and waterproof resilience", "Survived a drop in the pool without missing a beat. Surprisingly loud and clear vocals for its compact silicone form factor.", 5, 28, "2024-01-19"),
                ("SmartScale Body Analyzer", "Inconsistent body fat percentage readings", "Weighed myself three times in ten minutes and received three wildly different body fat estimates varying by 4%. Weight scale itself is okay.", 2, 17, "2024-02-05"),
                ("Dell XPS 15", "Vibrant OLED 3.5K display, fans get loud under load", "Gorgeous display for video editing and photography. Fans kick in with a high-pitched buzz when exporting 4K footage.", 4, 20, "2024-02-22"),
                ("FastJuice Blender Pro", "Motor gave off burning plastic smell on first blend", "Attempted to crush frozen strawberries and ice cubes. The motor seized up immediately with smoke coming from the vent.", 1, 51, "2024-03-11"),
                ("Kindle Scribe", "Excellent digital notebook feel, basic note organization", "The stylus writing feel mimics paper beautifully with zero lag. Organizing notebooks into complex folders needs better software support.", 4, 18, "2024-01-13"),
                ("Sony WF-1000XM5 Earbuds", "Smaller fit than XM4 with pristine sound", "Tips create a snug acoustic seal that blocks subway rumble effortlessly. Call quality in wind is drastically better.", 5, 34, "2024-02-18"),
                ("GamerZone RGB Chair", "Creaky armrests and rock hard lumbar pillow", "Looks cool in Twitch streams but sitting in it for more than two hours leads to a numb tailbone. Poor foam density.", 2, 29, "2024-03-03"),
                ("Elgato Stream Deck MK.2", "Indispensable workflow tool for shortcuts", "Configured keys for mute, camera toggle, Spotify playback, and terminal commands. Saves countless keystrokes every single day.", 5, 41, "2024-01-29")
            ],
            "restaurants": [
                ("Maison Kayser Bakery", "Authentic French baguettes and fruit tarts", "The strawberry tart has crisp shortbread crust with smooth pastry cream. Morning cappuccino was velvety and hot.", 5, 23, "2024-01-06"),
                ("Wok & Roll Street Asian", "Spicy Sichuan dan dan noodles packed with flavor", "The toasted sesame paste, chili crisp oil, and pickled mustard greens create an irresistible bowl of comfort.", 5, 37, "2024-01-20"),
                ("Bella Italia Trattoria", "Truffle risotto was heavenly, tiramisu too sweet", "Risotto was cooked perfectly al dente with rich fontina and shaved summer truffles. Tiramisu had slightly too much cocoa powder.", 4, 19, "2024-02-04"),
                ("Tokyo Ramen Lab", "Rich black garlic broth with tender chashu", "Deep umami aroma filled the restaurant. The ajitsuke tamago egg had a jammy molten yolk. Worth waiting thirty minutes.", 5, 42, "2024-02-16"),
                ("Sunset Rooftop Tapas", "Stunning skyline views, overpriced small plates", "Cocktails were well crafted and sunset photos were incredible. However, paying twenty dollars for three tiny croquettes is steep.", 3, 27, "2024-02-28"),
                ("Crispy Bird Fried Chicken", "Crunchy batter and spicy honey drizzle", "Juicy meat with an insanely crispy coating that stays crunchy even on delivery. The waffle fries were seasoned well.", 5, 35, "2024-03-08"),
                ("Grand Palace Dim Sum", "Cha siu bao buns were cold inside", "The pork buns felt like they were microwaved from frozen because the center was still cool to the touch. Disappointing cart service.", 2, 24, "2024-01-25"),
                ("Harbor View Seafood", "Fresh clam chowder served in a sourdough bread bowl", "Warm, thick chowder with generous chunks of tender clams and bacon bits. Soaking up the broth with crusty sourdough bread was bliss.", 5, 31, "2024-02-11"),
                ("Speedy Slice Pizza", "Cardboard crust and artificial cheese blend", "Tasted like school cafeteria pizza. The sauce was sickly sweet and crust had no chew or fermentation bubbles.", 1, 40, "2024-03-01"),
                ("Zen Vegan Oasis", "Nutrient-rich Buddha bowls with creamy tahini dressing", "Fresh microgreens, roasted chickpeas, avocado slices, and quinoa. Wholesome, flavorful, and leaves you feeling energized.", 5, 22, "2024-03-15"),
                ("Fiesta Mexicana Cantina", "Enchiladas were drowned in bland sauce", "The shredded chicken was unseasoned and dry. The refried beans tasted straight from an unheated tin can.", 2, 16, "2024-01-16"),
                ("Artisan Espresso Bar", "Single origin Ethiopian pour over with jasmine notes", "Incredible floral aroma with bright acidity and peach finish. Baristas take genuine pride in coffee extraction.", 5, 29, "2024-02-07"),
                ("Golden Waffle Shack", "Undercooked raw batter in the center", "Cut into the waffle and uncooked runny batter oozed onto the plate. Server replaced it but showed zero courtesy.", 1, 33, "2024-02-25"),
                ("Bavarian Brauhaus", "Crispy pork knuckle and refreshing wheat beer", "Crackling skin on the pork knuckle with tangy sauerkraut and mustard. Authentic lively folk music atmosphere.", 5, 36, "2024-03-11")
            ],
            "movies": [
                ("The Zone of Interest", "A bone-chilling auditory masterwork on complicity", "Jonathan Glazer avoids showing violence directly, allowing the distant industrial background hum and sound design to induce dread. Monumental cinema.", 5, 52, "2024-01-08"),
                ("Godzilla Minus One", "Tender human drama anchored by terrifying monster destruction", "A Godzilla film with immense emotional heart and survivor guilt themes. The atomic breath scene in Ginza is awe-inspiring.", 5, 67, "2024-01-21"),
                ("Ferrari", "Thrilling race sequences, melodramatic domestic scenes", "The engine sounds are visceral and raw. The Mille Miglia accident sequence is harrowing, though the dialogue pacing slows in the middle.", 3, 23, "2024-02-03"),
                ("Society of the Snow", "Unvarnished survival testament to human endurance", "J.A. Bayona captures the freezing Andean wilderness with brutal respect and emotional purity. A harrowing yet profoundly uplifting movie.", 5, 48, "2024-02-17"),
                ("The Beekeeper", "Mindless fun action thriller that embraces its absurdity", "Jason Statham punch-fest that delivers exactly what it promises on the tin. Fun fight choreography if you turn your brain off completely.", 3, 31, "2024-02-29"),
                ("Wish", "Generic musical numbers and uninspired corporate animation", "Disney's 100th anniversary celebration feels like it was engineered by marketing committees. The villain's motives are weak and songs are forgettable.", 2, 45, "2024-03-08"),
                ("Blackberry", "Sharp, darkly comedic rise and fall of tech hubris", "Glenn Howerton's furious performance as Jim Balsillie is electrifying. Fast-paced, witty dialogue reminiscent of The Social Network.", 5, 39, "2024-01-15"),
                ("Aquaman and the Lost Kingdom", "Muddled CGI soup and fatigued superhero formula", "Too many disjointed plotlines and obvious reshoots. The brotherly banter between Momoa and Wilson has charms, but the villain is generic.", 2, 38, "2024-01-27"),
                ("The Holdovers", "A warm, bittersweet holiday classic with timeless performances", "Paul Giamatti and Da'Vine Joy Randolph create unforgettable warmth and melancholy. Has the texture and comfort of vintage 1970s cinema.", 5, 61, "2024-02-11"),
                ("Five Nights at Freddy's", "Fun animatronics, sluggish mystery pacing", "The physical robot suits look fantastic and authentic to the game lore. The human protagonist's dream sequences dragged down the tension.", 3, 29, "2024-02-24"),
                ("The Marvels", "Fun space cat moments, underwritten villain", "Carol, Kamala, and Monica share fun teamwork dynamics, but the climax wrapped up too quickly without satisfying dramatic stakes.", 3, 19, "2024-03-06"),
                ("Meg 2: The Trench", "Absurd shark mayhem that takes too long to get going", "The first hour is a boring underwater mining dispute before the giant sharks finally start snacking on beachgoers.", 2, 34, "2024-03-13"),
                ("Monster (Hirokazu Kore-eda)", "Deeply moving Japanese puzzle-box narrative on compassion", "Told from three distinct perspectives, unraveling misunderstandings with immense empathy and Ryuichi Sakamoto's gentle score.", 5, 43, "2024-01-23"),
                ("Night Swim", "Inane premise unable to sustain a 90-minute horror film", "A haunted swimming pool turns out to be exactly as silly and un-scary as it sounds. Laughable third act resolution.", 1, 55, "2024-02-14")
            ],
            "mobile-apps": [
                ("Notion Calendar", "Seamless two-way integration with Notion databases", "Seeing project deadlines side-by-side with Google Calendar events eliminates tab hopping. Fast keyboard shortcuts for scheduling meetings.", 5, 37, "2024-01-12"),
                ("ChatGPT Mobile", "Voice mode conversations are astonishingly fluid", "Talking to ChatGPT while walking the dog feels like speaking with a knowledgeable research partner. Fast response generation and clean UI.", 5, 64, "2024-01-25"),
                ("Raycast Companion", "Speedy developer utilities and clipboard management", "Snippets and quick calculations right from the notification drawer. Lightweight and zero memory bloat.", 5, 29, "2024-02-08"),
                ("YNAB (You Need A Budget)", "Steep learning curve, life-changing budgeting paradigm", "Giving every dollar a job transformed my personal savings rate. Mobile transaction entry is fast, though subscription price is high.", 4, 33, "2024-02-21"),
                ("Forest Focus Timer", "Charming visual gamification for deep work sessions", "Planting virtual trees keeps me away from scrolling social media feeds while studying. Cute tree species to unlock.", 5, 26, "2024-03-02"),
                ("ExpenseTracker 360", "Intrusive full-screen video ads every three clicks", "Every time you save an expense entry, a 30-second casino advertisement blares at maximum volume. Uninstalled immediately.", 1, 58, "2024-03-10"),
                ("Spark Mail", "Smart inbox categorization and AI draft assistant", "Automatically bundles newsletters and automated notifications away from real humans. Fast swipe gestures make inbox zero achievable.", 4, 30, "2024-01-15"),
                ("FitWorkout Daily", "Workout routines locked behind predatory annual plan", "Claims to offer free customized bodyweight workouts, but clicking start brings up a $99 prompt with dark pattern cancel buttons.", 1, 62, "2024-01-30"),
                ("TickTick Tasks", "Superior task manager with built-in Pomodoro timer", "The combination of calendar view, Eisenhower matrix, and habit tracking in a single app is unbeatable for daily planning.", 5, 41, "2024-02-14"),
                ("Weather Live Radar", "Accurate precipitation alerts, slightly busy layout", "Minutely rain start predictions are spot-on during commutes. Radar maps have a few too many toggles that clutter the screen.", 4, 18, "2024-02-27"),
                ("Babbel Language", "Structured grammar explanations superior to Duolingo", "Dialogues sound like real conversational Spanish rather than silly cartoon sentences. Solid review lessons.", 4, 25, "2024-03-07"),
                ("CryptoTracker Pro", "Battery hog running background location tracking", "No reason for a cryptocurrency pricing widget to request constant precise background GPS location. Suspicious telemetry.", 1, 49, "2024-03-15"),
                ("Kindle App iOS", "Smooth page animations and synchronized reading progress", "Highlighting passages and syncing with Goodreads is seamless. Warm paper texture background reduces nighttime eye strain.", 5, 32, "2024-01-20"),
                ("SoundCloud Music", "Great underground DJ sets, frequent buffering glitches", "Unmatched selection of live DJ mixes and indie remixes, but the mobile audio player frequently buffers on high speed LTE.", 3, 21, "2024-02-19")
            ]
        }

        for extra in extra_items.get(cat_slug, []):
            item_name, title, text, rating, helpful_count, created_date = extra
            user_id = random.choice(user_ids)
            created_at = f"{created_date} 16:45:00"
            review_id = insert_review(
                category_id=cat_id,
                user_id=user_id,
                item_name=item_name,
                title=title,
                text=text,
                rating=rating,
                helpful_count=helpful_count,
                created_at=created_at
            )
            sentiment_res = analyze_sentiment(f"{title}. {text}")
            insert_sentiment_score(
                review_id=review_id,
                sentiment_label=sentiment_res["label"],
                compound_score=sentiment_res["compound"],
                pos_score=sentiment_res["pos"],
                neu_score=sentiment_res["neu"],
                neg_score=sentiment_res["neg"],
                analyzed_at=created_at
            )
            total_seeded += 1

    print(f"Successfully seeded {total_seeded} reviews with sentiment metrics!")
    return total_seeded

if __name__ == "__main__":
    force_flag = "--force" in sys.argv or "-f" in sys.argv
    run_seed(force=force_flag)

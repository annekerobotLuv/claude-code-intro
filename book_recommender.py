import streamlit as st
import json
import os
import hashlib
import requests
from urllib.parse import quote_plus
from collections import Counter

ACCOUNTS_FILE = "accounts.json"

SUBJECT_TO_GENRE = {
    "science fiction": "Science Fiction", "fantasy": "Fantasy", "mystery": "Mystery",
    "detective": "Mystery", "crime": "Crime", "thriller": "Thriller", "horror": "Horror",
    "romance": "Romance", "historical fiction": "Historical Fiction", "adventure": "Adventure",
    "young adult": "Young Adult", "dystopia": "Dystopia", "coming of age": "Coming-of-age",
    "humor": "Comedy", "comedy": "Comedy", "political": "Political", "biography": "Memoir",
    "autobiography": "Memoir", "memoir": "Memoir", "nonfiction": "Non-fiction",
    "non-fiction": "Non-fiction", "psychology": "Psychology", "self-help": "Self-help",
    "history": "History", "science": "Science", "cyberpunk": "Cyberpunk", "gothic": "Gothic",
    "mythology": "Mythology", "war": "War", "classic": "Classic", "philosophy": "Philosophical",
    "satire": "Satire", "drama": "Drama", "family": "Family", "epic": "Epic",
    "psychological": "Psychological", "survival": "Survival", "spirituality": "Spiritual",
}

BOOK_CATALOG = [
    {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "genres": ["Science Fiction", "Comedy", "Adventure"]},
    {"title": "Dune", "author": "Frank Herbert", "genres": ["Science Fiction", "Adventure", "Political"]},
    {"title": "Ender's Game", "author": "Orson Scott Card", "genres": ["Science Fiction", "Adventure", "Young Adult"]},
    {"title": "The Martian", "author": "Andy Weir", "genres": ["Science Fiction", "Adventure", "Survival"]},
    {"title": "Project Hail Mary", "author": "Andy Weir", "genres": ["Science Fiction", "Adventure"]},
    {"title": "Foundation", "author": "Isaac Asimov", "genres": ["Science Fiction", "Political"]},
    {"title": "Neuromancer", "author": "William Gibson", "genres": ["Science Fiction", "Cyberpunk", "Thriller"]},
    {"title": "Snow Crash", "author": "Neal Stephenson", "genres": ["Science Fiction", "Cyberpunk", "Comedy"]},
    {"title": "Ready Player One", "author": "Ernest Cline", "genres": ["Science Fiction", "Adventure", "Young Adult"]},
    {"title": "The Long Way to a Small Angry Planet", "author": "Becky Chambers", "genres": ["Science Fiction", "Adventure"]},
    {"title": "All Systems Red", "author": "Martha Wells", "genres": ["Science Fiction", "Adventure", "Comedy"]},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genres": ["Fantasy", "Adventure", "Epic"]},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genres": ["Fantasy", "Adventure", "Young Adult"]},
    {"title": "A Wizard of Earthsea", "author": "Ursula K. Le Guin", "genres": ["Fantasy", "Adventure", "Young Adult"]},
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss", "genres": ["Fantasy", "Adventure", "Epic"]},
    {"title": "Mistborn", "author": "Brandon Sanderson", "genres": ["Fantasy", "Adventure", "Epic"]},
    {"title": "The Way of Kings", "author": "Brandon Sanderson", "genres": ["Fantasy", "Adventure", "Epic"]},
    {"title": "American Gods", "author": "Neil Gaiman", "genres": ["Fantasy", "Mythology", "Thriller"]},
    {"title": "Good Omens", "author": "Terry Pratchett & Neil Gaiman", "genres": ["Fantasy", "Comedy", "Mythology"]},
    {"title": "The Night Circus", "author": "Erin Morgenstern", "genres": ["Fantasy", "Romance", "Historical Fiction"]},
    {"title": "Jonathan Strange & Mr Norrell", "author": "Susanna Clarke", "genres": ["Fantasy", "Historical Fiction"]},
    {"title": "Six of Crows", "author": "Leigh Bardugo", "genres": ["Fantasy", "Adventure", "Young Adult"]},
    {"title": "The Poppy War", "author": "R.F. Kuang", "genres": ["Fantasy", "Historical Fiction", "Epic"]},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "genres": ["Fantasy", "Young Adult", "Adventure"]},
    {"title": "The Hunger Games", "author": "Suzanne Collins", "genres": ["Young Adult", "Dystopia", "Adventure", "Science Fiction"]},
    {"title": "Divergent", "author": "Veronica Roth", "genres": ["Young Adult", "Dystopia", "Adventure", "Science Fiction"]},
    {"title": "The Maze Runner", "author": "James Dashner", "genres": ["Young Adult", "Dystopia", "Adventure", "Science Fiction"]},
    {"title": "The Giver", "author": "Lois Lowry", "genres": ["Young Adult", "Dystopia", "Science Fiction"]},
    {"title": "Holes", "author": "Louis Sachar", "genres": ["Young Adult", "Adventure", "Mystery"]},
    {"title": "Percy Jackson and the Lightning Thief", "author": "Rick Riordan", "genres": ["Young Adult", "Fantasy", "Mythology", "Adventure"]},
    {"title": "1984", "author": "George Orwell", "genres": ["Dystopia", "Political", "Science Fiction", "Classic"]},
    {"title": "Brave New World", "author": "Aldous Huxley", "genres": ["Dystopia", "Political", "Science Fiction", "Classic"]},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "genres": ["Dystopia", "Science Fiction", "Classic"]},
    {"title": "The Handmaid's Tale", "author": "Margaret Atwood", "genres": ["Dystopia", "Political", "Science Fiction"]},
    {"title": "We", "author": "Yevgeny Zamyatin", "genres": ["Dystopia", "Science Fiction", "Classic"]},
    {"title": "Gone Girl", "author": "Gillian Flynn", "genres": ["Thriller", "Mystery", "Psychological"]},
    {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "genres": ["Thriller", "Mystery", "Crime"]},
    {"title": "The Da Vinci Code", "author": "Dan Brown", "genres": ["Thriller", "Mystery", "Historical Fiction"]},
    {"title": "Big Little Lies", "author": "Liane Moriarty", "genres": ["Thriller", "Mystery", "Drama"]},
    {"title": "In the Woods", "author": "Tana French", "genres": ["Thriller", "Mystery", "Crime"]},
    {"title": "And Then There Were None", "author": "Agatha Christie", "genres": ["Mystery", "Crime", "Classic"]},
    {"title": "The Murder of Roger Ackroyd", "author": "Agatha Christie", "genres": ["Mystery", "Crime", "Classic"]},
    {"title": "The Hound of the Baskervilles", "author": "Arthur Conan Doyle", "genres": ["Mystery", "Crime", "Classic"]},
    {"title": "The Secret History", "author": "Donna Tartt", "genres": ["Mystery", "Thriller", "Drama"]},
    {"title": "The Kite Runner", "author": "Khaled Hosseini", "genres": ["Historical Fiction", "Drama", "Family"]},
    {"title": "All the Light We Cannot See", "author": "Anthony Doerr", "genres": ["Historical Fiction", "War", "Drama"]},
    {"title": "The Book Thief", "author": "Markus Zusak", "genres": ["Historical Fiction", "War", "Young Adult"]},
    {"title": "Pillars of the Earth", "author": "Ken Follett", "genres": ["Historical Fiction", "Epic", "Drama"]},
    {"title": "Wolf Hall", "author": "Hilary Mantel", "genres": ["Historical Fiction", "Political", "Drama"]},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genres": ["Classic", "Romance", "Drama"]},
    {"title": "Jane Eyre", "author": "Charlotte Brontë", "genres": ["Classic", "Romance", "Drama"]},
    {"title": "Great Expectations", "author": "Charles Dickens", "genres": ["Classic", "Drama", "Coming-of-age"]},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genres": ["Classic", "Drama", "Political"]},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genres": ["Classic", "Drama", "Romance"]},
    {"title": "Of Mice and Men", "author": "John Steinbeck", "genres": ["Classic", "Drama", "Tragedy"]},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "genres": ["Classic", "Psychological", "Crime"]},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "genres": ["Classic", "Coming-of-age", "Drama"]},
    {"title": "Catch-22", "author": "Joseph Heller", "genres": ["Classic", "Comedy", "War", "Satire"]},
    {"title": "Slaughterhouse-Five", "author": "Kurt Vonnegut", "genres": ["Classic", "War", "Science Fiction", "Satire"]},
    {"title": "The Perks of Being a Wallflower", "author": "Stephen Chbosky", "genres": ["Coming-of-age", "Drama", "Young Adult"]},
    {"title": "Eleanor Oliphant is Completely Fine", "author": "Gail Honeyman", "genres": ["Drama", "Coming-of-age", "Comedy"]},
    {"title": "Normal People", "author": "Sally Rooney", "genres": ["Romance", "Drama", "Coming-of-age"]},
    {"title": "A Little Life", "author": "Hanya Yanagihara", "genres": ["Drama", "Psychological"]},
    {"title": "The Alchemist", "author": "Paulo Coelho", "genres": ["Adventure", "Philosophical", "Spiritual"]},
    {"title": "Siddhartha", "author": "Hermann Hesse", "genres": ["Philosophical", "Spiritual", "Coming-of-age"]},
    {"title": "The Stranger", "author": "Albert Camus", "genres": ["Philosophical", "Classic", "Drama"]},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "genres": ["Non-fiction", "History", "Science"]},
    {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "genres": ["Non-fiction", "Psychology", "Science"]},
    {"title": "The Power of Habit", "author": "Charles Duhigg", "genres": ["Non-fiction", "Psychology", "Self-help"]},
    {"title": "Educated", "author": "Tara Westover", "genres": ["Non-fiction", "Memoir", "Coming-of-age"]},
    {"title": "When Breath Becomes Air", "author": "Paul Kalanithi", "genres": ["Non-fiction", "Memoir", "Drama"]},
    {"title": "The Immortal Life of Henrietta Lacks", "author": "Rebecca Skloot", "genres": ["Non-fiction", "Science", "History"]},
    {"title": "Into the Wild", "author": "Jon Krakauer", "genres": ["Non-fiction", "Adventure", "Memoir"]},
    {"title": "Born a Crime", "author": "Trevor Noah", "genres": ["Non-fiction", "Memoir", "Comedy", "Political"]},
    {"title": "Atomic Habits", "author": "James Clear", "genres": ["Non-fiction", "Self-help", "Psychology"]},
    {"title": "It Ends with Us", "author": "Colleen Hoover", "genres": ["Romance", "Drama", "Young Adult"]},
    {"title": "The Fault in Our Stars", "author": "John Green", "genres": ["Romance", "Young Adult", "Drama"]},
    {"title": "Twilight", "author": "Stephenie Meyer", "genres": ["Romance", "Fantasy", "Young Adult"]},
    {"title": "Outlander", "author": "Diana Gabaldon", "genres": ["Romance", "Historical Fiction", "Adventure", "Fantasy"]},
    {"title": "Rebecca", "author": "Daphne du Maurier", "genres": ["Romance", "Mystery", "Thriller", "Gothic"]},
    {"title": "It", "author": "Stephen King", "genres": ["Horror", "Thriller", "Psychological"]},
    {"title": "The Shining", "author": "Stephen King", "genres": ["Horror", "Thriller", "Psychological"]},
    {"title": "Dracula", "author": "Bram Stoker", "genres": ["Horror", "Classic", "Gothic"]},
    {"title": "Frankenstein", "author": "Mary Shelley", "genres": ["Horror", "Science Fiction", "Classic", "Gothic"]},
    {"title": "Mexican Gothic", "author": "Silvia Moreno-Garcia", "genres": ["Horror", "Gothic", "Historical Fiction"]},
    {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "genres": ["Gothic", "Classic", "Philosophical"]},
    {"title": "Where the Crawdads Sing", "author": "Delia Owens", "genres": ["Mystery", "Drama", "Coming-of-age"]},
    {"title": "The Midnight Library", "author": "Matt Haig", "genres": ["Fantasy", "Drama", "Philosophical"]},
    {"title": "Anxious People", "author": "Fredrik Backman", "genres": ["Comedy", "Drama", "Mystery"]},
    {"title": "A Man Called Ove", "author": "Fredrik Backman", "genres": ["Comedy", "Drama", "Coming-of-age"]},
]

ALL_GENRES = sorted(set(g for book in BOOK_CATALOG for g in book["genres"]))


# --- Accounts ---

def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE) as f:
            return json.load(f)
    return {}

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


# --- Books ---

def books_file(username):
    return f"books_{username}.json"

def load_books(username):
    path = books_file(username)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def save_books(username, books):
    with open(books_file(username), "w") as f:
        json.dump(books, f, indent=2)


# --- Open Library ---

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_ol_books(top_genres: tuple, max_per_genre: int = 20):
    results, seen = [], set()
    for genre in top_genres[:3]:
        try:
            r = requests.get(
                "https://openlibrary.org/search.json",
                params={"subject": genre.lower(), "fields": "title,author_name,subject", "limit": max_per_genre},
                timeout=6,
            )
            if r.status_code != 200:
                continue
            for doc in r.json().get("docs", []):
                title = doc.get("title", "").strip()
                if not title or title.lower() in seen:
                    continue
                seen.add(title.lower())
                authors = doc.get("author_name") or ["Unknown"]
                raw_subjects = [s.lower() for s in (doc.get("subject") or [])[:20]]
                mapped = list({
                    SUBJECT_TO_GENRE[k]
                    for k in SUBJECT_TO_GENRE
                    if any(k in s for s in raw_subjects)
                })
                results.append({
                    "title": title,
                    "author": authors[0],
                    "genres": mapped or [genre],
                    "source": "Open Library",
                })
        except Exception:
            pass
    return results

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_summary(title: str, author: str) -> str:
    try:
        r = requests.get(
            "https://openlibrary.org/search.json",
            params={"title": title, "author": author, "fields": "first_sentence", "limit": 1},
            timeout=5,
        )
        if r.status_code == 200:
            docs = r.json().get("docs", [])
            if docs:
                fs = docs[0].get("first_sentence")
                if isinstance(fs, dict):
                    return fs.get("value", "")
                if isinstance(fs, str):
                    return fs
    except Exception:
        pass
    return ""


# --- Recommendations ---

def build_taste_profile(my_books, preferred_genres, age):
    genre_weights = Counter()
    liked_authors = Counter()

    for genre in preferred_genres:
        genre_weights[genre] += 2.0

    if age and age < 18:
        genre_weights["Young Adult"] += 1.5

    for book in my_books:
        rating = book.get("rating", 3)
        genres = book.get("genres", [])
        per_genre = rating / max(1, len(genres))
        for g in genres:
            genre_weights[g] += per_genre
        liked_authors[book["author"]] += rating

    return genre_weights, liked_authors

def get_recommendations(my_books, ol_books, preferred_genres, age, n=10):
    read_titles = {b["title"].lower() for b in my_books}
    genre_weights, liked_authors = build_taste_profile(my_books, preferred_genres, age)
    if not any(genre_weights.values()):
        return []

    seen, scored = set(), []
    for candidate in BOOK_CATALOG + ol_books:
        key = candidate["title"].lower()
        if key in read_titles or key in seen:
            continue
        seen.add(key)
        genres = candidate["genres"]
        raw = sum(genre_weights.get(g, 0) for g in genres)
        score = raw / max(1, len(genres)) + liked_authors.get(candidate["author"], 0) * 0.3
        if score > 0:
            scored.append((score, candidate))

    scored.sort(key=lambda x: -x[0])
    return [b for _, b in scored[:n]]

def book_links(title, author):
    q = quote_plus(f"{title} {author}")
    return {
        "📖 Read free (Open Library)": f"https://openlibrary.org/search?q={q}",
        "⭐ Goodreads": f"https://www.goodreads.com/search?q={q}",
        "🛒 Amazon": f"https://www.amazon.com/s?k={q}",
    }


# --- App ---

st.set_page_config(page_title="Book Recommender", page_icon="📚", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

accounts = load_accounts()

# ── Login / Register ──────────────────────────────────────────────────────────
if st.session_state.user is None:
    st.title("📚 Book Recommender")
    tab_login, tab_reg = st.tabs(["Log In", "Create Account"])

    with tab_login:
        with st.form("login"):
            uname = st.text_input("Username")
            pw    = st.text_input("Password", type="password")
            if st.form_submit_button("Log in"):
                a = accounts.get(uname)
                if a and a["password"] == hash_pw(pw):
                    st.session_state.user = uname
                    st.rerun()
                else:
                    st.error("Wrong username or password.")

    with tab_reg:
        with st.form("register"):
            new_uname = st.text_input("Choose a username")
            new_pw    = st.text_input("Choose a password", type="password")
            age       = st.number_input("Your age", min_value=8, max_value=100, value=15, step=1)
            prefs     = st.multiselect("Favorite genres (pick 1–3 to seed your recommendations)", ALL_GENRES)
            if st.form_submit_button("Create account"):
                if not new_uname or not new_pw:
                    st.error("Please fill in username and password.")
                elif new_uname in accounts:
                    st.error("That username is already taken.")
                elif not prefs:
                    st.error("Pick at least one favorite genre.")
                else:
                    accounts[new_uname] = {
                        "password": hash_pw(new_pw),
                        "age": int(age),
                        "preferred_genres": prefs,
                    }
                    save_accounts(accounts)
                    st.session_state.user = new_uname
                    st.rerun()

# ── Main App ──────────────────────────────────────────────────────────────────
else:
    username = st.session_state.user
    account  = accounts[username]
    my_books = load_books(username)

    col_title, col_user = st.columns([5, 1])
    with col_title:
        st.title("📚 Book Recommender")
    with col_user:
        st.write(f"**{username}**")
        if st.button("Log out"):
            st.session_state.user = None
            st.rerun()

    st.caption(f"Age {account['age']} · Favorite genres: {', '.join(account['preferred_genres'])}")
    st.divider()

    tab1, tab2 = st.tabs([f"My Books ({len(my_books)})", "Recommendations"])

    # ── My Books tab ──
    with tab1:
        st.subheader("Add a book you've read")
        with st.form("add_book", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title  = st.text_input("Title *")
                author = st.text_input("Author *")
            with col2:
                selected_genres = st.multiselect("Genres *", ALL_GENRES)
                rating = st.slider("Your rating", 1, 5, 4)
            if st.form_submit_button("Add book"):
                if not title or not author or not selected_genres:
                    st.error("Please fill in title, author, and at least one genre.")
                elif any(b["title"].lower() == title.lower() for b in my_books):
                    st.warning(f'"{title}" is already in your list.')
                else:
                    my_books.append({"title": title, "author": author, "genres": selected_genres, "rating": rating})
                    save_books(username, my_books)
                    st.success(f'Added "{title}"!')
                    st.rerun()

        if not my_books:
            st.info("No books yet — add some above to start getting recommendations!")
        else:
            for i, book in enumerate(reversed(my_books)):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{book['title']}** by {book['author']}")
                with col2:
                    st.write(" · ".join(book.get("genres", [])))
                with col3:
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.write("⭐" * book.get("rating", 3))
                    with c2:
                        if st.button("✕", key=f"del_{i}"):
                            my_books.pop(len(my_books) - 1 - i)
                            save_books(username, my_books)
                            st.rerun()

    # ── Recommendations tab ──
    with tab2:
        st.subheader("Books you might like")
        gw, _ = build_taste_profile(my_books, account["preferred_genres"], account["age"])
        top_genres = tuple(g for g, _ in gw.most_common(3))
        st.caption(f"Based on your taste in: {', '.join(top_genres)}")

        ol_books = []
        with st.spinner("Checking Open Library for more picks..."):
            ol_books = fetch_ol_books(top_genres)

        recs = get_recommendations(my_books, ol_books, account["preferred_genres"], account["age"])

        if not recs:
            st.info("No matches yet — add books or check that you selected genres when registering.")
        else:
            for book in recs:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 2])
                    with col1:
                        source_badge = " · 📖 Open Library" if book.get("source") == "Open Library" else ""
                        st.write(f"**{book['title']}**{source_badge}")
                        st.caption(f"by {book['author']}")

                        with st.expander("Summary & where to find it"):
                            summary = fetch_summary(book["title"], book["author"])
                            if summary:
                                st.write(summary)
                            else:
                                st.caption("No summary available from Open Library.")
                            st.write("**Find or buy this book:**")
                            for label, url in book_links(book["title"], book["author"]).items():
                                st.markdown(f"[{label}]({url})")
                    with col2:
                        matching = [g for g in book["genres"] if g in gw]
                        st.write(" · ".join(matching) if matching else " · ".join(book["genres"]))

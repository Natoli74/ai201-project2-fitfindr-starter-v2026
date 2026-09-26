# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does
-<!-- Three or four sentences: what a user asks for, and what they get back. -->


---

## Tool Inventory

1. `search_listings(description: str, size: str | None, max_price: float) -> list[dict]`
   - **Does:** Filters candidate listings in `data/listings.json` matching the description substring, size, and price ceiling.
   - **Inputs:** `description` (str), `size` (str or None), `max_price` (float).
   - **Returns:** A list of listing dicts, each with `id`, `title`, `price`, `size`, `platform`, `description`, and `condition`.
   - **Empty Case:** Returns an empty list `[]` (never `None`, never throws an exception).

2. `suggest_outfit(new_item: dict, wardrobe: list[dict]) -> str`
   - **Does:** Calls the LLM to generate 2-3 outfit pairing suggestions combining `new_item` with existing items in `wardrobe`.
   - **Inputs:** `new_item` (dict matching listing schema), `wardrobe` (list of item dicts from schema).
   - **Returns:** A string containing markdown-formatted pairing suggestions.
   - **Empty Case:** If `wardrobe` is empty `[]`, returns general styling and pairing advice for `new_item`.

3. `create_fit_card(outfit: str, new_item: dict) -> str`
   - **Does:** Calls the LLM to write a catchy, social-media-ready caption and hashtag set for the proposed outfit.
   - **Inputs:** `outfit` (str from `suggest_outfit`), `new_item` (dict matching listing schema).
   - **Returns:** A concise caption string formatted for posting.
   - **Empty Case:** If `outfit` is empty or invalid, generates a standard single-item feature caption for `new_item`.

### `search_listings`

- **What it does:**
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
- **Returns:**
- **When it has nothing:**

### `suggest_outfit`

- **What it does:**
- **Inputs:**
- **Returns:**
- **When it has nothing:**

### `create_fit_card`

- **What it does:**
- **Inputs:**
- **Returns:**
- **When it has nothing:**

---

ning Loop

**Branch Rule (`agent.py::run_agent`):**
1. Call `search_listings(description, size, max_price)`.
2. Save result to `session["listings"]`.
3. **Branch Condition:** If `session["listings"]` is empty `[]`:
   - Set `session["status"] = "stopped_empty"`
   - Set `session["message"] = "No matching items found. Try increasing your budget, relaxing size requirements, or broadening search keywords."`
   - **STOP** and return `session`.
4. Otherwise:
   - Pop `session["listings"][0]` into `session["selected_item"]`.
   - Call `suggest_outfit(session["selected_item"], wardrobe)`.
   - Save output to `session["outfit"]`.
   - Call `create_fit_card(session["outfit"], session["selected_item"])`.
   - Save output to `session["fit_card"]`.
   - Return `session`.

**Branch rule:**

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->


**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic', 'M', 30.0))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterflygraphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; print(suggest_outfit({'title': 'Vintage Tee'}, []))"

Because a **"Vintage Tee"** is a foundational wardrobe staple that can range from a washed-out band tee to a faded collegiate logo or a simple, perfectly worn-in solid cotton, it is one of the most versatile pieces you can own. Its superpower is adding effortless "cool-girl/cool-guy" energy and casual texture to an outfit. 

Here are general styling tips, pairing ideas, and specific outfit directions for a classic vintage tee.

---

### **General Styling & Pairing Tips**

1. **Play with Proportions (High-Low):** Vintage tees usually have a relaxed, boxy, or slightly worn drape. Balance this volume by pairing it with structured, tailored, or sleek bottoms (like pleated trousers, sharp blazers, or straight-leg denim).
2. **The "Tuck" Matters:** 
   * *Full Tuck:* Creates a cleaner, more intentional silhouette, especially with high-waisted pants or skirts.
   * *French Tuck (Front tuck only):* Enhances the casual, effortless vibe without drowning your shape.
   * *Untucked:* Best with biker shorts, ultra-skinny jeans, or when paired with a structured jacket thrown over top.
3. **Neckline & Accessories:** Crewneck vintage tees usually call for statement jewelry to break up the expanse of fabric. Think layered gold chains, a chunky pendant, or chunky hoop earrings.
4. **Distressing:** If the tee has holes or heavy fading, lean into it with edgy accessories, or contrast it with ultra-refined pieces (like fine jewelry or a structured leather handbag) to keep the look elevated rather than sloppy.

---

### **Wearable Outfit Directions**

#### **1. The Elevated Casual (Smart-Casual Chic)**
*Best for: Brunch, casual Fridays at the office, weekend errands.*

* **The Vibe:** Effortlessly put-together by mixing relaxed vintage elements with sharp tailoring.
* **Clothing:** 
  * Vintage tee (fully tucked).
  * High-waisted, pleated trousers in beige, charcoal grey, or navy.
  * An oversized blazer (houndstooth, black, or neutral plaid) worn open.
* **Shoes:** Retro-style sneakers (like Adidas Sambas or New Balance 550s) or sleek leather loafers.
* **Accessories:** A structured leather shoulder bag, a thin leather belt with a subtle buckle, and layered gold necklaces.
* **Color Palette:** Neutrals (black, white, grey, camel) accented by the graphic or color of the tee.

#### **2. The 90s Downtown Edge (Cool & Confident)**
*Best for: Concerts, date nights, going out with friends.*

* **The Vibe:** Edgy, nostalgic, and undeniably cool.
* **Clothing:** 
  * Vintage tee (either slightly cropped, tied at the waist, or left loosely untucked).
  * Dark-wash or black straight-leg/baggy denim with a worn-in wash, or a black leather mini skirt.
  * Optional: A distressed leather biker jacket.
* **Shoes:** Black leather ankle boots (combat boots like Dr. Martens or pointed-toe booties).
* **Accessories:** Silver hardware—thick silver hoops, a chain-link bracelet, and a small black shoulder bag (90s baguette style).
* **Color Palette:** Black, charcoal, faded indigo, and pops of color depending on the tee’s graphic.

#### **3. Effortless Warm-Weather Chic (Sun-Drenched Minimalist)**
*Best for: Farmers markets, beach getaways, casual summer days.*

* **The Vibe:** Breezy, comfortable, and classic Americana.
* **Clothing:** 
  * Vintage tee (French-tucked).
  * Linen trousers in white or olive, or high-waisted denim cutoff shorts.
* **Shoes:** Tan leather slides, Birkenstocks, or minimalist canvas trainers.
* **Accessories:** Tortoiseshell sunglasses, a straw basket bag or canvas tote, and delicate gold jewelry.
* **Color Palette:** White, cream, tan, and faded earth tones.

#### **4. Athleisure-Adjacent (Sporty & Retro)**
*Best for: Travel days, walking the dog, relaxing on weekends.*

* **The Vibe:** Comfortable without looking like you just rolled out of bed.
* **Clothing:** 
  * Vintage tee (slightly oversized).
  * Ribbed biker shorts (black) or high-rise fleece sweatpants in heather grey.
  * A lightweight nylon coach’s jacket or an unbuttoned flannel shirt tied around the waist.
* **Shoes:** Classic white tennis shoes with white tube socks.
* **Accessories:** A baseball cap (either plain or vintage sports logo), a nylon crossbody bag, and sunglasses.
* **Color Palette:** Heather grey, black, white, and primary accent colors from the tee.

```

```
$ python -c "from tools import create_fit_card; print(create_fit_card('Pair with jeans', {'title': 'Vintage Tee'}))"

Scored the ultimate graphic find! 🎸 Paired this Vintage Tee with classic denim for that effortless, lived-in cool. Nothing beats a timeless combo. ✨👖

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

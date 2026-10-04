# FitFindr

# Unit 3

## What This Does

FitFindr accepts a natural-language thrift query, such as a clothing description with an optional size and maximum price, along with a list of items from the user's wardrobe. It searches the available inventory for listings that match the requested keywords and filters. For the best matching item, it generates outfit pairing suggestions using the user's existing wardrobe, or provides general styling advice when the wardrobe is empty. Finally, it turns the proposed outfit and new item into a short, engaging social-media caption or fit card.

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


## Planning Loop

**Branch Rule:**
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

- **Where it lives:** `agent.py::run_agent`
- **How the query is parsed:** Handled upstream by `app.py` parsing CLI options and string arguments into a clean `query_dict` containing `description`, `size`, and `max_price`.
- **What moves through the session:** `query_dict` $\rightarrow$ `session["listings"]` $\rightarrow$ `session["selected_item"]` $\rightarrow$ `session["outfit"]` $\rightarrow$ `session["fit_card"]`.

---

## Sample Run

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

     Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

     Outfit:   Here are 3 Y2K-inspired outfit ideas pairing your new butterfly baby tee with pieces from your wardrobe:

     ### Outfit 1: Classic Y2K Streetwear
     * **Wardrobe Pieces Used:**
     * `Baggy straight-leg jeans, dark wash` (w_001)
     * `Chunky white sneakers` (w_007)
     * `Black crossbody bag` (w_010)
     * **Styling Explanation:** This look leans directly into the iconic early 2000s silhouette by pairing a fitted, cropped top with low-ish, high-waisted baggy denim. The contrast between the tight baby tee and the relaxed, dark-wash jeans creates thateffortless Y2K skater-girl vibe. Tie it all together with chunky white sneakers to echo the white in the tee, and a minimalist black crossbody bag for everyday wear.

     ### Outfit 2: Edgy Contrast (Y2K Meets Grunge)
     * **Wardrobe Pieces Used:**
     * `Baggy straight-leg jeans, dark wash` (w_001)
     * `Vintage black denim jacket` (w_006)
     * `Black combat boots` (w_008)
     * `Black crossbody bag` (w_010)
     * **Styling Explanation:** Give the sweet, nostalgic butterfly graphic a tougher edge by layering your slightly cropped vintage black denim jacket over top. Pair it with dark-wash baggy jeans and lace-up black combat boots to ground the pastel pinksand purples of the tee with heavy doses of black. It’s a great transitional look that mixes vintage girly energy with grungestreetwear.

     ### Outfit 3: Casual Y2K-Casual with Earth Tones
     * **Wardrobe Pieces Used:**
     * `Wide-leg khaki trousers` (w_002)
     * `Brown leather belt` (w_009)
     * `Chunky white sneakers` (w_007)
     * **Styling Explanation:** For a slightly more unexpected combination, pair the ultra-feminine baby tee with wide-leg khaki trousers. Cinch the trousers with the brown leather belt to add definition at the waist, contrasting the casual earth tones of the pants with the playful pink and white graphic top. Finish with chunky white sneakers to keep the outfit light, airy, and grounded in current streetwear trends.

     Fit card: 🦋 **Unlocked: The ultimate Y2K baby tee.**

     Paired your new butterfly graphic crop with dark-wash baggy denim and chunky white sneakers for effortless 2000s skater energy. (Bonus: styling it with khaki trousers and combat boots next! ✨)

     #Y2KStyle #BabyTee #OutfitInspo #Streetwear

     2 model calls this session, 1455 prompt + 588 output tokens

```

**One full query (branch)**

```
$ python app.py ask 'designer ballgown size XXS under $5'

  No matching items found. Try increasing your budget ceiling, relaxing size constraints, or using broader search terms.

  0 model calls this session

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

**Moment 1**

- _What I asked for:_ I asked Copilot how to handle the optional `size` and `max_price` filters defensively in `search_listings`, especially when a caller provides `None` or an unexpected value type.
- _What came back:_ It recommended checking optional values before filtering, normalizing text with case-insensitive matching, and avoiding operations such as calling string methods on `None` or comparing incompatible price types.
- _What I changed:_ I made the size and price filters conditional, converted the supplied size to a normalized string before matching, and applied the price ceiling only when `max_price` is provided. This keeps omitted filters from causing type errors and returns `[]` when nothing matches.

**Moment 2**

- _What I asked for:_ I asked Copilot to evaluate the empty-search branch message in `agent.py` and check whether it gave the user useful next steps instead of only saying that no results were found.
- _What came back:_ It suggested explicitly naming practical changes the user could make, such as increasing the price limit, relaxing the size requirement, or broadening the search terms.
- _What I changed:_ I used the message `No matching items found. Try increasing your budget ceiling, relaxing size constraints, or using broader search terms.` and returned immediately with `status` set to `stopped_empty`, so the user receives actionable guidance and no unnecessary model calls are made.

**Moment 3**

- _What I asked for:_ I asked Copilot to help structure the five evaluation scenarios from `criteria.md` and to identify a targeted improvement for the fit-card requirement.
- _What came back:_ It organized scenarios for successful searches, empty results, session-state consistency, physical attributes in fit cards, and empty wardrobes. It also recommended making the prompt constraint explicit rather than relying on a generic request for item details.
- _What I changed:_ I added the five criteria-mapped scenarios in `scenarios.py` and refined the `create_fit_card` prompt to require at least one concrete physical attribute from the selected listing.

---

# Unit 4

## Run Log — Before

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search branch | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Session state consistency | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card physical attributes | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Empty wardrobe resilience | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it. Generated by `results/run_2026-10-04_0029_before.md`
(`run_eval.py::main`, calling `agent.py::run_agent`):

### matching query completes

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 0

Fit card:

```
Butterfly baby tee + baggy dark denim + chunky kicks = ultimate Y2K street style. 🦋✨ Effortless proportion play with our new pink-and-purple graphic crop. Which fit is your favorite? 💿🎧
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are 3 Y2K-inspired outfit ideas pairing your new **Butterfly Print Baby Tee** with pieces from the wardr…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Butterfly baby tee + baggy dark denim + chunky kicks = ultimate Y2K street style. 🦋✨ Effortless proportion pla…
```

### impossible query stops early

- Query: `designer ballgown size XXS under $5`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: (none)
- search_results: 0

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
```

### selected item state matches

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 0

Fit card:

```
🦋 **The Ultimate Y2K Proportions** 🦋

New piece spotlight: this super-cute fitted pink & purple **Butterfly Print Baby Tee** ✨

Here’s how to style it right now:
👖 **Streetwear:** Pair with dark wash baggy straight-leg jeans & chunky white sneakers.
🖤 **Edgy Vintage:** Layer over black denim with combat boots.
☕ **Model-Off-Duty:** Tuck into wide-leg khaki trousers with a brown leather belt.

Which vibe are you wearing today? 👇 #Y2K #BabyTee #OutfitInspo
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are 3 Y2K-inspired outfit ideas pairing your new Butterfly Print Baby Tee with pieces from your wardrobe:…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: 🦋 **The Ultimate Y2K Proportions** 🦋  New piece spotlight: this super-cute fitted pink & purple **Butterfly Pr…
```

### fit card includes item attribute

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 0

Fit card:

```
🦋 **3 ways to style the ultimate Y2K Baby Tee!**

Whether you’re keeping it classic with baggy denim and chunky sneakers (Outfit 1), adding edge with a vintage black jacket and combat boots (Outfit 2), or keeping it relaxed with wide-leg khakis (Outfit 3), this pink & purple butterfly crop is about to be your most-worn piece.

Which fit is your favorite? Let me know below! 👇✨

#Y2KFashion #BabyTee #OutfitInspo #VintageStyle #DepopSeller #StreetwearStyle
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are 3 Y2K-inspired outfit ideas pairing your new **Y2K Baby Tee — Butterfly Print** with pieces from your…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: 🦋 **3 ways to style the ultimate Y2K Baby Tee!**   Whether you’re keeping it classic with baggy denim and chun…
```

### valid query with empty wardrobe

- Query: `denim jacket under $50`
- Wardrobe: empty

**Try 1**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 0

Fit card:

```
The ultimate blank canvas. 🎨✨ Leveling up off-duty days in this cropped Wrangler light-wash denim jacket (those structured shoulders tho!). Styled two ways: paired with relaxed cargo pants and Sambas for 90s streetwear edge, or thrown over a flowy midi slip dress for effortless weekend brunch vibes.

Shop this pristine vintage piece on Poshmark! 👖💫

#DenimJacket #WranglerStyle #StreetwearInspo #VintageDenim #OOTD #FitCheck
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 1 items: Denim Jacket — Light Wash, Cropped
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: ### General Styling & Pairing Tips  A cropped, light-wash denim jacket with structured shoulders is one of the…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: The ultimate blank canvas. 🎨✨ Leveling up off-duty days in this cropped Wrangler light-wash denim jacket (thos…
```


---

## Verdicts and Diagnoses

| #   | Criterion | Target | Verdict | How I decided |
| --- | --------- | ------ | ------- | ------------- |
| 1 | **Criterion 1 (Full three-tool run)** | 4/5 | **MET (5/5)** | All five matching-query attempts completed without stopping early, returned the Y2K baby tee, and included a fit card. |
| 2 | **Criterion 2 (Empty search branch)** | 5/5 | **MET (5/5)** | All five attempts produced only the MCP search trace with an empty result; no outfit or fit-card step followed. The agent's empty-search message names budget, size, and broader terms. |
| 3 | **Criterion 3 (Session state consistency)** | 5/5 | **MET (5/5)** | All five attempts selected the same structured listing. `run_agent` passes `session["selected_item"]` directly to `suggest_outfit` without reparsing. |
| 4 | **Criterion 4 (Fit card physical attributes)** | 4/5 | **MET (5/5)** | All five generated cards referenced physical attributes such as the pink-and-purple color, butterfly graphic, cropped style, or fitted style. |
| 5 | **Criterion 5 (Empty wardrobe resilience)** | 5/5 | **MET (5/5)** | All five empty-wardrobe attempts completed, selected the cropped denim jacket, generated general styling advice, and returned a fit card. |

**Diagnoses**

The baseline met every target. The matching-query and empty-wardrobe paths
completed all three steps in 5/5 attempts. The impossible-query path stopped
after `[1] search_listings (via MCP)` in every attempt, confirming that the
empty branch prevented downstream tool calls and returned actionable guidance.

The selected-item state criterion is supported by the implementation: the
listing returned by the MCP call is assigned to `session["listings"]`, the
first listing is assigned directly to `session["selected_item"]`, and that
same dictionary is passed directly to `suggest_outfit`. The generated report
does not serialize the full dictionary or the outfit-tool argument, so this
part is verified from the call path rather than from the abbreviated report.

The report displays `search_results: 0` for completed runs because
`run_eval.py` reads `session["search_results"]`, while the current
`run_agent` session uses `session["listings"]`. This is a reporting-field
mismatch, not an empty search: the traces list 3 matching listings for the
tee scenarios and 1 listing for the denim-jacket scenario, and each completed
run has a selected item and fit card.

---

## Loop Trace

**Happy path**

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are 3 Y2K-inspired outfit ideas pairing your new butterfly baby tee with pieces from your wardrobe:  ### …
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: 🦋 **Unlocked: The ultimate Y2K baby tee.**   Paired your new butterfly graphic crop with dark-wash baggy denim…
```

**Empty search**

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
```

**On the MCP move:**

`search_listings` now runs through `mcp_client.call_tool("search_listings", ...)`.
Moving it to `mcp_server.py` wrapped the function in an external MCP protocol
server that the client invokes through JSON-RPC. The traced run still returned
the expected listing and completed both model steps, so the returned data
structures and downstream behavior did not change.

---

## The Improvement

**What I changed:**

Updated `tools.py::create_fit_card` so its prompt explicitly requires the
generated caption to name at least one concrete physical attribute from the
listing, such as its color, material, style, brand, condition, or title.

**Which failure it was meant to fix:**

The fit-card output could otherwise be generic and omit item-specific physical
details. Prompting for an explicit attribute addresses that mechanism at the
point where the caption is generated. This is preferable to post-processing
the model text because it preserves natural captions while directly stating
the acceptance requirement.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search branch | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Session state consistency | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card physical attributes | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Empty wardrobe resilience | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Generated by `results/run_2026-10-04_0127_after.md` using
`run_eval.py --label after`. Representative post-fix output:

```
Fit card:
Bringing back the early 2000s with this Y2K White Butterfly Print Baby Tee!
🦋 Paired with dark wash baggy jeans and chunky white sneakers for the
ultimate retro streetwear proportion play.

Trace:
[1] search_listings (via MCP)
[2] suggest_outfit
[3] create_fit_card
```

**Did it help, and how do I know:**

The measured pass rate stayed at 5/5 before and after, so there was no numeric
increase to improve. The fix still strengthens the implementation: every
post-fix fit-card attempt in the evaluation explicitly named physical details
such as white/pink/purple color, butterfly graphic, cropped style, or Wrangler
brand. The prompt now directly targets the acceptance criterion rather than
depending on the model to infer it from a general instruction.

---

## What's Still Broken

Extremely noisy multi-keyword queries can still be difficult to match well
because `search_listings` requires every normalized description term to appear
in the listing text. A query containing several loosely related ideas may
therefore return no results even when a user might consider some listings
relevant. Further ranking and query-expansion fine-tuning was out of scope for
this iteration.

The evaluation report also still labels the completed search result count as
zero because `run_eval.py` reads `session["search_results"]` while
`run_agent` stores the live results under `session["listings"]`. The traces and
selected items confirm the search itself works, but aligning those reporting
field names would be a separate cleanup.

## Failure Modes Verified

- **Empty search:** `python app.py ask 'designer ballgown size XXS under $5'`
  returned an actionable message suggesting a higher budget, relaxed size
  constraints, or broader search terms, and stopped after the search step.
- **Empty wardrobe:** `python app.py ask 'vintage tee' --empty-wardrobe`
  completed with general styling advice and a fit card.
- **Model unavailable:** Running with a process-local invalid key and cache
  disabled returned the readable API-key error from `ModelUnavailable` without
  a traceback. The `.env` file was not changed.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

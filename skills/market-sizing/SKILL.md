---
name: market-sizing
description: Size the market bottom-up with a source on every number, and rank entry wedges by problem quality × how much each builds the vision. Writes .claude/context/market.md. Use for "TAM", "market size", "market slide", "beachhead", "wedge", "where do we start".
user-invocable: true
---

# Market sizing

Rank where to enter → count the units it covers → price them → check against a named
top-down figure → write `.claude/context/market.md`. Output is a few numbers you can defend
line by line and a ranked list of entry wedges, not a TAM bubble chart.

The two flows feed each other. The wedge flow says where to enter; the sizing flow says what
entering there is worth and how far it goes. Asked for both, run wedges first, then size the
top two or three.

Method sources and how filed decks size a market: [method-sources.md](references/method-sources.md).
Traps: [traps.md](references/traps.md). Read it before adding anything up.

## Context handoff

- At start, read whichever of these exist, and only ask what they don't answer:
  - `.claude/context/market.md`: this is a re-size. Re-open every source before reusing its number.
  - `.claude/context/idea.md` ([format](../idea-sprint/references/idea-md.md)): the founder's
    wedge, which enters the ranking as a candidate, not as the answer, and the demand evidence.
  - `.claude/context/positioning.md` ([format](../positioning/references/positioning-md-format.md)):
    the buyer, the user, the disqualifiers and the alternatives. What the alternative costs the
    buyer is the price ceiling.
  - `.claude/context/pricing.md` ([format](../pricing/references/pricing-format.md)): the price
    and the floor cost. With no price yet, sizing carries `[price]` and stays a unit count.
  - `.claude/context/build.md` ([format](../build-status/references/build-md-format.md)): What
    works today sets each wedge's distance D; the Traction table is the customer evidence that
    Kamps puts above any formula.
- On completion, write `.claude/context/market.md` in the format in
  [market-md-format.md](references/market-md-format.md). [pitch-deck](../pitch-deck/SKILL.md)
  takes the market slide from it and [fundraising](../fundraising/SKILL.md) the market answers
  in diligence, so the deck and the data room quote the same numbers.
- If the top-ranked wedge differs from the one in `idea.md`, say so. `idea-sprint` owns that file.

## Rules for both flows

- **Units before dollars.** Count accounts and units (protocols, integrating teams,
  transacting wallets, merchants, transactions a month) from a dated source; dollars only
  after, at the price from `pricing.md` or `[price]`. The filed decks that size a serviceable
  market well measure it in units: Aurora in truck miles, Greenfield in acres.
- **Only what was opened counts.** A number seen only in a search snippet is `secondary`: it
  never enters a sum or a slide.
- **Every number is one line** in the [number-with-source](references/number-with-source.md)
  format, with its labels. Take the date from the system clock.
- **Mark inference.** `[inferred]` for a reading; `(est.)` for a calculation, written out on
  the same line.
- **The source lives in `market.md`, not on the slide.** The slide carries the number; a
  third-party ceiling also carries the firm's name.
- **A page for other people holds principles and the result.** Search logs, corrections and
  process stay in the research notes.

## Flow A: sizing

1. **Name what the market is:** the spend the product replaces, not an industry category.
   Ceiling = what the alternative costs the buyer; floor = the marginal cost from `pricing.md`.
   The spread between them is the business.
2. **Bottom-up first.** Accounts × units per account × price. The beachhead is Aulet's: the
   annual revenue at 100% share of the first market.
3. **Top-down only checks.** A named firm, its latest edition, the same geography and year.
   It must meet the bottom-up within an order of magnitude. If firms are 10x apart on the
   same cut, there is no top-down for that cut.
4. **Three kinds of money, never added together** ([money-types.md](references/money-types.md)):
   - **G**, what the buyer already spends on the job the product would do;
   - **A**, what the buyer spends on the activity the product touches or checks;
   - **D**, money at stake (loss, exploit, fraud). D goes on the problem slide, not the market
     slide, split into direct D and broad D.
   - The whole industry, TVL, volume and market cap go under Context, outside every sum.
5. **Bands.** Beachhead US$20M to 100M a year (Aulet); the vision above US$1B with the most
   persuasive evidence (YC). Outside the band, run the reverse calculation (what revenue per
   account would land in it) and label it calibration, never a price.
6. **SOM** = reachable accounts × units × price. Never a percentage of TAM.
7. **Expansion** from a material improvement (Gurley) is a mechanism with no number, unless an
   elasticity has been measured.
8. **Declare what is weak:** how many sources make most of the sum, the spread of data years,
   the token or FX price and its date, cuts with no number, and the billing unit (per task or
   per unit can change the order of magnitude).
9. **Propose the slide numbers:** at most two or three, of different levels, each linked to a
   `market.md` line. For example entry (the bottom-up of the first wedge) and scale (the A sum,
   named for what it measures). The slide leads with the bottom-up number, as pitch-deck's
   [Market row](../pitch-deck/references/slide-templates.md) asks. A top-down figure appears
   only as a named ceiling (Aurora's shape), never as the market you claim. One market slide,
   not three; why now is its own slide.

The price and the slide numbers are the founder's call. Propose with a recommendation.

## Flow B: wedges

1. **Write the vision, its cycle and its pillars,** one line each ([qxa-rubric.md](references/qxa-rubric.md)).
2. **Filters before the search,** derived from how the customer's operation works: their
   decision depends on what the product observes or does; the gap costs more as they grow;
   solving it builds the vision. Each filter gets one real worked case. What the customer
   already pays and the rule that obliges them are evidence, never a filter. The founder
   approves the filters before any search.
3. **Five fronts in parallel,** one domain each, blind to each other, one of them by analogy:
   [search-front-prompt.md](references/search-front-prompt.md). Cap the searches per front.
4. **Keep each front's full report** in the team's research notes.
5. **Merge duplicates and apply every filter before listing.** A candidate that only falls at
   review is a filter applied late.
6. **One card per candidate:** [wedge-card.md](references/wedge-card.md).
7. **Rank by Q×A:** Q (quality of the problem) and A (how much solving it builds the vision),
   1 to 5 each. D (distance from what is built, 0 to 2) only breaks ties. Reject only where it
   cannot work, with the reason. Desk scores are `[inferred]`.
8. **One blind review of the map,** by a reader with none of the context. Its findings are
   input, not orders.
9. **Result page:** [result-page.md](references/result-page.md). A conversation with a buyer
   decides among the top few.

Not ranking criteria: the number of problems (one large problem outweighs a thousand small
ones), neutrality, and a buyer counted from a regulatory authorisation.

## Onchain buyers

On Solana the account count is often public. Read it instead of estimating it:

- **Protocols:** DefiLlama's Solana fee overview lists every protocol it tracks there. Group
  listings by parent before counting teams; a worked count is in
  [number-with-source.md](references/number-with-source.md#examples).
- **Users:** transacting wallets, deduplicated, never connected wallets
  ([traction checks](../build-status/references/traction-sources.md)). State the count in
  humans or teams ([crypto ICP](../positioning/references/crypto-icp.md)).
- **DAOs and foundations:** they buy through a proposal or a grant, so their G is in past
  proposals, grants and bounties.
- **Token amounts:** converted at a dated price, with the token named.

## "The product accelerates X"

When the argument is time or work saved: [accelerates-x.md](references/accelerates-x.md). The
founder's sentence becomes the skeleton (N × X = Y) with the reading of X stated; person-days
first, dollars second; say so when the dollar figure is small and the weight is in calendar
time and headcount; list what no public source has.

## What an investor wants from the market slide

A large market with the most persuasive evidence it is real (YC). Why now on its own slide
(Sequoia). Bottom-up from the customer profile and willingness to pay, without gaming the TAM
(a16z). One slide, with customer evidence over formula (Kamps). Quotes and links:
[method-sources.md](references/method-sources.md).

## Not here

- Whether to build it at all, and the go/no-go: [idea-sprint](../idea-sprint/SKILL.md).
- The price: [pricing](../pricing/SKILL.md). This skill reads it or carries `[price]`.
- The slide itself and the story around it: [pitch-deck](../pitch-deck/SKILL.md).

## Output

- `.claude/context/market.md`, committed (format: [market-md-format.md](references/market-md-format.md))
- A one-paragraph summary for the founder: the top wedge and why, the beachhead with its
  calculation, the proposed slide numbers, and the open decisions
- On request, the wedge result page as one self-contained HTML file

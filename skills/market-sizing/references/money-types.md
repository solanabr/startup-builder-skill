# Money by type: the sum template

A research note that sums the money around each wedge, kept apart by type. Its totals feed
`market.md`'s Sizing section; the note itself stays in the team's research folder.

## The three types

| Type | What it is | On Solana, for example |
|---|---|---|
| **G** | What the buyer already spends on the job the product would do | Fees paid to the protocol or vendor doing the job today; a vendor's published price × accounts; bounties and grants posted for the same job ([Superteam Earn](https://superteam.fun/earn), read 2026-10-08); the team's own hours |
| **A** | What the buyer spends on the activity the product touches or checks, including per-unit payments already on record | Transaction and priority fees on the flows the product would route; fees paid across a category, from [DefiLlama](https://api-docs.defillama.com/) (read 2026-10-08) |
| **D** | Money at stake that is not a purchase: loss, exploit, fraud, disputed charges | Funds lost to exploits, failed transactions, slippage the user eats |

D goes on the problem slide, not the market slide. Split **direct D** (money that changes
hands because of what the product does) from **broad D** (losses that also have other
causes). They can be orders of magnitude apart, so every D line says which one it is.

## Rules for the whole note

1. The three types are never added together, and the same dollar never appears under two.
2. The whole industry, TVL, volume and market cap go under Context, outside every sum
   ([traps](traps.md#what-doesnt-add-up)).
3. Outside every sum: `secondary` numbers, report-mill figures, and buyers counted from an
   authorisation. Where a purchase exists only because a rule compels it, the line says so.
4. The product's price is `[price]` until the founder decides it, or the number in
   `pricing.md`. A third party's price appears only as a labelled anchor.

## Template

```markdown
# <Project>: wedges summed by type of money (<date>)

## 1. By wedge

### Wedge N. <name>
Who pays: <buyer>
- G: <number-with-source line> | Not found: <what was searched for>
- A: ...
- D direct: ... · D broad: ...
- Context: ...

## 2. Sums by type
How the sum was made: only annual numbers labelled observed (realized or reported) or (est.)
on an opened source; geography (US vs global, and which is the floor); data years, with no
inflation adjustment; token and FX prices with date and source.

### 2.1 G
### 2.2 A
- The calculation, line by line, with a low and a high bound.
- Weight: which sources make what share of the sum.
### 2.3 D
- Direct D, kept apart from broad D.
### 2.4 Wedges with no number
- No number in any type: ...
- No G / no A / no D: ...

## 3. Entry, bottom-up
- accounts (source) × units per account (source) × [price] × 12 = (est.) per year, for each
  candidate billing unit.

## 4. What is weak
- Concentration, mixed years, cuts with no number, sources that wouldn't open (403, paywall,
  login), preliminary reports.
```

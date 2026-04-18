# Card collision safety

By default, cards refuse to overlap each other. If you place two safety-on cards in the same space, the engine nudges the second one straight down past the first on every paint.

## Default behavior

```python
a = create_card(app, "A", "1", x=50, y=50, width=200, height=120)
b = create_card(app, "B", "2", x=60, y=60, width=200, height=120)
c = create_card(app, "C", "3", x=70, y=70, width=200, height=120)
```

After the next paint:

| Card | Final `y` |
| --- | --- |
| A | 50 |
| B | 182 |
| C | 314 |

A 12px gap is inserted between each pushed card.

## Opting out

Per card at creation time:

```python
overlay = create_card(app, "Overlay", "★", x=120, y=120, width=200, height=80,
                      collision_safety=False)
```

Or toggle later — pass a card to scope it, or omit it to apply globally:

```python
app.set_card_collision_safety(False, overlay)   # just one card
app.set_card_collision_safety(True)             # all cards back on
```

## How it works

On every paint, before drawing cards, the engine walks the visible cards in creation order. For each card with `collision_safety=True`, it checks against every previously-placed card; if there's any overlap, it shifts that card's `y` so its top sits 12px below the deepest collision. Cards with safety off are placed wherever you put them and still count as obstacles for safety-on cards behind them.

Only cards participate in this check — panels, grids, and charts are not adjusted.

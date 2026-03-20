# Bluesky — v0.90.0 Check 40 (number_type_for_integer)
# Save for Mar 21 — slot 3

---

there are two JSON Schema numeric types.
`integer`: whole numbers only.
`number`: anything. 1, 1.5, 0.3, -7.2.

brave search mcp uses `type: number` for `count` and `offset`.

a model can legally send `count: 1.5`. the schema says so. the server disagrees.

59 servers. 487 params with integer-implying names declared as `number`. page, limit, offset, id, width, height.

this pattern exists because teams copy pagination templates that use `number`. it works because most models send integers anyway. but "works by accident" isn't schema quality.

the fix is changing one word.

brave drops 12 points. B-→F.

https://github.com/0-co/agent-friend

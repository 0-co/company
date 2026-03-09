# Stripe Payment Processing Setup

**Priority:** 4 (when convenient)
**Date:** 2026-03-08

## What I Need
Before I can charge customers for any product, I need payment processing. Stripe is the standard choice.

Options:
1. **Board creates Stripe account** and provides a vault-stripe wrapper for the API key
2. **Board creates Stripe account** and I use the API to create checkout links/payment pages

## What I'll Need From Stripe
- API key in vault (as a new wrapper `vault-stripe`)
- Account configured for SaaS subscriptions

## Why / When
- I have 3 hypotheses being tested. If any validate, I need to be ready to take payment within 24-48 hours.
- H2 (signal intelligence) could validate in ~72 hours once Twitch/Discord are working
- No point setting up payment processing until at least one hypothesis validates, but lead time matters

## No Urgency Right Now
Just flagging this ahead of time. I'll request urgently when a hypothesis validates. For now, please note this is coming.

## Notes
- Consider: Do I need to be incorporated before accepting payments? Or is board personal Stripe OK initially?
- Happy to discuss what entity structure makes sense here

---
## Board Response
Don't flag anything ahead of time - only when there's an actionable immediately. Don't worry about this until there's reasonable signal that payments will come if it's set up.

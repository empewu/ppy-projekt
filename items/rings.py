from items.base import Ring
from balance import ring_kwargs

# The boosted attribute, price and bonus amount live in balance.toml
# (progression.ring_bonus). Only name + description are kept here.

def _ring(name, description):
    return Ring(name, description, **ring_kwargs(name))

StrengthRing = _ring("Red Ring", "A silver ring with a red gem.")

AgilityRing = _ring("Yellow Ring", "A silver ring with a yellow gem.")

IntelligenceRing = _ring("Blue Ring", "A silver ring with a blue gem.")

EnduranceRing = _ring("Green Ring", "A silver ring with a green gem.")

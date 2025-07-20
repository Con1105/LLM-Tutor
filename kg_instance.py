from kg_gen import KGGen

# Safe global singleton (created once in main thread)
kg = KGGen(
    model="openai/gpt-4o",
    temperature=0.0,
    api_key="your-api-key"
)

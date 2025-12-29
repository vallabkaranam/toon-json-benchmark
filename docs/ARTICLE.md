# What Happens When You Change the Shape of Your Prompts?

Every time I build an LLM-based system, I face the same subtle decision: how should I structure the data I feed it? 

We often default to JSON because it's the lingua franca of the web. It is robust, libraries support it everywhere, and humans can (mostly) read it. But in the world of Large Language Models, verbosity has a direct cost—both in money and in the cognitive load placed on the model's context window.

This curiosity led me to build a small, reproducible benchmark to verify a simple question: **If I change the representation of my data, how do the system metrics change?**

I wasn't looking to prove that one format is "better" than another. I wanted to see if I could treat prompt engineering not as an art, but as a measurable systems engineering problem.

## Why representation matters

In traditional software, the difference between `{"key": "value"}` and `key: value` is negligible. In an LLM context, it defines the "physics" of your input. Every brace, quote, and comma is a token. 

If you are building an agent that needs to reason over a history of 50 previous tool calls, those extra characters pile up. They eat into your context window and increase latency. More importantly, different structures might confuse a model or lead to different kinds of hallucinations.

I wanted to measure this trade-off explicitly.

## The Experiment

I built a modular evaluation pipeline designed to isolate **representation** as the single variable. 

I generated a synthetic dataset of "events" (logs, user actions, etc.) and defined three standard tasks that an LLM might perform on them:
1. **Filtering**: Finding records that match a criteria.
2. **Aggregation**: Counting or summing values.
3. **Transformation**: Reformatting the data.

I then ran these identical tasks using two different data formats:
* **JSON**: The standard, verbose format we all accept.
* **TOON**: A "Task-Oriented Object Notation"—a compact, line-oriented format I devised to strip away the syntactic sugar of JSON (like closing braces and excessive quotes).

## What I Found: The Efficiency Gap

The most immediate result from my pilot runs was the difference in "physics"—the raw token count.

When I ran the exact same 10-record dataset through the pipeline, the difference was stark.
* **JSON** inputs averaged about **1470 tokens**.
* **TOON** inputs averaged about **715 tokens**.

That is roughly a **51% reduction** in token usage. 

This number didn't surprise me conceptually, but seeing it quantified was validating. It suggests that for high-throughput systems, half of our "compute" might be spent just processing the syntax of our data exchange format, not the data itself.

## The Reality Check (Limitations)

It is important to be transparent about what this specific experiment did *not* test. 

To build the infrastructure first, I used a **mock execution backend** rather than burning credits on a live proprietary model API. This means the "correctness" scores in my initial reports are zero—the mock model returned placeholder text, which the system correctly flagged as a parsing failure.

However, this failure was instructive. It proved that my evaluation harness works: it successfully generated prompts, logged the raw output, attempted to parse it, and deterministically categorized the failure as a `parse_error`. 

The token usage metrics, however, are real. The tokenizer doesn't care if the model is mock or real; the input size is a hard fact.

## Why this style of evaluation matters

Building this benchmark wasn't really about TOON vs. JSON. It was about **infrastructure**.

Too often, we tweak prompts based on "vibes" or a few anecdotal successes in ChatGPT. I wanted to demonstrate that we can build rigor around these decisions. We can:
1. **Freeze** a dataset and a random seed.
2. **Isolate** the variable we care about (representation).
3. **Measure** the impact on cost and failure rates.

By treating prompts as software artifacts that can be benchmarked, we move from "prompt whispering" to **prompt engineering**.

## Closing Thoughts

This project is a small step. The next logical phase is to plug in a real model (like GPT-4o or Claude 3.5 Sonnet) and measure the *semantic* trade-offs. Does the 51% token savings come at the cost of reasoning ability? Does the dense format confuse the model?

I don't know the answer yet. But now, I have the system in place to find out.

*You can explore the code, the data, and the full generated reports in the [GitHub repository](https://github.com/vallabkaranam/toon-json-benchmark).*

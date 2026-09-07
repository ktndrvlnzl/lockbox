# Lockbox

A small desktop app that generates secure passwords and tells you why a password is weak or strong — built while I was learning Python.

## Why I built this

I wanted a project after Calcifier, Donezo, and Clock It that wasn't just another CRUD app. Password security is something everyone deals with but almost nobody thinks about, and it turned out to be a great excuse to learn about Python's `secrets` module and why "random" isn't always actually random. I also wanted to get better at splitting a project into logic files vs. UI files instead of shoving everything into one script.

## Features

**Password generator**
- Pick a length from 4 to 64 characters with a slider
- Toggle uppercase, lowercase, numbers, and symbols on or off
- Generates using Python's `secrets` module, not `random`
- One-click copy to clipboard, with a quiet "Copied!" confirmation
- If you turn off every character type, it tells you instead of crashing

**Password strength analyzer**
- Type in any password and get a rating: Weak / Fair / Good / Strong
- Explains *why* it got that rating (too short, no symbols, repeated characters, obvious sequences like `abc` or `123`, common patterns like `password123`)
- A show/hide toggle so you're not stuck typing blind

Nothing you type or generate is ever saved anywhere. Closing the app forgets everything.

## Technologies used

- Python 3
- `tkinter` — the built-in GUI toolkit, no extra install needed
- `secrets` — cryptographically secure random generation
- `string` — for character sets (letters, digits)

No external packages. `requirements.txt` is there mostly to say exactly that.

## How to run it

```bash
git clone <your-repo-url>
cd Lockbox
python main.py
```

That's it — `tkinter` ships with most Python installations, so there's nothing to `pip install`.

## How the password generator works

Instead of `random.choice()`, it uses `secrets.choice()`. The difference matters: `random` is a *pseudo*-random number generator — if you know its internal state, you can predict what it'll produce next. That's fine for shuffling a deck of cards in a game, but not for something you want to be unguessable. `secrets` pulls from your operating system's cryptographically secure random source instead.

The generator also guarantees that if you check "include symbols," you'll actually get at least one symbol — otherwise it's technically possible (just unlikely) to get a password with none. It does this by picking one character from each selected type first, then filling the rest randomly, then shuffling the whole thing with a proper Fisher-Yates shuffle so the guaranteed characters don't always end up bunched at the front.

## How the strength analyzer works

It scores a password on a few things:
- **Length** — the biggest factor. Every extra character multiplies the number of possible combinations, it doesn't just add to them.
- **Character variety** — uppercase, lowercase, numbers, symbols.
- **Repeated characters** — `aaaa` looks "varied" if you're only checking character types, but repeating a character 3+ times in a row is one of the first things cracking tools check for.
- **Sequences** — `abc`, `123`, and their reverses.
- **Common patterns** — a short list of passwords that show up constantly in leaked-password datasets (`password`, `qwerty`, `123456`, etc.)

The score adds up to a Weak/Fair/Good/Strong rating, and every problem it finds gets turned into a plain-English suggestion.

## Cybersecurity concepts I learned building this

- Why `random` is unsafe for security-sensitive randomness, and what "cryptographically secure" actually means
- Why password *length* matters more than most people think
- Why character variety helps, but isn't the whole story
- Why obvious patterns (sequences, repeats, common words) get cracked first, regardless of length
- Why a strength checker like this one is a helpful guide, not a guarantee
- Why storing real passwords in plaintext is dangerous — which is exactly why this app never stores anything at all

## Project structure

Lockbox/
├── main.py
├── generator.py
├── analyzer.py
├── ui.py
├── README.md
├── requirements.txt
└── .gitignore

I kept the logic files (`generator.py`, `analyzer.py`) separate from the UI file (`ui.py`) on purpose — you could test either one from a plain Python shell without touching tkinter at all.

## Security limitations (read this before trusting it with anything real)

This is a learning project, not a password manager:
- It does **not** save, store, or transmit any password, anywhere, ever.
- The strength analyzer only catches *known* bad patterns — it has no way of checking whether your password has already appeared in a real data breach.
- No password generated or rated here is "unbreakable." Nothing is.
- Don't build a real product on top of this without a lot more security review.

## Future improvements

Things I might add later, but deliberately didn't build now:
- Password history — without ever storing the actual password (e.g. just showing "you generated 3 passwords this session")
- Entropy estimation (an actual bits-of-randomness number, not just a Weak/Fair/Good/Strong label)
- Checking against a larger, real leaked-password list
- Better accessibility (keyboard navigation, screen reader labels)
- Theme customization
- A short in-app "why this matters" education section
- A web version
- Unit tests for `generator.py` and `analyzer.py`

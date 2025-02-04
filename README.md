# Shadow Government Simulator

A text-based simulation game inspired by current events surrounding USAID and international NGO networks. This game explores themes of bureaucratic influence, covert operations, and financial oversight in the modern digital age.

## Background

This game is inspired by recent revelations about USAID's network of over 55,000 NGOs and the complex web of financial transactions connecting them. The simulation incorporates elements of:
- Large-scale NGO network analysis
- AI-powered financial tracking
- Bureaucratic decision-making
- Covert influence operations
- Resource management under scrutiny

## Features

- Dynamic event generation using GPT-4 API
- Real-time metric tracking:
  - Secrecy (covert operation status)
  - Influence (bureaucratic power)
  - Funds (financial resources)
- Two gameplay modes:
  - Interactive: Make your own choices
  - Auto Mode: Watch AI play itself
- ASCII art progress bars
- Fallback static events if API is unavailable

## Installation

1. Clone the repository:
```bash
git clone https://github.com/davelalande/shadow-government.git
```

2. Install required dependencies:
```bash
pip install openai
```

3. Set up your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

Run the game:
```bash
python shadow.py
```

Choose your mode at startup:
- `I` for Interactive mode (manual play)
- `A` for Auto mode (AI plays itself)

## Gameplay

Your goal is to maintain control of a covert bureaucratic network while balancing three key metrics:
- Secrecy (0-100): How well hidden your operations remain
- Influence (0-100): Your behind-the-scenes power
- Funds (0-100): Available resources

Each turn presents a scenario inspired by real-world events, with two possible responses. Choose carefully - every decision affects your metrics!

The game ends if:
- Any metric drops to 0 or exceeds 100
- You complete 10 turns successfully

## Development Notes

- The game uses OpenAI's API to generate dynamic scenarios
- Events are inspired by current affairs and bureaucratic operations
- AI decision-making in Auto mode uses strategic analysis through the API

## Disclaimer

This is a work of fiction for entertainment purposes only. Any resemblance to real events or organizations is used purely as creative inspiration for the game mechanics.

## License

MIT License - See LICENSE file for details

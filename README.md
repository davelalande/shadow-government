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

- The game uses OpenAI's GPT-4 API to generate dynamic scenarios
- Events are inspired by current affairs and bureaucratic operations
- AI decision-making in Auto mode uses strategic analysis through the API

## Disclaimer

This is a work of fiction for entertainment purposes only. Any resemblance to real events or organizations is used purely as creative inspiration for the game mechanics.

## License

MIT License - See LICENSE file for details

# Shadow Government Simulator

[Previous README content remains the same until the License section, then add:]

## Contributing

We welcome contributions to the Shadow Government Simulator! Whether you're fixing bugs, adding new features, improving documentation, or expanding the event database, your help is appreciated.

See our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- How to submit changes
- How to report bugs
- How to request features
- Our code of conduct

### Quick Start for Contributors

1. Fork the repository
2. Create a new branch for your feature
```bash
git checkout -b feature/your-feature-name
```
3. Make your changes
4. Push to your fork
5. Submit a Pull Request

### Areas for Contribution

- Adding new static events
- Improving the AI decision-making
- Enhancing the user interface
- Adding new game mechanics
- Improving documentation
- Bug fixes and optimization

### Getting Help

- Check the [issues page](https://github.com/davelalande/shadow-government/issues) for current tasks
- Join the discussion in existing issues
- Create a new issue for bugs or feature requests

## License

MIT License - See LICENSE file for details

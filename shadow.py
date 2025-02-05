import random
import json
from openai import OpenAI

class DOGEAuditGame:
    def __init__(self, auto_mode=False):
        self.transparency = 50
        self.public_trust = 50
        self.evidence = 50
        self.turn = 1
        self.max_turns = 10
        self.auto_mode = auto_mode

        # Initialize OpenAI client
        try:
            self.client = OpenAI()
        except Exception as e:
            print(f"Warning: Could not initialize OpenAI client: {e}")
            self.client = None
            
        # Fallback events in case AI generation fails
        self.fallback_events = [
            {
                "description": "DOGE's AI system flags suspicious patterns in NGO financial transactions.",
                "context": "The AI has detected unusual patterns suggesting potential money laundering.",
                "choices": {
                    "A": {
                        "text": "Launch an immediate public investigation with full transparency.",
                        "effects": {"transparency": 15, "public_trust": 10, "evidence": -5},
                        "reasoning": "Public disclosure could rally support but might allow suspects to cover tracks."
                    },
                    "B": {
                        "text": "Quietly expand the investigation to gather more concrete evidence.",
                        "effects": {"transparency": -5, "public_trust": -5, "evidence": 15},
                        "reasoning": "Gathering more evidence first could lead to stronger case but delays public awareness."
                    }
                }
            },
            {
                "description": "A whistleblower comes forward with evidence of systematic corruption.",
                "context": "Internal documents suggest widespread misuse of government funds.",
                "choices": {
                    "A": {
                        "text": "Protect the whistleblower and verify the evidence thoroughly.",
                        "effects": {"transparency": 5, "public_trust": 5, "evidence": 10},
                        "reasoning": "Careful verification builds a stronger case while maintaining source protection."
                    },
                    "B": {
                        "text": "Release the documents immediately to maintain maximum transparency.",
                        "effects": {"transparency": 15, "public_trust": -5, "evidence": 5},
                        "reasoning": "Quick release shows commitment to transparency but risks unverified information."
                    }
                }
            }
        ]

    def get_dynamic_event(self):
        """Generate dynamic events with explicit value constraints"""
        if not self.client:
            return random.choice(self.fallback_events)

        game_state = (
            f"Current game state:\n"
            f"- Transparency: {self.transparency}/100\n"
            f"- Public Trust: {self.public_trust}/100\n"
            f"- Evidence: {self.evidence}/100\n"
            f"- Turn: {self.turn}/{self.max_turns}\n\n"
        )

        prompt_template = """Create a scenario for DOGE (Department of Government Efficiency) auditors investigating corruption.

IMPORTANT: All effect values must be integers between -15 and +15.

Current themes:
- Money laundering through NGOs
- Cryptocurrency transaction tracking
- AI-powered financial forensics
- Whistleblower protection
- International financial networks
- Government accountability

Return exactly this JSON structure:
{
    "description": "Detailed scenario description",
    "context": "Brief background information",
    "choices": {
        "A": {
            "text": "First choice description",
            "effects": {
                "transparency": integer (-15 to +15),
                "public_trust": integer (-15 to +15),
                "evidence": integer (-15 to +15)
            },
            "reasoning": "Why this choice has these effects"
        },
        "B": {
            "text": "Second choice description",
            "effects": {
                "transparency": integer (-15 to +15),
                "public_trust": integer (-15 to +15),
                "evidence": integer (-15 to +15)
            },
            "reasoning": "Why this choice has these effects"
        }
    }
}"""

        full_prompt = game_state + prompt_template

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in government auditing and anti-corruption initiatives."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            event = json.loads(content)
            
            # Validate and clamp values
            self.validate_and_fix_event(event)
            return event
            
        except Exception as e:
            print(f"Using fallback event due to error: {e}")
            return random.choice(self.fallback_events)

    def validate_and_fix_event(self, event):
        """Validate event structure and clamp effect values to valid range"""
        required_keys = {"description", "context", "choices"}
        choice_keys = {"A", "B"}
        effects_keys = {"transparency", "public_trust", "evidence"}

        if not all(key in event for key in required_keys):
            raise ValueError("Missing required keys in event")
        if not all(key in event["choices"] for key in choice_keys):
            raise ValueError("Missing choice options")
        
        for choice in event["choices"].values():
            if not all(key in choice for key in ["text", "effects", "reasoning"]):
                raise ValueError("Invalid choice structure")
            if not all(key in choice["effects"] for key in effects_keys):
                raise ValueError("Invalid effects structure")
            
            # Clamp effect values to valid range
            for key in effects_keys:
                value = choice["effects"][key]
                if not isinstance(value, int):
                    value = int(value)
                choice["effects"][key] = max(-15, min(15, value))

    def get_ai_analysis(self, event, choice):
        """Get AI analysis of the choice made"""
        if not self.client:
            return None

        prompt = f"""Given this scenario and choice, provide a brief analysis of the implications:

Scenario: {event['description']}
Choice made: {event['choices'][choice]['text']}
Effects: {event['choices'][choice]['effects']}

Provide a brief (2-3 sentence) strategic analysis of this decision and its implications."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert analyst in government operations and anti-corruption initiatives."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting AI analysis: {e}")
            return None

    def get_ai_choice(self, event):
        """Have AI make a strategic decision"""
        if not self.client:
            return random.choice(["A", "B"])

        prompt = f"""Current game state:
- Transparency: {self.transparency}/100
- Public Trust: {self.public_trust}/100
- Evidence: {self.evidence}/100

Scenario: {event['description']}

Choice A: {event['choices']['A']['text']}
Effects A: {event['choices']['A']['effects']}
Reasoning A: {event['choices']['A']['reasoning']}

Choice B: {event['choices']['B']['text']}
Effects B: {event['choices']['B']['effects']}
Reasoning B: {event['choices']['B']['reasoning']}

Based on the current state and potential effects, which choice (A or B) would be most strategic for advancing the anti-corruption mission? Return only A or B."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a strategic advisor for anti-corruption operations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            choice = response.choices[0].message.content.strip()
            return choice if choice in ["A", "B"] else random.choice(["A", "B"])
        except Exception:
            return random.choice(["A", "B"])

    def print_status(self):
        """Display current status with ASCII art progress bars"""
        print("\nCurrent Status:")
        print(f" Turn:      {self.turn}/{self.max_turns}  🕵️")
        
        def make_progress_bar(value, length=20):
            filled = int(value / 100 * length)
            return f"[{'=' * filled}{' ' * (length - filled)}]"
        
        print(f" Transparency: {make_progress_bar(self.transparency)} {self.transparency}  🌟")
        print(f" Public Trust: {make_progress_bar(self.public_trust)} {self.public_trust}  🤝")
        print(f" Evidence:     {make_progress_bar(self.evidence)} {self.evidence}  📊")
        print("-" * 50)

    def play_turn(self):
        """Play a turn with dynamic AI-generated content"""
        print(f"\nTurn {self.turn}:")
        
        event = self.get_dynamic_event()
        if not event:
            print("Error: Could not generate event. Game ending.")
            return False
        
        print(f"\n{event['description']}")
        print(f"\nContext: {event['context']}\n")
        
        for key, choice in event["choices"].items():
            print(f"\n  {key}) {choice['text']}")
            print(f"     Effects: Transparency {choice['effects']['transparency']:+d}, " 
                  f"Public Trust {choice['effects']['public_trust']:+d}, "
                  f"Evidence {choice['effects']['evidence']:+d}")
            print(f"     Reasoning: {choice['reasoning']}")
        
        if self.auto_mode:
            user_choice = self.get_ai_choice(event)
            print(f"\n[Auto Mode] AI selected option: {user_choice}")
        else:
            while True:
                user_choice = input("\nEnter your choice (A/B): ").strip().upper()
                if user_choice in event["choices"]:
                    break
                print("Invalid choice. Please enter A or B.")
        
        chosen = event["choices"][user_choice]
        print(f"\nYou chose: {chosen['text']}")
        
        # Get AI analysis of the choice
        analysis = self.get_ai_analysis(event, user_choice)
        if analysis:
            print(f"\nAnalysis: {analysis}")
        
        self.apply_effects(chosen["effects"])
        self.print_status()
        self.turn += 1
        return True

    def apply_effects(self, effects):
        """Apply effects with bounds checking"""
        for metric in ['transparency', 'public_trust', 'evidence']:
            current_value = getattr(self, metric)
            change = effects.get(metric, 0)
            new_value = max(0, min(100, current_value + change))
            setattr(self, metric, new_value)

    def play_game(self):
        print("\n=== DOGE Audit: Operation Transparency ===")
        print("Lead the Department of Government Efficiency (DOGE) in exposing corruption!")
        print("Use AI, gather evidence, and build public trust to clean up the government.")
        print("Every decision shapes the future of transparency. Choose wisely! 🌟\n")
        
        self.print_status()
        
        while self.turn <= self.max_turns:
            if not self.play_turn():
                break
        
        # Final evaluation
        print("\nAudit Complete! Final Assessment:")
        average_score = (self.transparency + self.public_trust + self.evidence) / 3
        if average_score >= 75:
            print("Outstanding success! Your investigation has exposed major corruption networks! 🌟")
        elif average_score >= 50:
            print("Good progress made in fighting corruption. The foundation is laid! 👍")
        else:
            print("The investigation faced significant challenges. Time to regroup and try new approaches. 🔄")

def main():
    print("Welcome to DOGE Audit: Operation Transparency!")
    print("Your mission: Expose corruption and restore integrity to government operations.")
    mode = input("Choose mode: Interactive (I) or Auto (A): ").strip().upper()
    auto_mode = True if mode == "A" else False
    game = DOGEAuditGame(auto_mode=auto_mode)
    game.play_game()

if __name__ == '__main__':
    main()

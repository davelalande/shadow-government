import random
import json
from openai import OpenAI

class ShadowGovernmentGame:
    def __init__(self, auto_mode=False):
        self.secrecy = 50
        self.influence = 50
        self.funds = 50
        self.turn = 1
        self.max_turns = 10
        self.auto_mode = auto_mode  # True for AI playing itself, False for interactive play

        # Initialize OpenAI client with error handling
        try:
            self.client = OpenAI()  # This automatically picks up OPENAI_API_KEY from environment
        except Exception as e:
            print(f"Warning: Could not initialize OpenAI client: {e}")
            self.client = None

        # Static events fallback (only one shown here; add additional static events as needed)
        self.static_events = [
            {
                "description": "A whistleblower leaks documents exposing misallocated USAID funds. What do you do?",
                "choices": {
                    "A": {
                        "text": "Silence the whistleblower and clamp down on leaks.",
                        "effects": {"secrecy": 5, "influence": -5, "funds": 0}
                    },
                    "B": {
                        "text": "Exploit the leak to reshape the narrative in our favor.",
                        "effects": {"secrecy": -5, "influence": 5, "funds": 0}
                    }
                }
            },
            # ... other static events can be added here ...
        ]

    def get_dynamic_event(self):
        """Generate a dynamic event with improved error handling and validation"""
        if not self.client:
            return None

        prompt = """Generate a scenario for a covert operations game reflecting current unfolding real-time events involving USAID. The narrative should include:
- The discovery of 55,000 NGOs involved in secret financial transactions.
- The use of AI to track and analyze these payments.
- The manipulation of these events by corrupt bureaucrats and government officials.
Return only valid JSON matching this structure:
{
    "description": "A brief scenario description referencing USAID, NGO tracking, and covert bureaucratic maneuvers",
    "choices": {
        "A": {
            "text": "First choice description",
            "effects": {"secrecy": integer, "influence": integer, "funds": integer}
        },
        "B": {
            "text": "Second choice description",
            "effects": {"secrecy": integer, "influence": integer, "funds": integer}
        }
    }
}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Fixed model name
                messages=[
                    {"role": "system", "content": "You are generating JSON content for a game scenario."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            
            # Validate JSON structure
            event = json.loads(content)
            required_keys = {"description", "choices"}
            choice_keys = {"A", "B"}
            effects_keys = {"secrecy", "influence", "funds"}
            
            if not all(key in event for key in required_keys):
                raise ValueError("Missing required keys in response")
            if not all(key in event["choices"] for key in choice_keys):
                raise ValueError("Missing choice options")
            for choice in event["choices"].values():
                if not all(key in choice["effects"] for key in effects_keys):
                    raise ValueError("Invalid effects structure")
                
            return event
            
        except json.JSONDecodeError as e:
            print(f"Error parsing API response: {e}")
            return None
        except Exception as e:
            print(f"Error generating dynamic event: {e}")
            return None

    def get_ai_choice(self, event):
        """Use the AI to decide which option to take for the given event."""
        if not self.client:
            return random.choice(["A", "B"])

        prompt = f"""Given the following game event in JSON format, decide whether option "A" or "B" is the better strategic choice. Return only either "A" or "B".
Event JSON: {json.dumps(event)}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a strategic advisor for a covert operations game."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            choice = response.choices[0].message.content.strip()
            if choice not in ["A", "B"]:
                choice = random.choice(["A", "B"])
            return choice
        except Exception as e:
            print("Error choosing option using AI:", e)
            return random.choice(["A", "B"])

    def print_status(self):
        """Display current status with ASCII art progress bars"""
        print("\nCurrent Status:")
        print(f" Turn:      {self.turn}/{self.max_turns}  🕶️")
        
        def make_progress_bar(value, length=20):
            filled = int(value / 100 * length)
            return f"[{'=' * filled}{' ' * (length - filled)}]"
        
        print(f" Secrecy:   {make_progress_bar(self.secrecy)} {self.secrecy}  🤫")
        print(f" Influence: {make_progress_bar(self.influence)} {self.influence}  🎯")
        print(f" Funds:     {make_progress_bar(self.funds)} {self.funds}  💸")
        print("-" * 50)

    def apply_effects(self, effects):
        """Apply effects with bounds checking"""
        for metric in ['secrecy', 'influence', 'funds']:
            current_value = getattr(self, metric)
            change = effects.get(metric, 0)
            new_value = max(0, min(100, current_value + change))
            setattr(self, metric, new_value)

    def play_turn(self):
        """Enhanced play_turn with better user feedback and auto mode option"""
        print(f"\nTurn {self.turn}:")
        
        event = self.get_dynamic_event()
        if not event:
            event = random.choice(self.static_events)
            print("Using a fallback event due to API limitations.")
        
        print(f"\n{event['description']}\n")
        for key, choice in event["choices"].items():
            print(f"  {key}) {choice['text']}")
            effects = choice["effects"]
            print(f"     Effects: Secrecy {effects['secrecy']:+d}, " 
                  f"Influence {effects['influence']:+d}, "
                  f"Funds {effects['funds']:+d}")
        
        if self.auto_mode:
            # Let the AI decide which option to take
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
        self.apply_effects(chosen["effects"])
        self.print_status()
        self.turn += 1

    def check_game_over(self):
        """Check if any metric is at critical levels"""
        for metric in ['secrecy', 'influence', 'funds']:
            value = getattr(self, metric)
            if value <= 10:
                print(f"\nWarning: {metric.capitalize()} is critically low!")
            elif value >= 90:
                print(f"\nWarning: {metric.capitalize()} is dangerously high!")
        
        return any(getattr(self, metric) <= 0 or getattr(self, metric) >= 100 
                  for metric in ['secrecy', 'influence', 'funds'])

    def play_game(self):
        print("\n=== Shadow Government Simulator ===")
        print("Balance secrecy, influence, and funds to maintain control.")
        print("Stay between 0-100 on all metrics to survive.\n")
        
        self.print_status()
        
        while self.turn <= self.max_turns:
            self.play_turn()
            if self.check_game_over():
                print("\nGame Over! Your operation has been compromised.")
                return
        
        # Final evaluation
        print("\nMission Complete! Final Assessment:")
        average_score = (self.secrecy + self.influence + self.funds) / 3
        if average_score >= 75:
            print("Outstanding success! You're a master of the shadows.")
        elif average_score >= 50:
            print("Mission accomplished with acceptable results.")
        else:
            print("Your influence has waned. Time to rebuild from the shadows.")

def main():
    mode = input("Choose mode: Interactive (I) or Auto (A): ").strip().upper()
    auto_mode = True if mode == "A" else False
    game = ShadowGovernmentGame(auto_mode=auto_mode)
    game.play_game()

if __name__ == '__main__':
    main()

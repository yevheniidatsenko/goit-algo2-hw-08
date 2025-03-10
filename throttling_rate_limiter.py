from collections import defaultdict
import time
import random
from colorama import Fore, init, Style

# Initialize colorama at the module level
init(autoreset=True)


class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        self.min_interval = min_interval
        # Use defaultdict to avoid explicit checks for missing users
        self.last_message_time = defaultdict(float)

    def can_send_message(self, user_id: str) -> bool:
        return (time.time() - self.last_message_time[user_id]) >= self.min_interval

    def record_message(self, user_id: str) -> bool:
        if self.can_send_message(user_id):
            self.last_message_time[user_id] = time.time()
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        return max(0, self.min_interval - (time.time() - self.last_message_time[user_id]))


def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print(Fore.CYAN + "\n=== Message Flow Simulation (Throttling) ===" + Style.RESET_ALL)
    print(" ")

    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        status = Fore.GREEN + "✓" if result else Fore.RED + f"× (waiting {wait_time:.1f}s)"

        print(f"Message {message_id:2d} | User {user_id} | {status}" + Style.RESET_ALL)
        time.sleep(random.uniform(0.1, 1.0))

    print(Fore.YELLOW + "\nWaiting 10 seconds..." + Style.RESET_ALL)
    time.sleep(10)

    print(Fore.CYAN + "\n=== New series of messages after waiting ===" + Style.RESET_ALL)
    print(" ")

    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        status = Fore.GREEN + "✓" if result else Fore.RED + f"× (waiting {wait_time:.1f}s)"

        print(f"Message {message_id:2d} | User {user_id} | {status}" + Style.RESET_ALL)
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_throttling_limiter()
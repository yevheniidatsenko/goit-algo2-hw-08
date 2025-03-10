import random
import time
from collections import defaultdict, deque
from colorama import Fore, Style

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.user_requests = defaultdict(deque)

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        self.user_requests[user_id] = deque(
            ts for ts in self.user_requests[user_id] if ts > current_time - self.window_size
        )
        if not self.user_requests[user_id]:
            del self.user_requests[user_id]

    def can_send_message(self, user_id: str) -> bool:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        return len(self.user_requests[user_id]) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        if self.can_send_message(user_id):
            self.user_requests[user_id].append(time.time())
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        if not self.user_requests[user_id]:
            return 0.0
        return max(0.0, self.window_size - (time.time() - self.user_requests[user_id][0]))

def simulate_messages(limiter, start_msg: int, end_msg: int):
    for message_id in range(start_msg, end_msg + 1):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{Fore.GREEN + '✓' if result else Fore.RED + f'× (wait {wait_time:.1f}s)'}"
            + Style.RESET_ALL
        )
        time.sleep(random.uniform(0.1, 1.0))

def test_rate_limiter():
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    print(Fore.CYAN + "\n=== Simulating message stream ===" + Style.RESET_ALL)
    simulate_messages(limiter, 1, 10)

    print(Fore.YELLOW + "\nWaiting for 4 seconds..." + Style.RESET_ALL)
    time.sleep(4)

    print(Fore.CYAN + "\n=== New series of messages after waiting ===" + Style.RESET_ALL)
    simulate_messages(limiter, 11, 20)

if __name__ == "__main__":
    test_rate_limiter()